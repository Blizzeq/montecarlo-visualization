import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass
import time


@dataclass
class Point:
    x: float
    y: float
    inside_circle: bool


@dataclass
class SimulationResult:
    points: List[Point]
    pi_estimate: float
    total_points: int
    points_inside: int
    error: float
    computation_time: float


class MonteCarloSimulator:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.points = []
        self.points_inside = 0
        self.total_points = 0
        self.pi_estimates = []
        self.errors = []
        self.computation_times = []
    
    def generate_random_point(self) -> Point:
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        inside_circle = (x**2 + y**2) <= 1.0
        return Point(x, y, inside_circle)
    
    def generate_batch_points(self, count: int) -> List[Point]:
        x_coords = np.random.uniform(-1, 1, count)
        y_coords = np.random.uniform(-1, 1, count)
        distances_squared = x_coords**2 + y_coords**2
        inside_mask = distances_squared <= 1.0
        
        points = [Point(x_coords[i], y_coords[i], inside_mask[i]) for i in range(count)]
        
        return points
    
    def add_points(self, count: int) -> SimulationResult:
        start_time = time.time()
        
        new_points = self.generate_batch_points(count)
        self.points.extend(new_points)
        
        new_inside = sum(p.inside_circle for p in new_points)
        self.points_inside += new_inside
        self.total_points += count
        
        pi_estimate = 4.0 * self.points_inside / self.total_points if self.total_points > 0 else 0.0
        error = abs(pi_estimate - np.pi)
        computation_time = time.time() - start_time
        
        self.pi_estimates.append(pi_estimate)
        self.errors.append(error)
        self.computation_times.append(computation_time)
        
        return SimulationResult(
            points=new_points,
            pi_estimate=pi_estimate,
            total_points=self.total_points,
            points_inside=self.points_inside,
            error=error,
            computation_time=computation_time
        )
    
    def get_current_estimate(self) -> float:
        if self.total_points == 0:
            return 0.0
        return 4.0 * self.points_inside / self.total_points
    
    def get_convergence_data(self) -> Tuple[List[int], List[float], List[float]]:
        x_data = list(range(0, len(self.pi_estimates)))
        return x_data, self.pi_estimates.copy(), self.errors.copy()
    
    def get_all_points(self) -> List[Point]:
        return self.points.copy()
    
    def get_statistics(self) -> dict:
        if not self.pi_estimates:
            return {
                'mean_estimate': 0.0,
                'std_estimate': 0.0,
                'min_error': 0.0,
                'max_error': 0.0,
                'mean_error': 0.0,
                'total_computation_time': 0.0
            }
        
        return {
            'mean_estimate': np.mean(self.pi_estimates),
            'std_estimate': np.std(self.pi_estimates),
            'min_error': np.min(self.errors),
            'max_error': np.max(self.errors),
            'mean_error': np.mean(self.errors),
            'total_computation_time': np.sum(self.computation_times)
        }


