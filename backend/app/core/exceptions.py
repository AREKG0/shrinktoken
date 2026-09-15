class ShrinkTokenError(Exception):
    """Base exception for ShrinkToken."""
    pass

class CompressionError(ShrinkTokenError):
    """Raised when compression fails."""
    pass

class ValidationError(ShrinkTokenError):
    """Raised when validation fails."""
    pass

class ConfigurationError(ShrinkTokenError):
    """Raised when configuration is invalid."""
    pass
