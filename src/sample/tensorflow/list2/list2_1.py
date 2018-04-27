import tensorflow as tf

# constantは定数定義のAPI
# 単一の数字のテンソル
t1 = tf.constant(1, name="Rank0")
# 配列のテンソル
t2 = tf.constant([1, 2], name="Rank1")
# 多次元配列のテンソル
t3 = tf.constant([[1, 2], [3, 4]], name="Rank2")

with tf.Session() as sess:
    print(sess.run(t1))
    print(sess.run(t2))
    print(sess.run(t3))
