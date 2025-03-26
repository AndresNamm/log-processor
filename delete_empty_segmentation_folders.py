import os

segmentation_files = []
segmentation_dir = 'segmentations'

for root, dirs, files in os.walk(segmentation_dir):
    for file in files:
        segmentation_files.append(os.path.join(root, file))


# if the folder is empty, delete it
for root, dirs, files in os.walk(segmentation_dir):

    if not files and not dirs:
        print(f"Empty folder: {root}")
        os.rmdir(root)
        print(f"Deleted empty folder: {root}")
    else:
        print(f"Folder not empty: {root}")