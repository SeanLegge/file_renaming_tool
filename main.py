import os
import shutil

from folder_utilites import get_target_folder_path,get_rename_list_path
from media_utilities import scrape_main_wiki_page,scrape_episode_page,scrape_table_for_row_data,scrape_single_row_for_data
from file_utilities import rename_file,search_file_name,find_season_number,find_episode_number
    

def main(): 
    target_path = None
    rename_path = None
    
    while target_path is None:
        target_path = get_target_folder_path()
        
    folder_name = os.path.basename(target_path)
    
    file_list = search_file_name(target_path, folder_name)
    
    for file in file_list:
        
        
        season_number = find_season_number(file)
        
        if season_number is None:
            print(f"Skipping file {file} as season number is not found.")
            continue
        
        if season_number.isnumeric():
                      
            episode_number = find_episode_number(file)        
            
            returned_table = scrape_episode_page(scrape_main_wiki_page(folder_name), season_number)            
            print(f"Scraping episode {episode_number} from season {season_number} of {folder_name}")
            returned_row = scrape_table_for_row_data(str(returned_table), episode_number)
            
            episode_name = scrape_single_row_for_data(str(returned_row))
            
            if '>' in str(episode_name):            
                formatted_string = str(episode_name).split('>', 1)[1]
                formatted_string = formatted_string.split('<br/>', 1)[0]
                formatted_string = formatted_string.strip('"')
                                                    
        elif not season_number.isnumeric():
            print(f"Skipping file {file} as season number is not numeric.")
            continue
        
        if int(season_number) < 10:    
            season_number = "0" + str(season_number)

        if int(episode_number) < 10:
            episode_number = "0" + str(episode_number)        
            
        final_formatted_string = folder_name + " - S" + str(season_number) + "E" + str(episode_number) + " - " + formatted_string
            
        file_extension = os.path.splitext(file)[1]
        full_rename_path = os.path.join(target_path, file)
        new_path = os.path.join(target_path, final_formatted_string + file_extension)
        try:
            shutil.move(full_rename_path, new_path)
            print(f"{file} renamed to {final_formatted_string}")
        except Exception as e:
            print(f"Error moving file {file}: {e}")
    
        
    
if __name__ == "__main__":
    main()
