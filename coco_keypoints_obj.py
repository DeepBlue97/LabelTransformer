"""
对象化的 coco 关键点标注文件里的东西
"""

import json


class CocoKeypointsJson:

    def __init__(self, images: list, annotations: list, categories: list):
        
        # self.info = 
        # self.licenses = 
        self.images = images
        self.annotations = annotations
        self.categories = categories

    def export_to_json_file(self, filename):
    
        d = {
            'images': [cocoImage.to_dict() for cocoImage in self.images],
            'annotations': [cocoAnnotation.to_dict() for cocoAnnotation in self.annotations],
            'categories':  [cocoCategory.to_dict() for cocoCategory in self.categories]
        }
        with open(filename, 'w') as f:
            json.dump(d, f)


class CocoImage:
    def __init__(self, file_name: str, width: int, height: int, id: int):
        
        self.file_name = file_name
        self.width = width
        self.height = height
        self.id = id

    def to_dict(self):
        return {
            'file_name': self.file_name,
            'width': self.width,
            'height': self.height,
            'id': self.id
        }

class CocoAnnotation:
    def __init__(self, segmentation: list, num_keypoints: int, area: float, iscrowd: int, 
                 keypoints: list, image_id: int, id: int, bbox: list, category_id: int):
        
        self.segmentation = segmentation
        self.num_keypoints = num_keypoints
        self.area = area
        self.iscrowd = iscrowd

        self.keypoints = keypoints
        self.image_id = image_id
        self.bbox = bbox
        self.category_id = category_id

        self.id = id

    def to_dict(self):
        return {
            'segmentation': self.segmentation,
            'num_keypoints': self.num_keypoints,
            'area': self.area,
            'iscrowd': self.iscrowd,
            'keypoints': self.keypoints,
            'image_id': self.image_id,
            'bbox': self.bbox,
            'category_id': self.category_id,
            'id': self.id,
        }

class CocoCategory:
    def __init__(self, supercategory, id, name, keypoints, skeleton):
        self.supercategory = supercategory
        self.id = id
        self.name = name
        self.keypoints = keypoints
        self.skeleton = skeleton

    def to_dict(self):
        return {
            'supercategory': self.supercategory,
            'id': self.id,
            'name': self.name,
            'keypoints': self.keypoints,
            'skeleton': self.skeleton,
        }
    