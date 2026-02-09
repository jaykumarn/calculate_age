# -*- coding: utf-8 -*-
"""
Core Interfaces Module
Defines contracts for all service implementations following Interface Segregation Principle.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain import AgeCalculationResult, CalculationRequest


class IDateTimeProvider(ABC):
    """Interface for datetime operations to enable testability."""
    
    @abstractmethod
    def get_current_time(self) -> datetime:
        """Returns the current datetime."""
        pass

    @abstractmethod
    def get_current_year(self) -> int:
        """Returns the current year."""
        pass

    @abstractmethod
    def get_current_month(self) -> int:
        """Returns the current month (1-12)."""
        pass

    @abstractmethod
    def get_current_day(self) -> int:
        """Returns the current day of month."""
        pass


class ILeapYearCalculator(ABC):
    """Interface for leap year determination."""
    
    @abstractmethod
    def is_leap_year(self, year: int) -> bool:
        """Determines if a given year is a leap year."""
        pass

    @abstractmethod
    def get_days_in_year(self, year: int) -> int:
        """Returns the number of days in a given year."""
        pass


class IMonthDaysCalculator(ABC):
    """Interface for calculating days in months."""
    
    @abstractmethod
    def get_days_in_month(self, month: int, is_leap_year: bool) -> int:
        """Returns the number of days in a given month."""
        pass

    @abstractmethod
    def get_days_up_to_month(self, month: int, is_leap_year: bool) -> int:
        """Returns total days from January 1 to the start of given month."""
        pass


class IAgeCalculationStrategy(ABC):
    """Strategy interface for different age calculation methods."""
    
    @abstractmethod
    def calculate(self, request: CalculationRequest) -> AgeCalculationResult:
        """Performs age calculation based on the request."""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Returns the name of this calculation strategy."""
        pass


class IAgeCalculatorService(ABC):
    """Main service interface for age calculations."""
    
    @abstractmethod
    def calculate_age(
        self,
        name: str,
        age_years: int
    ) -> AgeCalculationResult:
        """Calculates complete age information."""
        pass

    @abstractmethod
    def calculate_days_lived(self, age_years: int) -> int:
        """Calculates total days lived."""
        pass

    @abstractmethod
    def calculate_months_lived(self, age_years: int) -> int:
        """Calculates total months lived."""
        pass


class IValidationService(ABC):
    """Interface for input validation."""
    
    @abstractmethod
    def validate_name(self, name: str) -> bool:
        """Validates a person's name."""
        pass

    @abstractmethod
    def validate_age(self, age: int) -> bool:
        """Validates an age value."""
        pass

    @abstractmethod
    def validate_request(self, request: CalculationRequest) -> List[str]:
        """Validates a complete calculation request, returns list of errors."""
        pass


class IResultFormatter(ABC):
    """Interface for formatting calculation results."""
    
    @abstractmethod
    def format_for_display(self, result: AgeCalculationResult) -> str:
        """Formats result for UI display."""
        pass

    @abstractmethod
    def format_for_export(self, result: AgeCalculationResult) -> str:
        """Formats result for file export."""
        pass


class ICalculationRepository(ABC):
    """Repository interface for persisting calculation history."""
    
    @abstractmethod
    def save(self, result: AgeCalculationResult) -> str:
        """Saves a calculation result, returns ID."""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[AgeCalculationResult]:
        """Retrieves a calculation by ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[AgeCalculationResult]:
        """Retrieves all saved calculations."""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Deletes a calculation by ID."""
        pass

    @abstractmethod
    def clear_all(self) -> int:
        """Clears all calculations, returns count deleted."""
        pass


class IEventPublisher(ABC):
    """Interface for publishing domain events."""
    
    @abstractmethod
    def publish(self, event_type: str, data: dict) -> None:
        """Publishes an event."""
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler: callable) -> None:
        """Subscribes to an event type."""
        pass


__all__ = [
    'IDateTimeProvider',
    'ILeapYearCalculator',
    'IMonthDaysCalculator',
    'IAgeCalculationStrategy',
    'IAgeCalculatorService',
    'IValidationService',
    'IResultFormatter',
    'ICalculationRepository',
    'IEventPublisher'
]
