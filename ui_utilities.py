import os
import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import messagebox
from folder_utilites import get_target_folder_path,get_rename_list_path
from media_utilities import scrape_main_wiki_page,scrape_episode_page,scrape_table_for_row_data,scrape_single_row_for_data
from file_utilities import rename_file,search_file_name,find_season_number,find_episode_number,remove_invalid_characters
import shutil
from bs4 import BeautifulSoup
import sys

entry = None
user_input_target_path = None

def set_entry_widget(widget):
    global entry
    entry = widget

def browse_files():
    global entry
    folder_path = fd.askdirectory()
    if folder_path and entry is not None:
        entry.delete(0, ctk.END)
        entry.insert(0, folder_path)
    return folder_path

def handle_browse():
    global user_input_target_path
    user_input_target_path = browse_files()
    print(f"Selected folder path: {user_input_target_path}")
    return user_input_target_path

def on_rename_click(episode_format = None, alternate_season_name = None):
    
    response = messagebox.askyesno("Confirm", "Do you wish to continue?")
    if response:        
        
        # Add the code to continue the renaming process here
        folder_name = os.path.basename(user_input_target_path)
        
        if "Season" in folder_name:                
            adjusted_path = os.path.dirname(user_input_target_path)            
            season_number = find_season_number(folder_name)            
            folder_name = os.path.basename(adjusted_path)
            file_list = search_file_name(user_input_target_path, season_number)            
        elif "Season" not in folder_name:
            file_list = search_file_name(user_input_target_path, folder_name)            
                          
        for file in file_list:    

            # Determine if the folder selected is the lowest level folder, if not, get the folder name before going lower
            if season_number is None:
                if os.path.isdir(file):                
                    season_number = os.path.basename(file)
                else:                
                    season_number = find_season_number(file)                    
            
            if season_number.startswith('0'):
                season_number = season_number[1:]
            
            if not isinstance(season_number, str):
                season_number = find_season_number(file)                    
                continue
            
            if season_number is None:
                print(f"Skipping file {file} as season number is not found.")
                continue                                        
            
            if season_number.isnumeric():                              
                episode_number = find_episode_number(file, episode_format)  
                
                if alternate_season_name is not None:
                    season_number = alternate_season_name                                 
                    
                returned_table = scrape_episode_page(scrape_main_wiki_page(folder_name), season_number)                                                               
                returned_row = scrape_table_for_row_data(str(returned_table), episode_number)                
                
                if returned_row is None:
                    print(f"No data found for episode {episode_number}.")
                    break
                                        
                episode_name = scrape_single_row_for_data(str(returned_row))            
                if '>' in str(episode_name):            
                    formatted_string = str(episode_name).split('>', 1)[1]
                    formatted_string = formatted_string.split('<br/>', 1)[0]
                    formatted_string = formatted_string.strip('"')
                    formatted_string = remove_invalid_characters(formatted_string)
                    
                                                        
            elif not season_number.isnumeric():
                print(f"Skipping file {file} as season number is not numeric.")
                continue
            
            
            if isinstance(season_number, str):
                season_number = os.path.basename(user_input_target_path)
                season_number = ''.join(filter(str.isdigit, season_number))            
            
            if int(season_number) < 10:    
                season_number = "0" + str(season_number)

            if int(episode_number) < 10:
                episode_number = "0" + str(episode_number)        
               
             
            final_formatted_string = folder_name + " - S" + str(season_number) + "E" + str(episode_number) + " - " + formatted_string
                
            file_extension = os.path.splitext(file)[1]
            full_rename_path = os.path.join(user_input_target_path, file)
            new_path = os.path.join(user_input_target_path, final_formatted_string + file_extension)
            try:
                shutil.move(full_rename_path, new_path)
                print(f"{file} renamed to {final_formatted_string}")
            except Exception as e:
                print(f"Error moving file {file}: {e}")
    else:
        return False