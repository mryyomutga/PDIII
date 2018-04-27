import tensorflow as tf

# Sessionは演算グラフの実行単位
counter = tf.Variable(0)
step_size = tf.constant(1)

increment_op = tf.add(counter, step_size)
count_up_op = tf.assign(counter, increment_op)

print("first session")
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(3):
        print(sess.run(count_up_op))

# 異なるSessionでは演算結果が引き継がれない
print("\nsecond session")
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(5):
        print(sess.run(count_up_op))
