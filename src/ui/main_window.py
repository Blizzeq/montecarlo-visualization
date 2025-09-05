from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QSplitter, QStatusBar, QMenuBar, QMenu)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction, QIcon

from .widgets.simulation_canvas import SimulationCanvas
from .widgets.control_panel import ControlPanel
from .widgets.statistics_panel import StatisticsPanel
from ..core.monte_carlo import MonteCarloSimulator
from ..utils.colors import Colors, Styles


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulator = MonteCarloSimulator()
        self.simulation_timer = QTimer()
        self.is_running = False
        self.points_per_batch = 50  # Fixed batch size
        self.simulation_speed = 100  # ms between batches
        
        self.setup_ui()
        self.setup_connections()
        self.setup_timer()
        
    def setup_ui(self):
        self.setWindowTitle("Monte Carlo π Visualization")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet(f"background-color: {Colors.BACKGROUND.name()};")
        
        self.create_menu_bar()
        self.create_central_widget()
        self.create_status_bar()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar { color: white; background-color: #2e2e32; }")
        
        # File menu
        file_menu = menubar.addMenu('Plik')
        
        export_action = QAction('Eksportuj wyniki...', self)
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction('Wyjście', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Simulation menu
        sim_menu = menubar.addMenu('Symulacja')
        
        reset_action = QAction('Reset', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.triggered.connect(self.reset_simulation)
        sim_menu.addAction(reset_action)
        
        # View menu
        view_menu = menubar.addMenu('Widok')
        
        toggle_stats_action = QAction('Pokaż/Ukryj statystyki', self)
        toggle_stats_action.setShortcut('Ctrl+T')
        toggle_stats_action.triggered.connect(self.toggle_statistics_panel)
        view_menu.addAction(toggle_stats_action)
        
    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left side - simulation and controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Simulation canvas
        self.canvas = SimulationCanvas()
        left_layout.addWidget(self.canvas, stretch=1)
        
        # Control panel
        self.control_panel = ControlPanel()
        left_layout.addWidget(self.control_panel)
        
        main_splitter.addWidget(left_widget)
        
        # Right side - statistics
        self.statistics_panel = StatisticsPanel()
        main_splitter.addWidget(self.statistics_panel)
        
        # Set splitter proportions (66% left, 34% right for ~33% statistics panel)
        main_splitter.setSizes([900, 500])
        main_splitter.setStretchFactor(0, 2)  # Left side gets stretch priority
        main_splitter.setStretchFactor(1, 1)  # Right side also gets stretch but lower priority
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.addWidget(main_splitter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("color: white; background-color: #2e2e32;")
        self.status_bar.showMessage("Gotowy do symulacji")
        
    def setup_connections(self):
        # Control panel signals
        self.control_panel.start_simulation.connect(self.start_simulation)
        self.control_panel.pause_simulation.connect(self.pause_simulation)
        self.control_panel.reset_simulation.connect(self.reset_simulation)
        self.control_panel.speed_changed.connect(self.set_simulation_speed)
        
    def setup_timer(self):
        self.simulation_timer.timeout.connect(self.simulation_step)
        
    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.simulation_timer.start(self.simulation_speed)
            self.control_panel.set_running_state(True)
            self.status_bar.showMessage("Symulacja w toku...")
            
    def pause_simulation(self):
        if self.is_running:
            self.is_running = False
            self.simulation_timer.stop()
            self.control_panel.set_running_state(False)
            self.status_bar.showMessage("Symulacja wstrzymana")
            
    def reset_simulation(self):
        self.pause_simulation()
        self.simulator.reset()
        self.canvas.clear()
        self.statistics_panel.clear()
        self.control_panel.reset_display()
        self.status_bar.showMessage("Symulacja zresetowana")
        
    def set_simulation_speed(self, speed_ms: int):
        self.simulation_speed = speed_ms
        if self.is_running:
            self.simulation_timer.setInterval(self.simulation_speed)
            
        
    def simulation_step(self):
        if not self.is_running:
            return  # Don't process if simulation was paused
            
        try:
            # Add new points to simulation
            result = self.simulator.add_points(self.points_per_batch)
            
            # Update canvas with new points
            self.canvas.add_points(result.points)
            
            # Update statistics panel
            self.statistics_panel.update_statistics(result, self.simulator)
            
            # Update status bar
            accuracy = max(0, (1.0 - result.error / 3.14159) * 100)
            self.status_bar.showMessage(
                f"Punkty: {result.total_points:,} | π ≈ {result.pi_estimate:.6f} | "
                f"Dokładność: {accuracy:.2f}% | Uruchomione: {self.is_running}"
            )
            
            # Ensure timer continues running
            if self.is_running and not self.simulation_timer.isActive():
                print(f"Timer stopped unexpectedly at {result.total_points} points, restarting...")
                self.simulation_timer.start(self.simulation_speed)
            
        except Exception as e:
            print(f"Simulation error: {e}")
            self.status_bar.showMessage(f"Błąd symulacji: {str(e)}")
            # Don't pause simulation on error, just log it
            
    def toggle_statistics_panel(self):
        visible = self.statistics_panel.isVisible()
        self.statistics_panel.setVisible(not visible)
        
    def export_results(self):
        # TODO: Implement export functionality
        self.status_bar.showMessage("Eksport zostanie zaimplementowany wkrótce...")
        
    def closeEvent(self, event):
        self.pause_simulation()
        event.accept()