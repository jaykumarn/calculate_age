# -*- coding: utf-8 -*-
"""
Application Entry Point
Bootstrap and initialization of the Age Calculator application.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from typing import Optional
from config import ConfigurationManager, ApplicationConfig, Environment
from core import ServiceFactory
from presentation import MainView, MainController
from infrastructure import SimpleEventPublisher, EventTypes


class ApplicationBootstrapper:
    """Handles application initialization and dependency wiring."""
    
    _instance: Optional['ApplicationBootstrapper'] = None

    def __new__(cls) -> 'ApplicationBootstrapper':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._config_manager: Optional[ConfigurationManager] = None
        self._event_publisher: Optional[SimpleEventPublisher] = None
        self._main_view: Optional[MainView] = None
        self._initialized = True

    def configure(self, config_path: Optional[str] = None) -> 'ApplicationBootstrapper':
        self._config_manager = ConfigurationManager()
        self._config_manager.initialize(config_path)
        return self

    def setup_services(self) -> 'ApplicationBootstrapper':
        ServiceFactory.initialize(self._config_manager)
        return self

    def setup_events(self) -> 'ApplicationBootstrapper':
        self._event_publisher = SimpleEventPublisher()
        
        self._event_publisher.subscribe(
            EventTypes.CALCULATION_COMPLETED,
            lambda data: print(f"[EVENT] Calculation completed")
        )
        self._event_publisher.subscribe(
            EventTypes.CALCULATION_FAILED,
            lambda data: print(f"[EVENT] Calculation failed: {data.get('message')}")
        )
        return self

    def create_main_view(self) -> 'ApplicationBootstrapper':
        controller = MainController(
            age_calculator_service=ServiceFactory.get_age_calculator_service(),
            event_publisher=self._event_publisher
        )
        self._main_view = MainView(
            controller=controller,
            config_manager=self._config_manager
        )
        return self

    def run(self) -> int:
        try:
            if self._main_view is None:
                raise RuntimeError("Application not properly initialized")
            
            self._main_view.initialize()
            
            if self._event_publisher:
                self._event_publisher.publish(EventTypes.UI_INITIALIZED, {})
            
            self._main_view.show()
            
            if self._event_publisher:
                self._event_publisher.publish(EventTypes.UI_CLOSED, {})
            
            return 0
            
        except Exception as e:
            print(f"Application error: {e}")
            return 1

    @classmethod
    def reset(cls) -> None:
        if cls._instance:
            cls._instance._initialized = False
            cls._instance = None
        ServiceFactory.reset()


class Application:
    """Main application facade providing simplified startup."""
    
    @staticmethod
    def run(config_path: Optional[str] = None) -> int:
        bootstrapper = ApplicationBootstrapper()
        return (
            bootstrapper
            .configure(config_path)
            .setup_services()
            .setup_events()
            .create_main_view()
            .run()
        )

    @staticmethod
    def run_with_config(config: ApplicationConfig) -> int:
        config_manager = ConfigurationManager()
        config_manager._config = config
        
        bootstrapper = ApplicationBootstrapper()
        bootstrapper._config_manager = config_manager
        
        return (
            bootstrapper
            .setup_services()
            .setup_events()
            .create_main_view()
            .run()
        )


def main() -> int:
    return Application.run()


if __name__ == "__main__":
    sys.exit(main())
