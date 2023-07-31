"""
独立于任何标注格式的标注对象，标注转换时的中间格式
一张图中可以有多个对象，每个对象可以有多个标注（如一个框加数个关键点）
"""

class InterImage:
    def __init__(self, id, name, objs, width, height):
        self.set_id(id)
        self.name_ = name
        self.objs_ = []
        for obj in objs:
            self.add_obj(obj)
        self.set_width(width)
        self.set_height(height)

    @property
    def id(self):
        # assert isinstance(self.id_, int), f'id must be int, but now is: {self.id_}'
        # if self.id_<0 or self.id_==None:
        #     raise ValueError(f'id: {self.id_}')
        return self.id_
    
    def set_id(self, id: int):
        if id>=0:
            self.id_ = id

    def set_name(self, name):
        assert type(name) == str
        self.name_ = name

    @property
    def name(self):
        assert type(self.name_) == str
        return self.name_

    def add_obj(self, obj):
        if obj.is_valid:
            self.objs_.append(obj)
        else:
            raise Exception(f'obj is not valid: {obj}')

    # def set_objs(self, objs):
    #     self.objs = objs

    @property
    def objs(self):
        return self.objs_
    
    def set_width(self, width: int):
        # width = int(width)
        assert width>0, f'width must > 0, but now is: {width}'
        self.width_ = width
    
    @property
    def width(self):
        return self.width_
    
    def set_height(self, height):
        height = int(height)
        assert height>0, f'height must > 0, but now is: {height}'
        self.height_ = height

    @property
    def height(self):
        return self.height_
        # height = int(self.height_)
        # if height>0:
        #     return height
        # else:
        #     raise ValueError(f'height: {height}')


class InterObj:
    def __init__(self, annos, label, occluded=0, z_order=0):
        self.annos_ = annos

        self.set_label(label)

        self.occluded = occluded
        self.z_order = z_order

    @property
    def annos(self):
        return self.annos_
    
    def set_annos(self, annos):
        self.is_valid_list(annos)
        self.annos_ = annos

    def is_valid_list(self, l: list):
        # valid = True
        for i in l:
            if not i.is_valid:
                # valid = False
                raise ValueError(f'invalid anno: {i}')
    
    @property
    def is_valid(self):
        if self.is_valid_label(self.label):
            return True
        else:
            return False
    
    def is_valid_label(self, label):
        if type(label) == str and len(label) > 0:
            return True
        else:
            return False

    def add_anno(self, anno):
        if anno.is_valid:
            self.annos_.append(anno)

    @property
    def label(self):
        return self.label_

    def set_label(self, label):
        if self.is_valid_label(label):
            self.label_ = label
        else:
            raise ValueError(f'invalid label: {label}')

    # def get_occluded(self):
    #     return self.occluded

    def set_occluded(self, occluded):
        assert occluded >=0 and type(occluded) == int
        self.occluded = occluded


class InterAnno:
    def __init__(self, shape_type, points):
        self.shape_type = shape_type
        self.points = points
    

class InterPoint:
    def __init__(self, x, y, visibility=2):
        self.x = float(x)
        self.y = float(y)
        self.visibility = visibility
    
    def to_int(self):
        x = int(self.x)
        y = int(self.y)
        assert x>=0
        assert y>=0
        self.x = x
        self.y = y
        


# image = {
#     'objs': [],
#     'id': -1,
#     'name': '',
#     'width': -1,
#     'height': -1
# }

# obj = {
#     'annos': [],
#     'label': '',
#     'occluded': 0,
#     'z_order': 0
# }

# anno = {
#     'shape_type': '',
#     'points': [],
#     'label': ''
# }

# point = {
#     'pixel_x': -1,
#     'pixel_y': -1
# }