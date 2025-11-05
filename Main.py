"""Main entry point for Flashpapers application."""

import streamlit as st

from flashpapers.config import ConfigManager
from flashpapers.models import Flashpaper
from flashpapers.utils import FlashcardDataHandler, FlashcardStorage
from typing import List

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

# Cache management functions
def get_cached_flashpapers() -> List[Flashpaper]:
    """
    Get flashpapers from session state cache or load from storage.
    
    Returns:
        List of Flashpaper objects
    """
    cache_key = "_flashpapers_cache"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = st.session_state.storage.load_all()
    return st.session_state[cache_key]


def invalidate_flashpapers_cache() -> None:
    """Invalidate the flashpapers cache in session state."""
    cache_key = "_flashpapers_cache"
    if cache_key in st.session_state:
        del st.session_state[cache_key]
    # Also invalidate storage cache
    st.session_state.storage.invalidate_cache()

# Main page
st.title("📚 Flashpapers")
st.markdown(
    """
Welcome to **Flashpapers** - Your intelligent research paper memory system!

### Quick Start
- **Add Papers**: Add new research papers to your collection
- **Review**: Review papers using spaced repetition
- **Search**: Find papers by title, author, or keywords
- **Analytics**: Track your learning progress

Select a page from the sidebar to get started.
"""
)

# Categories management
st.divider()
st.subheader("📁 Categories")
current_categories = st.session_state.config.categories

# Display current categories in a nicer format
if current_categories:
    st.markdown("**Current categories:**")
    cols = st.columns(min(len(current_categories), 4))
    for idx, cat in enumerate(current_categories):
        with cols[idx % len(cols)]:
            st.markdown(f"🏷️ `{cat}`")
else:
    st.info("No categories yet. Add your first category below!")

# Add new category
with st.expander("➕ Add New Category", expanded=False):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_category = st.text_input(
            "Category name",
            placeholder="Enter category name...",
            label_visibility="collapsed"
        )
    with col2:
        add_button = st.button("Add", type="primary", use_container_width=True)
    
    if add_button:
        if new_category:
            new_category = new_category.strip()
            if new_category not in current_categories:
                current_categories.append(new_category)
                st.session_state.config_manager.update(categories=current_categories)
                st.success(f"✅ Added category: **{new_category}**")
                st.rerun()
            else:
                st.warning("⚠️ Category already exists")
        else:
            st.error("Please enter a category name")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Display statistics (uses cache)
    total_papers = len(get_cached_flashpapers())
    st.metric("Total Papers", total_papers)

    # Backup management
    st.subheader("Backup")
    if st.button("Create Backup"):
        backup_path = st.session_state.storage.create_backup()
        st.success(f"Backup created: {backup_path.name}")

    # About
    st.markdown("---")
    st.markdown("**Flashpapers** v0.1.0")
    st.markdown("Built with ❤️ using Streamlit")
