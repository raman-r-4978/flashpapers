"""CLI entry point for Flashpapers application."""

import sys
from pathlib import Path


def main():
    """Run the Streamlit application."""
    import streamlit.web.cli as stcli

    # Get the path to main_app.py relative to the project root
    project_root = Path(__file__).parent.parent
    app_path = project_root / "main_app.py"

    # Set up sys.argv for streamlit
    sys.argv = ["streamlit", "run", str(app_path)]

    # Run streamlit
    stcli.main()


if __name__ == "__main__":
    main()
