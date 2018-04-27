import tensorflow as tf

def inference(inputs, reuse=False):
    """
    入力の推論結果を返す
    Args:
        inputs: [batch_size, height, width, channels]のTensor
        reuse : 変数を再利用するか
    Returns:
        推論結果の[batch_size, 47]のtensor
    """
    
    # 畳み込み&プーリング層
    with tf.variable_scope("conv1", reuse=reuse):
        weight1 = tf.get_variable(
            "w", [3, 3, 1, 16],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        bias1 = tf.get_variable(
            "b", shape=[16],
            initializer=tf.zeros_initializer()
        )
        conv1 = tf.nn.conv2d(inputs, weight1, [1, 2, 2, 1], "VALID")
        out1 = tf.nn.relu(tf.add(conv1, bias1))
    pool1 = tf.nn.max_pool(out1, [1, 2, 2, 1], [1, 2, 2, 1], "VALID")

    with tf.variable_scope("conv2", reuse=reuse):
        weight2 = tf.get_variable(
            "w", [3, 3, 16, 24],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        bias2 = tf.get_variable(
            "b", shape=[24],
            initializer=tf.zeros_initializer()
        )
        conv2 = tf.nn.conv2d(pool1, weight2, [1, 1, 1, 1], "VALID")
        out2 = tf.nn.relu(tf.add(conv2, bias2))
    pool2 = tf.nn.max_pool(out2, [1, 2, 2, 1], [1, 2, 2, 1], "VALID")

    with tf.variable_scope("conv3", reuse=reuse):
        weight3 = tf.get_variable(
            "w", [3, 3, 24, 36],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        bias3 = tf.get_variable(
            "b", shape=[36],
            initializer=tf.zeros_initializer()
        )
        conv3 = tf.nn.conv2d(pool2, weight3, [1, 1, 1, 1], "VALID")
        out3 = tf.nn.relu(tf.add(conv3, bias3))
    pool3 = tf.nn.max_pool(out3, [1, 2, 2, 1], [1, 2, 2, 1], "VALID")

    # 全結合
    reshape = tf.reshape(pool3, [pool3.get_shape()[0].value, -1])
    with tf.variable_scope("fully_connect", reuse=reuse):
        weight4 = tf.get_variable(
            "w", [5 * 5 * 36, 47],
            initializer=tf.truncated_normal_initializer(stddev=0.01)
        )
        bias4 = tf.get_variable(
            "b", shape=[47],
            initializer=tf.zeros_initializer()
        )
        out4 = tf.add(tf.matmul(reshape, weight4), bias4)
    return out4