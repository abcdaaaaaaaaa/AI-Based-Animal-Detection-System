import os

# Define the range of subfolder names
start_range = 12659
end_range = 12721

# Get the current working directory
current_dir = os.getcwd()

# Process each subfolder in the specified range
for i in range(start_range, end_range + 1):
    subfolder_path = os.path.join(current_dir, str(i))  # Ensure full path
    
    # Check if the subfolder exists
    if os.path.exists(subfolder_path):
        # Get all files in the subfolder
        files = os.listdir(subfolder_path)
        
        # Rename and move each file to the main folder
        for filename in files:
            original_file_path = os.path.join(subfolder_path, filename)
            new_file_name = f"{i}{os.path.splitext(filename)[0]}{os.path.splitext(filename)[1]}"
            new_file_path = os.path.join(current_dir, new_file_name)  # Move to the main folder
            
            # Debugging output to check file paths
            print(f"Renaming and moving: {original_file_path} to {new_file_path}")
            
            # Rename and move the file to the main folder
            try:
                os.rename(original_file_path, new_file_path)
                print(f"{original_file_path} renamed and moved to {new_file_name}")
            except Exception as e:
                print(f"Error renaming and moving file: {e}")

print("Process completed.")
