import cv2
import numpy as np
import os
import shutil

def calculate_overlap_percentage(img1, img2):
    """
    Calculate the percentage of img1 that is covered by img2, and vice versa.
    Return the maximum of the two overlap percentages.
    Both images should be binary (0 or 255).
    """
    # Find the intersection (where both images have white pixels)
    intersection = cv2.bitwise_and(img1, img2)
    
    # Count white pixels in the intersection and in each of the images
    intersection_area = np.count_nonzero(intersection)
    img1_area = np.count_nonzero(img1)
    img2_area = np.count_nonzero(img2)
    
    # Avoid division by zero
    overlap_percentage1 = (intersection_area / img1_area) * 100 if img1_area > 0 else 0.0
    overlap_percentage2 = (intersection_area / img2_area) * 100 if img2_area > 0 else 0.0
    
    # Return the maximum of the two overlap percentages
    return max(overlap_percentage1, overlap_percentage2)

def find_overlapping_images(segmentation_dir, output_dir, threshold=10.0):
    """
    Check each image in segmentation_dir against previously loaded images within its subdirectory.
    If an image overlaps >threshold% with any other image in the same subdirectory, copy it to output_dir.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    all_subdirs = os.listdir(segmentation_dir)
    # Walk through each subdirectory in the segmentation directory
    total_subdirs = len(all_subdirs)
    for idx, subdir in enumerate(all_subdirs):
        print(f"Processing subdirectory {idx + 1}/{total_subdirs}: {subdir}")
        subdir_path = os.path.join(segmentation_dir, subdir)

        # Check if it's a directory
        if not os.path.isdir(subdir_path):
            continue

        # Collect all image files in the current subdirectory
        image_files = []
        for root, _, files in os.walk(subdir_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    image_files.append(os.path.join(root, file))

        # Load all images from the current subdirectory and store in memory
        loaded_images = []
        for file_path in image_files:
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            loaded_images.append((file_path, binary))

        # Compare each image with all others in the same subdirectory to find overlaps
        total_images = len(loaded_images)
        for i, (current_path, current_img) in enumerate(loaded_images):
            # Print progress
            if (i + 1) % max(1, int(total_images * 0.2)) == 0:
                progress = round(((i + 1) / total_images) * 100, 2)
                print(f"Subdirectory {subdir}: {progress}% compared")

            has_overlap = False

            # Compare with all previously loaded images in the same subdirectory
            for j, (other_path, other_img) in enumerate(loaded_images):
                if i == j:  # Skip comparing with itself
                    continue

                overlap = calculate_overlap_percentage(current_img, other_img)
                if overlap > threshold:
                    has_overlap = True
                    #print(f"Found overlap: {current_path} is covered {overlap:.2f}% by {other_path}")
                    break

            if has_overlap:
                # Copy the file to the output directory with the same subfolder structure
                rel_path = os.path.relpath(current_path, segmentation_dir)
                target_path = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                if not os.path.exists(target_path):
                    shutil.copy2(current_path, target_path)
                #print(f"Copied {current_path} to {target_path}")

if __name__ == "__main__": 
    segmentation_dir = 'segmentations'
    output_dir = 'withproblems'
    overlap_threshold = 10.0  # 10% overlap threshold
    
    find_overlapping_images(segmentation_dir, output_dir, overlap_threshold)
    print("Processing complete. Check the 'withproblems' folder for overlapping images.")
