"""
  [
    {
        "image_id": "image_name", 
        "keypoint_annotations": 
        {
            "human1":[px1, py1, pt1, px2, py2, pt2, ..., px14, py14, pt14],
            "human2",:[...],
            ...,
            "humanN",:[...]
        },
        "human_annotations": 
        {
            "human1": [x1,y1,x2,y2],
            "human2": [x1,y1,x2,y2],
            ...,
            "humanN":[x1,y1,x2,y2]
        }
    },
    {
        ...
    }
  ]
"""


"""
由于cvat不支持直接导出关键点标注为COCO格式；
且由于它没有跳过某些被遮挡关键点的功能，我们通过将被遮挡的关键点点在图片左上角来“跳过”这些点。
综合以上两点，我们写了这个转换脚本，将cvat格式的xml标注格式转换为 Vitis-AI中的Caffe支持的.json格式，如上所示。
"""

import xmltodict

from intermediate import InterImage, InterObj, InterAnno, InterPoint
from coco_keypoints_obj import CocoKeypointsJson, CocoAnnotation, CocoCategory, CocoImage

# 解析CVAT
interImages = []
labels = set()

with open('tuopan_16keypoints/annotations.xml', 'r') as f:
    xml_str = f.read()
    data_dict = xmltodict.parse(xml_str)
    
    for image in data_dict['annotations']['image']:

        interObjs = []

        if image.get('points', None) is not None:  # 如果有关键点标注

            objs = [image['points']] if type(image['points']) == dict else image['points']  # 每张图中的多个实体对象

            for obj in objs:
                # annos = [obj['@points']]
                points_xys = obj['@points'].split(';')
                points_xys = [InterPoint(x=xy.split(',')[0], y=xy.split(',')[1]) for xy in points_xys]
                for i in points_xys:
                    i.to_int()

                annos = InterAnno(shape_type='points', points=points_xys)

                labels.add(obj['@label'])

                interObj = InterObj(annos=[annos], label=obj['@label'], occluded=int(obj['@occluded']), z_order=int(obj['@z_order']))
                interObjs.append(interObj)

        interImage = InterImage(id=int(image['@id']), name=image['@name'], objs=interObjs, 
                                width=int(image['@width']), 
                                height=int(image['@height']))
        
        interImages.append(interImage)

labels = sorted(list(labels))


# Vitis-AI-Caffe-OpenPose所需格式
vitis_ai_caffe_openpose = []

# 组织成coco格式
coco_images = []
coco_annotations = []
coco_categories = []
# num_keypoints=26
num_keypoints=16

skeleton = {
    'pallet': []
}
keypoints_name = {  # 各个关键点名称
    'pallet': ['p_'+str(i) for i in range(num_keypoints)]
}
for label in keypoints_name:

    coco_category = CocoCategory(supercategory=label, id=labels.index(label), name=label, 
                                 keypoints=keypoints_name[label], skeleton=skeleton[label])
    coco_categories.append(coco_category)


for interImage in interImages:

    coco_image = CocoImage(file_name=interImage.name, width=interImage.width, height=interImage.height, id=interImage.id)

    for interObj in interImage.objs:

        points_cant_see = 0

        boundary_piexl_x_min = None
        boundary_piexl_x_max = None
        boundary_piexl_y_min = None
        boundary_piexl_y_max = None

        keypoints = []
        
        for point in interObj.annos[0].points:
            if point.x < 70 and point.y < 70:  # 一些遮挡点置为0
                points_cant_see += 1
                point.x = 0
                point.y = 0
                keypoints += [point.x, point.y, 3] # 3表示无效点，2表示遮挡，1表示完全可见
            else:
                keypoints += [point.x, point.y, 1]
            
            if point.x != 0:
                if boundary_piexl_x_min is None:
                    boundary_piexl_x_min = point.x
                elif boundary_piexl_x_min > point.x:
                    boundary_piexl_x_min = point.x
                if boundary_piexl_x_max is None:
                    boundary_piexl_x_max = point.x
                elif boundary_piexl_x_max < point.x:
                    boundary_piexl_x_max = point.x

            if point.y != 0:
                if boundary_piexl_y_min is None:
                    boundary_piexl_y_min = point.y
                elif boundary_piexl_y_min > point.y:
                    boundary_piexl_y_min = point.y
                if boundary_piexl_y_max is None:
                    boundary_piexl_y_max = point.y
                elif boundary_piexl_y_max < point.y:
                    boundary_piexl_y_max = point.y
        assert len(keypoints) == num_keypoints * 3   # 确保点的个数完全相同
        assert boundary_piexl_x_min != None
        assert boundary_piexl_x_max != None
        assert boundary_piexl_y_min != None
        assert boundary_piexl_y_max != None
        # assert coco_category.keypoints

    vitis_ai_caffe_openpose.append(

        {
            "image_id": interImage.name, 
            "keypoint_annotations": 
            {
                "pallet1":keypoints,
            },
            "human_annotations": 
            {
                "pallet1": [boundary_piexl_x_min,boundary_piexl_y_min,boundary_piexl_x_max,boundary_piexl_y_max],
            }
        }
    )

        # coco_annotation = CocoAnnotation(segmentation=[], num_keypoints=num_keypoints-points_cant_see, 
        #                                  area=(boundary_piexl_y_max-boundary_piexl_y_min)*boundary_piexl_x_max-boundary_piexl_x_min/2, 
        #                                  iscrowd=0, keypoints=keypoints, 
        #                                  image_id=coco_image.id, id=len(coco_annotations), 
        #                                  bbox=[(boundary_piexl_x_min+boundary_piexl_x_max)/2,
        #                                       (boundary_piexl_y_min+boundary_piexl_y_max)/2,
        #                                       boundary_piexl_x_max-boundary_piexl_x_min,
        #                                       boundary_piexl_y_max-boundary_piexl_y_min,
        #                                       ], 
        #                                 category_id=labels.index(interObj.label))
        # coco_annotations.append(coco_annotation)
    # if len(interImage.objs):  # 只保存有标注的图片
    #     coco_images.append(coco_image)


# cocoKeypointsJson = CocoKeypointsJson(images=coco_images, annotations=coco_annotations, categories=coco_categories)
# cocoKeypointsJson.export_to_json_file(filename='pallet_16keypoints.json')

import json
with open('vitis_ai_caffe_openpose.json', 'w') as f:
    json.dump(vitis_ai_caffe_openpose, f)
print()
