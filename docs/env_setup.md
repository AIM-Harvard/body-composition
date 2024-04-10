### Set-up 
The code was developed and tested with python 3.7.3 on Ubuntu 18.04 with CUDA 10.0 and cuDNN 7.4.2

For the code to run as intended, all the packages under `requirements.txt` should be installed. In order not to break previous installation, it's highly recommend to create a virtual environment to install such packages. Here follows an example of set-up by using `conda environment` from the root of the repository:

```
# Create a conda environment with python3.7.3 and activate it:
conda create -n bd python=3.7.3
conda activate bd

# Once the virtualenv is activated, install the dependencies
conda install -c conda-forge tensorflow=1.13
conda install nb_conda_kernels  # if you want to use jupyter notebook
# Once you change directories into the root path of the project
pip3 install -r requirements.txt  

# conda environment is setted up 
## if you want to delete the conda environment, type in: conda remove -n bd --all 
```