# Body Composition

This repository is intended for AIM personnel and authorized collaborators only. Don't share without written consent.

### Scripts Execution Sequence

1. `src/train_slice_selection.py`  
     - Train a DenseNet deep learning model for slice selection out of an input CT scan. Its horizontal size should be 512 * 512.
     - Input_1: numpy arrays (512 * 512) under the folder of '../data/train_selection/selection_npy'
     - Input_2: CT scans under the folder of '../data/train_selection/selection_csv'
     - [Further details](../docs/train_selection.md)

2. `src/test_selection.py`  or `src/selection_prediction.ipynb`  
     - Input: CT scans under the folder of '../data/test/input'
     - Output: CSV under the folder of '../data/test/output_csv'. 
     - An example of an output CSV could look like this:
      ```
      patient_id,         L3_Predicted_slice     
      000001,             60,    
      000002,             181,   
      000003,             20,    
      ```
     - [Further details](../docs/test.md)

3. `src/train_segmentation.py`  
     - Train a 2D UNet model for segmentating muscle, visceral fat, and subcutaneous fat on a particual slice of the input CT. 
     - Input: numpy arrays under the folder of '../data/train_segmentation' : train_images.npy, train_masks.npy, val_images.npy, val_masks.npy.
     - [Further details](../docs/train_segmentation.md)

4. `src/test_segmentation.py` or `src/segmentation_prediction.ipynb`
     - Output a segmentation in a the format of 3D NIFTI.
     - Input_1: CT scans under the folder of '../data/test/input'
     - Input_2: Prediction of L3 top slice of the CT scan '../data/test/output_csv/L3_Top_Slice_Prediction.csv'. 
     - Output: CT scans the folder of '../data/test/output_segmentation'. 
     - [Further details](../docs/test.md)
