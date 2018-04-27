import os
import re
import tensorflow as tf

base_dir = "./tmp/imagenet"

def main(argv=None):
    node_lookup = node_dict()
    # モデルファイルからグラフを復元
    with tf.gfile.FastGFile(os.path.join(base_dir, "classify_image_graph_def.pb"), "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name="")

    # 画像データを取得
    image_data = tf.gfile.FastGFile(os.path.join(base_dir, "moon.jpg"), "rb").read()
    with tf.Session() as sess:
        # 最終出力のTensorを取得
        softmax_tensor = sess.graph.get_tensor_by_name("softmax:0")
        # 画像を入力し、計算結果を取得
        predictons = sess.run(tf.squeeze(softmax_tensor), feed_dict={
            "DecodeJpeg/contents:0": image_data
        })
        # スコアの上位3件を取得し、ラベル名を出力
        top_k = predictons.argsort()[-3:][::-1]
        for node_id in top_k:
            human_string = node_lookup[node_id]
            score = predictons[node_id]
            print("{0} (score = {1})".format(human_string, score))

# ラベル定義ファイルから、認識結果のラベル番号とラベル名の対応辞書を生成
def node_dict():
    label_lookup_path = os.path.join(base_dir, "imagenet_2012_challenge_label_map_proto.pbtxt")
    uid_lookup_path = os.path.join(base_dir, "imagenet_synset_to_human_label_map.txt")

    uid_to_human = {}
    p = re.compile(r"[n\d]*[ \S,]*")
    for line in tf.gfile.GFile(uid_lookup_path).readlines():
        parsed_items = p.findall(line)
        uid = parsed_items[0]
        human_string = parsed_items[2]
        uid_to_human[uid] = human_string
    node_id_to_uid = {}
    for line in tf.gfile.GFile(label_lookup_path).readlines():
        if line.startswith("  target_class:"):
            target_class = int(line.split(": ")[1])
        if line.startswith("  target_class_string:"):
            target_class_string = line.split(": ")[1]
            node_id_to_uid[target_class] = target_class_string[1:-2]
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
        name = uid_to_human[val]
        node_id_to_name[key] = name
    return node_id_to_name

if __name__ == "__main__":
    tf.app.run()
