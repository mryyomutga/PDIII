import tensorflow as tf

# 変数(Variable)
counter = tf.Variable(0, name="counter")
step_size = tf.constant(1, name="step_size")

increment_op = tf.add(counter, step_size)
# 演算結果からcounterを更新する
count_up_op = tf.assign(counter, increment_op)

with tf.Session() as sess:
    # Variableを使用するときは初期化する
    sess.run(tf.global_variables_initializer())
    for i in range(3):
        print(sess.run(count_up_op))
