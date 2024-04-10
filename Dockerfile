# Specify the base image for the environment
# FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
FROM nvidia/cuda:11.4.0-devel-ubuntu20.04

# Authors of the image
LABEL authors="jjohnson78@bwh.harvard.edu"

# Remove any third-party apt sources to avoid issues with expiring keys.
RUN rm -f /etc/apt/sources.list.d/*.list

ARG DEBIAN_FRONTEND=noninteractive

# Install basic system utilities and useful packages
# Install common libraries that are needed by a number of models (e.g., nnUNet, Platipy, ...)
# (merge these in a single RUN command to avoid creating intermediate layers)
RUN apt update && apt install -y --no-install-recommends \
  sudo \
  ffmpeg \
  libsm6 \
  libxext6 \
  xvfb \
  wget \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

# Extra steps for installing Python 3.7
RUN apt update && apt install -y --no-install-recommends \
  build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.7-dev
RUN apt install -y python3-pip
RUN python3.7 -m pip install distutils


# Create a working directory and set it as the working directory
# Also create directories for input and output data (mounting points) in the same RUN to avoid creating intermediate layers
RUN mkdir /app /app/data /app/data/input_data /app/data/output_data
WORKDIR /app

# Install general utilities (specify version if necessary)
RUN python3.7 -m pip install --upgrade pip && pip3 install --no-cache-dir \
  SimpleITK==1.2.4 \
  h5py==2.10.0 \
  keras==2.2.4 \
  pandas==0.24.2 \
  scipy==1.2.1 \
  numpy==1.16.4 \
  scikit-image==0.16.2 \
  protobuf==3.20.* \
  tensorflow-gpu==1.13.1

# COPY requirements.txt requirements.txt
# RUN python3.7 -m pip install -r requirements.txt

# Set PYTHONPATH to the /app folder
ENV PYTHONPATH="/app"

# Copy over the project directory into the image
COPY . .

CMD [ "ls" ]