# -*- coding: utf-8 -*-
"""
Core Services Module
Implementation of business logic services.
"""
import time
from calendar import isleap
from datetime import datetime
from typing import List, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain import (
    AgeCalculationResult,
    CalculationRequest,
    PersonName,
    Age,
    AgeInMonths,
    AgeInDays,
    AgeInWeeks,
    AgeInHours,
    AgeInMinutes,
    CalculationTimestamp,
    AgeValidationException,
    NameValidationException,
    CalculationException
)
from core.interfaces import (
    IDateTimeProvider,
    ILeapYearCalculator,
    IMonthDaysCalculator,
    IAgeCalculatorService,
    IValidationService
)
from config import ConfigurationManager, ValidationConfig


class SystemDateTimeProvider(IDateTimeProvider):
    """System implementation of datetime provider."""
    
    def get_current_time(self) -> datetime:
        return datetime.now()

    def get_current_year(self) -> int:
        return time.localtime(time.time()).tm_year

    def get_current_month(self) -> int:
        return time.localtime(time.time()).tm_mon

    def get_current_day(self) -> int:
        return time.localtime(time.time()).tm_mday


class StandardLeapYearCalculator(ILeapYearCalculator):
    """Standard implementation using calendar module."""
    
    def is_leap_year(self, year: int) -> bool:
        return isleap(year)

    def get_days_in_year(self, year: int) -> int:
        return 366 if self.is_leap_year(year) else 365


class StandardMonthDaysCalculator(IMonthDaysCalculator):
    """Standard implementation for month days calculation."""
    
    DAYS_IN_MONTH = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    
    DAYS_IN_MONTH_LEAP = {
        1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    def get_days_in_month(self, month: int, is_leap_year: bool) -> int:
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}")
        lookup = self.DAYS_IN_MONTH_LEAP if is_leap_year else self.DAYS_IN_MONTH
        return lookup[month]

    def get_days_up_to_month(self, month: int, is_leap_year: bool) -> int:
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}")
        total = 0
        for m in range(1, month):
            total += self.get_days_in_month(m, is_leap_year)
        return total


class InputValidationService(IValidationService):
    """Service for validating user inputs."""
    
    def __init__(self, config: Optional[ValidationConfig] = None):
        self._config = config or ConfigurationManager().get_validation_config()

    def validate_name(self, name: str) -> bool:
        if not name or not name.strip():
            return False
        if len(name) < self._config.min_name_length:
            return False
        if len(name) > self._config.max_name_length:
            return False
        if self._config.strict_name_validation:
            return all(c in self._config.allowed_name_characters for c in name)
        return True

    def validate_age(self, age: int) -> bool:
        return self._config.min_age <= age <= self._config.max_age

    def validate_request(self, request: CalculationRequest) -> List[str]:
        errors = []
        if not self.validate_name(request.name):
            errors.append(f"Invalid name: must be {self._config.min_name_length}-{self._config.max_name_length} characters")
        if not self.validate_age(request.age_in_years):
            errors.append(f"Invalid age: must be between {self._config.min_age} and {self._config.max_age}")
        return errors

    def validate_name_with_exception(self, name: str) -> None:
        if not name or not name.strip():
            raise NameValidationException(
                message="Name cannot be empty",
                name_value=name,
                reason="empty_value"
            )
        if len(name) < self._config.min_name_length:
            raise NameValidationException(
                message=f"Name must be at least {self._config.min_name_length} characters",
                name_value=name,
                reason="too_short"
            )
        if len(name) > self._config.max_name_length:
            raise NameValidationException(
                message=f"Name cannot exceed {self._config.max_name_length} characters",
                name_value=name,
                reason="too_long"
            )

    def validate_age_with_exception(self, age: int) -> None:
        if age < self._config.min_age or age > self._config.max_age:
            raise AgeValidationException(
                message=f"Age must be between {self._config.min_age} and {self._config.max_age}",
                age_value=age,
                min_age=self._config.min_age,
                max_age=self._config.max_age
            )


class AgeCalculatorServiceImpl(IAgeCalculatorService):
    """Main implementation of age calculation service."""
    
    def __init__(
        self,
        datetime_provider: Optional[IDateTimeProvider] = None,
        leap_year_calculator: Optional[ILeapYearCalculator] = None,
        month_days_calculator: Optional[IMonthDaysCalculator] = None,
        validation_service: Optional[IValidationService] = None
    ):
        self._datetime_provider = datetime_provider or SystemDateTimeProvider()
        self._leap_year_calculator = leap_year_calculator or StandardLeapYearCalculator()
        self._month_days_calculator = month_days_calculator or StandardMonthDaysCalculator()
        self._validation_service = validation_service or InputValidationService()

    def calculate_age(self, name: str, age_years: int) -> AgeCalculationResult:
        try:
            self._validation_service.validate_name_with_exception(name)
            self._validation_service.validate_age_with_exception(age_years)
        except Exception:
            raise

        current_year = self._datetime_provider.get_current_year()
        current_month = self._datetime_provider.get_current_month()
        current_day = self._datetime_provider.get_current_day()

        total_days = self._calculate_total_days(
            age_years, current_year, current_month, current_day
        )
        total_months = age_years * 12 + current_month
        total_weeks = total_days // 7
        total_hours = total_days * 24
        total_minutes = total_hours * 60

        birth_year = current_year - age_years

        return AgeCalculationResult(
            name=PersonName(name),
            age_years=Age(age_years),
            age_months=AgeInMonths(total_months),
            age_days=AgeInDays(total_days),
            age_weeks=AgeInWeeks(total_weeks),
            age_hours=AgeInHours(total_hours),
            age_minutes=AgeInMinutes(total_minutes),
            calculation_timestamp=CalculationTimestamp.now(),
            birth_year=birth_year,
            current_year=current_year
        )

    def _calculate_total_days(
        self,
        age_years: int,
        current_year: int,
        current_month: int,
        current_day: int
    ) -> int:
        birth_year = current_year - age_years
        total_days = 0

        for year in range(birth_year, current_year):
            total_days += self._leap_year_calculator.get_days_in_year(year)

        is_current_leap = self._leap_year_calculator.is_leap_year(current_year)
        for month in range(1, current_month):
            total_days += self._month_days_calculator.get_days_in_month(
                month, is_current_leap
            )

        total_days += current_day

        return total_days

    def calculate_days_lived(self, age_years: int) -> int:
        current_year = self._datetime_provider.get_current_year()
        current_month = self._datetime_provider.get_current_month()
        current_day = self._datetime_provider.get_current_day()
        return self._calculate_total_days(
            age_years, current_year, current_month, current_day
        )

    def calculate_months_lived(self, age_years: int) -> int:
        current_month = self._datetime_provider.get_current_month()
        return age_years * 12 + current_month


__all__ = [
    'SystemDateTimeProvider',
    'StandardLeapYearCalculator',
    'StandardMonthDaysCalculator',
    'InputValidationService',
    'AgeCalculatorServiceImpl'
]
