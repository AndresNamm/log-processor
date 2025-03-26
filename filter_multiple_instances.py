import cv2
import numpy as np
import os
import shutil


def get_percentiles(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

    percentages = []
    for label_idx in range(1, num_labels):  # skip label 0 (background)
        area = stats[label_idx, cv2.CC_STAT_AREA]
        # Calculate the area as a percentage of the total image area
        percentage_area = round((area / (img.shape[0] * img.shape[1])) * 100, 2)
        percentages.append(percentage_area)
    return percentages


folder_path = "all"  # Replace with the actual path to your folder
largest_percentages = []
largest_percentages = []
all_files = os.listdir(folder_path)
all_files_length = len(all_files)
current_largest = 0 
for idx, filename in enumerate(all_files):
    step = max(1, int(all_files_length * 0.05))
    if (idx + 1) % step == 0:
        progress = round(((idx + 1) / all_files_length) * 100, 2)
        print(f"{progress}% processed")
    if filename.endswith(".png") or filename.endswith(".jpg"):  # Check for image files
        img_path = os.path.join(folder_path, filename)
        percentages = get_percentiles(img_path)
        if len(percentages) >= 2:
            second_largest = sorted(percentages, reverse=True)[1]
            largest = max(percentages)
            if largest > current_largest:
                current_largest = largest
                print(f"New largest found: {current_largest} at {filename}")
            if second_largest > 0.02:
            # Define the source and destination paths
                source_path = img_path
                destination_folder = "withproblems"
                # Extract the filename from the source path
                filename = os.path.basename(source_path)
                # Create the full destination path
                destination_path = os.path.join(destination_folder, filename)
                # Copy the file
                try:
                    shutil.copy2(source_path, destination_path)
                    print(f"File '{filename}' copied to '{destination_folder}'")
                except Exception as e:
                    print(f"Error copying file: {e}")

