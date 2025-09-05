#!/usr/bin/env python3
"""Monte Carlo π estimation visualization"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QDir
from PySide6.QtGui import QIcon

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
    app = QApplication(sys.argv)
    app.setApplicationName("Monte Carlo π Visualization")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Monte Carlo Lab")
    
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
    try:
        app = setup_application()
        window = MainWindow()
        window.show()
        
        print("Monte Carlo π Visualization")
        print("Right-click on canvas to toggle grid")
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