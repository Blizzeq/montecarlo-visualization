from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
import math
from typing import List
from ...core.monte_carlo import Point
from ...utils.colors import Colors


class AnimatedPoint:
    def __init__(self, point: Point):
        self.point = point
        self.alpha = 0
        self.scale = 0.0
        self.target_alpha = 255
        self.target_scale = 1.0
        self.animation_progress = 0.0
        
    def update_animation(self, dt: float):
        self.animation_progress = min(1.0, self.animation_progress + dt * 4.0)
        
        # Ease-out animation
        progress = 1 - (1 - self.animation_progress) ** 2
        
        self.alpha = int(progress * self.target_alpha)
        self.scale = progress * self.target_scale


class SimulationCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.animated_points: List[AnimatedPoint] = []
        self.all_points: List[Point] = []
        
        self.show_animations = True
        self.show_grid = False
        self.point_size = 4  # Increased for better visibility
        self.max_displayed_points = 100000  # Increased limit for more points
        
        self.setMinimumSize(400, 400)
        self.setStyleSheet(f"background-color: {Colors.CANVAS_BACKGROUND.name()};")
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(16)  # ~60 FPS
        
        self.last_time = 0
        
    def add_points(self, new_points: List[Point]):
        self.all_points.extend(new_points)
        
        # Keep only recent points for display to maintain performance
        if len(self.all_points) > self.max_displayed_points:
            self.all_points = self.all_points[-self.max_displayed_points:]
        
        if self.show_animations:
            for point in new_points:
                animated_point = AnimatedPoint(point)
                self.animated_points.append(animated_point)
        
        self.update()
        
    def clear(self):
        self.animated_points.clear()
        self.all_points.clear()
        self.update()
        
    def update_animations(self):
        current_time = self.animation_timer.remainingTime()
        dt = 0.016  # Assume 60 FPS
        
        # Update point animations
        self.animated_points = [
            p for p in self.animated_points 
            if p.animation_progress < 1.0
        ]
        
        for point in self.animated_points:
            point.update_animation(dt)
            
        if self.animated_points:
            self.update()
            
    def set_animation_enabled(self, enabled: bool):
        self.show_animations = enabled
        if not enabled:
            self.animated_points.clear()
            
    def set_grid_enabled(self, enabled: bool):
        self.show_grid = enabled
        self.update()
        
    def set_point_size(self, size: int):
        self.point_size = max(1, min(10, size))
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        # Get canvas dimensions
        width = self.width()
        height = self.height()
        size = min(width, height) - 20
        center_x = width // 2
        center_y = height // 2
        radius = size // 2
        
        # Transform coordinates: [-1,1] -> canvas coordinates
        def transform_point(x: float, y: float):
            canvas_x = center_x + x * radius
            canvas_y = center_y - y * radius  # Flip Y axis
            return canvas_x, canvas_y
        
        # Draw grid if enabled
        if self.show_grid:
            self.draw_grid(painter, center_x, center_y, radius)
            
        # Draw square boundary
        pen = QPen(Colors.SQUARE_OUTLINE, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        square_rect = QRectF(center_x - radius, center_y - radius, size, size)
        painter.drawRect(square_rect)
        
        # Draw circle
        pen = QPen(Colors.CIRCLE_OUTLINE, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        circle_rect = QRectF(center_x - radius, center_y - radius, size, size)
        painter.drawEllipse(circle_rect)
        
        # Draw points
        self.draw_points(painter, transform_point)
        
        # Draw legend
        self.draw_legend(painter)
        
    def draw_grid(self, painter: QPainter, center_x: int, center_y: int, radius: int):
        pen = QPen(QColor(60, 60, 65), 1)
        painter.setPen(pen)
        
        # Grid lines every 0.2 units
        for i in range(-5, 6):
            offset = i * 0.2 * radius
            # Vertical lines
            painter.drawLine(center_x + offset, center_y - radius, 
                           center_x + offset, center_y + radius)
            # Horizontal lines
            painter.drawLine(center_x - radius, center_y + offset,
                           center_x + radius, center_y + offset)
                           
    def draw_points(self, painter: QPainter, transform_func):
        # Draw regular points (older points) using batch drawing for performance
        displayed_points = self.all_points[-self.max_displayed_points:] if len(self.all_points) > self.max_displayed_points else self.all_points
        animated_point_set = {id(ap.point) for ap in self.animated_points}
        
        # Separate points by type for batch drawing
        inside_points = []
        outside_points = []
        
        for point in displayed_points:
            if id(point) not in animated_point_set:
                canvas_x, canvas_y = transform_func(point.x, point.y)
                if point.inside_circle:
                    inside_points.append((canvas_x, canvas_y))
                else:
                    outside_points.append((canvas_x, canvas_y))
        
        # Batch draw inside points (green)
        if inside_points:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(Colors.POINT_INSIDE))
            for x, y in inside_points:
                painter.drawEllipse(x - self.point_size/2, y - self.point_size/2, 
                                  self.point_size, self.point_size)
        
        # Batch draw outside points (red)
        if outside_points:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(Colors.POINT_OUTSIDE))
            for x, y in outside_points:
                painter.drawEllipse(x - self.point_size/2, y - self.point_size/2,
                                  self.point_size, self.point_size)
                
        # Draw animated points on top (keep individual drawing for animations)
        for animated_point in self.animated_points:
            self.draw_single_point(
                painter, 
                animated_point.point, 
                transform_func, 
                animated_point.alpha,
                animated_point.scale
            )
            
    def draw_single_point(self, painter: QPainter, point: Point, 
                         transform_func, alpha: int, scale: float):
        canvas_x, canvas_y = transform_func(point.x, point.y)
        
        # Choose color based on whether point is inside circle
        if point.inside_circle:
            color = QColor(Colors.POINT_INSIDE)
        else:
            color = QColor(Colors.POINT_OUTSIDE)
            
        color.setAlpha(alpha)
        
        # Draw point
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        
        point_size = self.point_size * scale
        painter.drawEllipse(
            canvas_x - point_size/2, 
            canvas_y - point_size/2,
            point_size, 
            point_size
        )
        
    def draw_legend(self, painter: QPainter):
        # Main educational info panel
        panel_width = 320
        panel_height = 120
        panel_x = 10
        panel_y = 10
        
        # Draw semi-transparent background
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(panel_x, panel_y, panel_width, panel_height, 8, 8)
        
        # Title
        painter.setPen(QPen(Colors.TEXT_HIGHLIGHT))
        title_font = painter.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(panel_x + 15, panel_y + 25, "Monte Carlo Algorithm for π")
        
        # Algorithm explanation
        painter.setPen(QPen(Colors.TEXT_PRIMARY))
        info_font = painter.font()
        info_font.setPointSize(10)
        info_font.setBold(False)
        painter.setFont(info_font)
        
        painter.drawText(panel_x + 15, panel_y + 45, "• Random points in square [-1,1] × [-1,1]")
        painter.drawText(panel_x + 15, panel_y + 60, f"• Check: x² + y² ≤ 1 (inside circle)")
        painter.drawText(panel_x + 15, panel_y + 75, "• π ≈ 4 × (points inside / all points)")
        
        # Legend with points
        legend_y = panel_y + 95
        
        # Inside circle
        painter.setBrush(QBrush(Colors.POINT_INSIDE))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(panel_x + 15, legend_y - 5, 10, 10)
        
        painter.setPen(QPen(Colors.SUCCESS))
        painter.setFont(info_font)
        painter.drawText(panel_x + 35, legend_y + 5, "Inside")
        
        # Outside circle  
        painter.setBrush(QBrush(Colors.POINT_OUTSIDE))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(panel_x + 100, legend_y - 5, 10, 10)
        
        painter.setPen(QPen(Colors.ERROR))
        painter.drawText(panel_x + 120, legend_y + 5, "Outside")
        
        # Count display
        if self.all_points:
            inside_count = sum(1 for p in self.all_points if p.inside_circle)
            outside_count = len(self.all_points) - inside_count
            
            painter.setPen(QPen(Colors.TEXT_HIGHLIGHT))
            count_font = painter.font()
            count_font.setPointSize(11)
            count_font.setBold(True)
            painter.setFont(count_font)
            painter.drawText(panel_x + 200, legend_y + 5, 
                           f"In: {inside_count} | Out: {outside_count}")
        
    def mousePressEvent(self, event):
        # Toggle grid on right click
        if event.button() == Qt.RightButton:
            self.set_grid_enabled(not self.show_grid)