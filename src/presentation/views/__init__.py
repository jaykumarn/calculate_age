# -*- coding: utf-8 -*-
"""
Views Module
Tkinter-based UI implementation following MVP pattern.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from abc import ABC, abstractmethod

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import ConfigurationManager, UIConfig
from presentation.controllers import MainController, IMainController
from presentation.view_models import ViewState


class IView(ABC):
    """Base interface for all views."""
    
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def hide(self) -> None:
        pass

    @abstractmethod
    def update_view(self) -> None:
        pass


class BaseView(ABC):
    """Abstract base class for views with common functionality."""
    
    def __init__(self, parent: Optional[tk.Widget] = None):
        self._parent = parent
        self._widgets: dict = {}

    @abstractmethod
    def _create_widgets(self) -> None:
        pass

    @abstractmethod
    def _setup_layout(self) -> None:
        pass

    @abstractmethod
    def _bind_events(self) -> None:
        pass


class InputPanelView(BaseView):
    """View component for input fields."""
    
    def __init__(
        self,
        parent: tk.Widget,
        ui_config: UIConfig,
        on_calculate: callable,
        on_clear: callable
    ):
        super().__init__(parent)
        self._ui_config = ui_config
        self._on_calculate = on_calculate
        self._on_clear = on_clear
        self._name_var = tk.StringVar()
        self._age_var = tk.StringVar()
        self._create_widgets()
        self._setup_layout()
        self._bind_events()

    def _create_widgets(self) -> None:
        self._frame = ttk.LabelFrame(
            self._parent,
            text="Enter Your Information",
            padding=self._ui_config.padding_medium
        )

        self._name_label = ttk.Label(self._frame, text="Name:")
        self._name_entry = ttk.Entry(
            self._frame,
            textvariable=self._name_var,
            width=self._ui_config.entry_width
        )

        self._age_label = ttk.Label(self._frame, text="Age (years):")
        self._age_entry = ttk.Entry(
            self._frame,
            textvariable=self._age_var,
            width=self._ui_config.entry_width
        )

        self._button_frame = ttk.Frame(self._frame)
        self._calculate_btn = ttk.Button(
            self._button_frame,
            text="Calculate",
            command=self._handle_calculate,
            width=self._ui_config.button_width
        )
        self._clear_btn = ttk.Button(
            self._button_frame,
            text="Clear",
            command=self._handle_clear,
            width=self._ui_config.button_width
        )

    def _setup_layout(self) -> None:
        self._frame.pack(
            fill=tk.X,
            padx=self._ui_config.padding_medium,
            pady=self._ui_config.padding_medium
        )

        self._name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self._name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        self._age_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self._age_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        self._button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        self._calculate_btn.pack(side=tk.LEFT, padx=5)
        self._clear_btn.pack(side=tk.LEFT, padx=5)

        self._frame.columnconfigure(1, weight=1)

    def _bind_events(self) -> None:
        self._name_entry.bind('<Return>', lambda e: self._age_entry.focus())
        self._age_entry.bind('<Return>', lambda e: self._handle_calculate())

    def _handle_calculate(self) -> None:
        self._on_calculate(self._name_var.get(), self._age_var.get())

    def _handle_clear(self) -> None:
        self._name_var.set("")
        self._age_var.set("")
        self._name_entry.focus()
        self._on_clear()

    def get_frame(self) -> ttk.LabelFrame:
        return self._frame

    def set_name_error(self, has_error: bool) -> None:
        pass

    def set_age_error(self, has_error: bool) -> None:
        pass

    def focus_name(self) -> None:
        self._name_entry.focus()


class ResultPanelView(BaseView):
    """View component for displaying calculation results."""
    
    def __init__(self, parent: tk.Widget, ui_config: UIConfig):
        super().__init__(parent)
        self._ui_config = ui_config
        self._create_widgets()
        self._setup_layout()
        self._bind_events()

    def _create_widgets(self) -> None:
        self._frame = ttk.LabelFrame(
            self._parent,
            text="Results",
            padding=self._ui_config.padding_medium
        )

        self._result_text = tk.Text(
            self._frame,
            height=12,
            width=50,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=(self._ui_config.font_family, self._ui_config.font_size_medium)
        )

        self._scrollbar = ttk.Scrollbar(
            self._frame,
            orient=tk.VERTICAL,
            command=self._result_text.yview
        )
        self._result_text.configure(yscrollcommand=self._scrollbar.set)

    def _setup_layout(self) -> None:
        self._frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=self._ui_config.padding_medium,
            pady=self._ui_config.padding_medium
        )

        self._result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _bind_events(self) -> None:
        pass

    def display_result(
        self,
        name: str,
        years: int,
        months: int,
        days: int,
        weeks: int,
        hours: int,
        minutes: int,
        birth_year: int
    ) -> None:
        self._result_text.configure(state=tk.NORMAL)
        self._result_text.delete(1.0, tk.END)

        result_lines = [
            f"╔══════════════════════════════════════════╗",
            f"║  Age Calculation Results for {name}",
            f"╠══════════════════════════════════════════╣",
            f"║",
            f"║  📅 Years:    {years:,} years",
            f"║  📆 Months:   {months:,} months",
            f"║  📋 Weeks:    {weeks:,} weeks",
            f"║  📊 Days:     {days:,} days",
            f"║  ⏰ Hours:    {hours:,} hours",
            f"║  ⏱️  Minutes:  {minutes:,} minutes",
            f"║",
            f"║  🎂 Born approximately in: {birth_year}",
            f"╚══════════════════════════════════════════╝",
        ]

        self._result_text.insert(tk.END, "\n".join(result_lines))
        self._result_text.configure(state=tk.DISABLED)

    def display_error(self, message: str) -> None:
        self._result_text.configure(state=tk.NORMAL)
        self._result_text.delete(1.0, tk.END)
        self._result_text.insert(tk.END, f"⚠️ Error: {message}")
        self._result_text.configure(state=tk.DISABLED)

    def clear(self) -> None:
        self._result_text.configure(state=tk.NORMAL)
        self._result_text.delete(1.0, tk.END)
        self._result_text.insert(tk.END, "Enter your name and age, then click Calculate.")
        self._result_text.configure(state=tk.DISABLED)

    def get_frame(self) -> ttk.LabelFrame:
        return self._frame


class StatusBarView(BaseView):
    """View component for status bar."""
    
    def __init__(self, parent: tk.Widget, ui_config: UIConfig):
        super().__init__(parent)
        self._ui_config = ui_config
        self._status_var = tk.StringVar(value="Ready")
        self._create_widgets()
        self._setup_layout()
        self._bind_events()

    def _create_widgets(self) -> None:
        self._frame = ttk.Frame(self._parent)
        self._status_label = ttk.Label(
            self._frame,
            textvariable=self._status_var,
            anchor=tk.W
        )

    def _setup_layout(self) -> None:
        self._frame.pack(fill=tk.X, side=tk.BOTTOM)
        self._status_label.pack(fill=tk.X, padx=5, pady=2)

    def _bind_events(self) -> None:
        pass

    def set_status(self, message: str) -> None:
        self._status_var.set(message)

    def set_ready(self) -> None:
        self._status_var.set("Ready")

    def set_loading(self) -> None:
        self._status_var.set("Calculating...")

    def set_success(self) -> None:
        self._status_var.set("Calculation complete")

    def set_error(self) -> None:
        self._status_var.set("Error occurred")


class MainView(IView):
    """Main application view composing all UI components."""
    
    def __init__(
        self,
        controller: Optional[IMainController] = None,
        config_manager: Optional[ConfigurationManager] = None
    ):
        self._controller = controller or MainController()
        self._config_manager = config_manager or ConfigurationManager()
        self._ui_config = self._config_manager.get_ui_config()
        
        self._root: Optional[tk.Tk] = None
        self._input_panel: Optional[InputPanelView] = None
        self._result_panel: Optional[ResultPanelView] = None
        self._status_bar: Optional[StatusBarView] = None

        self._controller.register_view_update_callback(self.update_view)

    def initialize(self) -> None:
        self._root = tk.Tk()
        self._root.title(self._ui_config.window_title)
        self._root.geometry(
            f"{self._ui_config.window_width}x{self._ui_config.window_height}"
        )
        self._root.minsize(
            self._ui_config.window_min_width,
            self._ui_config.window_min_height
        )
        self._root.resizable(
            self._ui_config.resizable_width,
            self._ui_config.resizable_height
        )

        self._setup_styles()
        self._create_components()
        self._setup_menu()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.configure(
            'TLabel',
            font=(self._ui_config.font_family, self._ui_config.font_size_medium)
        )
        style.configure(
            'TButton',
            font=(self._ui_config.font_family, self._ui_config.font_size_medium)
        )
        style.configure(
            'TEntry',
            font=(self._ui_config.font_family, self._ui_config.font_size_medium)
        )

    def _create_components(self) -> None:
        main_container = ttk.Frame(self._root, padding=5)
        main_container.pack(fill=tk.BOTH, expand=True)

        self._input_panel = InputPanelView(
            main_container,
            self._ui_config,
            on_calculate=self._on_calculate,
            on_clear=self._on_clear
        )

        self._result_panel = ResultPanelView(main_container, self._ui_config)
        self._result_panel.clear()

        self._status_bar = StatusBarView(self._root, self._ui_config)

    def _setup_menu(self) -> None:
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear", command=self._on_clear)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_exit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

    def _on_calculate(self, name: str, age: str) -> None:
        self._status_bar.set_loading()
        self._controller.calculate_age(name, age)

    def _on_clear(self) -> None:
        self._controller.clear_form()
        self._result_panel.clear()
        self._status_bar.set_ready()

    def _on_exit(self) -> None:
        self._root.quit()

    def _show_about(self) -> None:
        messagebox.showinfo(
            "About Age Calculator",
            "Age Calculator Pro v2.0.0\n\n"
            "Calculate your age in various units:\n"
            "• Years\n"
            "• Months\n"
            "• Weeks\n"
            "• Days\n"
            "• Hours\n"
            "• Minutes"
        )

    def show(self) -> None:
        if self._root:
            self._input_panel.focus_name()
            self._root.mainloop()

    def hide(self) -> None:
        if self._root:
            self._root.withdraw()

    def update_view(self) -> None:
        view_model = self._controller.get_view_model()

        if view_model.state == ViewState.LOADING:
            self._status_bar.set_loading()

        elif view_model.state == ViewState.SUCCESS and view_model.result:
            result = view_model.result
            self._result_panel.display_result(
                name=result.name,
                years=result.years,
                months=result.months,
                days=result.days,
                weeks=result.weeks,
                hours=result.hours,
                minutes=result.minutes,
                birth_year=result.birth_year
            )
            self._status_bar.set_success()

        elif view_model.state == ViewState.ERROR:
            self._result_panel.display_error(view_model.error.message)
            self._status_bar.set_error()

            if view_model.error.field_name == "name":
                self._input_panel.set_name_error(True)
            elif view_model.error.field_name == "age":
                self._input_panel.set_age_error(True)

        elif view_model.state == ViewState.IDLE:
            self._status_bar.set_ready()


__all__ = [
    'IView',
    'BaseView',
    'InputPanelView',
    'ResultPanelView',
    'StatusBarView',
    'MainView'
]
