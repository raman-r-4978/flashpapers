import logging
from datetime import date

import pandas as pd
import streamlit as st
from data_manager import ensure_directories, load_config, load_flashpapers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("flashpapers_app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Streamlit App Configuration (Set the page title and icon)
st.set_page_config(
    page_title="Flashpapers",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://github.com/your_repo/issues",  # TODO: Replace with your repo
        "Report a bug": "https://github.com/your_repo/issues",  # TODO: Replace with your repo
        "About": "# Flashpapers App\n\nThis app helps you retain research papers effectively using the SRS method.",
    },
)


# Initialize Session State
def initialize_session_state():
    """
    Initializes session state variables if they don't exist.
    """
    try:
        if "config" not in st.session_state:
            st.session_state["config"] = load_config()
            logger.info("Config loaded into session state.")
        if "flashpapers" not in st.session_state:
            st.session_state["flashpapers"] = load_flashpapers()
            logger.info("Flashpapers loaded into session state.")
    except Exception as e:
        logger.error(f"Error initializing session state: {e}")
        st.exception(e)


def run_app():
    st.write(
        """
        # Flashpapers App
        ## Enhance your research retention!
        """
    )
    with st.sidebar:
        st.header("Settings")


if __name__ == "__main__":
    run_app()
