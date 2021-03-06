#!/usr/bin/env python3
import h5py as h5
import numpy as np
import tensorflow as tf
import argparse

#
# This script generates a pack of random input data (.h5) expected by the input tflite model
#
# Basic usage:
#   gen_h5_inputs.py --model <path/to/tflite/model> --num_data <number/of/data>
#   ex: gen_h5_inputs.py --model add.tflite --num_data 3
#   (This will create add.tflite.input.h5 composed of three random inputs in the same directory as the model)
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--num_data', type=int, required=True)
args = parser.parse_args()

model = args.model

num_data = args.num_data

# Build TFLite interpreter. (to get the information of model input)
interpreter = tf.lite.Interpreter(model)
input_details = interpreter.get_input_details()

# Create h5 file
h5_file = h5.File(model + ".input.h5", 'w')
group = h5_file.create_group("value")
group.attrs['desc'] = "Input data for " + model

# Generate random data
for i in range(num_data):
    sample = group.create_group(str(i))
    sample.attrs['desc'] = "Input data " + str(i)

    for j in range(len(input_details)):
        input_detail = input_details[j]
        input_data = np.array(
            np.random.random_sample(input_detail["shape"]), input_detail["dtype"])
        sample.create_dataset(str(j), data=input_data)

h5_file.close()
