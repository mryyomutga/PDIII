import numpy as np
import os
import tensorflow as tf
import PIL.Image as Image

from object_detection.utils import label_map_util, visualization_utils

# モデル・テストデータのファイルパス
PATH_TO_LABELS = os.path.join("object_detection", "data", "mscoco_label_map.pbtxt")
NUM_CLASSES = 90
PATH_TO_IMAGE_DIR = "test_images"
TEST_IMAGE_PATHS = [os.path.join("object_detection", "test_images", "image{}.jpg".format(i)) for i in range(1, 4)]
MODEL_NAME = "ssd_inception_v2_coco_11_06_2017"
PATH_TO_CKPT = os.path.join("./tmp/object_detection", MODEL_NAME, "frozen_inference_graph.pb")

def main(argv=None):
    # 物体識別に用いるカテゴリ・ラベル名の対応辞書
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map,
        max_num_classes=NUM_CLASSES,
        use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # モデル定義ファイルからグラフを復元
    graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, "rb") as f:
        graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name="")

    # 入力画像
    jpeg = tf.placeholder(tf.string)
    decode = tf.image.decode_jpeg(jpeg)

    with tf.Session() as sess:
        graph = tf.get_default_graph()
        for image_path in TEST_IMAGE_PATHS:
            # 画像データの取得
            with tf.gfile.GFile(image_path, "rb") as f:
                data = f.read()
            image = sess.run(decode, feed_dict={jpeg: data})
            # 出力
            image_tensor = graph.get_tensor_by_name("image_tensor:0")
            boxes = graph.get_tensor_by_name("detection_boxes:0")
            scores = graph.get_tensor_by_name("detection_scores:0")
            classes = graph.get_tensor_by_name("detection_classes:0")
            num_detections = graph.get_tensor_by_name("num_detections:0")

            # 画像を入力して計算結果を取得する
            boxes, scores, classes, num_detections = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: np.expand_dims(image, axis=0)}
            )

            # 結果を用いて可視化
            visualization_utils.visualize_boxes_and_labels_on_image_array(
                image,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True
            )
            Image.fromarray(image).show()

if __name__ == "__main__":
    tf.app.run()
