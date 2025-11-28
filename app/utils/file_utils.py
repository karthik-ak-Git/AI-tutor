"""
File utility functions
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def ensure_upload_dir(upload_dir: str = "uploads") -> Path:
    """Ensure upload directory exists."""
    upload_path = Path(upload_dir)
    upload_path.mkdir(exist_ok=True)
    return upload_path


def validate_pdf_file(file_path: Path) -> bool:
    """Validate if file is a valid PDF."""
    try:
        # Check extension
        if not file_path.suffix.lower() == ".pdf":
            return False

        # Check if file exists and is readable
        if not file_path.exists() or not file_path.is_file():
            return False

        # Basic PDF validation - check magic bytes
        with open(file_path, "rb") as f:
            header = f.read(4)
            if header != b"%PDF":
                return False

        return True
    except Exception as e:
        logger.error(f"Error validating PDF: {e}")
        return False


def cleanup_old_files(upload_dir: str = "uploads", max_age_days: int = 30):
    """Clean up old uploaded files."""
    try:
        upload_path = Path(upload_dir)
        if not upload_path.exists():
            return

        # This is a placeholder - implement actual cleanup logic if needed
        # For now, we'll keep all files
        pass
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")
