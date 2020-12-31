import os
from glob import glob
import hashlib

def scan_dir(path, file_list=[], extension='.tif', include='LEFT_RGB'):
    for i in os.listdir(path):
        temp_dir = os.path.join(path, i)
        if os.path.isdir(temp_dir):
            scan_dir(temp_dir, file_list, extension, include)
        else:
            if temp_dir.endswith(extension) and include in temp_dir:
                file_list.append(temp_dir)
    return file_list

def md5sum(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def create_list(image_folder, disparity_folder):
    img_list = scan_dir(image_folder)

    left_img = []
    right_img = []
    left_disp = []

    for filename in img_list:
        right_filename = filename.replace('LEFT', 'RIGHT')
        if md5sum(filename) == md5sum(right_filename):
            print("all pixels are the same")
            continue

        left_disp_filename = filename.replace(image_folder + '/' + filename.split('/')[-2], disparity_folder)
        left_disp_filename = left_disp_filename.replace('RGB', 'DSP')

        left_img.append(filename)
        right_img.append(right_filename)
        left_disp.append(left_disp_filename)

    return left_img, right_img, left_disp

def gen_dfc(image_path, disp_path):
    left_imgs, right_imgs, left_disps = create_list(image_path, disp_path)
    train_file = 'DFC_train.txt'
    val_file = 'DFC_val.txt'
    with open(val_file, 'w') as val_f:
        for i in range(len(left_imgs)):
            if i % 20 == 0:
                val_f.write(left_imgs[i] + ' ')
                val_f.write(right_imgs[i] + ' ')
                val_f.write(left_disps[i] + '\n')
    # with open(train_file, 'w') as train_f:
    #     for i in range(len(left_imgs)):
    #         train_f.write(left_imgs[i] + ' ')
    #         train_f.write(right_imgs[i] + ' ')
    #         train_f.write(left_disps[i] + '\n')



# def gen_kitti_2015():
#     data_dir = 'data/KITTI/kitti_2015/data_scene_flow'
#
#     train_file = 'KITTI_2015_train.txt'
#     val_file = 'KITTI_2015_val.txt'
#
#     # Split the training set with 4:1 raito (160 for training, 40 for validation)
#     with open(train_file, 'w') as train_f, open(val_file, 'w') as val_f:
#         dir_name = 'image_2'
#         left_dir = os.path.join(data_dir, 'training', dir_name)
#         left_imgs = sorted(glob(left_dir + '/*_10.png'))
#
#         print('Number of images: %d' % len(left_imgs))
#
#         for left_img in left_imgs:
#             right_img = left_img.replace(dir_name, 'image_3')
#             disp_path = left_img.replace(dir_name, 'disp_occ_0')
#
#             img_id = int(os.path.basename(left_img).split('_')[0])
#
#             if img_id % 5 == 0:
#                 val_f.write(left_img.replace(data_dir + '/', '') + ' ')
#                 val_f.write(right_img.replace(data_dir + '/', '') + ' ')
#                 val_f.write(disp_path.replace(data_dir + '/', '') + '\n')
#             else:
#                 train_f.write(left_img.replace(data_dir + '/', '') + ' ')
#                 train_f.write(right_img.replace(data_dir + '/', '') + ' ')
#                 train_f.write(disp_path.replace(data_dir + '/', '') + '\n')


if __name__ == '__main__':
    image_path = '/media/omnisky/24ef2133-7131-4681-865f-7f5e2a0dc3fa/DataFusionContest'
    disp_path = '/media/omnisky/24ef2133-7131-4681-865f-7f5e2a0dc3fa/DataFusionContest/Track2-Truth'
    gen_dfc(image_path, disp_path)
