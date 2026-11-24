import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .util import find_git_repo


class Commit:
    repo: Path
    sha: str
    raw: str
    tags: list[str]
    filename: str | None

    def __init__(self, repo: Path, sha: str) -> None:
        self.repo = repo
        self.sha = sha
        self.raw = subprocess.run(
            ["git", "cat-file", "-p", sha], stdout=subprocess.PIPE, check=True, cwd=repo
        ).stdout.decode()

        raw_filename = "unknown"

        for line in self.raw.splitlines():
            if ".patch" in line:
                raw_filename = line
                break

        match = re.match(r"\[(.*)\] (.*)", raw_filename)
        if match is None:
            self.filename = raw_filename
            self.tags = []
        else:
            self.filename = match.group(2)
            self.tags = match.group(1).split(",")

        if self.filename == "unknown":
            self.filename = None

    @property
    def parent(self) -> str | None:
        parentm = re.findall(r"parent (.*)", self.raw)
        if len(parentm) == 0:
            return None
        if isinstance(parentm[0], str):
            return parentm[0]
        return None

    def format_patch(self, output: Path | str) -> None:
        cmd = [
            "git",
            "format-patch",
            "-1",
            self.sha,
            "--output=" + str(output),
        ]
        _ = subprocess.run(cmd, check=True, cwd=self.repo)

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        if len(self.tags) == 0:
            return f'Commit("{self.filename}")'
        else:
            return f'Commit("{self.filename}", tags={self.tags})'


def get_head(repo: Path) -> str:
    cmd = ["git", "rev-parse", "HEAD"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, check=True, cwd=repo)
    return res.stdout.decode().strip()


def interdiff(path1: str, path2: str) -> str:
    res = subprocess.run(
        ["interdiff", path1, path2],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return res.stdout.decode().strip()


def get_commits(repo: Path) -> list[Commit]:
    head = get_head(repo)
    commits = [Commit(repo, head)]
    while commits[-1].parent:
        commit = Commit(repo, commits[-1].parent)
        if ".patch" not in commit.raw and "[skip]" not in commit.raw:
            break
        commits.append(commit)
    return commits


def check_patch_applies(repo: Path, parent_sha: str, target_patch: Path) -> bool:
    try:
        _ = subprocess.run(
            ["git", "switch", "--detach", parent_sha],
            cwd=repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _ = subprocess.run(
            ["git", "apply", "--check", target_patch],
            cwd=repo,
            check=True,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        pass
    finally:
        _ = subprocess.run(
            ["git", "switch", "-"],
            cwd=repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return False


@dataclass
class PatchArgs:
    output: str | None
    filename: str | None
    list: bool


class Patcher:
    repo: Path
    commits: list[Commit]
    ref: str
    target_dir: Path

    def __init__(self, repo: Path, output: str | None) -> None:
        self.repo = repo
        self.commits = get_commits(self.repo)
        self.ref = self.find_ref()

        if output:
            self.target_dir = Path(output)
        else:
            self.target_dir = self.get_target_dir()

    def get_head(self, repo: Path) -> str:
        cmd = ["git", "rev-parse", "HEAD"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, check=True, cwd=repo)
        return res.stdout.decode().strip()

    def find_ref(self) -> str:
        refs = subprocess.run(
            ["git", "show-ref"], stdout=subprocess.PIPE, check=True, cwd=self.repo
        )
        refs = refs.stdout.decode().strip().split("\n")

        for commit in self.commits:
            for ref in refs:
                if commit.sha in ref and "refs/heads" in ref:
                    start = len(commit.sha) + 1 + len("refs/heads/")
                    return ref[start:]

        raise RuntimeError("Could not find branch name!")

    def get_target_dir(self) -> Path:
        homedir = Path(os.environ.get("HOME") or "/")
        aportsdir_env = os.environ.get("APORTSDIR")
        aports = Path(aportsdir_env) if aportsdir_env else homedir / "aports"

        match self.ref:
            case "aports-esr":
                return aports / "community/firefox-esr"
            case "aports-stable":
                return aports / "community/firefox"
            case "aports-thunderbird":
                return aports / "community/thunderbird"
            case "aports-aurora":
                return aports / "testing/firefox-developer-edition"
            case "aports-nightly":
                # special case :)
                twoports = homedir / "2ports"
                if twoports.is_dir():
                    return twoports / "testing/firefox-nightly"
                return aports / "testing/firefox-nightly"
            case ref:
                raise RuntimeError(f"Unknown branch name: {ref}")

    def list(self) -> None:
        for commit in self.commits:
            if commit.filename is None:
                continue
            print(commit)

    def run(self, args: PatchArgs) -> None:
        if self.ref == "aports-thunderbird":
            self.commits += get_commits(self.repo / "comm")

        filenames = [commit.filename for commit in self.commits]

        # remove patch files that do not exist in the git tree
        existing = self.target_dir.glob("*.patch")
        for file in existing:
            if file.name not in filenames:
                print(f"[-] {file.name}")
                file.unlink()

        for commit in self.commits:
            if commit.filename is None or commit.parent is None:
                continue
            if args.filename is not None and commit.filename != args.filename:
                continue

            output_file = self.target_dir / commit.filename
            output_file_tmp = output_file.with_suffix(".tmp")

            commit.format_patch(output_file_tmp)

            if commit.repo != self.repo:
                fixup_patch_file(output_file_tmp, commit.repo)

            if output_file.is_file():
                idiff = interdiff(str(output_file), str(output_file_tmp))
                if idiff != "" and not check_patch_applies(
                    commit.repo, commit.parent, output_file
                ):
                    print(f"[*] {commit.filename}")
                    _ = output_file_tmp.rename(output_file)
                else:
                    output_file_tmp.unlink()
            else:
                print(f"[+] {commit.filename}")
                _ = output_file_tmp.rename(output_file)


def fixup_patch_file(patch: Path, repo: Path) -> None:
    with patch.open("r+") as file:
        lines: list[str] = []
        for line in file:
            if line.startswith(("diff --git", "+++", "---")):
                line = line.replace(" a/", f" a/{repo}/")
                line = line.replace(" b/", f" b/{repo}/")
            lines.append(line)
        _ = file.seek(0)
        file.writelines(lines)
        _ = file.truncate()


def do_patch(args: PatchArgs) -> None:
    path = find_git_repo()

    version_file = path / "browser" / "config" / "version_display.txt"
    if not version_file.is_file():
        print("error: not in a gecko-dev repository")
        sys.exit(1)

    patcher = Patcher(path, args.output)
    if args.list:
        patcher.list()
        return

    patcher.run(args)
