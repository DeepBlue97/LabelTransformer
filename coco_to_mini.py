"""
由于工业领域的深度学习视觉算法应用时，数据集的规模往往没有公开数据集那么大。
为了方便算法效果验证更贴近落地时，并且缩短算法前期验证周期，
故编写以下脚本，来减小公开数据集的规模。

主要思路是：
1. 读取json文件
2. 随机抽取N个Image
3. 删除多余的Annotation
4. 另存为.json文件

其中第3步删除多余的Annotation，或许可省略。
"""

import random
import json

select_num_images = 5000  # 抽取图片数目
src_json = 'person_keypoints_train2017.json'  # 原始文件名
dst_json = 'mini_5000_person_keypoints_train2017.json'  # 保存文件名

with open(src_json, 'r') as large_f:
    full_dict = json.load(large_f)

random_integers = random.sample(range(0, len(full_dict['images'])), select_num_images)

small_images = []
images_mini_ids = set()

for i in random_integers:
    small_images.append(
        full_dict['images'][i]
    )
    images_mini_ids.add(full_dict['images'][i]['id'])

full_dict['images'] = small_images

anns_mini = []
for ann in full_dict['annotations']:
    if ann['image_id'] in images_mini_ids:
        anns_mini.append(ann)

full_dict['annotations'] = anns_mini

with open(dst_json, 'w') as mini_f:
    json.dump(full_dict, mini_f)
