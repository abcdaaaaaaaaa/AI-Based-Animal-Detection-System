import os
import shutil

# Get the current working directory
current_dir = os.getcwd()

# Get a list of all subfolders in the current directory
subfolders = [f for f in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, f))]

# Process each subfolder
for subfolder in subfolders:
    subfolder_path = os.path.join(current_dir, subfolder)  # Ensure full path
    
    # Get all files in the subfolder
    files = os.listdir(subfolder_path)
    
    # Rename and move each file to the main folder
    for filename in files:
        original_file_path = os.path.join(subfolder_path, filename)
        new_file_name = f"{subfolder}{os.path.splitext(filename)[0]}{os.path.splitext(filename)[1]}"
        new_file_path = os.path.join(current_dir, new_file_name)  # Move to the main folder
        
        # Debugging output to check file paths
        print(f"Renaming and moving: {original_file_path} to {new_file_path}")
        
        # Rename and move the file to the main folder
        try:
            os.rename(original_file_path, new_file_path)
            print(f"{original_file_path} renamed and moved to {new_file_name}")
        except Exception as e:
            print(f"Error renaming and moving file: {e}")
    
    # Remove the subfolder after all files have been moved
    try:
        shutil.rmtree(subfolder_path)
        print(f"Subfolder {subfolder_path} deleted.")
    except Exception as e:
        print(f"Error deleting subfolder: {e}")

print("Process completed.")
