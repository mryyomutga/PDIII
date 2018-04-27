import numpy as np
import tensorflow as tf
import urllib.request

IRIS_TRAINING = "iris_training.csv"
IRIS_TRAINING_URL = "http://download.tensorflow.org/data/iris_training.csv"

IRIS_TEST = "iris_test.csv"
IRIS_TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

with open(IRIS_TRAINING, "wb") as f:
    f.write(urllib.request.urlopen(IRIS_TRAINING_URL).read())

with open(IRIS_TEST, "wb") as f:
    f.write(urllib.request.urlopen(IRIS_TEST_URL).read())

training_data = np.loadtxt("./iris_training.csv", delimiter=",", skiprows=1)
train_x = training_data[:, :-1]
train_y = training_data[:, -1]

test_data = np.loadtxt("./iris_test.csv", delimiter=",", skiprows=1)
test_x = test_data[:, :-1]
test_y = test_data[:, -1]

# 指定されたバッチサイズの数だけランダムに取得
def next_batch(data, label, batch_size):
    indices = np.random.randint(data.shape[0], size=batch_size)
    return data[indices], label[indices]

# Neural Network
# input layer
x = tf.placeholder(tf.float32, [None, 4], name="input")

# hidden layer
hidden1 = tf.layers.dense(inputs=x, units=10, activation=tf.nn.relu, name="hidden1")
# next layer's inputs last layer's output
hidden2 = tf.layers.dense(inputs=hidden1, units=20, activation=tf.nn.relu, name="hidden2")
hidden3 = tf.layers.dense(inputs=hidden2, units=10, activation=tf.nn.relu)

# output layer
y = tf.layers.dense(inputs=hidden3, units=3, activation=tf.nn.softmax, name="output")

# 学習の設定
labels = tf.placeholder(tf.int64, [None], name="teacher")
y_ = tf.one_hot(labels, depth=3, dtype=tf.float32)

# 元データとネットワークの出力比較
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))

# 学習結果の評価
correct_prediction = tf.equal(tf.arg_max(y, 1), tf.arg_max(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Training
train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

batch_size = 20
epoch = 200
batches_in_epoch = training_data.shape[0]

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(epoch):
        for j in range(batches_in_epoch):
            batch_train_x, batch_train_y = next_batch(train_x, train_y, batch_size)
            sess.run(train_op, feed_dict={x:batch_train_x, labels:batch_train_y})
        print(sess.run(accuracy, feed_dict={x:test_x, labels: test_y}))
