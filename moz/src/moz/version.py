import json
import urllib.request
from dataclasses import dataclass
from http.client import HTTPResponse


@dataclass
class VersionArgs:
    release: str | None


def parse_versions(resp: HTTPResponse) -> dict[str, str]:
    data = json.load(resp)  # pyright: ignore[reportAny]

    res: dict[str, str] = {}

    if not isinstance(data, dict):
        return res

    for key, value in data.items():  # pyright: ignore[reportUnknownVariableType]
        if isinstance(key, str) and isinstance(value, str):
            if "esr" in value:
                res[key] = value.replace("esr", "")
            elif "b" in value:
                res[key] = value.replace("b", "_beta")
            else:
                res[key] = value

    return res


def get_upstream_versions() -> dict[str, str]:
    url = "https://product-details.mozilla.org/1.0/firefox_versions.json"
    res: HTTPResponse = urllib.request.urlopen(url)  # pyright: ignore[reportAny]
    return parse_versions(res)


def get_aports_version(pkg: str, branch: str) -> str | None:
    url = f"https://git.alpinelinux.org/aports/plain/{pkg}/APKBUILD?h={branch}"
    res: HTTPResponse = urllib.request.urlopen(url)  # pyright: ignore[reportAny]
    version = None
    for line in res:
        if line.startswith(b"pkgver"):
            version = line.decode()[7:].strip()
    return version


def do_version(args: VersionArgs):
    release = args.release or "edge"
    branch = "master" if release == "edge" else release[1:] + "-stable"
    pkgs = [
        ("LATEST_FIREFOX_VERSION", "community/firefox"),
        ("FIREFOX_ESR", "community/firefox-esr"),
        ("LATEST_FIREFOX_VERSION", "community/thunderbird"),
    ]
    if release == "edge":
        pkgs.append(("FIREFOX_DEVEDITION", "testing/firefox-developer-edition"))

    versions = get_upstream_versions()

    for key, pkg in pkgs:
        latest = versions[key]

        current = get_aports_version(pkg, branch)

        if current == latest:
            print(f"{pkg}: up to date!")
        else:
            print(f"{pkg}: outdated (have {current}, want {latest})")
