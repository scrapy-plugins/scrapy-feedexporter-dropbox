import os


def parse_uri(uri):
    """Takes in uri and returns the dropbox path"""
    if not uri.startswith("dropbox://"):
        return None

    dropbox_path = uri.replace("dropbox:/", "")
    _, file_extension = os.path.splitext(dropbox_path)

    if not file_extension:
        return None

    return dropbox_path
