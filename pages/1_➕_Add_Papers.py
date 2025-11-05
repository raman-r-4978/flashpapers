"""Add new papers to the collection."""

import streamlit as st

from flashpapers.models import Flashpaper

st.set_page_config(page_title="Add Papers", page_icon="➕", layout="wide")

st.title("➕ Add New Paper")

# Get instances from session state
data_handler = st.session_state.data_handler
config = st.session_state.config

# Add paper form
with st.form("add_paper_form", clear_on_submit=True):
    st.subheader("Paper Information")

    col1, col2 = st.columns(2)

    with col1:
        paper_title = st.text_input("Paper Title *", placeholder="Enter the paper title")
        authors = st.text_input("Authors *", placeholder="e.g., Smith, J., Doe, A.")

    with col2:
        categories = st.multiselect("Categories", options=config.categories)
        keywords = st.text_input("Keywords (comma-separated)", placeholder="e.g., ML, NLP, GPT")

    # Link
    link = st.text_input("Paper URL", placeholder="https://...")

    st.subheader("Paper Details")

    # Create tabs for organized input
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Background & Objectives", "Methodology", "Results", "Contributions"]
    )

    with tab1:
        background = st.text_area(
            "Background of the Study",
            placeholder="What is the context and motivation for this research?",
            height=150,
        )
        objectives = st.text_area(
            "Research Objectives and Hypothesis",
            placeholder="What are the main research questions and hypotheses?",
            height=150,
        )

    with tab2:
        methodology = st.text_area(
            "Methodology",
            placeholder="How was the research conducted? What methods were used?",
            height=200,
        )

    with tab3:
        results = st.text_area(
            "Results and Findings",
            placeholder="What were the key findings and results?",
            height=150,
        )
        discussion = st.text_area(
            "Discussion and Interpretation",
            placeholder="How do the authors interpret the results?",
            height=150,
        )

    with tab4:
        contributions = st.text_area(
            "Contributions to the Field",
            placeholder="What are the main contributions of this work?",
            height=150,
        )
        significance = st.text_area(
            "Achievements and Significance",
            placeholder="Why is this work important?",
            height=150,
        )

    # Notes
    notes = st.text_area("Additional Notes", placeholder="Any additional notes or thoughts...")

    # PDF upload
    pdf_file = st.file_uploader("Upload PDF (optional)", type=["pdf"])

    # Submit button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        submitted = st.form_submit_button("Add Paper", use_container_width=True, type="primary")
    with col2:
        clear = st.form_submit_button("Clear Form", use_container_width=True)

    if submitted:
        # Validate required fields
        if not paper_title or not authors:
            st.error("Please fill in the required fields (Paper Title and Authors)")
        else:
            # Process keywords
            keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]

            # Create flashpaper
            try:
                flashpaper_id = data_handler.add_flashcard(
                    paper_title=paper_title,
                    authors=authors,
                    background_of_the_study=background,
                    research_objectives_and_hypothesis=objectives,
                    methodology=methodology,
                    results_and_findings=results,
                    discussion_and_interpretation=discussion,
                    contributions_to_the_field=contributions,
                    achievements_and_significance=significance,
                    link=link or None,
                    notes=notes,
                    keywords=keyword_list,
                    category=categories,
                )

                # Handle PDF upload
                if pdf_file:
                    from flashpapers.utils.pdf_utils import save_pdf

                    pdf_path = save_pdf(pdf_file.getvalue(), paper_title, flashpaper_id)

                    # Update flashpaper with PDF path
                    flashpaper = data_handler.get_flashcard_by_id(flashpaper_id)
                    flashpaper.pdf_path = pdf_path
                    data_handler.update_flashcard(flashpaper)

                st.success(f"✅ Paper added successfully! (ID: {flashpaper_id[:8]}...)")
                st.balloons()

            except Exception as e:
                st.error(f"Error adding paper: {e}")

# Quick stats
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Papers", st.session_state.storage.get_count())
with col2:
    from flashpapers.utils import AnalyticsUtils

    analytics = AnalyticsUtils(st.session_state.storage)
    stats = analytics.get_analytics()
    st.metric("Papers Reviewed", stats["reviewed_papers"])
with col3:
    st.metric("Due for Review", stats["papers_due_today"])
