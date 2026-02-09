# -*- coding: utf-8 -*-
"""
Infrastructure Adapters Module
Adapters for external systems and services.
"""
from typing import Dict, List, Callable
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.interfaces import IEventPublisher, IResultFormatter
from domain import AgeCalculationResult


class SimpleEventPublisher(IEventPublisher):
    """Simple in-process event publisher implementation."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def publish(self, event_type: str, data: dict) -> None:
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Event handler error: {e}")

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> bool:
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
                return True
            except ValueError:
                return False
        return False


class ConsoleResultFormatter(IResultFormatter):
    """Formatter for console/text output."""
    
    def format_for_display(self, result: AgeCalculationResult) -> str:
        lines = []
        if result.name:
            lines.append(f"Name: {result.name.get_display_name()}")
        if result.age_years:
            lines.append(f"Age in Years: {result.age_years.years}")
        if result.age_months:
            lines.append(f"Age in Months: {result.age_months.months:,}")
        if result.age_days:
            lines.append(f"Age in Days: {result.age_days.days:,}")
        if result.age_weeks:
            lines.append(f"Age in Weeks: {result.age_weeks.weeks:,}")
        if result.age_hours:
            lines.append(f"Age in Hours: {result.age_hours.hours:,}")
        if result.age_minutes:
            lines.append(f"Age in Minutes: {result.age_minutes.minutes:,}")
        return "\n".join(lines)

    def format_for_export(self, result: AgeCalculationResult) -> str:
        import json
        return json.dumps(result.to_dict(), indent=2)


class EventTypes:
    CALCULATION_STARTED = "calculation.started"
    CALCULATION_COMPLETED = "calculation.completed"
    CALCULATION_FAILED = "calculation.failed"
    VALIDATION_FAILED = "validation.failed"
    UI_INITIALIZED = "ui.initialized"
    UI_CLOSED = "ui.closed"


__all__ = [
    'SimpleEventPublisher',
    'ConsoleResultFormatter',
    'EventTypes'
]
