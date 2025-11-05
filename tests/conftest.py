"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest

from flashpapers.config import ConfigManager
from flashpapers.models import Flashpaper
from flashpapers.utils import AnalyticsUtils, FlashcardDataHandler, FlashcardStorage, SearchUtils


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


@pytest.fixture
def storage(temp_dir):
    """Create a FlashcardStorage instance with temporary storage."""
    storage_path = temp_dir / "test_flashpapers.json"
    return FlashcardStorage(storage_path=storage_path)


@pytest.fixture
def config_manager(temp_dir):
    """Create a ConfigManager instance with temporary config."""
    config_path = temp_dir / "test_config.json"
    return ConfigManager(config_path=config_path)


@pytest.fixture
def data_handler(storage, config_manager):
    """Create a FlashcardDataHandler instance."""
    return FlashcardDataHandler(storage=storage, config_manager=config_manager)


@pytest.fixture
def analytics(storage):
    """Create an AnalyticsUtils instance."""
    return AnalyticsUtils(storage=storage)


@pytest.fixture
def search_utils(storage):
    """Create a SearchUtils instance."""
    return SearchUtils(storage=storage)


@pytest.fixture
def sample_flashpaper():
    """Create a sample flashpaper for testing."""
    return Flashpaper(
        paper_title="Attention Is All You Need",
        authors="Vaswani et al.",
        background_of_the_study="Sequence modeling with RNNs",
        research_objectives_and_hypothesis="Propose transformer architecture",
        methodology="Self-attention mechanism",
        results_and_findings="State-of-the-art results on translation",
        discussion_and_interpretation="Transformers outperform RNNs",
        contributions_to_the_field="Introduced transformer architecture",
        achievements_and_significance="Foundation for modern NLP",
        link="https://arxiv.org/abs/1706.03762",
        notes="Seminal paper",
        keywords=["transformers", "attention", "NLP"],
        category=["Deep Learning", "Natural Language Processing"],
    )


@pytest.fixture
def sample_flashpapers():
    """Create multiple sample flashpapers for testing."""
    papers = [
        Flashpaper(
            paper_title="BERT: Pre-training of Deep Bidirectional Transformers",
            authors="Devlin et al.",
            keywords=["BERT", "pre-training", "NLP"],
            category=["Deep Learning", "Natural Language Processing"],
        ),
        Flashpaper(
            paper_title="GPT-3: Language Models are Few-Shot Learners",
            authors="Brown et al.",
            keywords=["GPT", "language models", "few-shot"],
            category=["Deep Learning", "Natural Language Processing"],
        ),
        Flashpaper(
            paper_title="ResNet: Deep Residual Learning",
            authors="He et al.",
            keywords=["ResNet", "CNN", "residual"],
            category=["Deep Learning", "Computer Vision"],
        ),
    ]
    return papers
