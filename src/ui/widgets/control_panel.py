from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QSlider, QLabel, QSpinBox, QGroupBox, QCheckBox,
                             QProgressBar, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import math
from ...utils.colors import Colors, Styles


class ControlPanel(QWidget):
    # Signals
    start_simulation = Signal()
    pause_simulation = Signal()
    reset_simulation = Signal()
    speed_changed = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        self.setMinimumHeight(300)
        self.setMaximumHeight(400)
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {Colors.PANEL_BACKGROUND.name()};
            border-radius: 8px;
        }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel("Control Panel")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin-bottom: 5px;")
        layout.addWidget(title_label)
        
        # Control buttons group
        self.create_control_buttons(layout)
        
        # Speed control group
        self.create_speed_controls(layout)
        
        layout.addStretch()
        
        # Force layout update
        self.updateGeometry()
        self.update()
        
    def create_control_buttons(self, parent_layout):
        group = QGroupBox("Simulation Control")
        group.setStyleSheet("""
        QGroupBox {
            color: white; 
            font-weight: bold; 
            font-size: 12px;
            border: 2px solid #555;
            border-radius: 6px;
            margin: 5px;
        }
        QGroupBox::title {
            padding: 0 10px;
        }
        """)
        layout = QHBoxLayout(group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 15)
        
        self.start_btn = QPushButton("▶ Start")
        self.start_btn.setStyleSheet(Styles.BUTTON_STYLE)
        self.start_btn.setToolTip("Start Monte Carlo simulation")
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setStyleSheet(Styles.BUTTON_STYLE)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setToolTip("Pause simulation")
        
        self.reset_btn = QPushButton("⟲ Reset")
        self.reset_btn.setStyleSheet(Styles.BUTTON_STYLE)
        self.reset_btn.setToolTip("Reset simulation")
        
        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.reset_btn)
        
        parent_layout.addWidget(group)
        
    def create_speed_controls(self, parent_layout):
        group = QGroupBox("Simulation Speed")
        group.setStyleSheet("""
        QGroupBox {
            color: white; 
            font-weight: bold; 
            font-size: 12px;
            border: 2px solid #555;
            border-radius: 6px;
            margin: 5px;
        }
        QGroupBox::title {
            padding: 0 10px;
        }
        """)
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Speed slider
        speed_layout = QHBoxLayout()
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10, 1000)  # 10ms to 1000ms
        self.speed_slider.setValue(100)
        self.speed_slider.setStyleSheet(Styles.SLIDER_STYLE)
        self.speed_slider.setToolTip("Delay between iterations (ms)")
        
        self.speed_label = QLabel("100 ms")
        self.speed_label.setStyleSheet(Styles.LABEL_STYLE)
        self.speed_label.setMinimumWidth(60)
        
        fast_label = QLabel("Fast")
        fast_label.setStyleSheet(Styles.LABEL_STYLE)
        slow_label = QLabel("Slow") 
        slow_label.setStyleSheet(Styles.LABEL_STYLE)
        
        speed_layout.addWidget(fast_label)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(slow_label)
        speed_layout.addWidget(self.speed_label)
        
        layout.addLayout(speed_layout)
        parent_layout.addWidget(group)
        
    def create_batch_controls(self, parent_layout):
        group = QGroupBox("Rozmiar Partii")
        group.setStyleSheet("""
        QGroupBox {
            color: white; 
            font-weight: bold; 
            font-size: 12px;
            border: 2px solid #555;
            border-radius: 6px;
            margin: 5px;
        }
        QGroupBox::title {
            padding: 0 10px;
        }
        """)
        layout = QHBoxLayout(group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 15)
        
        label = QLabel("Punkty na iterację:")
        label.setStyleSheet(Styles.LABEL_STYLE)
        
        self.batch_spinbox = QSpinBox()
        self.batch_spinbox.setRange(1, 1000)
        self.batch_spinbox.setValue(10)
        self.batch_spinbox.setStyleSheet(Styles.SPINBOX_STYLE)
        self.batch_spinbox.setToolTip("Liczba punktów generowanych w jednej iteracji")
        
        layout.addWidget(label)
        layout.addWidget(self.batch_spinbox)
        layout.addStretch()
        
        parent_layout.addWidget(group)
        
    def create_display_info(self, parent_layout):
        group = QGroupBox("Wyniki")
        group.setStyleSheet("""
        QGroupBox {
            color: white; 
            font-weight: bold; 
            font-size: 12px;
            border: 2px solid #555;
            border-radius: 6px;
            margin: 5px;
        }
        QGroupBox::title {
            padding: 0 10px;
        }
        """)
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Pi estimate - prominent display
        pi_card = QFrame()
        pi_card.setStyleSheet(f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {Colors.ACCENT_CYAN.name()}, stop:1 #0099CC);
            border-radius: 8px;
            padding: 8px;
            margin: 2px;
        }}
        """)
        pi_card_layout = QHBoxLayout(pi_card)
        pi_card_layout.setContentsMargins(12, 8, 12, 8)
        
        pi_symbol = QLabel("π =")
        pi_symbol.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        pi_card_layout.addWidget(pi_symbol)
        
        self.pi_label = QLabel("0.000000")
        self.pi_label.setStyleSheet("color: white; font-family: monospace; font-size: 20px; font-weight: bold;")
        pi_card_layout.addWidget(self.pi_label)
        pi_card_layout.addStretch()
        
        layout.addWidget(pi_card)
        
        # Stats row
        stats_layout = QHBoxLayout()
        
        # Total points card
        points_card = QFrame()
        points_card.setStyleSheet(f"""
        QFrame {{
            background-color: {Colors.CARD_BACKGROUND.name()};
            border: 1px solid {Colors.SUCCESS.name()};
            border-radius: 6px;
            padding: 4px;
        }}
        """)
        points_card_layout = QVBoxLayout(points_card)
        points_card_layout.setContentsMargins(8, 6, 8, 6)
        
        points_title = QLabel("Punkty")
        points_title.setStyleSheet(f"color: {Colors.SUCCESS.name()}; font-size: 10px; font-weight: bold;")
        points_card_layout.addWidget(points_title)
        
        self.points_label = QLabel("0")
        self.points_label.setStyleSheet("color: white; font-family: monospace; font-size: 14px; font-weight: bold;")
        points_card_layout.addWidget(self.points_label)
        stats_layout.addWidget(points_card)
        
        # Error card
        error_card = QFrame()
        error_card.setStyleSheet(f"""
        QFrame {{
            background-color: {Colors.CARD_BACKGROUND.name()};
            border: 1px solid {Colors.ERROR.name()};
            border-radius: 6px;
            padding: 4px;
        }}
        """)
        error_card_layout = QVBoxLayout(error_card)
        error_card_layout.setContentsMargins(8, 6, 8, 6)
        
        error_title = QLabel("Błąd")
        error_title.setStyleSheet(f"color: {Colors.ERROR.name()}; font-size: 10px; font-weight: bold;")
        error_card_layout.addWidget(error_title)
        
        self.error_label = QLabel("0.000000")
        self.error_label.setStyleSheet("color: white; font-family: monospace; font-size: 12px; font-weight: bold;")
        error_card_layout.addWidget(self.error_label)
        stats_layout.addWidget(error_card)
        
        layout.addLayout(stats_layout)
        
        # Accuracy progress bar
        accuracy_title = QLabel("Dokładność")
        accuracy_title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY.name()}; font-size: 11px; font-weight: bold; margin-top: 5px;")
        layout.addWidget(accuracy_title)
        
        self.accuracy_bar = QProgressBar()
        self.accuracy_bar.setRange(0, 100)
        self.accuracy_bar.setValue(0)
        self.accuracy_bar.setStyleSheet(f"""
        QProgressBar {{
            border: 2px solid {Colors.CARD_BACKGROUND.name()};
            border-radius: 8px;
            text-align: center;
            color: white;
            height: 25px;
            font-weight: bold;
            background-color: {Colors.CARD_BACKGROUND.name()};
        }}
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {Colors.SUCCESS.name()}, stop:1 #66BB6A);
            border-radius: 6px;
        }}
        """)
        layout.addWidget(self.accuracy_bar)
        
        parent_layout.addWidget(group)
        
    def create_options(self, parent_layout):
        group = QGroupBox()
        group.setTitle("Opcje Wyświetlania")
        group.setStyleSheet("""
        QGroupBox {
            color: white; 
            font-weight: bold; 
            font-size: 12px;
            border: 2px solid #555;
            border-radius: 6px;
            margin: 5px;
        }
        QGroupBox::title {
            padding: 0 10px;
        }
        """)
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 15)
        
        self.animation_checkbox = QCheckBox("Animacje punktów")
        self.animation_checkbox.setChecked(True)
        self.animation_checkbox.setStyleSheet("color: white;")
        
        self.grid_checkbox = QCheckBox("Siatka współrzędnych")
        self.grid_checkbox.setChecked(False)
        self.grid_checkbox.setStyleSheet("color: white;")
        
        layout.addWidget(self.animation_checkbox)
        layout.addWidget(self.grid_checkbox)
        
        parent_layout.addWidget(group)
        
    def setup_connections(self):
        self.start_btn.clicked.connect(self.on_start_clicked)
        self.pause_btn.clicked.connect(self.on_pause_clicked)
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        
    def on_start_clicked(self):
        self.start_simulation.emit()
        
    def on_pause_clicked(self):
        self.pause_simulation.emit()
        
    def on_reset_clicked(self):
        self.reset_simulation.emit()
        
    def on_speed_changed(self, value):
        self.speed_label.setText(f"{value} ms")
        self.speed_changed.emit(value)
        
    def set_running_state(self, running: bool):
        self.is_running = running
        self.start_btn.setEnabled(not running)
        self.pause_btn.setEnabled(running)
        
        if running:
            self.start_btn.setText("▶ Start")
        else:
            self.start_btn.setText("▶ Start")
            
    def reset_display(self):
        self.set_running_state(False)