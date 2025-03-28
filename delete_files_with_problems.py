import os
import sys

def delete_matching_files(withproblems_dir, segmentations_dir):
    """
    Delete files from segmentations_dir that also exist in withproblems_dir,
    maintaining the same directory structure.
    """
    deleted_count = 0
    
    # Walk through all directories and files in withproblems_dir
    for root, dirs, files in os.walk(withproblems_dir):
        for file in files:
            # Get the relative path from withproblems_dir
            rel_path = os.path.relpath(os.path.join(root, file), withproblems_dir)
            
            # Construct the corresponding path in segmentations_dir
            segmentation_file_path = os.path.join(segmentations_dir, rel_path)
            
            # Check if the file exists in segmentations_dir
            if os.path.exists(segmentation_file_path):
                try:
                    # Delete the file
                    os.remove(segmentation_file_path)
                    print(f"Deleted: {segmentation_file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {segmentation_file_path}: {e}")
    
    print(f"Total files deleted: {deleted_count}")

if __name__ == "__main__":
    # Define the directories
    withproblems_dir = "withproblems"
    segmentations_dir = "segmentations"
    
    # Check if directories exist
    if not os.path.exists(withproblems_dir):
        print(f"Error: {withproblems_dir} directory does not exist.")
        sys.exit(1)
    
    if not os.path.exists(segmentations_dir):
        print(f"Error: {segmentations_dir} directory does not exist.")
        sys.exit(1)
    
    # Confirm with the user before proceeding
    confirmation = input(f"This will delete files from '{segmentations_dir}' if they exist in '{withproblems_dir}'.\nContinue? (y/n): ")
    
    if confirmation.lower() == 'y':
        delete_matching_files(withproblems_dir, segmentations_dir)
    else:
        print("Operation cancelled.")