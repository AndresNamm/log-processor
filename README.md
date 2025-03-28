# ASSUMPTIONS 

The input files are places in folder segmentations/ where each original image file has separate folder for it with individual log segmentation masks. 

# PROCESSING GUIDANCE

0. run analyze_img_sizes.ipynb to get the image sizes histogram
1. run connected_component_show.py with some segmentation file to see all segmentations masks with boxes
2. run analyze_get_component_size_percentiles.ipynb to see the histogram of how large in terms of % each segmentation mask is 
3. run find_multiple_instances.py to extract instance files with multiple segments to folder withproblems. Check the withproblems folder. Remove those files from segmented dataset using  delete_empty_segmentation_folders.py
4. run transform_connected_components.py to have smoothened components with right sizes
5. loop over with ui of the generated files. 
5. run find_repeating_components.py to find segmentation instances of the same instances.
6. run get_boxes.py to calculate surrounding boxes for segmentations
