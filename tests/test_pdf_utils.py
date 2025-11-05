"""Tests for PDF utilities."""

from io import BytesIO
from pathlib import Path

from flashpapers.utils.pdf_utils import delete_pdf, get_pdf_path, save_pdf


class TestPDFUtils:
    """Tests for PDF utility functions."""

    def test_save_pdf_from_bytes(self, temp_dir):
        """Test saving a PDF from bytes."""
        pdf_content = b"%PDF-1.4 test pdf content"
        pdf_path = save_pdf(pdf_content, "Test Paper", "test-id-123", pdf_dir=temp_dir)

        assert Path(pdf_path).exists()
        assert "test-id-123" in pdf_path
        assert pdf_path.endswith(".pdf")

        # Verify content
        with open(pdf_path, "rb") as f:
            content = f.read()
        assert content == pdf_content

    def test_save_pdf_from_bytesio(self, temp_dir):
        """Test saving a PDF from BytesIO."""
        pdf_content = b"%PDF-1.4 test pdf content"
        pdf_file = BytesIO(pdf_content)

        pdf_path = save_pdf(pdf_file, "Test Paper", "test-id-456", pdf_dir=temp_dir)

        assert Path(pdf_path).exists()
        assert "test-id-456" in pdf_path

    def test_save_pdf_filename_sanitization(self, temp_dir):
        """Test that PDF filename is sanitized."""
        pdf_content = b"%PDF-1.4"
        pdf_path = save_pdf(
            pdf_content, "Test/Paper:With*Invalid|Characters", "test-id", pdf_dir=temp_dir
        )

        # Should remove invalid characters
        assert "/" not in Path(pdf_path).name
        assert ":" not in Path(pdf_path).name
        assert "*" not in Path(pdf_path).name

    def test_save_pdf_long_title(self, temp_dir):
        """Test saving PDF with very long title."""
        pdf_content = b"%PDF-1.4"
        long_title = "A" * 100  # Very long title

        pdf_path = save_pdf(pdf_content, long_title, "test-id", pdf_dir=temp_dir)

        # Filename should be truncated
        assert len(Path(pdf_path).stem) < 100

    def test_delete_pdf(self, temp_dir):
        """Test deleting a PDF."""
        # Create a PDF first
        pdf_content = b"%PDF-1.4"
        pdf_path = save_pdf(pdf_content, "Test", "test-id", pdf_dir=temp_dir)

        # Verify it exists
        assert Path(pdf_path).exists()

        # Delete it
        success = delete_pdf(pdf_path)
        assert success is True
        assert not Path(pdf_path).exists()

    def test_delete_nonexistent_pdf(self):
        """Test deleting a non-existent PDF."""
        success = delete_pdf("/nonexistent/path/to/file.pdf")
        assert success is False

    def test_get_pdf_path(self, temp_dir):
        """Test getting PDF path by paper ID."""
        # Create a PDF
        pdf_content = b"%PDF-1.4"
        saved_path = save_pdf(pdf_content, "Test Paper", "test-id-789", pdf_dir=temp_dir)

        # Find it by ID
        found_path = get_pdf_path("test-id-789", pdf_dir=temp_dir)

        assert found_path is not None
        assert str(found_path) == saved_path

    def test_get_pdf_path_not_found(self, temp_dir):
        """Test getting PDF path when it doesn't exist."""
        found_path = get_pdf_path("nonexistent-id", pdf_dir=temp_dir)
        assert found_path is None

    def test_get_pdf_path_no_directory(self, temp_dir):
        """Test getting PDF path when directory doesn't exist."""
        nonexistent_dir = temp_dir / "nonexistent"
        found_path = get_pdf_path("test-id", pdf_dir=nonexistent_dir)
        assert found_path is None
