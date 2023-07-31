"""
合并两个COCO Keypoints数据集为一个
"""

import json
import os


anno_file_1 = '/home/peter/workspace/scratch/colmap_postprocess/prj4_pallet_16keypoints.json'
anno_file_2 = '/home/peter/workspace/scratch/colmap_postprocess/prj4_pallet_16keypoints.json'
anno_file_target = 'merged_pallet_16keypoints.json'


# 加载两个标注文件
anno_1 = json.loads(open(anno_file_1).read()) 
anno_2 = json.loads(open(anno_file_2).read()) 


# 遍历第二个标注文件的所有 image的id 和 annotation的id，均加上第一个标注的最大id
max_image_id = 0
max_anno_id = 0

# 求最大id
for image in anno_1['images']:
    if image['id'] > max_image_id:
        max_image_id = image['id']

for anno in anno_1['annotations']:
    if anno['id'] > max_anno_id:
        max_anno_id = anno['id']

# 改第二个标注文件的id
for image in anno_2['images']:
    image['id'] = image['id'] + max_image_id + 1
       
for anno in anno_2['annotations']:
    anno['id'] = anno['id'] + max_anno_id + 1
    anno['image_id'] = anno['image_id'] + max_image_id + 1

# 合并字典
anno_1['images'].extend(anno_2['images'])
anno_1['annotations'].extend(anno_2['annotations'])

# 保存文件
with open(anno_file_target, 'w') as f:
    json.dump(anno_1, f)
