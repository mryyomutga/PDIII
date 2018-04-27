import tensorflow as tf

# Placeholder(外部からの入力に対応する)
# データ入力時にいろいろな値が入るときはplaceholder
# ニューラルネットワークの重みにはVariable
x = tf.placeholder(tf.int32, name="x")
y = tf.placeholder(tf.int32, name="y")

add_op = tf.add(x, y)
mul_op = tf.multiply(x, y)

with tf.Session() as sess:
    # feed_dictにx=1, y=2を設定する
    print(sess.run(add_op, feed_dict={x:1, y:2}))
    print(sess.run(mul_op, feed_dict={x:1, y:2}))

    print(sess.run(add_op, feed_dict={x:100, y:200}))
    print(sess.run(mul_op, feed_dict={x:100, y:200}))
