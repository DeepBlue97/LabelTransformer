
import json
import os
import random


anno_file_src = 'merged_pallet_16keypoints.json'
anno_file_train = 'pallet_16keypoints_train.json'
anno_file_test = 'pallet_16keypoints_test.json'

train_ratio = 0.9

anno_test = {}

anno_src = json.loads(open(anno_file_src).read()) 

# 训练集分配图片数
train_image_number = int(len(anno_src['images']) * train_ratio)

# 测试集图片信息
images_test = random.sample(anno_src['images'], len(anno_src['images'])-train_image_number) # test的图片
images_idx_test = set([i['id'] for i in images_test]) # test的图片ID

# 测试集标注信息
annos_test = []  # test的annos

# 找出test中的图片的所有标注
for anno in anno_src['annotations']:
    if anno['image_id'] in images_idx_test:
        annos_test.append(anno)

annos_idx_test = set([i['id'] for i in annos_test])

# 删除源标签中的测试图片和标注，作为训练集
anno_src['images'] = [i for i in anno_src['images'] if i['id'] not in images_idx_test]
anno_src['annotations'] = [i for i in anno_src['annotations'] if i['id'] not in annos_idx_test]

# 组织test标签
anno_test['images'] = images_test
anno_test['annotations'] = annos_test
anno_test['categories'] = anno_src['categories']


with open(anno_file_train, 'w') as f:
    json.dump(anno_src, f)

with open(anno_file_test, 'w') as f:
    json.dump(anno_test, f)

print('Split Done!')
