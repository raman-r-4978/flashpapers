"""PDF handling utilities."""

from io import BytesIO
from pathlib import Path
from typing import Union


def save_pdf(
    pdf_file: Union[BytesIO, bytes], paper_title: str, paper_id: str, pdf_dir: Path = None
) -> str:
    """
    Save a PDF file to the storage directory.

    Args:
        pdf_file: PDF file content (BytesIO or bytes)
        paper_title: Title of the paper (for filename)
        paper_id: ID of the paper
        pdf_dir: Directory to save PDFs. Defaults to data/pdfs

    Returns:
        Path to the saved PDF file
    """
    if pdf_dir is None:
        pdf_dir = Path("data/pdfs")

    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_title = "".join(c for c in paper_title if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_title = safe_title[:50]  # Limit length

    filename = f"{paper_id}_{safe_title}.pdf"
    pdf_path = pdf_dir / filename

    # Write PDF content
    if isinstance(pdf_file, BytesIO):
        content = pdf_file.getvalue()
    else:
        content = pdf_file

    with open(pdf_path, "wb") as f:
        f.write(content)

    return str(pdf_path)


def delete_pdf(pdf_path: str) -> bool:
    """
    Delete a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        path = Path(pdf_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting PDF: {e}")
        return False


def get_pdf_path(paper_id: str, pdf_dir: Path = None) -> Union[Path, None]:
    """
    Get the PDF path for a paper by ID.

    Args:
        paper_id: ID of the paper
        pdf_dir: Directory where PDFs are stored

    Returns:
        Path to PDF if found, None otherwise
    """
    if pdf_dir is None:
        pdf_dir = Path("data/pdfs")

    if not pdf_dir.exists():
        return None

    # Find PDF file starting with paper_id
    for pdf_file in pdf_dir.glob(f"{paper_id}_*.pdf"):
        return pdf_file

    return None
