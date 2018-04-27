import tensorflow as tf

# テンソルの演算
t1 = tf.constant(1)
t2 = tf.constant(2)

# 0次元のテンソルを計算
add_op = tf.add(t1, t2)
mul_op = tf.multiply(t1, t2)

with tf.Session() as sess:
    print(sess.run(add_op))
    print(sess.run(mul_op))
