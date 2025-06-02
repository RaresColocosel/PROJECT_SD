import os

class FileDataExtractor:
    @staticmethod
    def extract_text(filepath):
        _, ext = os.path.splitext(filepath.lower())
        if ext == ".txt":
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
            except Exception:
                return ""
        # Other file types: we return empty content
        return ""

    @staticmethod
    def extract_type(filepath):
        _, ext = os.path.splitext(filepath.lower())
        if ext.startswith("."):
            return ext[1:]
        return ""
