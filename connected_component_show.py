

import cv2
import numpy as np


img = "segmentations\\IMG_0071\\00014.png"
#    - If your image is already strictly black/white, this is just to ensure we have a single channel.
img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

# 2) Threshold to ensure it’s binary (0 or 255). Adjust threshold if needed.
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)
colors[0] = [0, 0, 0]  # Background is black

color_img = np.zeros((binary.shape[0], binary.shape[1], 3), dtype=np.uint8)

# Assign colors and draw bounding boxes in a single loop
for label_idx in range(1, num_labels):
    color_img[labels == label_idx] = colors[label_idx]
    
    # Get bounding box coordinates
    x = stats[label_idx, cv2.CC_STAT_LEFT]
    y = stats[label_idx, cv2.CC_STAT_TOP]
    w = max(stats[label_idx, cv2.CC_STAT_WIDTH], 5)
    h = max(stats[label_idx, cv2.CC_STAT_HEIGHT], 5)
    
    # Draw rectangle
    cv2.rectangle(color_img, (x, y), (x + w, y + h), (255, 255, 255), 2)

# Display the image with colored components and bounding boxes
cv2.namedWindow('Connected Components', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Connected Components', color_img.shape[1]//4, color_img.shape[0]//4)
resized = cv2.resize(color_img, (color_img.shape[1], color_img.shape[0]))
cv2.imshow('Connected Components', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()