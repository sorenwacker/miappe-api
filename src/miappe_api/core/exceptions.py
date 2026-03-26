"""Custom exceptions for MIAPPE-API.

This module defines the exception hierarchy for the MIAPPE-API package.
"""


class MiappeError(Exception):
    """Base exception for MIAPPE-API errors.

    All custom exceptions in the package inherit from this class.
    """


class SpecError(MiappeError):
    """Exception raised for specification-related errors.

    This includes errors loading, parsing, or validating YAML specifications.
    """


class ModelError(MiappeError):
    """Exception raised for model-related errors.

    This includes errors generating, registering, or accessing Pydantic models.
    """


class ValidationFailedError(MiappeError):
    """Exception raised when validation fails.

    This is raised when entity data fails validation rules.
    """


class StorageIOError(MiappeError):
    """Exception raised for storage-related I/O errors.

    This includes errors reading from or writing to files.
    """
