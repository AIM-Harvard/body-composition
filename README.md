# Body Composition AIM

This repository is intended for AIM personnel and authorized collaborators only. Don't share without written consent. 

This repository provides code for training and running the body composition pipeline, which consists of two deep learning models. The first model is to localize the L3 slice from the input CT scan. The second model is to segment the localized slice into three components: muscle, subcutaneous fat  and visceral fat.

### Getting Started

See the documentation pages for further details:
* [Env_setup](docs/env_setup.md) - For installing packages directly on your system
* [Training_1](docs/train_selection.md) - For training a deep learning model for L3 slice selection
* [Training_2](docs/train_segmentation.md) - For training a deep learning model for segmentation
* [Inference](docs/test.md) - For running the model on new CT scans

## Repository Structure

The LiverSeg repository is structured as follows:

* All the source code to run the liver segmentation model is found under the `src` folder.
* Three example CT images, the corresponding manual segmentation masks, and optional data curation scripts are stored under the `data` folder.
* Model weights for pre-trained/trained models are saved in `model` folder.

### Reference

This repository is modified after the following work under [GPL 3.0 License](LICENSE):

https://github.com/CPBridge/ct_body_composition
