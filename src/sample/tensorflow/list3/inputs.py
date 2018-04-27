import re
import os
import random
import tensorflow as tf

def get_data():
    train, test = [], []
    topdir = os.path.join("images_background_small2", "Japanese_(katakana)")
    regexp = re.compile(r"character(\d+)")
    for dirpath, _, files in os.walk(topdir, followlinks=True):
        match = regexp.search(dirpath)
        if match is None:
            continue
        label = int(match.group(1)) - 1
        data = [(label, os.path.join(dirpath, file)) for file in files]
        random.shuffle(data)
        num_train = int(len(data) * 0.8)
        train += data[:num_train]
        test += data[num_train:]
    return train, test

def train_batch(data_list):
    labels, paths = [], []
    for data in data_list:
        labels.append(data[0])
        paths.append(data[1])
    queue = tf.train.slice_input_producer([labels, paths])
    label = queue[0]
    png = tf.read_file(queue[1])
    image = tf.image.decode_png(png, channels=1)
    image.set_shape([105, 105, 1])
    image = tf.image.per_image_standardization(image)
    return tf.train.shuffle_batch(
        [image, label],
        batch_size=32,
        capacity=len(data_list)*2+3*32,
        min_after_dequeue=len(data_list) * 2
    )

def test_batch(data_list):
    labels, paths = [], []
    for data in data_list:
        labels.append(data[0])
        paths.append(data[1])
    queue = tf.train.slice_input_producer([labels, paths])
    label = queue[0]
    png = tf.read_file(queue[1])
    image = tf.image.decode_png(png, channels=1)
    image.set_shape([105, 105, 1])
    image = tf.image.per_image_standardization(image)
    return tf.train.batch(
        [image, label],
        len(data_list)
    )
    