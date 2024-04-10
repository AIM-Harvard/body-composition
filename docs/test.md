
### Model preidiciton of the L3 top slice

The selection model is tested with the `test_selection.py` script in the 'src' directory. The script takes a NIFTI image and output in csv the predicted number of the L3 slice. You can run the basic test routine by passing the two required arguments:

`data_dir` -- Directory in which the test ct images are stored. Default path is '../data/test/input'

`model_dir` -- Directory in which trained model are stored. Default model is 'model/test/L3_Top_Selection_Model_Weight.h5'

For example:
```bash
$ python test_selection.py 
```
#### We can check the selection performance by overlaping the prediction slice into the input CT series, in this [script](../data/test/optional_scripts_for_test_performance_check/selection_check_by_screenshots.ipynb)

### Model segmentaion of the L3 top slice

The segmentation model is tested with the `test_segmentation.py` script in 'src' directory. The script takes a NIFTI image and L3 top slice and output the segmented CT scanin NIFTI format.  You can run the basic test routine by passing required arguments:

`data_dir` -- Directory in which the test ct images, labels and automatic segmentations are stored. Default path is '../data/test/input'

`model_dir` -- Directory in which well-trained model are stored. Default model is 'model/test/L3_Top_Segmentation_Model_Weight.hdf5'


For example:
```bash
$ python test_segmentation.py 
```
#### We can check the segmentation performance by overlaping the model segmentation into the input L3 slice, in this [script](../data/test/optional_scripts_for_test_performance_check/segmentation_check_in_screenshots_L3slice_auto.ipynb)


### Data Structure for testing models
Before test the model you must prepare the data in NIFTI format. The files should be placed within data directory with structure below :

```
- data/

|- test/

|  |- input/
|  |  |- test-volume-11.nii.gz
|  |  |- test-volume-8.nii.gz

|  |- output_segmentation/
|  |  |- test-volume-11_AI_seg_L3.nii.gz
|  |  |- test-volume-8_AI_seg_L3.nii.gz


|  |- output_csv/

|  |  |- L3_Top_Slice_Prediction.csv
|  |  |- L3_body_comp_area_density.csv

```
#### Example Data Source

https://competitions.codalab.org/competitions/17094#learn_the_details-overview

Under licence of https://creativecommons.org/licenses/by-nc-nd/4.0/
