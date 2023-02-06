class WrongQueryParameters(Exception):
    """Raised when the query parameters are wrong."""

    def __str__(self):
        return "Wrong query parameters."


class UnauthorizedAccess(Exception):
    """Raised when API key is not provided."""

    def __str__(self):
        return "API key is not provided"


class WrongAPIKey(Exception):
    """Raised when provided API key is wrong."""

    def __str__(self):
        return "Wrong API key."


class WrongDirectory(Exception):
    """Raised when the directory for cache does not exist."""

    def __str__(self):
        return "The provided directory for a cache does not exist."
