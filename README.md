# Flashpapers App

A modular, robust, and user-friendly flashpapers app built with Streamlit. Supports Markdown/LaTeX, PDF attachments, spaced repetition, analytics, and seamless backup/restore.

## Features
- Add, review, and search flashpapers with Markdown/LaTeX support
- Attach and view PDFs for each flashpapers
- Spaced Repetition System (SRS) for efficient learning
- Analytics and tag-based filtering
- Backup/restore (JSON + PDFs as .zip)
- Modular codebase for easy maintenance

## Project Structure
- `Main.py`: Main Streamlit entry point
- `pages/`: Streamlit multipage app (Add, Review, Search)
- `data/`: Stores flashpapers, PDFs, and backups

## Getting Started
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Run the app:
   ```bash
   streamlit run main_app.py --server.port INT
   ```

## Requirements
- Python 3.8+
- Streamlit
- Pandas
- Arxiv

