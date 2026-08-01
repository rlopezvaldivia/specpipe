"""
File management utilities for specpipe.
"""

from pathlib import Path
import shutil


class FileManager:
    """
    Basic file and directory operations.
    """

    @staticmethod
    def make_dir(path):
        """
        Create directory if it does not exist.
        """
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def remove(path):
        """
        Remove file or directory.
        """
        p = Path(path)

        if not p.exists():
            return

        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()

    @staticmethod
    def copy(source, destination):
        """
        Copy file or directory.
        """
        source = Path(source)
        destination = Path(destination)

        if source.is_dir():
            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True
            )
        else:
            shutil.copy2(
                source,
                destination
            )

    @staticmethod
    def move(source, destination):
        """
        Move file or directory.
        """
        shutil.move(
            str(source),
            str(destination)
        )

    @staticmethod
    def list_files(path, pattern="*.fits"):
        """
        List files matching pattern.
        """
        return sorted(
            Path(path).glob(pattern)
        )

    @staticmethod
    def clean_directory(path, pattern="*"):
        """
        Remove matching files.
        """
        for item in Path(path).glob(pattern):
            FileManager.remove(item)
