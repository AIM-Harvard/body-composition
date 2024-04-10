import os
import SimpleITK as sitk
import numpy as np
from scripts.unet import get_unet_2D
from scripts.image_processing.image_window import get_image_path_by_id, remove_arm_area
from scripts.image_processing.get_sitk_from_array import write_sitk_from_array_by_template

import pandas as pd


def test(image_dir, model_weight_path, l3_slice_csv_path, output_dir):
    
    model = get_unet_2D( 4,   (512, 512, 1)    ,num_convs=2,  activation='relu',
            compression_channels=[16, 32, 64, 128, 256, 512],
            decompression_channels=[256, 128, 64, 32, 16]   )
    model.load_weights(model_weight_path)
    
    
    df_prediction_l3 = pd.read_csv(l3_slice_csv_path,index_col=0)
    for idx in  range(df_prediction_l3.shape[0]):
        
        patient_id = str(df_prediction_l3.iloc[idx,0])
        infer_3d_path = output_dir + patient_id + '_AI_seg_L3.nii.gz'

        image_path = get_image_path_by_id(patient_id,image_dir)
        image_sitk =  sitk.ReadImage(image_path)
        image_array_3d  = sitk.GetArrayFromImage(image_sitk)
        im_xy_size = image_array_3d.shape[1]

        l3_slice_auto = int(df_prediction_l3.iloc[idx,1])

        image_array  = sitk.GetArrayFromImage(image_sitk)[l3_slice_auto,:,:].reshape(1,512,512,1) 
        image_array_2d  = sitk.GetArrayFromImage(image_sitk)[l3_slice_auto,:,:]

        target_area = remove_arm_area(image_array_2d)
        infer_seg_array = model.predict(image_array)

        softmax_threshold = 0.5
        muscle_seg = (infer_seg_array[:,:,:,1] >= softmax_threshold) * 1.0 * target_area
        sfat_seg = (infer_seg_array[:,:,:,2] >= softmax_threshold) * 2.0 * target_area
        vfat_seg = (infer_seg_array[:,:,:,3] >= softmax_threshold) * 3.0 * target_area
        infer_seg_array_2d = muscle_seg+sfat_seg+vfat_seg
        infer_seg_array_3d = np.zeros(image_array_3d.shape)
        infer_seg_array_3d[l3_slice_auto,:,:] = infer_seg_array_2d

        write_sitk_from_array_by_template(infer_seg_array_3d, image_sitk, infer_3d_path )

        print(idx,'th image:',patient_id,'(l3_slice_auto:',l3_slice_auto,')  segmentation_in_NIFTI saved into')
        print(infer_3d_path)
        print()
