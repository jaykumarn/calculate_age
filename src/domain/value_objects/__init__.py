# -*- coding: utf-8 -*-
"""
Value Objects Module
Immutable domain value objects for type safety and domain modeling.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class PersonName:
    """Value object representing a validated person name."""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Name cannot be empty")

    def __str__(self) -> str:
        return self.value

    def get_display_name(self) -> str:
        return self.value.strip().title()


@dataclass(frozen=True)
class Age:
    """Value object representing a validated age in years."""
    years: int

    def __post_init__(self):
        if self.years < 0:
            raise ValueError("Age cannot be negative")

    def __str__(self) -> str:
        return f"{self.years} years"

    def to_months(self, current_month: int = 1) -> int:
        return self.years * 12 + current_month

    def is_adult(self, adult_age: int = 18) -> bool:
        return self.years >= adult_age


@dataclass(frozen=True)
class AgeInMonths:
    """Value object representing age in months."""
    months: int

    def __str__(self) -> str:
        return f"{self.months} months"

    def to_years(self) -> int:
        return self.months // 12

    def remaining_months(self) -> int:
        return self.months % 12


@dataclass(frozen=True)
class AgeInDays:
    """Value object representing age in days."""
    days: int

    def __str__(self) -> str:
        return f"{self.days:,} days"

    def to_weeks(self) -> int:
        return self.days // 7

    def to_hours(self) -> int:
        return self.days * 24


@dataclass(frozen=True)
class AgeInWeeks:
    """Value object representing age in weeks."""
    weeks: int

    def __str__(self) -> str:
        return f"{self.weeks:,} weeks"


@dataclass(frozen=True)
class AgeInHours:
    """Value object representing age in hours."""
    hours: int

    def __str__(self) -> str:
        return f"{self.hours:,} hours"


@dataclass(frozen=True)
class AgeInMinutes:
    """Value object representing age in minutes."""
    minutes: int

    def __str__(self) -> str:
        return f"{self.minutes:,} minutes"


@dataclass(frozen=True)
class CalculationTimestamp:
    """Value object representing when a calculation was performed."""
    timestamp: datetime

    @classmethod
    def now(cls) -> 'CalculationTimestamp':
        return cls(datetime.now())

    def __str__(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")


__all__ = [
    'PersonName',
    'Age',
    'AgeInMonths',
    'AgeInDays',
    'AgeInWeeks',
    'AgeInHours',
    'AgeInMinutes',
    'CalculationTimestamp'
]
