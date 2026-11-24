#!/usr/bin/env python3

import argparse

from .patch import PatchArgs, do_patch
from .readme import do_readme
from .version import VersionArgs, do_version


class Args(argparse.Namespace):
    output: str | None  # pyright: ignore [reportUninitializedInstanceVariable]
    cmd: str  # pyright: ignore [reportUninitializedInstanceVariable]
    filename: str | None  # pyright: ignore [reportUninitializedInstanceVariable]
    list: bool  # pyright: ignore [reportUninitializedInstanceVariable]
    release: str | None  # pyright: ignore [reportUninitializedInstanceVariable]

    @staticmethod
    def parse() -> "Args":
        parser = argparse.ArgumentParser()
        _ = parser.add_argument("--release", help="Alpine release to use (e.g. v3.24)")

        cmds = parser.add_subparsers(dest="cmd")

        patch = cmds.add_parser("patch")
        _ = patch.add_argument(
            "--output",
            help="APKBUILD directory to use (default: detected from branch name)",
        )
        _ = patch.add_argument("--filename", help="Single patch filename to apply")
        _ = patch.add_argument("--list", action="store_true", help="Only list commits")

        _ = cmds.add_parser("readme")

        nsp = Args()
        return parser.parse_args(namespace=nsp)


def main() -> None:
    args = Args.parse()

    match args.cmd:
        case "patch":
            args = PatchArgs(args.output, args.filename, args.list)
            do_patch(args)
        case "readme":
            do_readme()
        case _:
            args = VersionArgs(args.release)
            do_version(args)


if __name__ == "__main__":
    main()
