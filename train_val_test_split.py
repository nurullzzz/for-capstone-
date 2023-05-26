
# Script for Split Dataset to train 80%, validation 10%, test 10%
# Based off code from GitHub user EdjeElectronics: https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/util_scripts/train_val_test_split.py

import glob
from pathlib import Path
import random
import os

# Define paths to image folders
image_folder = '/content/images/all'
train_folder = '/content/images/train'
val_folder = '/content/images/validation'
test_folder = '/content/images/test'

# Get list of all image folders
folder_list = ['baik', 'bangku', 'bel', 'dia', 'meja', 'pramuka', 'sakit', 'saya', 'teman', 'tugas']

# Function to move files to destination folder
def move_files(file_list, dest_folder):
    for file_path in file_list:
        filename = os.path.basename(file_path)
        xml_file = os.path.splitext(filename)[0] + '.xml'
        dest_file_path = os.path.join(dest_folder, filename)
        dest_xml_path = os.path.join(dest_folder, xml_file)
        os.rename(file_path, dest_file_path)
        os.rename(os.path.join(file_path.parent, xml_file), dest_xml_path)

# Iterate through each folder
for folder_name in folder_list:
    # Create destination folders for current folder
    train_folder_path = os.path.join(train_folder, folder_name)
    val_folder_path = os.path.join(val_folder, folder_name)
    test_folder_path = os.path.join(test_folder, folder_name)
    os.makedirs(train_folder_path, exist_ok=True)
    os.makedirs(val_folder_path, exist_ok=True)
    os.makedirs(test_folder_path, exist_ok=True)

    # Get list of image files in current folder
    image_files = list(Path(os.path.join(image_folder, folder_name)).rglob('*.jpg')) + \
                  list(Path(os.path.join(image_folder, folder_name)).rglob('*.JPG')) + \
                  list(Path(os.path.join(image_folder, folder_name)).rglob('*.png')) + \
                  list(Path(os.path.join(image_folder, folder_name)).rglob('*.bmp'))
    random.shuffle(image_files)

    # Determine number of files to move to each folder
    num_files = len(image_files)
    train_num = int(num_files * 0.8)
    val_num = int(num_files * 0.1)
    test_num = num_files - train_num - val_num

    # Move files to train folder
    train_files = image_files[:train_num]
    move_files(train_files, train_folder_path)

    # Move files to validation folder
    val_files = image_files[train_num:train_num+val_num]
    move_files(val_files, val_folder_path)

    # Move files to test folder
    test_files = image_files[train_num+val_num:]
    move_files(test_files, test_folder_path)

    print('Images in folder %s moved to train: %d, validation: %d, test: %d' % (folder_name, train_num, val_num, test_num))
