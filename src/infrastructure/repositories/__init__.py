# -*- coding: utf-8 -*-
"""
Repository Implementations
Provides data persistence layer implementations.
"""
from typing import Optional, List, Dict
from datetime import datetime
import json
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from domain import AgeCalculationResult
from core.interfaces import ICalculationRepository


class InMemoryCalculationRepository(ICalculationRepository):
    """In-memory implementation for calculation history storage."""
    
    def __init__(self):
        self._storage: Dict[str, AgeCalculationResult] = {}

    def save(self, result: AgeCalculationResult) -> str:
        self._storage[result.id] = result
        return result.id

    def get_by_id(self, id: str) -> Optional[AgeCalculationResult]:
        return self._storage.get(id)

    def get_all(self) -> List[AgeCalculationResult]:
        return list(self._storage.values())

    def delete(self, id: str) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False

    def clear_all(self) -> int:
        count = len(self._storage)
        self._storage.clear()
        return count

    def get_count(self) -> int:
        return len(self._storage)


class FileBasedCalculationRepository(ICalculationRepository):
    """File-based implementation for persistent calculation history."""
    
    def __init__(self, file_path: str = "calculation_history.json"):
        self._file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self._file_path):
            with open(self._file_path, 'w') as f:
                json.dump([], f)

    def _load_data(self) -> List[dict]:
        try:
            with open(self._file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self, data: List[dict]) -> None:
        with open(self._file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def save(self, result: AgeCalculationResult) -> str:
        data = self._load_data()
        result_dict = result.to_dict()
        
        existing_idx = next(
            (i for i, item in enumerate(data) if item.get('id') == result.id),
            None
        )
        
        if existing_idx is not None:
            data[existing_idx] = result_dict
        else:
            data.append(result_dict)
        
        self._save_data(data)
        return result.id

    def get_by_id(self, id: str) -> Optional[AgeCalculationResult]:
        data = self._load_data()
        for item in data:
            if item.get('id') == id:
                return self._dict_to_result(item)
        return None

    def get_all(self) -> List[AgeCalculationResult]:
        data = self._load_data()
        return [self._dict_to_result(item) for item in data]

    def delete(self, id: str) -> bool:
        data = self._load_data()
        original_length = len(data)
        data = [item for item in data if item.get('id') != id]
        if len(data) < original_length:
            self._save_data(data)
            return True
        return False

    def clear_all(self) -> int:
        data = self._load_data()
        count = len(data)
        self._save_data([])
        return count

    def _dict_to_result(self, data: dict) -> AgeCalculationResult:
        from domain import (
            PersonName, Age, AgeInMonths, AgeInDays,
            AgeInWeeks, AgeInHours, AgeInMinutes
        )
        
        return AgeCalculationResult(
            id=data.get('id', ''),
            name=PersonName(data['name']) if data.get('name') else None,
            age_years=Age(data['age_years']) if data.get('age_years') else None,
            age_months=AgeInMonths(data['age_months']) if data.get('age_months') else None,
            age_days=AgeInDays(data['age_days']) if data.get('age_days') else None,
            age_weeks=AgeInWeeks(data['age_weeks']) if data.get('age_weeks') else None,
            age_hours=AgeInHours(data['age_hours']) if data.get('age_hours') else None,
            age_minutes=AgeInMinutes(data['age_minutes']) if data.get('age_minutes') else None,
            birth_year=data.get('birth_year'),
            current_year=data.get('current_year')
        )


__all__ = [
    'InMemoryCalculationRepository',
    'FileBasedCalculationRepository'
]
