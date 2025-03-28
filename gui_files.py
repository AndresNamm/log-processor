import cv2
import glob
import numpy as np
import os

import json

click = None
# Add variables for box drawing


def mouse_callback(event, x, y, flags, param):
    global click, box_start, box_end, drawing_box
    
    # Original point selection
    if event == cv2.EVENT_LBUTTONDOWN:
        click = (x, y, True)
        print(f"Clicked positive at: ({x}, {y})")
    if event == cv2.EVENT_RBUTTONDOWN:
        click = (x, y, False)
        print(f"Clicked negative at: ({x}, {y})")

def main():
    global click, box_mode, box_start, box_end, drawing_box

    confs = json.load(open("conf.json"))

    input_image_directory = confs["input_image_directory"]
    input_image_directory = os.path.normpath(input_image_directory)
    input_image_directory = input_image_directory.rstrip(os.path.sep)
    img_types = confs["img_type"].split(",")
    downscale = 2
    i = 0  # Increase this to skip first i images in the folder

    name = os.path.basename(input_image_directory)


    cv2.namedWindow("display")
    cv2.setMouseCallback("display", mouse_callback)

    filenames = []
    for img_type in img_types:
        filenames.extend(glob.glob(os.path.join(input_image_directory, f"*.{img_type.strip()}")))

    filenames = sorted(filenames)

    print(len(filenames), "files found")

    file_filter = ['IMG_0056', 'IMG_0059', 'IMG_0062', 'IMG_0063', 'IMG_0071']



    filenames = [filename for filename in filenames if any(f in filename for f in file_filter)]

    print(filenames)

    exiting = False
    while True:
        filename = filenames[i]
        imgname_raw = os.path.basename(filename).split(".")[0]
        os.makedirs(os.path.join("segmentations",  imgname_raw), exist_ok=True)
        img = cv2.imread(filename)

        disp_img = cv2.resize(img, None, fx=1/downscale, fy=1/downscale)

        old_mask = None
        save_index = 0
        mask_files = {}  # Dictionary to store individual masks and their file paths
        
        for imgname in glob.glob(os.path.join("segmentations",  imgname_raw, "*")):
            print(f"Loading {imgname}")
            this_mask = cv2.imread(imgname, cv2.IMREAD_GRAYSCALE)
            # Store the individual mask and its file path
            resized_mask = cv2.resize(this_mask, None, fx=1/downscale, fy=1/downscale)
            mask_files[imgname] = resized_mask
            
            if old_mask is None:
                old_mask = this_mask
            else:
                old_mask[this_mask > 0] = 255
            save_index = max(save_index, int(imgname.split(os.sep)[-1].split(".")[0]) + 1)
        
        if old_mask is not None:
            old_mask = cv2.resize(old_mask, None, fx=1/downscale, fy=1/downscale)
        else:
            old_mask = np.zeros((disp_img.shape[0], disp_img.shape[1]), dtype=np.uint8)

        masks = None
        mask = None
        small_mask = None
        sam_index = 0
        sam_mask_amount = 1
        pos_points = []
        neg_points = []

        counter = 0
        
        while True:
            counter += 1
            if counter % 10 == 0:
                print(f"Counter: {counter}")
            # Display the image
            true_disp = disp_img.copy()
            # ADD IMAGE name
            cv2.putText(
                true_disp,
                imgname_raw,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),
                2,
            )


            if old_mask is not None:
                green_overlay = np.zeros_like(true_disp)
                green_overlay[:, :] = [0, 255, 0]
                if np.any(old_mask > 0):
                    true_disp[old_mask > 0] = cv2.addWeighted(true_disp[old_mask > 0], 0.5, green_overlay[old_mask > 0], 0.5, 0)

            if small_mask is not None:
                red_overlay = np.zeros_like(true_disp)
                red_overlay[:, :] = [0, 0, 255]
                if np.any(small_mask > 0):
                    true_disp[small_mask > 0] = cv2.addWeighted(true_disp[small_mask > 0], 0.5, red_overlay[small_mask > 0], 0.5, 0)

            
            cv2.imshow("display", true_disp)
            key = cv2.waitKey(20)
            #print(f"Clicked key: {key}")

            if key == ord("c"):
                break
            if key == ord("q"):
                exiting = True
                break
            if key == ord("r"):
                pos_points = []
                neg_points = []
                masks = None
                mask = None
                small_mask = None
                sam_index = 0
                sam_mask_amount = 1
            if key == ord(" "):
                # TODO: Save current mask
                cv2.imwrite(os.path.join("segmentations", name, imgname_raw, f"{save_index:05d}.png"), mask)
                old_mask[small_mask > 0] = 255
                save_index += 1
                pos_points = []
                neg_points = []
                masks = None
                mask = None
                small_mask = None
                sam_index = 0
                sam_mask_amount = 1
    

            if click is not None:
                x, y, is_pos = click
                click = None
                x *= downscale
                y *= downscale
                if is_pos:
                    pos_points.append([x, y])
                else:
                    # Check if we clicked on a mask to delete it
                    found_file = None
                    for file_path, mask_img in mask_files.items():
                        # Convert coordinates to match the downscaled mask
                        scaled_x, scaled_y = int(x / downscale), int(y / downscale)
                        if 0 <= scaled_y < mask_img.shape[0] and 0 <= scaled_x < mask_img.shape[1]:
                            if mask_img[scaled_y, scaled_x] > 0:
                                found_file = file_path
                                break
                    
                    if found_file:
                        print(f"Deleting mask file: {found_file}")
                        os.remove(found_file)
                        
                        # Reload all masks
                        old_mask = None
                        mask_files = {}
                        for imgname in glob.glob(os.path.join("segmentations", imgname_raw, "*")):
                            this_mask = cv2.imread(imgname, cv2.IMREAD_GRAYSCALE)
                            resized_mask = cv2.resize(this_mask, None, fx=1/downscale, fy=1/downscale)
                            mask_files[imgname] = resized_mask
                            
                            if old_mask is None:
                                old_mask = this_mask.copy()
                            else:
                                old_mask[this_mask > 0] = 255
                        
                        if old_mask is not None:
                            old_mask = cv2.resize(old_mask, None, fx=1/downscale, fy=1/downscale)
                        else:
                            old_mask = np.zeros((disp_img.shape[0], disp_img.shape[1]), dtype=np.uint8)
                    else:
                        neg_points.append([x, y])

        i += 1

        if exiting:
            break


if __name__ == '__main__':
    main()
