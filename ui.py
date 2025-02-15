import customtkinter as ctk
import ui_utilities as ui 
from ui_utilities import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Initialize the main window
app = ctk.CTk()
app.title("Automated Media Renamer")
app.geometry("600x500")

# Configure grid layout
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Add a label
label = ctk.CTkLabel(app, text="Welcome to Automated Media Renamer")
label.grid(row=0, column=0, columnspan=2, pady=20)

# Add an entry widget
entry = ctk.CTkEntry(app, placeholder_text="Enter media name")
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Function to handle browse button click
user_input_target_path = None

# Add button to browse local file system
browse_local_button = ctk.CTkButton(app, text="Browse", command=ui.handle_browse)
browse_local_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Add input field for target website path
label = ctk.CTkLabel(app, text="Optional: Enter target website path")
label.grid(row=2, column=0, columnspan=2, pady=10)

input_optional_target = ctk.CTkEntry(app, placeholder_text="Enter target website path")
input_optional_target.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Add input field for target website path
label = ctk.CTkLabel(app, text="Optional: Alternate season target name. Some shows may not have 'Season' in the name within the site used for scraping.")
label.grid(row=4, column=0, columnspan=2, pady=10)
# Add input field for target website path
input_alternate_season_name = ctk.CTkEntry(app)
input_alternate_season_name.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Add input field for target website path
label = ctk.CTkLabel(app, text="Optional: Format of Episode Number (e.g. _01_ or __01) Default value is s01e01")
label.grid(row=6, column=0, columnspan=2, pady=10)

# Add input field for target website path
input_episode_format = ctk.CTkEntry(app, placeholder_text="(e.g. s01e01")
input_episode_format.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Add checkboxes for title in English or Japanese
label = ctk.CTkLabel(app, text="Select title language")
label.grid(row=8, column=0, columnspan=2, pady=10)

checkbox_var_english = ctk.StringVar(value="off")
checkbox_var_japanese = ctk.StringVar(value="off")

checkbox_english = ctk.CTkCheckBox(app, text="Title in English", variable=checkbox_var_english, onvalue="on", offvalue="off")
checkbox_english.grid(row=9, column=0, padx=10, pady=5, sticky="w")

checkbox_japanese = ctk.CTkCheckBox(app, text="Title in Japanese", variable=checkbox_var_japanese, onvalue="on", offvalue="off")
checkbox_japanese.grid(row=10, column=0, padx=10, pady=5, sticky="w")

# Add a button
button = ctk.CTkButton(app, text="Rename", command=lambda: ui.on_rename_click(input_episode_format.get(),input_alternate_season_name.get()))
button.grid(row=11, column=0, columnspan=2, pady=20)

# Set the entry widget in ui_utilities
ui.set_entry_widget(entry)

# Start the main loop
app.mainloop()