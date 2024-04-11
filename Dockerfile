# Specify the base image for the environment
# FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel

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

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget && \
    rm -rf /var/lib/apt/lists/*

# Download and install Python 3.7.4
RUN wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz && \
    tar xzf Python-3.7.4.tgz && \
    cd Python-3.7.4 && \
    ./configure && \
    make && \
    make install

# Cleanup
RUN rm -rf /Python-3.7.4 /Python-3.7.4.tgz

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