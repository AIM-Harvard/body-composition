import pandas as pd
import os

from scripts.image_processing.image_window import get_image_path_by_id,apply_window
from scripts.image_processing.slice_area_density import get_l3_slice_area,get_l3_slice_density
import SimpleITK as sitk
import numpy as np

csv_path = '/home/taf/Documents/L3_segmentations_final/Final_manual_segmentations/out_niftis.csv'
df_l3_prediction = pd.read_csv(csv_path, index_col = 0)

print(df_l3_prediction.shape)
(df_l3_prediction.head())

df_init = pd.DataFrame()
img_dir  = '/home/taf/Documents/NIFTIs'
seg_dir = '/home/taf/Documents/L3_segmentations_final/Final_manual_segmentations/'
csv_write_path = '/home/taf/Documents/L3_segmentations_final/Final_manual_segmentations/L3_body_comp_area_density.csv'

for idx,rows in df_l3_prediction.iterrows():
    patient_id =  rows['patient_id']
    image_path =  get_image_path_by_id(patient_id, img_dir)
    seg_path = get_image_path_by_id(patient_id, seg_dir)
    
    if os.path.exists(image_path) and os.path.exists(seg_path):
        l3_slice = int(rows['L3_Predict_slice'])

        muscle_auto_area,sfat_auto_area,vfat_auto_area = \
                            get_l3_slice_area(patient_id,l3_slice,seg_dir)  

        muscle_auto_density,sfat_auto_density,vfat_auto_density = \
                            get_l3_slice_density(patient_id,l3_slice,seg_dir,img_dir)

        round_num = 2
        df_inter = pd.DataFrame({'patient_id':patient_id,
                                    'muscle_manual_area':round(muscle_auto_area, round_num),
                                    'muscle_manual_density':round(muscle_auto_density, round_num),

                                    'sfat_manual_area':round(sfat_auto_area, round_num),
                                    'sfat_manual_density':round(sfat_auto_density, round_num),

                                    'vfat_manual_area':round(vfat_auto_area, round_num),
                                    'vfat_manual_density':round(vfat_auto_density, round_num)},index=[0])

        df_init = df_init.append(df_inter)
        df_init.to_csv(csv_write_path)
        print(idx,'th', patient_id, 'writen to', csv_write_path)
