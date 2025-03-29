"""
Custom exceptions for py-mail-me package.
"""

class PyMailMeError(Exception):
    """Base exception for py-mail-me package."""
    pass

class EmailConfigError(PyMailMeError):
    """Raised when there's an error in email configuration."""
    pass

class EmailAuthError(PyMailMeError):
    """Raised when authentication fails."""
    pass

class EmailSendError(PyMailMeError):
    """Raised when email sending fails."""
    pass

class TemplateError(PyMailMeError):
    """Raised when there's an error in email template."""
    pass 