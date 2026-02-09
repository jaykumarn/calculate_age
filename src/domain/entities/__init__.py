# -*- coding: utf-8 -*-
"""
Domain Entities Module
Core domain entities representing the business concepts.
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid

from ..value_objects import (
    PersonName,
    Age,
    AgeInMonths,
    AgeInDays,
    AgeInWeeks,
    AgeInHours,
    AgeInMinutes,
    CalculationTimestamp
)


@dataclass
class AgeCalculationResult:
    """Entity representing the complete result of an age calculation."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[PersonName] = None
    age_years: Optional[Age] = None
    age_months: Optional[AgeInMonths] = None
    age_days: Optional[AgeInDays] = None
    age_weeks: Optional[AgeInWeeks] = None
    age_hours: Optional[AgeInHours] = None
    age_minutes: Optional[AgeInMinutes] = None
    calculation_timestamp: CalculationTimestamp = field(
        default_factory=CalculationTimestamp.now
    )
    birth_year: Optional[int] = None
    current_year: Optional[int] = None

    def get_summary(self) -> str:
        parts = []
        if self.name:
            parts.append(f"{self.name.get_display_name()}'s age:")
        if self.age_years:
            parts.append(f"  • {self.age_years}")
        if self.age_months:
            parts.append(f"  • {self.age_months}")
        if self.age_days:
            parts.append(f"  • {self.age_days}")
        if self.age_weeks:
            parts.append(f"  • {self.age_weeks}")
        if self.age_hours:
            parts.append(f"  • {self.age_hours}")
        if self.age_minutes:
            parts.append(f"  • {self.age_minutes}")
        return "\n".join(parts)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': str(self.name) if self.name else None,
            'age_years': self.age_years.years if self.age_years else None,
            'age_months': self.age_months.months if self.age_months else None,
            'age_days': self.age_days.days if self.age_days else None,
            'age_weeks': self.age_weeks.weeks if self.age_weeks else None,
            'age_hours': self.age_hours.hours if self.age_hours else None,
            'age_minutes': self.age_minutes.minutes if self.age_minutes else None,
            'calculation_timestamp': str(self.calculation_timestamp),
            'birth_year': self.birth_year,
            'current_year': self.current_year
        }


@dataclass
class Person:
    """Entity representing a person whose age is being calculated."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: PersonName = None
    birth_year: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def set_name(self, name: str) -> None:
        self.name = PersonName(name)
        self.updated_at = datetime.now()

    def set_birth_year(self, year: int) -> None:
        self.birth_year = year
        self.updated_at = datetime.now()


@dataclass
class CalculationRequest:
    """Entity representing a request to calculate age."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    age_in_years: int = 0
    include_months: bool = True
    include_days: bool = True
    include_weeks: bool = True
    include_hours: bool = True
    include_minutes: bool = True
    requested_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> bool:
        return bool(self.name) and self.age_in_years >= 0


__all__ = [
    'AgeCalculationResult',
    'Person',
    'CalculationRequest'
]
