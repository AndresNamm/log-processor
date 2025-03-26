img = 'all/IMG_0055_00000.png'

import cv2
import numpy as np



#    - If your image is already strictly black/white, this is just to ensure we have a single channel.
img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

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
    print(area)

    # Create a color image to visualize the components
    color_img = np.zeros((binary.shape[0], binary.shape[1], 3), dtype=np.uint8)

    # Assign random colors to each component (except background)
    colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)
    colors[0] = [0, 0, 0]  # Background is black

    # Apply colors to the image based on labels
    for i in range(1, num_labels):
        color_img[labels == i] = colors[i]

    # Draw bounding boxes around each component
    for label_idx in range(1, num_labels):
        # Get bounding box coordinates
        x = stats[label_idx, cv2.CC_STAT_LEFT]
        y = stats[label_idx, cv2.CC_STAT_TOP]
        w = stats[label_idx, cv2.CC_STAT_WIDTH]
        h = stats[label_idx, cv2.CC_STAT_HEIGHT]
        
        # Draw rectangle
        cv2.rectangle(color_img, (x, y), (x + w, y + h), (255, 255, 255), 2)

    # Display the image with colored components and bounding boxes
    cv2.imshow('Connected Components', color_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()