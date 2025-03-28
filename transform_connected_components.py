import cv2
import numpy as np
import os

def keep_largest_component(img_path, output_path):
    # 1) Load image in grayscale
    #    - If your image is already strictly black/white, this is just to ensure we have a single channel.
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # 2) Threshold to ensure it’s binary (0 or 255). Adjust threshold if needed.
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # 3) Find connected components
    #    - connectivity=8 means we consider diagonal adjacency as connected.
    #    - labels is an array the same size as the image with integers identifying each component.
    #    - stats contains bounding box info and area for each component.
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

    # 4) Find the label of the largest connected component (ignoring background which is label 0)
    #    - stats[i, cv2.CC_STAT_AREA] is the area (in pixels) of component i.
    largest_label = None
    largest_area = 0
    for label_idx in range(1, num_labels):  # skip label 0 (background)
        area = stats[label_idx, cv2.CC_STAT_AREA]
        if area > largest_area:
            largest_area = area
            largest_label = label_idx

    # 5) Create a mask for only the largest component
    #    - Everything that’s not the largest component will be turned black (0).
    final_mask = np.zeros_like(binary)
    final_mask[labels == largest_label] = 255

    # 6) (Optional) Morphological operations to remove small holes or smooth edges:
    #    - For example, opening to remove small white specks inside black or 
    #      closing to fill small black holes inside white.
    #    - Typically: 
    kernel = np.ones((5,5),np.uint8)  # You can adjust the kernel size
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel) # Closing operation
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)  # Opening operation

    # 7) Save or return the processed mask
    cv2.imwrite(output_path, final_mask)

# Example usage:

segmentation_files = []
segmentation_dir = 'segmentations'

for root, dirs, files in os.walk(segmentation_dir):
    for file in files:
        segmentation_files.append(os.path.join(root, file))

all_files_length =  len(segmentation_files)
result_path = "transformed"


for idx, file_path in enumerate(segmentation_files):
    step = max(1, int(all_files_length * 0.05))
    if (idx + 1) % step == 0:
        progress = round(((idx + 1) / all_files_length) * 100, 2)
        print(f"{progress}% processed")
    if file_path.endswith(".png") or file_path.endswith(".jpg"):  # Check for image files
        img_path = os.path.join(file_path)
        file_name = os.path.basename(file_path)
        file_parent_dir = os.path.dirname(file_path)
        file_parent_dir_name = os.path.basename(file_parent_dir)

        output_dir = os.path.join(result_path, file_parent_dir_name)
        os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(result_path, file_name)
        output_path = os.path.join(output_dir, file_name)


        keep_largest_component(img_path, output_path)

