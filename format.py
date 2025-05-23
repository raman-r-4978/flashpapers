#!/usr/bin/env python3
# format all using isort and black

import sys
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.append(str(scripts_dir))

import argparse
import logging
from subprocess import run

# Define the directory to format
flashpapers_dir = scripts_dir / "flashpapers"


def format_python(check: bool = False) -> int:
    logging.info(f"Format {flashpapers_dir}")

    if not check:
        result = run(
            f"""
                black --line-length 100 \
                      {flashpapers_dir} \
                      && \
                isort --line-length 100 \
                      --profile black \
                      {flashpapers_dir} \
            """,
            shell=True,
        )
    else:
        result = run(
            f"""
                black --line-length 100 \
                      --check {flashpapers_dir} \
                      && \
                isort --line-length 100 \
                      --check \
                      --profile black \
                      {flashpapers_dir}
            """,
            shell=True,
        )

    return result.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")

    args = parser.parse_args()

    python = format_python(args.check)

    exit(python)
