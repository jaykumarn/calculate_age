# -*- coding: utf-8 -*-
"""
Factory Module
Provides factory implementations for creating service instances with proper dependency injection.
"""
from typing import Optional
from enum import Enum

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.interfaces import (
    IDateTimeProvider,
    ILeapYearCalculator,
    IMonthDaysCalculator,
    IAgeCalculatorService,
    IValidationService
)
from core.services import (
    SystemDateTimeProvider,
    StandardLeapYearCalculator,
    StandardMonthDaysCalculator,
    InputValidationService,
    AgeCalculatorServiceImpl
)
from config import ConfigurationManager


class ServiceType(Enum):
    DATETIME_PROVIDER = "datetime_provider"
    LEAP_YEAR_CALCULATOR = "leap_year_calculator"
    MONTH_DAYS_CALCULATOR = "month_days_calculator"
    AGE_CALCULATOR = "age_calculator"
    VALIDATION = "validation"


class ServiceFactory:
    """Abstract factory for creating service instances."""
    
    _instances: dict = {}
    _config_manager: Optional[ConfigurationManager] = None

    @classmethod
    def initialize(cls, config_manager: Optional[ConfigurationManager] = None) -> None:
        cls._config_manager = config_manager or ConfigurationManager()
        cls._instances.clear()

    @classmethod
    def get_datetime_provider(cls) -> IDateTimeProvider:
        if ServiceType.DATETIME_PROVIDER not in cls._instances:
            cls._instances[ServiceType.DATETIME_PROVIDER] = SystemDateTimeProvider()
        return cls._instances[ServiceType.DATETIME_PROVIDER]

    @classmethod
    def get_leap_year_calculator(cls) -> ILeapYearCalculator:
        if ServiceType.LEAP_YEAR_CALCULATOR not in cls._instances:
            cls._instances[ServiceType.LEAP_YEAR_CALCULATOR] = StandardLeapYearCalculator()
        return cls._instances[ServiceType.LEAP_YEAR_CALCULATOR]

    @classmethod
    def get_month_days_calculator(cls) -> IMonthDaysCalculator:
        if ServiceType.MONTH_DAYS_CALCULATOR not in cls._instances:
            cls._instances[ServiceType.MONTH_DAYS_CALCULATOR] = StandardMonthDaysCalculator()
        return cls._instances[ServiceType.MONTH_DAYS_CALCULATOR]

    @classmethod
    def get_validation_service(cls) -> IValidationService:
        if ServiceType.VALIDATION not in cls._instances:
            config = None
            if cls._config_manager:
                config = cls._config_manager.get_validation_config()
            cls._instances[ServiceType.VALIDATION] = InputValidationService(config)
        return cls._instances[ServiceType.VALIDATION]

    @classmethod
    def get_age_calculator_service(cls) -> IAgeCalculatorService:
        if ServiceType.AGE_CALCULATOR not in cls._instances:
            cls._instances[ServiceType.AGE_CALCULATOR] = AgeCalculatorServiceImpl(
                datetime_provider=cls.get_datetime_provider(),
                leap_year_calculator=cls.get_leap_year_calculator(),
                month_days_calculator=cls.get_month_days_calculator(),
                validation_service=cls.get_validation_service()
            )
        return cls._instances[ServiceType.AGE_CALCULATOR]

    @classmethod
    def reset(cls) -> None:
        cls._instances.clear()
        cls._config_manager = None


class DependencyContainer:
    """IoC Container for dependency injection."""
    
    _registrations: dict = {}
    _singletons: dict = {}

    @classmethod
    def register(cls, interface_type: type, implementation_type: type, singleton: bool = True) -> None:
        cls._registrations[interface_type] = {
            'implementation': implementation_type,
            'singleton': singleton
        }

    @classmethod
    def resolve(cls, interface_type: type):
        if interface_type not in cls._registrations:
            raise ValueError(f"No registration found for {interface_type}")
        
        registration = cls._registrations[interface_type]
        
        if registration['singleton']:
            if interface_type not in cls._singletons:
                cls._singletons[interface_type] = registration['implementation']()
            return cls._singletons[interface_type]
        
        return registration['implementation']()

    @classmethod
    def reset(cls) -> None:
        cls._registrations.clear()
        cls._singletons.clear()

    @classmethod
    def configure_defaults(cls) -> None:
        cls.register(IDateTimeProvider, SystemDateTimeProvider)
        cls.register(ILeapYearCalculator, StandardLeapYearCalculator)
        cls.register(IMonthDaysCalculator, StandardMonthDaysCalculator)
        cls.register(IValidationService, InputValidationService)


__all__ = [
    'ServiceType',
    'ServiceFactory',
    'DependencyContainer'
]
