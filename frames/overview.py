import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import datetime
from matplotlib.figure import Figure
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class DataProvider(ABC):
    """Abstract base class for data providers"""
    @abstractmethod
    def get_time_trend_data(self, time_range: str) -> Tuple[np.ndarray, np.ndarray, List[str], np.ndarray]:
        """Get time trend data based on time range"""
        pass
    
    @abstractmethod
    def get_violation_types_data(self) -> Tuple[List[str], List[int]]:
        """Get violation types data"""
        pass
    
    @abstractmethod
    def get_summary_stats(self) -> Dict[str, int]:
        """Get summary statistics"""
        pass


class MockDataProvider(DataProvider):
    """Mock data provider that generates larger random data"""
    def get_time_trend_data(self, time_range: str) -> Tuple[np.ndarray, np.ndarray, List[str], np.ndarray]:
        """Generate larger random time trend data based on time range"""
        if time_range == "Last 24 Hours":
            x = np.array(range(24))
            y = np.array([random.randint(5000, 20000) for _ in range(24)])
            x_labels = [f"{h}:00" for h in range(0, 24, 4)]
            x_ticks = np.array(range(0, 24, 4))
        elif time_range == "Last Week":
            x = np.array(range(7))
            y = np.array([random.randint(30000, 80000) for _ in range(7)])
            today = datetime.datetime.now()
            x_labels = [(today - datetime.timedelta(days=6-i)).strftime("%a") for i in range(7)]
            x_ticks = np.array(range(7))
        else:  # Last Month
            days_in_month = 30
            x = np.array(range(days_in_month))
            y = np.array([random.randint(100000, 300000) for _ in range(days_in_month)])
            x_labels = [f"{i+1}" for i in range(0, days_in_month, 5)]
            x_ticks = np.array(range(0, days_in_month, 5))
                
        return x, y, x_labels, x_ticks
            
    def get_violation_types_data(self) -> Tuple[List[str], List[int]]:
        """Generate larger random violation types data"""
        violation_types = ["Helmet", "Vest", "Gloves", "Boots", "Mask"]
        counts = [random.randint(50000, 200000) for _ in range(len(violation_types))]
        return violation_types, counts
            
    def get_summary_stats(self) -> Dict[str, int]:
        """Generate larger random summary statistics"""
        return {
            "Total Violations": random.randint(500000, 2000000),
            "Helmet Violations": random.randint(200000, 800000),
            "Vest Violations": random.randint(150000, 600000),
            "Gloves Violations": random.randint(100000, 400000)
        }

class ChartComponent(ABC):
    """Base class for chart components"""
    def __init__(self, master: ctk.CTkFrame, title: str):
        self.frame = ctk.CTkFrame(master)
        self.title_label = ctk.CTkLabel(self.frame, text=title, 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(10, 0))
        
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def get_frame(self) -> ctk.CTkFrame:
        """Get the frame containing the chart"""
        return self.frame
    
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Update the chart with new data"""
        pass

class TimeTrendChart(ChartComponent):
    """Chart component for time trend visualization"""
    def __init__(self, master: ctk.CTkFrame, data_provider: DataProvider):
        super().__init__(master, "Violations Over Time")
        self.data_provider = data_provider
    
    def update(self, time_range: str) -> None:
        """Update the time trend chart based on time range"""
        x, y, x_labels, x_ticks = self.data_provider.get_time_trend_data(time_range)
        
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Plot the data
        ax.bar(x, y, color="#3282B8", alpha=0.7)
        ax.plot(x, y, color="#0F4C75", marker="o", linewidth=2)
        
        # Set labels and ticks
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels)
        ax.set_ylabel("Violations")
        
        # Add grid
        ax.grid(True, linestyle="--", alpha=0.7)
        
        # Update canvas
        self.fig.tight_layout()
        self.canvas.draw()

class ViolationTypesChart(ChartComponent):
    """Chart component for violation types visualization"""
    def __init__(self, master: ctk.CTkFrame, data_provider: DataProvider):
        super().__init__(master, "Violation Types")
        self.data_provider = data_provider
    
    def update(self, *args, **kwargs) -> None:
        """Update the violation types chart"""
        violation_types, counts = self.data_provider.get_violation_types_data()
        
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Plot
        colors = ["#FF5252", "#FFB142", "#20BF6B", "#3B75F2", "#9C27B0"]
        bars = ax.bar(violation_types, counts, color=colors[:len(violation_types)])
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                   f"{height}", ha="center", va="bottom")
        
        # Labels
        ax.set_ylabel("Count")
        ax.set_ylim(0, max(counts) * 1.2)  # Add some space for labels
        
        # Update canvas
        self.fig.tight_layout()
        self.canvas.draw()

class SummaryStatsComponent:
    """Component for displaying summary statistics"""
    def __init__(self, master: ctk.CTkFrame, data_provider: DataProvider):
        self.frame = ctk.CTkFrame(master)
        self.data_provider = data_provider
        
        self.title_label = ctk.CTkLabel(self.frame, text="Summary Statistics", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(10, 0))
        
        # Create summary container
        self.stat_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.stat_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid for stats
        self.stat_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.stat_container.grid_rowconfigure(0, weight=1)
        
        # Initialize stats boxes (will be populated in update)
        self.stat_boxes = {}
    
    def get_frame(self) -> ctk.CTkFrame:
        """Get the frame containing the summary stats"""
        return self.frame
    
    def update(self, *args, **kwargs) -> None:
        """Update the summary statistics"""
        stats = self.data_provider.get_summary_stats()
        
        # Clear existing stat boxes
        for widget in self.stat_container.winfo_children():
            widget.destroy()
        
        # Create new stat boxes
        colors = ["#FF5252", "#FFB142", "#20BF6B", "#3B75F2"]
        for i, (title, value) in enumerate(stats.items()):
            self._create_stat_box(
                self.stat_container, 0, i, 
                title, str(value), 
                colors[i % len(colors)]
            )
    
    def _create_stat_box(self, parent: ctk.CTkFrame, row: int, col: int, 
                         title: str, value: str, color: str) -> None:
        """Create a statistics box with a title and value"""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14))
        title_label.pack(pady=(10, 5))
        
        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        value_label.pack(pady=(0, 10))
        
        # Add indicator bar
        indicator = ctk.CTkFrame(frame, height=5, fg_color=color)
        indicator.pack(fill="x", padx=10, pady=(0, 10))

class TimeRangeSelector:
    """Component for selecting time range"""
    def __init__(self, master: ctk.CTkFrame, callback):
        self.frame = ctk.CTkFrame(master)
        self.callback = callback
        
        self.time_label = ctk.CTkLabel(self.frame, text="Time Range:", font=ctk.CTkFont(size=14))
        self.time_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.time_var = ctk.StringVar(value="Last 24 Hours")
        self.time_menu = ctk.CTkOptionMenu(
            self.frame, 
            values=["Last 24 Hours", "Last Week", "Last Month"], 
            variable=self.time_var, 
            command=self._on_time_change
        )
        self.time_menu.grid(row=0, column=1, padx=10, pady=10)
    
    def get_frame(self) -> ctk.CTkFrame:
        """Get the frame containing the time range selector"""
        return self.frame
    
    def get_time_range(self) -> str:
        """Get the currently selected time range"""
        return self.time_var.get()
    
    def _on_time_change(self, value: str) -> None:
        """Handle time range change event"""
        if self.callback:
            self.callback(value)

class OverviewFrame(ctk.CTkFrame):
    """Main frame for the overview dashboard"""
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        # Initialize data provider
        self.data_provider = MockDataProvider()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(self, text="Overview Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w", columnspan=2)
        
        # Time range selection
        self.time_selector = TimeRangeSelector(self, self._on_time_range_change)
        self.time_selector.get_frame().grid(row=0, column=1, padx=20, pady=(20, 10), sticky="e")
        
        # Time trend plot
        self.time_trend_chart = TimeTrendChart(self, self.data_provider)
        self.time_trend_chart.get_frame().grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Violation types plot
        self.violation_chart = ViolationTypesChart(self, self.data_provider)
        self.violation_chart.get_frame().grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        
        # Summary statistics
        self.summary_stats = SummaryStatsComponent(self, self.data_provider)
        self.summary_stats.get_frame().grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        
        # Initial update of all components
        self._update_all_components()
    
    def _on_time_range_change(self, time_range: str) -> None:
        """Handle time range change event"""
        self._update_all_components()
    
    def _update_all_components(self) -> None:
        """Update all dashboard components"""
        time_range = self.time_selector.get_time_range()
        self.time_trend_chart.update(time_range)
        self.violation_chart.update()
        self.summary_stats.update() 