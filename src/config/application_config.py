# -*- coding: utf-8 -*-
"""
Application Configuration Module
Provides centralized configuration management with environment-based overrides.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum
import json
import os


class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass
class UIConfig:
    window_width: int = 600
    window_height: int = 500
    window_min_width: int = 400
    window_min_height: int = 350
    window_title: str = "Age Calculator Pro"
    resizable_width: bool = True
    resizable_height: bool = True
    theme: Theme = Theme.LIGHT
    font_family: str = "Helvetica"
    font_size_small: int = 10
    font_size_medium: int = 12
    font_size_large: int = 16
    font_size_xlarge: int = 24
    padding_small: int = 5
    padding_medium: int = 10
    padding_large: int = 20
    button_width: int = 15
    entry_width: int = 30
    background_color: str = "#f0f0f0"
    primary_color: str = "#2196F3"
    secondary_color: str = "#4CAF50"
    error_color: str = "#f44336"
    success_color: str = "#4CAF50"
    warning_color: str = "#ff9800"
    text_color: str = "#333333"
    text_color_light: str = "#666666"


@dataclass
class ValidationConfig:
    min_age: int = 0
    max_age: int = 150
    min_name_length: int = 1
    max_name_length: int = 100
    allowed_name_characters: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'"
    strict_name_validation: bool = False


@dataclass
class CalculationConfig:
    use_precise_leap_year: bool = True
    include_current_day: bool = True
    round_months: bool = False
    calculation_precision: int = 2


@dataclass
class LoggingConfig:
    enabled: bool = True
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size_mb: int = 10
    backup_count: int = 5


@dataclass
class ApplicationConfig:
    environment: Environment = Environment.DEVELOPMENT
    debug_mode: bool = False
    ui: UIConfig = field(default_factory=UIConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    calculation: CalculationConfig = field(default_factory=CalculationConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    version: str = "2.0.0"
    app_name: str = "AgeCalculatorPro"

    @classmethod
    def load_from_file(cls, config_path: str) -> 'ApplicationConfig':
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                return cls._from_dict(data)
        return cls()

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'ApplicationConfig':
        config = cls()
        if 'environment' in data:
            config.environment = Environment(data['environment'])
        if 'debug_mode' in data:
            config.debug_mode = data['debug_mode']
        if 'ui' in data:
            for key, value in data['ui'].items():
                if hasattr(config.ui, key):
                    setattr(config.ui, key, value)
        if 'validation' in data:
            for key, value in data['validation'].items():
                if hasattr(config.validation, key):
                    setattr(config.validation, key, value)
        return config

    def to_dict(self) -> Dict[str, Any]:
        return {
            'environment': self.environment.value,
            'debug_mode': self.debug_mode,
            'version': self.version,
            'ui': {
                'window_width': self.ui.window_width,
                'window_height': self.ui.window_height,
                'theme': self.ui.theme.value,
            },
            'validation': {
                'min_age': self.validation.min_age,
                'max_age': self.validation.max_age,
            }
        }


class ConfigurationManager:
    _instance: Optional['ConfigurationManager'] = None
    _config: Optional[ApplicationConfig] = None

    def __new__(cls) -> 'ConfigurationManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, config_path: Optional[str] = None) -> None:
        if config_path:
            self._config = ApplicationConfig.load_from_file(config_path)
        else:
            self._config = ApplicationConfig()

    @property
    def config(self) -> ApplicationConfig:
        if self._config is None:
            self._config = ApplicationConfig()
        return self._config

    def get_ui_config(self) -> UIConfig:
        return self.config.ui

    def get_validation_config(self) -> ValidationConfig:
        return self.config.validation

    def get_calculation_config(self) -> CalculationConfig:
        return self.config.calculation
