"""Minimal CLI for Phase 1 research validation."""

from __future__ import annotations

import argparse

from trident_lob.config import RunConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trident-lob",
        description="TRIDENT-LOB offline research scaffold.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the installed package version.",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("validate", help="Run offline validation placeholders.")
    subparsers.add_parser("config", help="Print the default non-secret config.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        from trident_lob import __version__

        print(__version__)
        return 0

    if args.command == "config":
        print(RunConfig.default().to_dict())
        return 0

    if args.command == "validate":
        print("Phase 1 offline validation scaffold only. No order routing exists.")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
