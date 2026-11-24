import urllib.request
from http.client import HTTPResponse

from .util import find_git_repo


def get_tags() -> dict[str, str]:
    req = urllib.request.Request(
        "https://github.com/ptrcnull/firefox-alpine.git/info/refs?service=git-upload-pack"
    )
    req.add_header("User-Agent", "git/2.48.0")
    res: HTTPResponse = urllib.request.urlopen(req)  # pyright: ignore[reportAny]

    tags: dict[str, str] = {}

    for line in res:
        if b"refs/tags/aports" in line:
            line = line.decode()
            parts = line.split("/")
            if len(parts) < 3:
                continue
            tag_name = parts[2].strip()
            if not tag_name.startswith("aports"):
                continue
            tag_name = tag_name[7:]

            if tag_name.endswith("base"):
                continue

            parts = tag_name.split("-")
            if len(parts) != 2:
                continue

            product, version = parts

            # 153.7 -> 153.7.0
            if product == "esr" and version.count(".") == 1:
                version += ".0"

            # 160 -> 160.0
            if len(version) == 3:
                version += ".0"

            # 161b5 -> 161.0b5
            version = version.replace("a", ".0a")
            version = version.replace("b", ".0b")

            tags[product] = version

    return tags


def do_readme() -> None:
    tags = get_tags()
    repo = find_git_repo()

    readme = repo / "README.md"

    with readme.open() as file:
        content = file.read()

    if "alpine" not in content:
        raise RuntimeError("Run this script on the readme branch of firefox-alpine!")

    lines = content.splitlines(keepends=True)

    for product, version in tags.items():
        for i in range(len(lines)):
            query = f'data-product="{product}"'
            line = lines[i]
            if query in line:
                lines[i] = f'\t\t<td align="center" {query}><b>{version}</b></td>\n'

    with readme.open("w") as file:
        file.writelines(lines)
