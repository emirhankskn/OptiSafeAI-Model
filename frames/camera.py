import customtkinter as ctk
import datetime

class CameraFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color='transparent')

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky='ew')

        self.title_label = ctk.CTkLabel(self.title_frame, text='Camera Monitoring',
                                        font = ctk.CTkFont(size=24, weight='bold'))
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        self.controls_frame = ctk.CTkFrame(self.title_frame)
        self.controls_frame.grid(row=0, column=1, padx=20, pady=10, sticky='e')

        self.start_button = ctk.CTkButton(self.controls_frame, text='Start Monitoring',
                                          command=self.start_monitoring, fg_color='#2ecc71')
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = ctk.CTkButton(self.controls_frame, text='Stop Monitoring',
                                         command=self.stop_monitoring, fg_color='#e74c3c')
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        self.stop_button.configure(state='disabled')

        self.camera_grid = ctk.CTkFrame(self)
        self.camera_grid.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
        self.camera_grid.grid_columnconfigure((0, 1), weight=1)
        self.camera_grid.grid_rowconfigure((0, 1), weight=1)

        self.CAMERA_WIDTH, self.CAMERA_HEIGHT = 400, 300

        self.camera_feeds = []
        for i in range(4):
            row, col = divmod(i, 2)
            feed_frame = ctk.CTkFrame(self.camera_grid)
            feed_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

            feed_frame.grid_rowconfigure(1, weight=1)
            feed_frame.grid_columnconfigure(0, weight=1)

            camera_label = ctk.CTkLabel(feed_frame, text=f'Camera {i+1}',
                                        font=ctk.CTkFont(size=14, weight='bold'))
            camera_label.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

            video_container = ctk.CTkFrame(feed_frame, width=self.CAMERA_WIDTH, height=self.CAMERA_HEIGHT)
            video_container.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
            video_container.grid_propagate(False)

            feed_label = ctk.CTkLabel(video_container, text='No video feed...')
            feed_label.place(relx=.5, rely=.5, anchor='center')

            status_frame = ctk.CTkFrame(feed_frame, height=30)
            status_frame.grid(row=2, column=0, sticky='ew')

            status_indicator = ctk.CTkFrame(status_frame, width=15, height=15, corner_radius=7, fg_color='gray')
            status_indicator.pack(side='left', padx=10, pady=5)

            status_text = ctk.CTkLabel(status_frame, text='Inactive')
            status_text.pack(side='left', padx=5, pady=5)

            self.camera_feeds.append({
                'frame': feed_frame,
                'container': video_container,
                'label': feed_label,
                'indicator': status_indicator,
                'status': status_text,
                'active': False,
                'video': None,
                'thread': None
            })

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')

        self.log_label = ctk.CTkLabel(self.log_frame, text='Event Log',
                                      font = ctk.CTkFont(size=16, weight='bold'))
        self.log_label.pack(pady=(10, 0))

        self.log_textbox = ctk.CTkTextbox(self.log_frame, wrap='word')
        self.log_textbox.pack(fill='both', expand=True, padx=10, pady=10)

        self.monitoring = False
        self.threads = []

        self.model = None
        self.model_loaded = False
        self.confidence_threshold = 0.5

        self.add_log('System initialized and ready.')
        self.add_log('Waiting for monitoring to start...')

    def add_log(self, message):
        """Add log entry to the log textbox."""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] : {message}\n"
        self.log_textbox.insert('end', log_entry)
        self.log_textbox.see('end')

    def start_monitoring(self):pass
    def stop_monitoring(self):pass