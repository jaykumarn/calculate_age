# -*- coding: utf-8 -*-
"""
View Models Module
Data transfer objects for presentation layer.
"""
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class ViewState(Enum):
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class InputViewModel:
    """View model for user input fields."""
    name: str = ""
    age: str = ""
    
    def is_valid(self) -> bool:
        return bool(self.name.strip()) and self.age.isdigit()

    def get_age_as_int(self) -> int:
        return int(self.age) if self.age.isdigit() else 0

    def clear(self) -> None:
        self.name = ""
        self.age = ""


@dataclass
class ResultViewModel:
    """View model for calculation results display."""
    name: str = ""
    years: int = 0
    months: int = 0
    days: int = 0
    weeks: int = 0
    hours: int = 0
    minutes: int = 0
    birth_year: int = 0
    current_year: int = 0

    def get_formatted_years(self) -> str:
        return f"{self.years:,} years"

    def get_formatted_months(self) -> str:
        return f"{self.months:,} months"

    def get_formatted_days(self) -> str:
        return f"{self.days:,} days"

    def get_formatted_weeks(self) -> str:
        return f"{self.weeks:,} weeks"

    def get_formatted_hours(self) -> str:
        return f"{self.hours:,} hours"

    def get_formatted_minutes(self) -> str:
        return f"{self.minutes:,} minutes"

    def get_birth_year_display(self) -> str:
        return f"Born approximately: {self.birth_year}"


@dataclass
class ErrorViewModel:
    """View model for error display."""
    message: str = ""
    field_name: Optional[str] = None
    error_code: Optional[str] = None

    def has_error(self) -> bool:
        return bool(self.message)

    def clear(self) -> None:
        self.message = ""
        self.field_name = None
        self.error_code = None


@dataclass
class MainViewModel:
    """Aggregate view model for the main view."""
    input: InputViewModel = field(default_factory=InputViewModel)
    result: Optional[ResultViewModel] = None
    error: ErrorViewModel = field(default_factory=ErrorViewModel)
    state: ViewState = ViewState.IDLE
    calculation_history: List[ResultViewModel] = field(default_factory=list)

    def set_loading(self) -> None:
        self.state = ViewState.LOADING
        self.error.clear()

    def set_success(self, result: ResultViewModel) -> None:
        self.state = ViewState.SUCCESS
        self.result = result
        self.error.clear()

    def set_error(self, message: str, field_name: Optional[str] = None) -> None:
        self.state = ViewState.ERROR
        self.error.message = message
        self.error.field_name = field_name
        self.result = None

    def reset(self) -> None:
        self.input.clear()
        self.result = None
        self.error.clear()
        self.state = ViewState.IDLE

    def is_loading(self) -> bool:
        return self.state == ViewState.LOADING

    def has_result(self) -> bool:
        return self.result is not None and self.state == ViewState.SUCCESS

    def has_error(self) -> bool:
        return self.error.has_error()


__all__ = [
    'ViewState',
    'InputViewModel',
    'ResultViewModel',
    'ErrorViewModel',
    'MainViewModel'
]
