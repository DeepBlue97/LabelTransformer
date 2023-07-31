import cv2
import os

src_folder = r'D:\Workspace\mitan\hangcha\tuopan_dataset\Color_2d_mini_15keypoints'
dst_folder = r'D:\Workspace\mitan\hangcha\tuopan_dataset\Color_2d_mini_15keypoints_jpg'

if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

for name in os.listdir(src_folder):
    if name.endswith('.bmp'):

        fullname = os.path.join(src_folder, name)

        img = cv2.imread(fullname)
        dst_fullname = os.path.join(dst_folder, name[:-3]+'jpg')
        cv2.imwrite(dst_fullname, img)
        print('saved: ', dst_fullname)
        