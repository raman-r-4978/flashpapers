# 📚 Flashpapers

> A professional, modular research paper management system with intelligent spaced repetition.

Flashpapers helps researchers and students efficiently manage, review, and retain knowledge from academic papers using proven spaced repetition techniques.

## ✨ Features

- **📄 Paper Management**: Add and organize research papers with detailed metadata
- **🔄 Spaced Repetition**: Intelligent review scheduling using SRS algorithm
- **🔍 Advanced Search**: Search by title, author, keywords, and categories
- **📊 Analytics Dashboard**: Track your learning progress and performance
- **🏷️ Smart Organization**: Categorize papers with tags and custom categories
- **📎 PDF Support**: Attach and manage PDF files for each paper
- **💾 Backup & Restore**: Automatic backup system for your data
- **🎨 Clean UI**: Intuitive Streamlit-based interface

## 🚀 Quick Start

### Using Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Run the application
poetry run streamlit run main_app.py
```

### Using Conda

```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate flashpapers

# Run the application
streamlit run main_app.py
```

### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pydantic pandas

# Run the application
streamlit run main_app.py
```

## 📁 Project Structure

```
flashpapers/
├── flashpapers/           # Main package
│   ├── models.py          # Pydantic data models
│   ├── config.py          # Configuration management
│   └── utils/             # Utility modules
│       ├── flashcard_storage.py    # Data persistence
│       ├── data_handler.py         # SRS logic
│       ├── analytics_utils.py      # Analytics
│       ├── search_utils.py         # Search functionality
│       └── pdf_utils.py            # PDF handling
├── pages/                 # Streamlit pages
│   ├── 1_➕_Add_Papers.py
│   ├── 2_🔄_Review.py
│   ├── 3_🔍_Search.py
│   └── 4_📊_Analytics.py
├── tests/                 # Test suite
├── main_app.py           # Application entry point
├── pyproject.toml        # Poetry configuration
└── environment.yml       # Conda configuration
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Using pytest
poetry run pytest

# With coverage report
poetry run pytest --cov=flashpapers --cov-report=term-missing

# Run integration test
python tests/test_app.py
```

## 📖 Usage Guide

### Adding Papers

1. Navigate to **➕ Add Papers**
2. Fill in required fields (Title, Authors)
3. Add detailed information in organized tabs:
   - Background & Objectives
   - Methodology
   - Results
   - Contributions
4. Optionally attach a PDF file
5. Click **Add Paper**

### Reviewing Papers

1. Navigate to **🔄 Review**
2. Click **Show Details** to view paper information
3. Rate your recall:
   - **😰 Hard**: Decrease review interval
   - **😐 Medium**: Keep current interval
   - **😊 Easy**: Increase review interval

The SRS algorithm automatically schedules the next review based on your performance.

### Searching Papers

1. Navigate to **🔍 Search**
2. Use the search box for full-text search
3. Apply advanced filters:
   - Filter by categories
   - Filter by keywords
4. Sort results by various criteria
5. View, edit, or delete papers

### Analytics

1. Navigate to **📊 Analytics**
2. View comprehensive statistics:
   - Total papers and reviews
   - Performance metrics
   - Category distribution
   - Upcoming reviews
   - Recent activity

## 🔧 Configuration

The application uses `data/config.json` for configuration. Default settings:

```json
{
  "categories": [
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Reinforcement Learning",
    "Optimization",
    "Other"
  ],
  "backup_frequency_days": 7,
  "srs_parameters": {
    "initial_ease_factor": 2.5,
    "minimum_interval_days": 1,
    "maximum_interval_days": 365,
    "easy_bonus": 1.3,
    "hard_penalty": 0.8
  }
}
```

## 🎯 Spaced Repetition Algorithm

Flashpapers uses a modified SM-2 algorithm:

- **Ease Factor**: Adjusts based on review difficulty
- **Interval**: Time between reviews increases with successful recalls
- **Adaptive**: Automatically adjusts to your learning pace

## 🗂️ Data Storage

- **Papers**: Stored in `data/flashpapers.json`
- **PDFs**: Stored in `data/pdfs/`
- **Backups**: Stored in `data/backups/`
- **Config**: Stored in `data/config.json`

## 🛠️ Development

### Code Quality

```bash
# Format code
poetry run black flashpapers tests
poetry run isort flashpapers tests

# Lint code
poetry run ruff check flashpapers tests

# Use the format script
python format.py
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_models.py

# Run with verbose output
poetry run pytest -v
```

## 📦 Requirements

- **Python**: 3.10 or higher
- **Core Dependencies**:
  - streamlit (^1.46.1)
  - pydantic (^2.10.5)
  - pandas (^2.2.3)
- **Dev Dependencies**:
  - pytest (^8.3.5)
  - pytest-cov (^6.0.0)
  - black (^25.1.0)
  - isort (^6.0.1)
  - ruff (^0.12.3)

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. Code is formatted with `black` and `isort`
2. Code passes `ruff` linting
3. All tests pass
4. New features include tests

## 📝 License

MIT License - feel free to use this project for your research and learning!

## 👨‍💻 Author

**Raman**
- Email: ramanrajarathinam@gmail.com

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by spaced repetition research and SuperMemo algorithm
