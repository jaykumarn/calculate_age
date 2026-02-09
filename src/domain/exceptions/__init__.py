# -*- coding: utf-8 -*-
"""
Domain Exception Hierarchy
Provides structured exception handling across all application layers.
"""
from typing import Optional, Dict, Any


class AgeCalculatorBaseException(Exception):
    """Base exception for all age calculator domain exceptions."""
    
    def __init__(
        self,
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details,
            'exception_type': self.__class__.__name__
        }


class ValidationException(AgeCalculatorBaseException):
    """Raised when input validation fails."""
    
    def __init__(
        self,
        message: str,
        field_name: str,
        invalid_value: Any = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={
                'field_name': field_name,
                'invalid_value': invalid_value,
                **(details or {})
            }
        )
        self.field_name = field_name
        self.invalid_value = invalid_value


class AgeValidationException(ValidationException):
    """Raised when age validation specifically fails."""
    
    def __init__(
        self,
        message: str,
        age_value: Any,
        min_age: int,
        max_age: int
    ):
        super().__init__(
            message=message,
            field_name="age",
            invalid_value=age_value,
            details={
                'min_age': min_age,
                'max_age': max_age
            }
        )
        self.error_code = "AGE_VALIDATION_ERROR"


class NameValidationException(ValidationException):
    """Raised when name validation fails."""
    
    def __init__(
        self,
        message: str,
        name_value: str,
        reason: str
    ):
        super().__init__(
            message=message,
            field_name="name",
            invalid_value=name_value,
            details={'reason': reason}
        )
        self.error_code = "NAME_VALIDATION_ERROR"


class CalculationException(AgeCalculatorBaseException):
    """Raised when age calculation fails."""
    
    def __init__(
        self,
        message: str,
        calculation_type: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="CALCULATION_ERROR",
            details={
                'calculation_type': calculation_type,
                **(details or {})
            }
        )


class ConfigurationException(AgeCalculatorBaseException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(
        self,
        message: str,
        config_key: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details={
                'config_key': config_key,
                **(details or {})
            }
        )


class UIException(AgeCalculatorBaseException):
    """Raised when UI operations fail."""
    
    def __init__(
        self,
        message: str,
        component: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="UI_ERROR",
            details={
                'component': component,
                **(details or {})
            }
        )


__all__ = [
    'AgeCalculatorBaseException',
    'ValidationException',
    'AgeValidationException',
    'NameValidationException',
    'CalculationException',
    'ConfigurationException',
    'UIException'
]
