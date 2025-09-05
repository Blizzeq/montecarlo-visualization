#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte Carlo π Visualization
Interactive visualization of Monte Carlo algorithm for π estimation

Author: Jakub Krasuski  
Requirements: PySide6, numpy, matplotlib, pyqtgraph
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QDir
from PySide6.QtGui import QIcon

# Dodaj katalog src do ścieżki
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.ui.main_window import MainWindow
    from src.utils.colors import Colors
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required libraries are installed:")
    print("pip install PySide6 numpy matplotlib pyqtgraph")
    sys.exit(1)


def setup_application():
    """Configure Qt application"""
    app = QApplication(sys.argv)
    
    # Application settings
    app.setApplicationName("Monte Carlo π Visualization")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Monte Carlo Lab")
    
    # Set global dark theme style
    app.setStyleSheet(f"""
    QApplication {{
        background-color: {Colors.BACKGROUND.name()};
        color: white;
    }}
    QMainWindow {{
        background-color: {Colors.BACKGROUND.name()};
    }}
    QWidget {{
        background-color: {Colors.BACKGROUND.name()};
        color: white;
    }}
    QToolTip {{
        background-color: #2e2e32;
        color: white;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 4px;
    }}
    """)
    
    return app


def main():
    """Main application function"""
    try:
        # Create Qt application
        app = setup_application()
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Show application info
        print("=" * 50)
        print("Monte Carlo π Visualization")
        print("=" * 50)
        print("Monte Carlo algorithm for π estimation")
        print("Use control panel to manage simulation")
        print("Right-click on canvas to toggle grid")
        print("Check statistics tabs for detailed analysis")
        print("=" * 50)
        
        # Run application loop
        return app.exec()
        
    except Exception as e:
        print(f"Critical application error: {e}")
        if 'app' in locals():
            QMessageBox.critical(
                None, 
                "Critical Error", 
                f"An unexpected error occurred:\n\n{str(e)}\n\nApplication will be closed."
            )
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)