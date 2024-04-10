import datetime
import json
import os
import numpy as np
import pandas as pd

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard, LearningRateScheduler, ModelCheckpoint
from tensorflow.keras.utils import multi_gpu_model
from tensorflow.keras.models import model_from_json
import tensorflow as tf

from scripts.generators import SliceSelectionSequence
from scripts.densenet_regression import DenseNet


def train(data_dir, model_dir, epochs=100, name=None, batch_size=16,
          load_weights=None, gpus=1, learning_rate=0.1, threshold=10.0,
          nb_layers_per_block=4, nb_blocks=4, nb_initial_filters=16,
          growth_rate=12, compression_rate=0.5, activation='relu',
          initializer='glorot_uniform', batch_norm=True, wandb_callback=True):

    args = locals()

    # Set up dataset
    train_image_dir = os.path.join(data_dir, 'selection_npy/train')
    val_image_dir = os.path.join(data_dir, 'selection_npy/val')
    train_meta_file = os.path.join(data_dir, 'selection_meta/train.csv')
    val_meta_file = os.path.join(data_dir, 'selection_meta/val.csv')
    train_labels = pd.read_csv(train_meta_file)['ZOffset'].values
    val_labels = pd.read_csv(val_meta_file)['ZOffset'].values
    print('\n\n\n','train_labels.shape:',train_labels.shape,'tuning_labels.shape:', val_labels.shape,'\n\n\n')
    train_jitter = 1000  # default 1000 times of image augmentation for each epoch
    val_jitter = 50  # default 50 times of image augmentation for each epoch

    train_generator = SliceSelectionSequence(
        train_labels, train_image_dir, batch_size, train_jitter, jitter=True, sigmoid_scale=threshold
    )
    val_generator = SliceSelectionSequence(
        val_labels, val_image_dir, batch_size, val_jitter, sigmoid_scale=threshold
    )

    # Directories and files to use
    if name is None:
        name = 'untitled_model_' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    output_dir = os.path.join(model_dir,'train/densenet_models', name)
    tflow_dir = os.path.join(output_dir, 'tensorboard_log')
    weights_path = os.path.join(output_dir, 'weights-{epoch:02d}-{val_loss:.4f}.hdf5')
    architecture_path = os.path.join(output_dir, 'architecture.json')
    tensorboard = TensorBoard(log_dir=tflow_dir, histogram_freq=0, write_graph=False, write_images=False)

    with tf.device('/cpu:0'):
        model = DenseNet(
            img_dim=(256, 256, 1),
            nb_layers_per_block=nb_layers_per_block,
            nb_dense_block=nb_blocks,
            growth_rate=growth_rate,
            nb_initial_filters=nb_initial_filters,
            compression_rate=compression_rate,
            sigmoid_output_activation=True,
            activation_type=activation,
            initializer=initializer,
            output_dimension=1,
            batch_norm=batch_norm
        )
    if load_weights is None:
        os.mkdir(output_dir)
        os.mkdir(tflow_dir)

        args_path = os.path.join(output_dir, 'args.json')
        with open(args_path, 'w') as json_file:
            json.dump(args, json_file, indent=4)

        # Create the model
        print('Compiling model')
    # Save the architecture
        with open(architecture_path, 'w') as json_file:
            json_file.write(model.to_json())

    else:
        # Load the weights
        model.load_weights(load_weights)

    # Move to multi GPUs
    # Use multiple devices
    if gpus > 1:
        parallel_model = multi_gpu_model(model, gpus)
        keras_model_checkpoint = MultiGPUModelCheckpoint(weights_path, monitor='val_loss', save_best_only=False)
    else:
        parallel_model = model
        keras_model_checkpoint = ModelCheckpoint(weights_path, monitor='val_loss', save_best_only=False)

    # Set up the learning rate scheduler
    def lr_func(e):
        print("Learning Rate Update at Epoch", e)
        if e > 0.75 * epochs:
            return 0.01 * learning_rate
        elif e > 0.5 * epochs:
            return 0.1 * learning_rate
        else:
            return learning_rate

    lr_scheduler = LearningRateScheduler(lr_func)
 
    model_callbacks = [keras_model_checkpoint, tensorboard, lr_scheduler]

    # Compile multi-gpu model
    loss = 'mean_absolute_error'
    parallel_model.compile(optimizer=Adam(lr=learning_rate), loss=loss)
    print('Starting training...')
    parallel_model.fit_generator(train_generator, epochs=epochs,
                                 shuffle=False, validation_data=val_generator,
                                 callbacks=model_callbacks,
                                 use_multiprocessing=True,
                                 workers=16)
    return model

