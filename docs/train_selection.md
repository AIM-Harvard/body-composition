
## Slice Selection Model - DenseNet (2D)

#### Preparing Training Data


The training data for the slice selection model consists of CT slices, with a physical offset from the levels of L3 Top slice.  To allow for efficient and precise loading during training, slices of input CT scans should be extracted out into numpy array (`.npy`) format. The spacings of the input CT could be different, but the horizontal size should be 512 * 512.

Each `.npy` array should have pixel values between 0 and 255 as a result of intensity clipping and rescaling the raw Hounsfield units. For example, raw pixel values below -160HU are transformed to a pixel value of 0, raw pixel values above 240HU are transformed to 255, and raw pixel vales between -160HU and 240HU should be transformed into a value between 0 and 255 (inclusive) with linear scaling.

#### Scripts to generate the npy files along its annotations are listed [here](../data/data_in_NIFTI/scipts_nifty_to_npy_transformation/NIFTI_to_npy_for_selection_training.ipynb). Example CSV for training is listed [here](../data/train/train_selection/selection_meta/train.csv).

The extracted numpy arrays should be divided into train and validation splits and placed in a directory according to the split. Each split should be accompanied by a CSV file that contains the offset from the level of L3 top slice. Train.csv and Tune.csv should consists of two columns like this:
```
index,   npy_file_name,      ZOffset_L3
0,       000000.npy,    -234.6
1,       000001.npy,    5.2
2,       000002.npy,    145.3  
```

The first column, `npy_file_name`, represents sorted file names in the `.npy` format. The order of npy_name should be the same as the order stored in each directory of the data folder. The second column, `ZOffset_L3`, should represent its offset above or below the level of interest in mm in the physical space of the scanner. Slices above L3 top slice (closer to the head) should be given positive offsets, and slices below L3 top slice (closer to the feet) should be given negative offsets.



The files described above should be placed within a directory with the following structure:
```
- data/train/train_selection/

|- selection_meta/
|  |- train.csv
|  |- val.csv

|- selection_npy/
|  |- train/
|  |  |- 000000.npy
|  |  |- 000001.npy
|  |  |- 00000n.npy (n>=2)

|  |- val/
|  |  |- 000000.npy
|  |  |- 000001.npy
|  |  |- 00000n.npy (n>=2)



```


#### Training the Model

The script `train_slice_selection.py` in the `src` directory is used to train the slice selection model. 

```bash
$ python train_slice_selection.py 
```

A number of optional arguments may be passed to control various aspects of the model architecture and training process. Of particular note are:

* `-d` - Directory in which the training data arrays are stored
* `-m` - Directory in which trained models are to be stored
* `-g` - Specify the number of GPUs to use for training
* `-l` - Specify the initial learning rate
* `-b` - Specify the batch size


Run the help for a full list of options:

```bash
$ python train_slice_selection.py --help
```
