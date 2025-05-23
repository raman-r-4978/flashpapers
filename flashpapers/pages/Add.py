import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st
from data_manager import (
    DEFAULT_CONFIG,
    DEFAULT_FLASHPAPER_STRUCTURE,
    FLASHPAPER_FILE,
    add_flashpaper,
    load_config,
)
from utils import fetch_from_arxiv

logger = logging.getLogger(__name__)

ADDED_DATE_FIELD = "added_date"
NEXT_REVIEW_DATE_FIELD = "next_review_date"

def init_page():
    """
    Initialize page configuration
    """

    st.set_page_config(page_title="Add", layout="wide")
    st.markdown("## 📝 New Flashpaper")
    st.markdown("---")


def create_manual_entry_form(categories: List[str]) -> Dict[str, Any]:
    """
    Create and process the manual entry form
    """

    st.subheader("Enter Paper Details Manually")

    with st.form("add_flashpaper_form_manual", clear_on_submit=True):
        keys = list(DEFAULT_FLASHPAPER_STRUCTURE.keys())
        values = list(DEFAULT_FLASHPAPER_STRUCTURE.values())

        # Required fields
        paper_title = st.text_input(f"{keys[0]} *", placeholder=values[0])
        authors = st.text_input(f"{keys[1]} *", placeholder=values[1])

        # Optional fields
        background_of_the_study = st.text_area(keys[2], placeholder=values[2])
        research_objectives_and_hypothesis = st.text_area(keys[3], placeholder=values[3])
        methodology = st.text_area(keys[4], placeholder=values[4])
        results_and_findings = st.text_area(keys[5], placeholder=values[5])
        discussion_and_interpretation = st.text_area(keys[6], placeholder=values[6])
        contributions_to_the_field = st.text_area(keys[7], placeholder=values[7])
        achievements_and_significance = st.text_area(keys[8], placeholder=values[8])
        link = st.text_input(keys[9], placeholder=values[9])
        notes = st.text_area(keys[10], placeholder=values[10])
        keywords = st.text_input(keys[11], placeholder=values[11])
        category = st.multiselect(f"{keys[12]} *", categories, default=categories[0])

        submit_button = st.form_submit_button(label="Add")

        if submit_button:
            # Validate required fields
            if not paper_title:
                st.error("Paper title is required")
                return None
            if not authors:
                st.error("Author information is required")
                return None
            if not category:
                st.error("At least one category must be selected")
                return None

            flashpaper = {
                "paper_title": paper_title,
                "authors": authors,
                "background_of_the_study": background_of_the_study,
                "research_objectives_and_hypothesis": research_objectives_and_hypothesis,
                "methodology": methodology,
                "results_and_findings": results_and_findings,
                "discussion_and_interpretation": discussion_and_interpretation,
                "contributions_to_the_field": contributions_to_the_field,
                "achievements_and_significance": achievements_and_significance,
                "link": link,
                "notes": notes,
                "keywords": ([k.strip() for k in keywords.split(",")] if keywords else []),
                "category": category,
                ADDED_DATE_FIELD: datetime.today(),
                NEXT_REVIEW_DATE_FIELD: datetime.today(),
            }
            return flashpaper

    return None


def create_arxiv_import_form() -> Optional[Dict[str, Any]]:
    """
    Create and process the arXiv import form
    """

    st.subheader("Import Paper from arXiv")

    with st.form("add_flashpaper_form_arxiv", clear_on_submit=True):
        arxiv_id = st.text_input(
            "arXiv ID or URL",
            placeholder="e.g., 2303.08774 or https://arxiv.org/abs/2303.08774",
        )

        categories = DEFAULT_CONFIG["categories"]
        category = st.multiselect("Category *", categories, default=categories[0])

        submit_button = st.form_submit_button(label="Import")

        if submit_button:
            if not arxiv_id:
                st.error("Please enter an arXiv ID or URL")
                return None

            if not category:
                st.error("At least one category must be selected")
                return None

            with st.spinner("Fetching paper from arXiv..."):
                pass


def main():
    """
    Main function to run the app
    """

    init_page()

    categories = DEFAULT_CONFIG["categories"]
    tab1, tab2 = st.tabs(["Manual Entry", "Import from arXiv"])

    with tab1:
        flashpaper_data = create_manual_entry_form(categories)
        if flashpaper_data is not None:
            try:
                add_flashpaper(flashpaper_data, FLASHPAPER_FILE)
                st.success("Flash Paper added successfully!")
                st.toast("Your new flashpaper has been added successfully!", icon="✅")
            except Exception as e:
                logger.error(f"Error saving flashpaper: {e}")
                st.error(f"Failed to save flashpaper: {str(e)}")

    with tab2:
        arxiv_paper_data = create_arxiv_import_form()
        if arxiv_paper_data is not None:
            try:
                add_flashpaper(arxiv_paper_data, FLASHPAPER_FILE)
                st.success("arXiv paper added successfully!")
                st.toast("Your new flashpaper has been added successfully!", icon="✅")
                # Clear the prefill data after successful addition
            except Exception as e:
                logger.error(f"Error saving arXiv paper: {e}")
                st.error(f"Failed to save arXiv paper: {str(e)}")

if __name__ == "__main__":
    main()
