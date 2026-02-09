#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Age Calculator Pro - Launcher
Run this file to start the application.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from application import Application

if __name__ == "__main__":
    sys.exit(Application.run())
