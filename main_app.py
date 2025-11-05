"""Main entry point for Flashpapers application."""

import streamlit as st

from flashpapers.config import ConfigManager
from flashpapers.utils import FlashcardDataHandler, FlashcardStorage

# Page configuration
st.set_page_config(
    page_title="Flashpapers",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "storage" not in st.session_state:
    st.session_state.storage = FlashcardStorage()

if "data_handler" not in st.session_state:
    st.session_state.data_handler = FlashcardDataHandler(storage=st.session_state.storage)

if "config_manager" not in st.session_state:
    st.session_state.config_manager = ConfigManager()
    st.session_state.config = st.session_state.config_manager.get_config()

# Main page
st.title("📚 Flashpapers")
st.markdown(
    """
Welcome to **Flashpapers** - Your intelligent research paper memory system!

### Quick Start
- **➕ Add Papers**: Add new research papers to your collection
- **🔄 Review**: Review papers using spaced repetition
- **🔍 Search**: Find papers by title, author, or keywords
- **📊 Analytics**: Track your learning progress

Select a page from the sidebar to get started.
"""
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Display statistics
    total_papers = st.session_state.storage.get_count()
    st.metric("Total Papers", total_papers)

    # Categories management
    st.subheader("Categories")
    current_categories = st.session_state.config.categories

    # Display current categories
    st.write("Current categories:")
    for cat in current_categories:
        st.text(f"• {cat}")

    # Add new category
    with st.expander("Add New Category"):
        new_category = st.text_input("Category name")
        if st.button("Add Category"):
            if new_category and new_category not in current_categories:
                current_categories.append(new_category)
                st.session_state.config_manager.update(categories=current_categories)
                st.success(f"Added category: {new_category}")
                st.rerun()
            elif new_category in current_categories:
                st.warning("Category already exists")

    # Backup management
    st.subheader("Backup")
    if st.button("Create Backup"):
        backup_path = st.session_state.storage.create_backup()
        st.success(f"Backup created: {backup_path.name}")

    # About
    st.markdown("---")
    st.markdown("**Flashpapers** v0.1.0")
    st.markdown("Built with ❤️ using Streamlit")
