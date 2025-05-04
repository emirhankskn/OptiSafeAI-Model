import os
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk

from frames.overview import OverviewFrame
from frames.camera import CameraFrame
from frames.admin import AdminFrame
from frames.license import LicenseFrame
from frames.info import InfoFrame
from frames.settings import SettingsFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NavigationButton:
    """Button class for sidebar navigation with consistent styling and behavior."""
    
    def __init__(self, parent, icon_path, text, command, row):
        self.parent = parent
        self.icon = None
        self.icon_path = icon_path
        self.text = text
        self.command = command
        self.row = row
        self.button = self._create_button()
        
    def _create_button(self):
        """Create and configure the button with standard styling."""
        button = ctk.CTkButton(
            self.parent,
            corner_radius=0,
            height=40,
            text=self.text,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=None,  # Will be set later
            compound="left",
            anchor="w",
            command=self.command
        )
        button.grid(row=self.row, column=0, sticky="ew", padx=5)
        return button
    
    def set_icon(self, icon):
        """Set the button's icon."""
        self.icon = icon
        self.button.configure(image=self.icon)
        
    def select(self, is_selected=True):
        """Update the button's appearance based on selection state."""
        self.button.configure(fg_color=("gray75", "gray25") if is_selected else "transparent")
    
    def configure_for_expanded(self):
        """Configure the button for expanded sidebar mode."""
        self.button.configure(
            text=self.text,
            image=self.icon,
            compound="left",
            anchor="w",
            padx=20
        )
    
    def configure_for_collapsed(self):
        """Configure the button for collapsed sidebar mode."""
        self.button.configure(
            text="",
            image=self.icon,
            compound="center",
            padx=10
        )


class NavigationManager:
    """Manages navigation components and state."""
    
    def __init__(self, parent, toggle_callback):
        self.parent = parent
        self.toggle_callback = toggle_callback
        self.is_expanded = True
        self.width_expanded = 200
        self.width_collapsed = 35
        
        self.frame = ctk.CTkFrame(parent, corner_radius=0, width=self.width_expanded)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_propagate(False)
        self.frame.grid_rowconfigure(8, weight=1)
        
        self.logo_label = ctk.CTkLabel(
            self.frame,
            text="SafetyAI",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.buttons = {}
        self.current_selected = None
        
        self.toggle_button_frame = ctk.CTkFrame(
            parent,
            width=26,
            height=26,
            corner_radius=13,
            fg_color=("gray75", "gray25")
        )
        
        self.toggle_button = ctk.CTkButton(
            self.toggle_button_frame,
            width=26,
            height=26,
            corner_radius=13,
            text=">",
            fg_color=("gray75", "gray25"),
            hover_color=("gray70", "gray30"),
            border_width=0,
            command=self.toggle
        )
        self.toggle_button.place(relx=0.5, rely=0.5, anchor="center")
        
        self.appearance_mode_label = ctk.CTkLabel(
            self.frame,
            text="Appearance Mode:",
            anchor="w"
        )
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.frame,
            values=["Light", "Dark", "System"],
            command=lambda mode: ctk.set_appearance_mode(mode)
        )
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_menu.set("Dark")
    
    def add_button(self, icon_path, text, command, row):
        """Add a navigation button."""
        button = NavigationButton(self.frame, icon_path, text, command, row)
        self.buttons[text.lower()] = button
        return button
    
    def select_item(self, name):
        """Select a navigation item by name."""
        name = name.lower()
        if self.current_selected and self.current_selected in self.buttons:
            self.buttons[self.current_selected].select(False)
        
        if name in self.buttons:
            self.buttons[name].select(True)
            self.current_selected = name
    
    def load_icons(self, icon_size=(20, 20)):
        """Load all navigation icons."""
        for button_name, button in self.buttons.items():
            try:
                icon = self._load_image(button.icon_path, icon_size)
                button.set_icon(icon)
            except Exception as e:
                print(f"Error loading icon {button.icon_path}: {str(e)}")
    
    def _load_image(self, path, size):
        """Load and resize an image for use as an icon."""
        return ctk.CTkImage(
            light_image=Image.open(path),
            dark_image=Image.open(path),
            size=size
        )
    
    def toggle(self):
        """Toggle sidebar between expanded and collapsed states."""
        self.is_expanded = not self.is_expanded
        
        if not self.is_expanded:
            self.frame.configure(width=self.width_collapsed)
            self.toggle_button.configure(text="<")
            
            for button in self.buttons.values():
                button.configure_for_collapsed()
            
            self.logo_label.grid_forget()
            self.appearance_mode_label.grid_forget()
            self.appearance_mode_menu.grid_forget()
        else:
            self.frame.configure(width=self.width_expanded)
            self.toggle_button.configure(text=">")
            
            for button in self.buttons.values():
                button.configure_for_expanded()
            
            self.logo_label.grid(row=0, column=0, padx=20, pady=20)
            self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
            self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=(10, 20))
        
        self.update_toggle_position()
        self.toggle_callback()
    
    def update_toggle_position(self):
        """Update toggle button position to vertical middle of frame."""
        nav_height = self.frame.winfo_height()
        if nav_height > 0:
            vertical_middle = nav_height // 2
            x_pos = self.width_expanded - 13 if self.is_expanded else self.width_collapsed - 13
            self.toggle_button_frame.place(x=x_pos, y=vertical_middle, anchor="e")


class ScreenManager:
    """Manages content screens and their visibility."""
    
    def __init__(self, parent):
        self.parent = parent
        self.screens = {}
        self.current_screen = None
    
    def add_screen(self, name, screen_class):
        """Add a screen to the manager."""
        screen = screen_class(self.parent)
        self.screens[name.lower()] = screen
        return screen
    
    def show_screen(self, name):
        """Show a screen by name and hide others."""
        name = name.lower()
        
        # Hide current screen
        if self.current_screen and self.current_screen in self.screens:
            self.screens[self.current_screen].grid_forget()
        
        # Show requested screen
        if name in self.screens:
            self.screens[name].grid(row=0, column=1, sticky="nsew")
            self.current_screen = name


class App(ctk.CTk):
    """Main application class with improved organization."""
    
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_required_dirs()
        self.setup_layout()
        self.setup_navigation()
        self.setup_screens()
        self.show_default_screen()
        
    def setup_window(self):
        """Configure the application window."""
        self.title("Safety Compliance Monitoring System")
        self.geometry("1280x720")
        self.minsize(1100, 650)
    
    def create_required_dirs(self):
        """Create required directories if they don't exist."""
        for directory in ["Videos", "assets"]:
            if not os.path.exists(directory): os.makedirs(directory)
    
    def setup_layout(self):
        """Configure the grid layout."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def setup_navigation(self):
        """Set up the navigation system."""
        self.nav_manager = NavigationManager(self, self.on_sidebar_toggle)
        
        self.nav_manager.add_button("assets/overview.png", "Overview", lambda: self.navigate_to("overview"), 1)
        self.nav_manager.add_button("assets/camera.png", "Camera", lambda: self.navigate_to("camera"), 2)
        self.nav_manager.add_button("assets/admin.png", "Admin Panel", lambda: self.navigate_to("admin"), 3)
        self.nav_manager.add_button("assets/licence.png", "License", lambda: self.navigate_to("license"), 4)
        self.nav_manager.add_button("assets/info.png", "Info", lambda: self.navigate_to("info"), 5)
        self.nav_manager.add_button("assets/settings.png", "Settings", lambda: self.navigate_to("settings"), 6)
        
        self.nav_manager.load_icons()
        self.bind("<Configure>", lambda e: self.nav_manager.update_toggle_position())
    
    def setup_screens(self):
        """Set up content screens."""
        self.screen_manager = ScreenManager(self)
        
        self.screen_manager.add_screen("overview", OverviewFrame)
        self.screen_manager.add_screen("camera", CameraFrame)
        self.screen_manager.add_screen("admin", AdminFrame)
        self.screen_manager.add_screen("license", LicenseFrame)
        self.screen_manager.add_screen("info", InfoFrame)
        self.screen_manager.add_screen("settings", SettingsFrame)
    
    def show_default_screen(self):
        """Show the default screen on startup."""
        self.navigate_to("overview")
    
    def navigate_to(self, screen_name):
        """Navigate to a specific screen."""
        self.screen_manager.show_screen(screen_name)
        self.nav_manager.select_item(screen_name)
    
    def on_sidebar_toggle(self): pass


if __name__ == "__main__":
    app = App()
    app.mainloop() 