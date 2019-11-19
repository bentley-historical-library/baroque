import unicodedata


def sanitize_text(string):
    """
    Helper function to remove newlines and extra spaces from a string"""
    if string is None:
        return ""
    else:
        string = string.replace("&", "and")

        # Replace "runs of consecutive whitespace" to single spaces AND remove trailing spaces
        # https://docs.python.org/3.8/library/stdtypes.html#str.split
        string = " ".join(string.split()).strip()

        # Remove non-alphanumeric characters BUT keeps single spaces and "/" (for date format)
        # https://stackoverflow.com/questions/7406102/create-sane-safe-filename-from-any-unsafe-string
        keep_characters = (" ", "/")
        string = "".join(c for c in string if c.isalnum() or c in keep_characters)

        # Normalize unicode accents AND remove unicode-specific characters
        # https://stackoverflow.com/questions/44431730/how-to-replace-accented-characters-in-python?rq=1
        # https://docs.python.org/3.8/library/unicodedata.html#unicodedata.normalize
        string = unicodedata.normalize('NFKC', string).encode('ascii', 'ignore').decode()

        return string
