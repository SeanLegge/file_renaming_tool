import os


def get_target_folder_path():
    target_path = input("Enter the absolute path of the folder you would like to rename the contents of: ").strip()
    
    if not os.path.exists(target_path):
        print(f"Error: {target_path} is not an absolute path. Please use absolute paths only.")
        return None
    if not os.path.isdir(target_path):
        print(f"Error: {target_path} is not a folder. Please point to a valid folder.")
        return None
    
    return target_path


def get_rename_list_path():
    '''
        Take in a path that will contain a comma delimited list of names to rename files to.
    '''
    target_path = input("Enter the absolute path of the file that contains the list of names you would like to rename the contents of the folder to: ").strip()
    
    if not os.path.exists(target_path):
        print(f"Error: {target_path} is not an absolute path. Please use absolute paths only.")
        return None
    if not os.path.isfile(target_path):
        print(f"Error: {target_path} is not a folder. Please point to a valid folder.")
        return None
