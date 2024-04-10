## Segmentation Model - UNet (2D)

#### Preparing Training Data

Model training data consists of a set of 2D CT slices and corresponding segmentation masks. Each should be prepared as a numpy array stored in a `.npy` file as follows, and all files should be placed under '../data/train_segmentation'.

`../data/train/train_segmentation/train_images.npy` -- A numpy array of size (*N* x 512 x 512 x 1), where *N* is the number of training samples. This represents all *N* training CT images stacked down the first dimension of the array, and a singleton channel dimension at the end. The pixel intensities should be raw Hounsfield units, without intensity windowing or scaling. The data type should be `float`. These images are used to train the model.

`../data/train/train_segmentation/val_images.npy` -- An array of validation images that are used to monitor the progress of the training process and compare the generalization performance of different models. Its construction is identical to train_images.npy (note that the number of images in the validation will usually different to the
number of images in the training set).

`../data/train/train_segmentation/train_masks.npy` -- An array the same shape as train_images.npy, where all spatial dimensions correspond to the train_images.npy array. Each slice of the masks array is the segmentation mask for the same slice in the images array. The masks should have a `uint8` data type, and each pixel encodes the segmentation label of the corresponding pixel in the image array. A value of 0 denotes the background class, 1 denotes the 'muscle' class, 2 denotes the 'subcutaneous fat' class, and 3 denotes the 'visceral fat' class.

`../data/train/train_segmentation/val_masks.npy` -- Mask array for the validation images in val_images.npy. Construction is otherwise identical to train_masks.npy.

#### Training the Model

The segmentation model is trained with the `train_segmentation.py` script in the `src` directory. 

For example:

```bash
$ python train_segmentation.py -d
```

There are a number of other options you can specify to tweak the model
architecture and training procedure. Of particular note are:

* `-d` -- Directory in which the training data (e.g. `train_images.npy`) arrays are stored.
* `-m` -- The model checkpoints and associated files will be stored in a sub-directory of this directory.
* `-g` - Specify the number of GPUs to use for training
* `-l` - Specify the initial learning rate
* `-b` - Specify the batch size

Run the help for a full list of options:

```bash
$ python train_segmentation.py --help
```


The files described above should be placed within a directory with the following structure:
```
- data/train/train_segmentation/

|- train_images.npy
|- train_masks.npy
|- val_images.npy
|- val_masks.npy
```

