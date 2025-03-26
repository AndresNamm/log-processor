# ASSUMPTIONS 

The input files are places in folder segmentations/ where each original image file has separate folder for it with individual log segmentation masks. 

# PROCESSING GUIDANCE

0. run get_img_sizes.py to get the image sizes histogram
1. run connected_component_show.py with some segmentation file to see all segmentations masks with boxes
2. run analyze_get_component_size_percentiles.ipynb to see the histogram of how large in terms of % each segmentation mask is 
3. run filter_multiple_instances.py to extract instance files with multiple segments to folder withproblems
4. run transform_connected_components.py to make each file only have 1 connected component smoothened out. 
5. run merge_components.py to join segmentation instances of the same instances.
6. run get_boxes.py to calculate surrounding boxes fore 
