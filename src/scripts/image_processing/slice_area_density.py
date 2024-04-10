import numpy as np
import SimpleITK as sitk
from scripts.image_processing.image_window import get_image_path_by_id

def get_l3_slice_area(patient_id,l3_slice,seg_dir):
       
    seg_path = get_image_path_by_id(patient_id,seg_dir)
    seg_sitk =  sitk.ReadImage(seg_path)
    seg_array  = sitk.GetArrayFromImage(seg_sitk)[l3_slice,:,:]
    area_per_pixel =  seg_sitk.GetSpacing()[0]*seg_sitk.GetSpacing()[1]

    muscle_seg = (seg_array==1)*1.0
    sfat_seg  = (seg_array==2)*1.0
    vfat_seg  = (seg_array==3)*1.0
    
    muscle_area = np.sum(muscle_seg)*area_per_pixel/100
    sfat_area = np.sum(sfat_seg)*area_per_pixel/100
    vfat_area = np.sum(vfat_seg)*area_per_pixel/100    
   
    return [muscle_area,sfat_area,vfat_area]

def get_l3_slice_density(patient_id,l3_slice,seg_dir,img_dir):
    
    image_path = get_image_path_by_id(patient_id,img_dir)
    image_sitk =  sitk.ReadImage(image_path)
    l3_array = sitk.GetArrayFromImage(image_sitk)[l3_slice,:,:]
    
    seg_path = get_image_path_by_id(patient_id,seg_dir)
    seg_sitk =  sitk.ReadImage(seg_path)
    seg_array  = sitk.GetArrayFromImage(seg_sitk)[l3_slice,:,:]

    muscle_seg = (seg_array==1)*1.0
    sfat_seg  = (seg_array==2)*1.0
    vfat_seg  = (seg_array==3)*1.0
    
    muscle_hu = np.sum(muscle_seg*l3_array)/np.sum(muscle_seg)
    sfat_hu   =  np.sum(sfat_seg*l3_array)/np.sum(sfat_seg)
    vfat_hu   =  np.sum(vfat_seg*l3_array)/np.sum(vfat_seg)
    
    return [muscle_hu,sfat_hu,vfat_hu]