import os

def list_files_in_withproblems(folder_path):
    """Lists all files in the specified folder."""
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    folder_path = "withproblems"  # Replace with the actual path if needed
    files = list_files_in_withproblems(folder_path)

    folders = []
    for file in files:
        folder=file.split("_")[:-1]
        file="_".join(file.split("_")[-1:])
        folder="_".join(folder)
        file_to_delete = os.path.join("segmentations",folder, file)
        if os.path.exists(file_to_delete):
            print(f"Deleting {file_to_delete}")
            os.remove(file_to_delete)
        else:
            print(f"The file {file_to_delete} does not exist")

