#!/usr/bin/env python3
"""Format Python code using isort, black, and ruff."""

import argparse
import logging
import sys
from pathlib import Path
from subprocess import run

# Setup paths
SCRIPT_DIR = Path(__file__).parent
FLASHPAPERS_DIR = SCRIPT_DIR / "flashpapers"
TESTS_DIR = SCRIPT_DIR / "tests"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def run_command(desc: str, cmd: list) -> bool:
    """Run a command and return True if successful."""
    result = run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info(f"✓ {desc}")
        return True
    else:
        logger.error(f"✗ {desc} failed")
        if result.stdout:
            logger.error(result.stdout.strip())
        if result.stderr:
            logger.error(result.stderr.strip())
        return False


def format_directory(directory: Path, check: bool = False) -> bool:
    """Format a directory with isort, black, and optionally ruff."""
    logger.info(f"Processing {directory.name}")
    
    commands = [
        ("isort", ["isort", "--line-length", "100", "--profile", "black", 
                  *(["--check"] if check else []), str(directory)]),
        ("black", ["black", "--line-length", "100", 
                  *(["--check"] if check else []), str(directory)]),
    ]
    
    if not check:
        commands.append(("ruff", ["ruff", "check", str(directory)]))
    
    return all(run_command(desc, cmd) for desc, cmd in commands)


def main():
    parser = argparse.ArgumentParser(description="Format Python code with isort, black, and ruff")
    parser.add_argument("--check", action="store_true", help="Check formatting without making changes")
    args = parser.parse_args()

    directories = [FLASHPAPERS_DIR, TESTS_DIR]
    success = all(format_directory(d, args.check) for d in directories)
    
    if success:
        logger.info("All formatting completed successfully")
        sys.exit(0)
    else:
        logger.error("Some formatting operations failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
