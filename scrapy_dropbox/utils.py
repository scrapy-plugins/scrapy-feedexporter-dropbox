""" misc util methods"""


def parse_uri(uri):
    """Takes in uri and returns the dropbox path"""
    dropbox_path_parts = uri.split("dropbox:/", maxsplit=1)
    if (
        len(dropbox_path_parts) == 2
        and dropbox_path_parts[1]
        and dropbox_path_parts[1] != "/"
    ):
        return dropbox_path_parts[1]
    return None
