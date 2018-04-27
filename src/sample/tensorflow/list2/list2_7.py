import numpy as np
import tensorflow as tf

# tf.contrib.learnを用いる

IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"

# Load datasets
training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
    filename = IRIS_TRAINING,
    target_dtype = np.int,
    features_dtype = np.float32
)

test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
    filename = IRIS_TEST,
    target_dtype = np.int,
    features_dtype = np.float32
)

# 特徴を実数値であることを伝える
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]

# 3層DNN
# 指定がない場合、活性化関数は自動的にReLuが選択される
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=3,
                                            model_dir="./iris_model")

# 学習データの入力定義
def get_train_inputs():
    x = tf.constant(training_set.data)
    y = tf.constant(training_set.target)

    return x, y

# テストデータの入力定義
def get_test_inputs():
    x = tf.constant(test_set.data)
    y = tf.constant(test_set.target)

    return x, y

# モデルのフィッティング
classifier.fit(input_fn=get_train_inputs,
               steps=2000)
# 精度評価
print(classifier.evaluate(input_fn=get_test_inputs, steps=1)["accuracy"])
