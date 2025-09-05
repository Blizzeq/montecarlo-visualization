#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte Carlo π Visualization
Interaktywna wizualizacja algorytmu Monte Carlo do wyznaczania wartości π

Autor: Assistant
Wymaga: PySide6, numpy, matplotlib, pyqtgraph
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
    print(f"Błąd importu: {e}")
    print("Upewnij się, że zainstalowane są wszystkie wymagane biblioteki:")
    print("pip install PySide6 numpy matplotlib pyqtgraph")
    sys.exit(1)


def setup_application():
    """Konfiguruje aplikację Qt"""
    app = QApplication(sys.argv)
    
    # Ustawienia aplikacji
    app.setApplicationName("Monte Carlo π Visualization")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Monte Carlo Lab")
    
    # Ustaw globalny styl dark theme
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
    """Główna funkcja aplikacji"""
    try:
        # Utwórz aplikację Qt
        app = setup_application()
        
        # Utwórz i pokaż główne okno
        window = MainWindow()
        window.show()
        
        # Pokaż informacje o aplikacji
        print("=" * 50)
        print("Monte Carlo π Visualization")
        print("=" * 50)
        print("Algorytm Monte Carlo do wyznaczania wartości π")
        print("Użyj panelu kontrolnego do sterowania symulacją")
        print("PPM na canvas aby przełączyć siatkę")
        print("Sprawdź zakładki statystyk aby zobaczyć analizy")
        print("=" * 50)
        
        # Uruchom pętlę aplikacji
        return app.exec()
        
    except Exception as e:
        print(f"Błąd krytyczny aplikacji: {e}")
        if 'app' in locals():
            QMessageBox.critical(
                None, 
                "Błąd Krytyczny", 
                f"Wystąpił nieoczekiwany błąd:\n\n{str(e)}\n\nAplikacja zostanie zamknięta."
            )
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)