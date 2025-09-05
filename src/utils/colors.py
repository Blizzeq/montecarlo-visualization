from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class Colors:
    BACKGROUND = QColor(26, 26, 26)         # Darker background
    CANVAS_BACKGROUND = QColor(20, 20, 20)  # Even darker for canvas
    
    POINT_INSIDE = QColor(0, 255, 136)      # Bright green
    POINT_OUTSIDE = QColor(255, 68, 68)     # Bright red
    
    CIRCLE_OUTLINE = QColor(255, 255, 255)  # White for better contrast
    SQUARE_OUTLINE = QColor(200, 200, 200)  # Light gray
    
    TEXT_PRIMARY = QColor(255, 255, 255)    # White
    TEXT_SECONDARY = QColor(189, 189, 189)  # Light gray
    TEXT_HIGHLIGHT = QColor(0, 212, 255)    # Cyan highlight
    
    ACCENT_CYAN = QColor(0, 212, 255)       # Main accent color
    ACCENT_PURPLE = QColor(156, 39, 176)    # Purple
    ACCENT_ORANGE = QColor(255, 152, 0)     # Orange
    
    SUCCESS = QColor(0, 255, 136)           # Bright green
    WARNING = QColor(255, 193, 7)           # Yellow  
    ERROR = QColor(255, 107, 107)           # Bright red
    
    CARD_BACKGROUND = QColor(40, 40, 45)    # Card backgrounds
    PANEL_BACKGROUND = QColor(35, 35, 40)   # Panel backgrounds


class Styles:
    BUTTON_STYLE = """
    QPushButton {
        background-color: #2e2e32;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 8px 16px;
        color: white;
        font-weight: bold;
        min-height: 30px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #3a3a3f;
    }
    QPushButton:pressed {
        background-color: #1e1e22;
    }
    QPushButton:disabled {
        background-color: #1a1a1d;
        color: #666;
    }
    """
    
    SLIDER_STYLE = """
    QSlider {
        min-height: 25px;
    }
    QSlider::groove:horizontal {
        height: 8px;
        background: #3a3a3f;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #2196F3;
        border: none;
        width: 18px;
        height: 18px;
        border-radius: 9px;
        margin: -5px 0;
    }
    QSlider::handle:horizontal:hover {
        background: #1976D2;
    }
    """
    
    LABEL_STYLE = """
    QLabel {
        color: white;
        font-size: 12px;
    }
    """
    
    PANEL_STYLE = """
    QFrame {
        background-color: #2e2e32;
        border: 1px solid #555;
        border-radius: 6px;
        margin: 4px;
    }
    """
    
    SPINBOX_STYLE = """
    QSpinBox {
        background-color: #3a3a3f;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 6px;
        color: white;
        min-height: 25px;
        font-size: 12px;
    }
    QSpinBox:focus {
        border-color: #2196F3;
    }
    """