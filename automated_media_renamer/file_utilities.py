import os
import re 
import sys 

def search_file_name(parent_folder, search_term):
    '''
        Search for a file name in the target folder.
    '''
    matching_files = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if search_term in file:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, parent_folder)
                matching_files.append(relative_path)        
                
     # Sort the matching files in alphabetical order
    matching_files.sort()                            
    return matching_files

def find_season_number(file_name):
    '''
        Find the season and episode number in a file name.
    '''
    season = None    
    
    # Split the file name into parts
    parts = file_name.split(" ")    
    
    # Look for the season number
    for part in parts:
        print(part)
        if part.isdigit():
            season = part
            break

    # Check if season contains any variations of 'E' and remove all values after that
    if season:
        season = re.split(r'[eE]', season)[0]
        
    return season

def find_episode_number(file_name, custom_format):    
    '''
        Searches `input_string` for a pattern like s01e01, s1 - e1, etc.
        Returns a tuple (season, episode) if found, otherwise None.
    '''
    # Explanation of the regex:
    #  1) s(\d{1,2})        -> 's' or 'S', capturing 1-2 digits (season)
    #  2) \s*(?:-\s*)?      -> optional dash and any spaces, e.g. " - " or none
    #  3) e(\d{1,2})        -> 'e' or 'E', capturing 1-2 digits (episode)
    # pattern = re.compile(r"s(\d{1,2})\s*(?:-\s*)?e(\d{1,2})", re.IGNORECASE)
    pattern = re.compile(r"s(\d{1,3})\s*(?:-\s*)?(?:e)?(\d{1,3})", re.IGNORECASE)
    
    if custom_format:    
            num_numerical_chars = sum(c.isdigit() for c in custom_format)                       
            pre_custom_format = re.split(r'\d', custom_format, 1)[0]
            post_custom_format = re.split(r'\d', custom_format)[-1]        
            custom_format = f'{pre_custom_format}[0-9]{{{num_numerical_chars}}}{post_custom_format}'                                            
            pattern = re.compile(custom_format)
                
    
    match = pattern.search(file_name)
    if match:    
        if custom_format:            
            episode_str = re.sub(re.escape(pre_custom_format), '', match.group(0))
            episode_str = re.sub(re.escape(post_custom_format), '', episode_str)
        else:
            episode_str = match.group(2)
               
        
        # Convert to integers if you like, or keep them as strings        
        episode = int(episode_str)    

        return (episode)
    else:
        return None


def rename_file(target, new_name):
    '''
        Rename a file to a new name.
    '''
    try:
        os.rename(target, new_name)
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False
    
def remove_invalid_characters(filename):
    # Define a regex pattern for invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    # Remove invalid characters
    sanitized_filename = re.sub(invalid_chars, '', filename)
    return sanitized_filename