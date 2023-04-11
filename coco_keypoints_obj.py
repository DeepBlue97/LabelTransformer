"""
['info', 'licenses', 'images', 'annotations', 'categories']

{'url': 'http://creativecommons.org/licenses/by-nc-sa/2.0/', 'id': 1, 'name': 'Attribution-NonCommercial-ShareAlike License'}

['url', 'id', 'name']


{'license': 4, 'file_name': '000000397133.jpg', 'coco_url': 'http://images.cocodataset.org/val2017/000000397133.jpg', 'height': 427, 'width': 640, 'date_captured': '2013-11-14 17:02:52', 'flickr_url': 'http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg', 'id': 397133}

['license', 'file_name', 'coco_url', 'height', 'width', 'date_captured', 'flickr_url', 'id']


{'segmentation': [[125.12, 539.69, 140.94, 522.43, 100.67, 496.54, 84.85, 469.21, 73.35, 450.52, 104.99, 342.65, 168.27, 290.88, 179.78, 288, 189.84, 286.56, 191.28, 260.67, 202.79, 240.54, 221.48, 237.66, 248.81, 243.42, 257.44, 256.36, 253.12, 262.11, 253.12, 275.06, 299.15, 233.35, 329.35, 207.46, 355.24, 206.02, 363.87, 206.02, 365.3, 210.34, 373.93, 221.84, 363.87, 226.16, 363.87, 237.66, 350.92, 237.66, 332.22, 234.79, 314.97, 249.17, 271.82, 313.89, 253.12, 326.83, 227.24, 352.72, 214.29, 357.03, 212.85, 372.85, 208.54, 395.87, 228.67, 414.56, 245.93, 421.75, 266.07, 424.63, 276.13, 437.57, 266.07, 450.52, 284.76, 464.9, 286.2, 479.28, 291.96, 489.35, 310.65, 512.36, 284.76, 549.75, 244.49, 522.43, 215.73, 546.88, 199.91, 558.38, 204.22, 565.57, 189.84, 568.45, 184.09, 575.64, 172.58, 578.52, 145.26, 567.01, 117.93, 551.19, 133.75, 532.49]], 'num_keypoints': 10, 'area': 47803.27955, 'iscrowd': 0, 'keypoints': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 142, 309, 1, 177, 320, 2, 191, 398, 2, 237, 317, 2, 233, 426, 2, 306, 233, 2, 92, 452, 2, 123, 468, 2, 0, 0, 0, 251, 469, 2, 0, 0, 0, 162, 551, 2], 'image_id': 425226, 'bbox': [73.35, 206.02, 300.58, 372.5], 'category_id': 1, 'id': 183126}

['segmentation', 'num_keypoints', 'area', 'iscrowd', 'keypoints', 'image_id', 'bbox', 'category_id', 'id']


{'supercategory': 'person', 'id': 1, 'name': 'person', 'keypoints': ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle'], 'skeleton': [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]}

['supercategory', 'id', 'name', 'keypoints', 'skeleton']
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

"""
    "images": [
        {
            "license": 4,
            "file_name": "000000397133.jpg",
            "coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
            "height": 427,
            "width": 640,
            "date_captured": "2013-11-14 17:02:52",
            "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
            "id": 397133
        },
"""

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
    