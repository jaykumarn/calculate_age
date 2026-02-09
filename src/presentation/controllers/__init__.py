# -*- coding: utf-8 -*-
"""
Controllers Module
Mediates between views and services following MVC pattern.
"""
from typing import Optional, Callable, List
from abc import ABC, abstractmethod

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain import (
    AgeCalculationResult,
    AgeValidationException,
    NameValidationException,
    CalculationException
)
from core import ServiceFactory, IAgeCalculatorService
from infrastructure import SimpleEventPublisher, EventTypes, InMemoryCalculationRepository
from presentation.view_models import (
    MainViewModel,
    InputViewModel,
    ResultViewModel,
    ErrorViewModel,
    ViewState
)


class IMainController(ABC):
    """Interface for main controller."""
    
    @abstractmethod
    def calculate_age(self, name: str, age: str) -> None:
        pass

    @abstractmethod
    def clear_form(self) -> None:
        pass

    @abstractmethod
    def get_view_model(self) -> MainViewModel:
        pass

    @abstractmethod
    def register_view_update_callback(self, callback: Callable) -> None:
        pass


class MainController(IMainController):
    """Main controller implementation handling user interactions."""
    
    def __init__(
        self,
        age_calculator_service: Optional[IAgeCalculatorService] = None,
        event_publisher: Optional[SimpleEventPublisher] = None,
        repository: Optional[InMemoryCalculationRepository] = None
    ):
        self._service = age_calculator_service or ServiceFactory.get_age_calculator_service()
        self._event_publisher = event_publisher or SimpleEventPublisher()
        self._repository = repository or InMemoryCalculationRepository()
        self._view_model = MainViewModel()
        self._view_update_callbacks: List[Callable] = []

    def calculate_age(self, name: str, age: str) -> None:
        self._view_model.set_loading()
        self._notify_view_update()

        self._event_publisher.publish(EventTypes.CALCULATION_STARTED, {
            'name': name,
            'age': age
        })

        if not name or not name.strip():
            self._handle_validation_error("Please enter a name", "name")
            return

        if not age or not age.strip():
            self._handle_validation_error("Please enter an age", "age")
            return

        try:
            age_int = int(age)
        except ValueError:
            self._handle_validation_error("Age must be a valid number", "age")
            return

        try:
            result = self._service.calculate_age(name.strip(), age_int)
            self._repository.save(result)
            result_vm = self._map_to_view_model(result)
            self._view_model.set_success(result_vm)
            self._view_model.calculation_history.append(result_vm)

            self._event_publisher.publish(EventTypes.CALCULATION_COMPLETED, {
                'result': result.to_dict()
            })

        except NameValidationException as e:
            self._handle_validation_error(e.message, "name")
        except AgeValidationException as e:
            self._handle_validation_error(e.message, "age")
        except CalculationException as e:
            self._handle_error(f"Calculation error: {e.message}")
        except Exception as e:
            self._handle_error(f"Unexpected error: {str(e)}")

        self._notify_view_update()

    def _handle_validation_error(self, message: str, field: str) -> None:
        self._view_model.set_error(message, field)
        self._event_publisher.publish(EventTypes.VALIDATION_FAILED, {
            'message': message,
            'field': field
        })
        self._notify_view_update()

    def _handle_error(self, message: str) -> None:
        self._view_model.set_error(message)
        self._event_publisher.publish(EventTypes.CALCULATION_FAILED, {
            'message': message
        })
        self._notify_view_update()

    def _map_to_view_model(self, result: AgeCalculationResult) -> ResultViewModel:
        return ResultViewModel(
            name=result.name.get_display_name() if result.name else "",
            years=result.age_years.years if result.age_years else 0,
            months=result.age_months.months if result.age_months else 0,
            days=result.age_days.days if result.age_days else 0,
            weeks=result.age_weeks.weeks if result.age_weeks else 0,
            hours=result.age_hours.hours if result.age_hours else 0,
            minutes=result.age_minutes.minutes if result.age_minutes else 0,
            birth_year=result.birth_year or 0,
            current_year=result.current_year or 0
        )

    def clear_form(self) -> None:
        self._view_model.reset()
        self._notify_view_update()

    def get_view_model(self) -> MainViewModel:
        return self._view_model

    def register_view_update_callback(self, callback: Callable) -> None:
        self._view_update_callbacks.append(callback)

    def _notify_view_update(self) -> None:
        for callback in self._view_update_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"View update callback error: {e}")

    def get_calculation_history(self) -> List[ResultViewModel]:
        return self._view_model.calculation_history

    def clear_history(self) -> None:
        self._view_model.calculation_history.clear()
        self._repository.clear_all()
        self._notify_view_update()


__all__ = [
    'IMainController',
    'MainController'
]
