import inputs
import cnn
import numpy as np
import tensorflow as tf

def inference(inputs, reuse=False):
    """
    入力を受け取り、推論の結果を返す
    Args:
        inputs:[batch_size, height, width, channels]のTensor
        reuse:変数を再利用するか
    Returns:
        推論結果の[batch_size, 47]のTensor
    """
    # [batch_size, height * width * channels]に変形
    reshaped = tf.reshape(inputs, [inputs.get_shape()[0].value, -1])
    # hidden layer
    with tf.variable_scope("fully_connect1", reuse=reuse):
        weight1 = tf.get_variable(
            "w", [105 * 105, 100],
            initializer=tf.truncated_normal_initializer(stddev=0.01)
        )
        bias1 = tf.get_variable(
            "b", shape=[100],
            initializer=tf.zeros_initializer()
        )
        out1 = tf.nn.relu(tf.add(tf.matmul(reshaped, weight1), bias1))

    # output layer
    with tf.variable_scope("fully_connect2", reuse=reuse):
        weight2 = tf.get_variable(
            "w", [100, 47],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        bias2 = tf.get_variable(
            "b", [47],
            initializer=tf.zeros_initializer()
        )
        out2 = tf.add(tf.matmul(out1, weight2), bias2)

    return out2

def loss(labels, logits):
    """
    推論結果と正解ラベルとの間の誤差を定義
    Args:
        labels:正解ラベルの値を持つ[batch_size]のTensor
        logits:推論結果の[batch_size, 47]のTensor
    Returns:
        誤差を表すTensor
    """
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        labels=labels,
        logits=logits
    )
    return tf.reduce_mean(cross_entropy)

def training(loss):
    """
    学習するためのOperationを返す
    """
    optimizer = tf.train.AdamOptimizer(0.01)
    return optimizer.minimize(loss)

def main():
    # 学習用のimages, labelsのbatchを取得
    train, test = inputs.get_data()
    train_images, train_labels = inputs.train_batch(train)
    # 推論結果、誤差、学習のためのOperationを定義
    train_logits = cnn.inference(train_images)
    losses = loss(train_labels, train_logits)
    train_op = training(losses)

    test_images, test_labels = inputs.test_batch(test)
    test_logits = cnn.inference(test_images, reuse=True)
    correct_prediction = tf.equal(tf.argmax(test_logits, 1), tf.to_int64(test_labels))
    accuracy = tf.reduce_mean(tf.to_float(correct_prediction))

    with tf.Session() as sess:
        # batchからデータを取り出すためのスレッドの準備
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        sess.run(tf.global_variables_initializer())

        # 学習を繰り返す
        for i in range(300):
            _, loss_value, accuracy_value = sess.run([train_op, losses, accuracy])
            print("step {:3d} : {:5f} ({:3f})".format(i + 1, loss_value, accuracy_value * 100.0))

        coord.request_stop()
        coord.join(threads)

if __name__ == "__main__":
    main()
