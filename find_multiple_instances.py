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



largest_percentages = []
largest_percentages = []
segmentation_files = []
segmentation_dir = 'segmentations'

for root, dirs, files in os.walk(segmentation_dir):
    for file in files:
        segmentation_files.append(os.path.join(root, file))
all_files_length = len(segmentation_files)

print(all_files_length)

current_largest = 0 
for idx, file_path in enumerate(segmentation_files):
    step = max(1, int(all_files_length * 0.01))
    if (idx + 1) % step == 0:
        progress = round(((idx + 1) / all_files_length) * 100, 2)
        print(f"{progress}% processed")
    if file_path.endswith(".png") or file_path.endswith(".jpg"):  # Check for image files
        img_path = os.path.join(file_path)
        percentages = get_percentiles(img_path)
        if len(percentages) >= 2:
            second_largest = sorted(percentages, reverse=True)[1]
            largest = max(percentages)
            if largest > current_largest:
                current_largest = largest
                print(f"New largest found: {current_largest} at {file_path}")
            if second_largest > 0.02:
                # Define the source and destination paths
                source_path = img_path
                destination_folder = "withproblems"
                
                # Get the relative path structure to maintain directory hierarchy
                rel_path = os.path.relpath(source_path, segmentation_dir)
                destination_path = os.path.join(destination_folder, rel_path)
                
                # Create necessary subdirectories
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                # Copy the file
                try:
                    if not os.path.exists(destination_path):
                        shutil.copy2(source_path, destination_path)
                        print(f"Copied {source_path} to {destination_path}")
                    else:
                        print(f"File already exists: {destination_path}")
                except Exception as e:
                    print(f"Error copying file: {e}")

