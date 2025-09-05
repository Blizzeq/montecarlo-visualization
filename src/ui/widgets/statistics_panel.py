from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTabWidget, QGroupBox, QTextEdit, QSplitter, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import pyqtgraph as pg
import numpy as np
from typing import List
from ...core.monte_carlo import MonteCarloSimulator, SimulationResult
from ...utils.colors import Colors, Styles


class StatisticsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.convergence_data_x = []
        self.convergence_data_y = []
        self.error_data_y = []
        self.max_points_to_display = 1000
        
        self.setup_ui()
        
    def setup_ui(self):
        self.setMinimumWidth(350)
        self.setStyleSheet(Styles.PANEL_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title_label = QLabel("Statystyki i Analizy")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin-bottom: 5px;")
        layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #2e2e32;
        }
        QTabBar::tab {
            background-color: #3a3a3f;
            color: white;
            padding: 6px 12px;
            margin: 2px;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #2196F3;
        }
        QTabBar::tab:hover {
            background-color: #4a4a4f;
        }
        """)
        
        # Create tabs
        self.create_convergence_tab()
        self.create_statistics_tab()
        self.create_distribution_tab()
        
        layout.addWidget(self.tab_widget)
        
    def create_convergence_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Convergence plot
        self.convergence_plot = pg.PlotWidget(background='#1a1a1a')
        
        # Set up the plot with proper margins for labels
        self.convergence_plot.getPlotItem().setContentsMargins(10, 10, 10, 15)  # left, top, right, bottom
        
        self.convergence_plot.setLabel('left', 'Estymowana wartość π', color='white', size='11pt')
        self.convergence_plot.setLabel('bottom', 'Numer iteracji', color='white', size='11pt')
        self.convergence_plot.setTitle('Zbieżność do prawdziwej wartości π', color='#00D4FF', size='13pt')
        self.convergence_plot.showGrid(x=True, y=True, alpha=0.4)
        
        # Set initial axis ranges
        self.convergence_plot.setYRange(2.8, 3.4)
        self.convergence_plot.setXRange(0, 10)
        
        # Style the axes with better visibility
        left_axis = self.convergence_plot.getAxis('left')
        bottom_axis = self.convergence_plot.getAxis('bottom')
        left_axis.setTextPen('white')
        bottom_axis.setTextPen('white')
        left_axis.setPen('white')
        bottom_axis.setPen('white')
        
        # Force label update
        left_axis.setLabel('Estymowana wartość π', color='white', size='12pt')
        bottom_axis.setLabel('Numer iteracji', color='white', size='12pt')
        
        # Add reference line for π
        self.pi_line = pg.InfiniteLine(pos=np.pi, angle=0, pen=pg.mkPen('yellow', width=2, style=Qt.DashLine))
        self.convergence_plot.addItem(self.pi_line)
        
        # Add text label for π line
        pi_text = pg.TextItem('π = 3.14159...', color='yellow', anchor=(0, 1))
        pi_text.setPos(1, np.pi)
        self.convergence_plot.addItem(pi_text)
        
        self.convergence_curve = self.convergence_plot.plot(pen=pg.mkPen('#4FC3F7', width=2))
        
        layout.addWidget(self.convergence_plot)
        
        # Error plot
        self.error_plot = pg.PlotWidget(background='#1a1a1a')
        
        # Set up the plot with proper margins for labels
        self.error_plot.getPlotItem().setContentsMargins(10, 10, 10, 15)  # left, top, right, bottom
        
        self.error_plot.setLabel('left', 'Błąd bezwzględny', color='white', size='11pt')
        self.error_plot.setLabel('bottom', 'Numer iteracji', color='white', size='11pt')
        self.error_plot.setTitle('Błąd estymacji π', color='#00D4FF', size='13pt')
        self.error_plot.showGrid(x=True, y=True, alpha=0.4)
        
        # Start with linear scale from 0, not logarithmic
        self.error_plot.setLogMode(y=False)
        self.error_plot.setYRange(0, 0.2)  # Smaller range for typical error values
        self.error_plot.setXRange(0, 10)
        
        # Style the axes with better visibility
        error_left_axis = self.error_plot.getAxis('left')
        error_bottom_axis = self.error_plot.getAxis('bottom')
        error_left_axis.setTextPen('white')
        error_bottom_axis.setTextPen('white')
        error_left_axis.setPen('white')
        error_bottom_axis.setPen('white')
        
        # Force label update
        error_left_axis.setLabel('Błąd bezwzględny', color='white', size='12pt')
        error_bottom_axis.setLabel('Numer iteracji', color='white', size='12pt')
        
        self.error_curve = self.error_plot.plot(pen=pg.mkPen('#FF7043', width=2))
        
        layout.addWidget(self.error_plot)
        
        self.tab_widget.addTab(tab, "Zbieżność")
        
    def create_statistics_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Current statistics - colorful cards layout
        current_title = QLabel("📊 Aktualne Statystyki")
        current_title.setStyleSheet(f"color: {Colors.TEXT_HIGHLIGHT.name()}; font-size: 16px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(current_title)
        
        # Create grid layout for cards
        cards_layout = QVBoxLayout()
        cards_layout.setSpacing(8)
        
        self.stats_labels = {}
        
        # Stats cards data: (key, icon, title, default_value, color)
        stats_cards = [
            ("current_pi", "π", "Aktualne π", "0.000000", Colors.ACCENT_CYAN),
            ("total_points", "📍", "Wszystkie punkty", "0", Colors.SUCCESS),
            ("points_inside", "✅", "Punkty w kole", "0", Colors.SUCCESS),
            ("points_outside", "❌", "Punkty poza kołem", "0", Colors.ERROR),
            ("current_error", "⚠", "Błąd bezwzględny", "0.000000", Colors.WARNING),
            ("relative_error", "%", "Błąd względny", "0.00%", Colors.ACCENT_ORANGE)
        ]
        
        # Create cards in pairs (2 per row)
        for i in range(0, len(stats_cards), 2):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(8)
            
            for j in range(2):
                if i + j < len(stats_cards):
                    key, icon, title, default_value, color = stats_cards[i + j]
                    
                    # Create card
                    card = QFrame()
                    card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {Colors.CARD_BACKGROUND.name()};
                        border: 2px solid {color.name()};
                        border-radius: 8px;
                        padding: 8px;
                        margin: 2px;
                    }}
                    """)
                    card_layout = QVBoxLayout(card)
                    card_layout.setSpacing(4)
                    card_layout.setContentsMargins(12, 8, 12, 8)
                    
                    # Icon and title row
                    header_layout = QHBoxLayout()
                    icon_label = QLabel(icon)
                    icon_label.setStyleSheet(f"color: {color.name()}; font-size: 16px; font-weight: bold;")
                    title_label = QLabel(title)
                    title_label.setStyleSheet(f"color: {color.name()}; font-size: 11px; font-weight: bold;")
                    
                    header_layout.addWidget(icon_label)
                    header_layout.addWidget(title_label)
                    header_layout.addStretch()
                    card_layout.addLayout(header_layout)
                    
                    # Value label
                    value_label = QLabel(default_value)
                    value_label.setStyleSheet("color: white; font-family: monospace; font-size: 14px; font-weight: bold;")
                    card_layout.addWidget(value_label)
                    
                    self.stats_labels[key] = value_label
                    row_layout.addWidget(card)
                else:
                    row_layout.addStretch()
                    
            cards_layout.addLayout(row_layout)
            
        layout.addLayout(cards_layout)
        
        # Historical statistics section
        historical_title = QLabel("📈 Statystyki Historyczne")
        historical_title.setStyleSheet(f"color: {Colors.TEXT_HIGHLIGHT.name()}; font-size: 16px; font-weight: bold; margin: 15px 0 5px 0;")
        layout.addWidget(historical_title)
        
        # Historical stats card
        historical_card = QFrame()
        historical_card.setStyleSheet(f"""
        QFrame {{
            background-color: {Colors.CARD_BACKGROUND.name()};
            border: 2px solid {Colors.TEXT_SECONDARY.name()};
            border-radius: 8px;
            padding: 12px;
            margin: 2px;
        }}
        """)
        historical_layout = QVBoxLayout(historical_card)
        
        self.historical_stats_text = QTextEdit()
        self.historical_stats_text.setReadOnly(True)
        self.historical_stats_text.setMinimumHeight(200)
        self.historical_stats_text.setStyleSheet(f"""
        QTextEdit {{
            background-color: {Colors.BACKGROUND.name()};
            color: {Colors.TEXT_PRIMARY.name()};
            border: 1px solid {Colors.TEXT_SECONDARY.name()};
            border-radius: 6px;
            font-family: monospace;
            font-size: 11px;
            padding: 8px;
        }}
        """)
        
        historical_layout.addWidget(self.historical_stats_text)
        layout.addWidget(historical_card, 1)  # Give it stretch factor of 1 to expand
        
        self.tab_widget.addTab(tab, "Statystyki")
        
    def create_distribution_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Points distribution plot
        self.distribution_plot = pg.PlotWidget(background='#1a1a1a')
        
        # Set up the plot with proper margins for labels
        self.distribution_plot.getPlotItem().setContentsMargins(10, 10, 10, 15)  # left, top, right, bottom
        
        self.distribution_plot.setLabel('left', 'Liczba punktów', color='white', size='12pt')
        self.distribution_plot.setLabel('bottom', 'Odległość od środka koła', color='white', size='12pt')
        self.distribution_plot.setTitle('Histogram odległości punktów od centrum', color='#00D4FF', size='14pt')
        self.distribution_plot.showGrid(x=True, y=True, alpha=0.4)
        
        # Set initial axis ranges
        self.distribution_plot.setXRange(0, 1.5)
        self.distribution_plot.setYRange(0, 100)
        
        # Style the axes with better visibility
        dist_left_axis = self.distribution_plot.getAxis('left')
        dist_bottom_axis = self.distribution_plot.getAxis('bottom')
        dist_left_axis.setTextPen('white')
        dist_bottom_axis.setTextPen('white')
        dist_left_axis.setPen('white')
        dist_bottom_axis.setPen('white')
        
        # Force label update
        dist_left_axis.setLabel('Liczba punktów', color='white', size='12pt')
        dist_bottom_axis.setLabel('Odległość od środka koła', color='white', size='12pt')
        
        layout.addWidget(self.distribution_plot)
        
        # Efficiency metrics
        efficiency_group = QGroupBox("Metryki Wydajności")
        efficiency_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        efficiency_layout = QVBoxLayout(efficiency_group)
        
        self.efficiency_labels = {}
        efficiency_info = [
            ("points_per_second", "Punkty na sekundę:", "0"),
            ("avg_batch_time", "Śr. czas partii:", "0.000 ms"),
            ("memory_usage", "Użycie pamięci:", "~0 MB")
        ]
        
        for key, label_text, default_value in efficiency_info:
            row_layout = QHBoxLayout()
            
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            
            value_label = QLabel(default_value)
            value_label.setStyleSheet("color: #4CAF50; font-family: monospace; font-weight: bold;")
            
            self.efficiency_labels[key] = value_label
            
            row_layout.addWidget(label)
            row_layout.addStretch()
            row_layout.addWidget(value_label)
            
            efficiency_layout.addLayout(row_layout)
            
        layout.addWidget(efficiency_group)
        
        self.tab_widget.addTab(tab, "Rozkład")
        
    def update_statistics(self, result: SimulationResult, simulator: MonteCarloSimulator):
        # Update convergence plots
        self.update_convergence_plots(simulator)
        
        # Update current statistics
        self.update_current_statistics(result, simulator)
        
        # Update distribution plot
        self.update_distribution_plot(simulator)
        
        # Update efficiency metrics
        self.update_efficiency_metrics(result, simulator)
        
    def update_convergence_plots(self, simulator: MonteCarloSimulator):
        x_data, pi_data, error_data = simulator.get_convergence_data()
        
        if not x_data or not pi_data or not error_data:
            return
            
        if len(x_data) > self.max_points_to_display:
            # Subsample data for performance
            step = len(x_data) // self.max_points_to_display
            x_data = x_data[::step]
            pi_data = pi_data[::step]
            error_data = error_data[::step]
            
        # Update convergence plot
        self.convergence_curve.setData(x_data, pi_data)
        
        # Auto-scale convergence plot
        if len(pi_data) > 0:
            y_min = min(min(pi_data), 2.8)
            y_max = max(max(pi_data), 3.4)
            self.convergence_plot.setYRange(y_min - 0.1, y_max + 0.1)
            self.convergence_plot.setXRange(0, max(x_data) + 1)
        
        # Update error plot
        self.error_curve.setData(x_data, error_data)
        
        # Auto-scale error plot
        if len(error_data) > 0:
            y_max = max(error_data)
            y_min = min(error_data)
            
            # Always use linear scale and start from 0
            self.error_plot.setLogMode(y=False)
            
            # Set reasonable range based on data
            if y_max < 0.01:
                # Very small errors - use tight range
                self.error_plot.setYRange(0, max(0.02, y_max * 1.5))
            elif y_max < 0.1:
                # Small errors - normal range  
                self.error_plot.setYRange(0, max(0.1, y_max * 1.2))
            elif y_max < 1.0:
                # Medium errors
                self.error_plot.setYRange(0, max(0.5, y_max * 1.2))
            else:
                # Large errors
                self.error_plot.setYRange(0, y_max * 1.2)
                
            self.error_plot.setXRange(0, max(x_data) + 1)
        
    def update_current_statistics(self, result: SimulationResult, simulator: MonteCarloSimulator):
        stats = simulator.get_statistics()
        
        self.stats_labels["current_pi"].setText(f"{result.pi_estimate:.6f}")
        self.stats_labels["total_points"].setText(f"{result.total_points:,}")
        self.stats_labels["points_inside"].setText(f"{result.points_inside:,}")
        self.stats_labels["points_outside"].setText(f"{result.total_points - result.points_inside:,}")
        self.stats_labels["current_error"].setText(f"{result.error:.6f}")
        self.stats_labels["relative_error"].setText(f"{(result.error / np.pi * 100):.2f}%")
        
        # Update historical statistics text
        self.update_historical_text(stats, result)
        
    def update_historical_text(self, stats: dict, result: SimulationResult):
        historical_text = f"""📊 STATYSTYKI SYMULACJI

🎯 Estymacja π:
   • Średnia: {stats['mean_estimate']:.6f}
   • Odchylenie std: {stats['std_estimate']:.6f}
   • Aktualna: {result.pi_estimate:.6f}

⚠️  Analiza błędu:
   • Minimalny: {stats['min_error']:.6f}
   • Maksymalny: {stats['max_error']:.6f}
   • Średni: {stats['mean_error']:.6f}
   • Aktualny: {result.error:.6f}

📐 Porównanie z π:
   • Teoretyczne π: {np.pi:.6f}
   • Różnica: {abs(result.pi_estimate - np.pi):.6f}
   • Dokładność: {(1 - result.error / np.pi) * 100:.2f}%

⏱️  Wydajność:
   • Czas obliczeń: {stats['total_computation_time']:.3f}s
   • Punkty: {result.total_points:,}
        """.strip()
        
        self.historical_stats_text.setPlainText(historical_text)
        
    def update_distribution_plot(self, simulator: MonteCarloSimulator):
        points = simulator.get_all_points()
        
        if len(points) > 1000:  # Limit for performance
            points = points[-1000:]
            
        if not points:
            # If no points, clear the plot and show empty state
            self.distribution_plot.clear()
            return
            
        try:
            distances = [np.sqrt(p.x**2 + p.y**2) for p in points]
            
            # Create histogram
            hist, bin_edges = np.histogram(distances, bins=20, range=(0, 1.5))
            
            # Clear previous plot
            self.distribution_plot.clear()
            
            # Only plot if we have data
            if len(hist) > 0 and np.sum(hist) > 0:
                # Plot histogram as bars
                width = bin_edges[1] - bin_edges[0]
                x = bin_edges[:-1] + width/2
                
                # Color bars based on whether they're inside or outside circle
                colors = []
                for center in x:
                    if center <= 1.0:
                        colors.append('#4CAF50')  # Green for inside circle
                    else:
                        colors.append('#F44336')  # Red for outside circle
                
                # Create bars with different colors
                for i, (xi, hi) in enumerate(zip(x, hist)):
                    if hi > 0:  # Only draw if there's data
                        bar = pg.BarGraphItem(x=[xi], height=[hi], width=width*0.8, 
                                            brush=pg.mkBrush(colors[i]), pen=pg.mkPen('white'))
                        self.distribution_plot.addItem(bar)
                
                # Add vertical line at radius = 1
                circle_line = pg.InfiniteLine(pos=1.0, angle=90, pen=pg.mkPen('#FFD700', width=3, style=Qt.DashLine))
                self.distribution_plot.addItem(circle_line)
                
                # Add text label for circle radius - positioned at top of chart
                max_height = max(hist) if len(hist) > 0 and max(hist) > 0 else 100
                radius_text = pg.TextItem('← Promień koła (r=1)', color='#FFD700', anchor=(0, 1))
                radius_text.setPos(1.02, max_height * 0.9)  # Position near top
                self.distribution_plot.addItem(radius_text)
                
                # Update axis range
                if max_height > 0:
                    self.distribution_plot.setYRange(0, max_height * 1.1)
                    
        except Exception as e:
            print(f"Error updating distribution plot: {e}")
            self.distribution_plot.clear()
        
    def update_efficiency_metrics(self, result: SimulationResult, simulator: MonteCarloSimulator):
        # Points per second (rough estimate)
        if result.computation_time > 0:
            pps = len(result.points) / result.computation_time
            self.efficiency_labels["points_per_second"].setText(f"{pps:.0f}")
            
        # Average batch time
        avg_time_ms = result.computation_time * 1000
        self.efficiency_labels["avg_batch_time"].setText(f"{avg_time_ms:.3f} ms")
        
        # Rough memory usage estimate
        estimated_memory = len(simulator.get_all_points()) * 32 / (1024 * 1024)  # rough estimate
        self.efficiency_labels["memory_usage"].setText(f"~{estimated_memory:.1f} MB")
        
    def clear(self):
        # Clear plots
        self.convergence_curve.clear()
        self.error_curve.clear()
        self.distribution_plot.clear()
        
        # Reset labels safely
        for key, label in self.stats_labels.items():
            if "points" in key or "punktów" in key:
                label.setText("0")
            else:
                label.setText("0.000000")
                
        for label in self.efficiency_labels.values():
            if label:  # Safety check
                label.setText("0")
            
        self.historical_stats_text.clear()