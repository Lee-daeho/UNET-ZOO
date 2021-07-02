import torch.utils.data as data
import PIL.Image as Image
from sklearn.model_selection import train_test_split
import os
import random
import numpy as np
from skimage.io import imread
import cv2
from glob import glob
import imageio
from torchvision import transforms


class DaconDataset(data.Dataset):
    def __init__(self, state, transform=None, target_trasnform=None):
        self.state = state
        self.train_img_root = "/home/dacon/data/100_train_input_img_256"
        self.train_label_root = "/home/dacon/data/100_train_label_img_256"

        self.val_img_root = "/home/dacon/data/100_val_input_img_256"
        self.val_label_root = "/home/dacon/data/100_val_label_img_256"

        self.imgs, self.labels = self.getDataPath()
        self.transform = transform
        self.target_transform = target_trasnform
        self.base_transform = transforms.Compose([
            transforms.ToTensor()
        ])

    def getDataPath(self):
        assert self.state =='train' or self.state == 'val' or self.state =='test'

        imgs = []
        labels = []

        if self.state == 'train':
            img_root = self.train_img_root
            label_root = self.train_label_root

        if self.state == 'val':
            img_root = self.val_img_root
            label_root = self.val_label_root

        for name in os.listdir(img_root):
            img = os.path.join(img_root, name)
            label = os.path.join(label_root, name)

            imgs.append(img)
            labels.append(label)

        return imgs, labels

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        pic_path = self.imgs[idx]
        label_path = self.labels[idx]

        img = Image.fromarray(np.uint8(np.load(pic_path))).convert('RGB')
        label = Image.fromarray(np.uint8(np.load(label_path))).convert('RGB')
        
        if self.transform is not None:
            img = self.transform(img)
        else:
            img = self.base_transform(img)
        
        if self.target_transform is not None:
            label = self.target_transform(label)
        else:
            label = self.base_transform(label)

        return img, label, pic_path, label_path


class LiverDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.train_root = r"E:\codes\new\u_net_liver-master\data\liver\train"
        self.val_root = r"E:\codes\new\u_net_liver-master\data\liver\val"
        self.test_root = self.val_root
        self.pics,self.masks = self.getDataPath()
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        assert self.state =='train' or self.state == 'val' or self.state =='test'
        if self.state == 'train':
            root = self.train_root
        if self.state == 'val':
            root = self.val_root
        if self.state == 'test':
            root = self.test_root

        pics = []
        masks = []
        n = len(os.listdir(root)) // 2  # ?�为?�据?�中一套�?练数??��?�有�?��?�和mask?�，?�以要??
        for i in range(n):
            img = os.path.join(root, "%03d.png" % i)  # liver is %03d
            mask = os.path.join(root, "%03d_mask.png" % i)
            pics.append(img)
            masks.append(mask)
            #imgs.append((img, mask))
        return pics,masks

    def __getitem__(self, index):
        #x_path, y_path = self.imgs[index]
        x_path = self.pics[index]
        y_path = self.masks[index]
        origin_x = Image.open(x_path)
        origin_y = Image.open(y_path)
        # origin_x = cv2.imread(x_path)
        # origin_y = cv2.imread(y_path,cv2.COLOR_BGR2GRAY)
        if self.transform is not None:
            img_x = self.transform(origin_x)
        if self.target_transform is not None:
            img_y = self.target_transform(origin_y)
        return img_x, img_y,x_path,y_path

    def __len__(self):
        return len(self.pics)

class esophagusDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.train_root = r"E:\datasets\data_sta_all\train_data"
        self.val_root = r"E:\datasets\data_sta_all\test_data"
        self.test_root = self.val_root
        self.pics,self.masks = self.getDataPath()
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        assert self.state =='train' or self.state == 'val' or self.state == 'test'
        if self.state == 'train':
            root = self.train_root
        if self.state == 'val':
            root = self.val_root
        if self.state == 'test':
            root = self.test_root
        pics = []
        masks = []
        n = len(os.listdir(root)) // 2  # ?�为?�据?�中一套�?练数??��?�有�?��?�和mask?�，?�以要??
        for i in range(n):
            img = os.path.join(root, "%05d.png" % i)  # liver is %03d
            mask = os.path.join(root, "%05d_mask.png" % i)
            pics.append(img)
            masks.append(mask)
            #imgs.append((img, mask))
        return pics,masks

    def __getitem__(self, index):
        #x_path, y_path = self.imgs[index]
        x_path = self.pics[index]
        y_path = self.masks[index]
        # origin_x = Image.open(x_path)
        # origin_y = Image.open(y_path)
        origin_x = cv2.imread(x_path)
        origin_y = cv2.imread(y_path,cv2.COLOR_BGR2GRAY)
        if self.transform is not None:
            img_x = self.transform(origin_x)
        if self.target_transform is not None:
            img_y = self.target_transform(origin_y)
        return img_x, img_y,x_path,y_path

    def __len__(self):
        return len(self.pics)

class dsb2018CellDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.aug = True
        self.root = r'E:\codes\pytorch-nested-unet-master\pytorch-nested-unet-master\input\dsb2018_256'
        self.img_paths = None
        self.mask_paths = None
        self.train_img_paths, self.val_img_paths = None,None
        self.train_mask_paths, self.val_mask_paths = None,None
        self.pics,self.masks = self.getDataPath()
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        self.img_paths = glob(self.root + '\images\*')
        self.mask_paths = glob(self.root + '\masks\*')
        self.train_img_paths, self.val_img_paths, self.train_mask_paths, self.val_mask_paths = \
            train_test_split(self.img_paths, self.mask_paths, test_size=0.2, random_state=41)
        assert self.state == 'train' or self.state == 'val' or self.state == 'test'
        if self.state == 'train':
            return self.train_img_paths,self.train_mask_paths
        if self.state == 'val':
            return self.val_img_paths,self.val_mask_paths
        if self.state == 'test':
            return self.val_img_paths,self.val_mask_paths  #?�数??��没有测试?�，?�以用验证?�代??
    def __getitem__(self, index):
        pic_path = self.pics[index]
        mask_path = self.masks[index]
        # origin_x = Image.open(x_path)
        # origin_y = Image.open(y_path)
        pic = cv2.imread(pic_path)
        mask = cv2.imread(mask_path,cv2.COLOR_BGR2GRAY)
        pic = pic.astype('float32') / 255
        mask = mask.astype('float32') / 255
        # if self.aug:
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[:, ::-1, :].copy()
        #         mask = mask[:, ::-1].copy()
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[::-1, :, :].copy()
        #         mask = mask[::-1, :].copy()
        if self.transform is not None:
            img_x = self.transform(pic)
        if self.target_transform is not None:
            img_y = self.target_transform(mask)
        return img_x, img_y,pic_path,mask_path

    def __len__(self):
        return len(self.pics)

class CornealDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.aug = True
        self.root = r'E:\datasets\CORN\CORN\Corneal nerve curivilinear segmentation\Corneal nerve curivilinear segmentation'
        self.img_paths = None
        self.mask_paths = None
        self.train_img_paths, self.val_img_paths,self.test_img_paths = None,None,None
        self.train_mask_paths, self.val_mask_paths,self.test_mask_paths = None,None,None
        self.pics,self.masks = self.getDataPath()
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        self.train_img_paths = glob(self.root + r'\training\train_images\*')
        self.train_mask_paths = glob(self.root + r'\training\train_mask\*')
        self.val_img_paths = glob(self.root + r'\val\val_images\*')
        self.val_mask_paths = glob(self.root + r'\val\val_mask\*')
        self.test_img_paths = glob(self.root + r'\test\test_images\*')
        self.test_mask_paths = glob(self.root + r'\test\test_mask\*')
        # self.train_img_paths, self.val_img_paths, self.train_mask_paths, self.val_mask_paths = \
        #     train_test_split(self.img_paths, self.mask_paths, test_size=0.2, random_state=41)
        assert self.state == 'train' or self.state == 'val' or self.state == 'test'
        if self.state == 'train':
            return self.train_img_paths,self.train_mask_paths
        if self.state == 'val':
            return self.val_img_paths,self.val_mask_paths
        if self.state == 'test':
            return self.test_img_paths,self.test_mask_paths

    def __getitem__(self, index):
        pic_path = self.pics[index]
        mask_path = self.masks[index]
        # origin_x = Image.open(x_path)
        # origin_y = Image.open(y_path)
        pic = cv2.imread(pic_path)
        mask = cv2.imread(mask_path,cv2.COLOR_BGR2GRAY)
        pic = pic.astype('float32') / 255
        mask = mask.astype('float32') / 255
        # if self.aug:
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[:, ::-1, :].copy()
        #         mask = mask[:, ::-1].copy()
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[::-1, :, :].copy()
        #         mask = mask[::-1, :].copy()
        if self.transform is not None:
            img_x = self.transform(pic)
        if self.target_transform is not None:
            img_y = self.target_transform(mask)
        return img_x, img_y,pic_path,mask_path

    def __len__(self):
        return len(self.pics)

class DriveEyeDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.aug = True
        self.root = r'E:\datasets\DRIVE\DRIVE'
        self.pics, self.masks = self.getDataPath()
        self.img_paths = None
        self.mask_paths = None
        self.train_img_paths, self.val_img_paths,self.test_img_paths = None,None,None
        self.train_mask_paths, self.val_mask_paths,self.test_mask_paths = None,None,None
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        self.train_img_paths = glob(self.root + r'\training\images\*')
        self.train_mask_paths = glob(self.root + r'\training\1st_manual\*')
        self.val_img_paths = glob(self.root + r'\test\images\*')
        self.val_mask_paths = glob(self.root + r'\test\1st_manual\*')
        self.test_img_paths = self.val_img_paths
        self.test_mask_paths = self.val_mask_paths
        assert self.state == 'train' or self.state == 'val' or self.state == 'test'
        if self.state == 'train':
            return self.train_img_paths, self.train_mask_paths
        if self.state == 'val':
            return self.val_img_paths, self.val_mask_paths
        if self.state == 'test':
            return self.test_img_paths, self.test_mask_paths

    def __getitem__(self, index):
        imgx,imgy=(576,576)
        pic_path = self.pics[index]
        mask_path = self.masks[index]
        # origin_x = Image.open(x_path)
        # origin_y = Image.open(y_path)
        #print(pic_path)
        pic = cv2.imread(pic_path)
        mask = cv2.imread(mask_path,cv2.COLOR_BGR2GRAY)
        if mask == None:
            mask = imageio.mimread(mask_path)
            mask = np.array(mask)[0]
        pic = cv2.resize(pic,(imgx,imgy))
        mask = cv2.resize(mask, (imgx, imgy))
        pic = pic.astype('float32') / 255
        mask = mask.astype('float32') / 255
        # if self.aug:
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[:, ::-1, :].copy()
        #         mask = mask[:, ::-1].copy()
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[::-1, :, :].copy()
        #         mask = mask[::-1, :].copy()
        if self.transform is not None:
            img_x = self.transform(pic)
        if self.target_transform is not None:
            img_y = self.target_transform(mask)
        return img_x, img_y,pic_path,mask_path

    def __len__(self):
        return len(self.pics)

class IsbiCellDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.aug = True
        self.root = r'E:\datasets\isbi'
        self.img_paths = None
        self.mask_paths = None
        self.train_img_paths, self.val_img_paths,self.test_img_paths = None,None,None
        self.train_mask_paths, self.val_mask_paths,self.test_mask_paths = None,None,None
        self.pics,self.masks = self.getDataPath()
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        self.img_paths = glob(self.root + r'\train\images\*')
        self.mask_paths = glob(self.root + r'\train\label\*')
        # self.val_img_paths = glob(self.root + r'\val\val_images\*')
        # self.val_mask_paths = glob(self.root + r'\val\val_mask\*')
        # self.test_img_paths = glob(self.root + r'\test\test_images\*')
        # self.test_mask_paths = glob(self.root + r'\test\test_mask\*')
        self.train_img_paths, self.val_img_paths, self.train_mask_paths, self.val_mask_paths = \
            train_test_split(self.img_paths, self.mask_paths, test_size=0.2, random_state=41)
        self.test_img_paths, self.test_mask_paths = self.val_img_paths,self.val_mask_paths
        assert self.state == 'train' or self.state == 'val' or self.state == 'test'
        if self.state == 'train':
            return self.train_img_paths,self.train_mask_paths
        if self.state == 'val':
            return self.val_img_paths,self.val_mask_paths
        if self.state == 'test':
            return self.test_img_paths,self.test_mask_paths

    def __getitem__(self, index):
        pic_path = self.pics[index]
        mask_path = self.masks[index]
        # origin_x = Image.open(x_path)
        # origin_y = Image.open(y_path)
        pic = cv2.imread(pic_path)
        mask = cv2.imread(mask_path,cv2.COLOR_BGR2GRAY)
        pic = pic.astype('float32') / 255
        mask = mask.astype('float32') / 255
        # if self.aug:
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[:, ::-1, :].copy()
        #         mask = mask[:, ::-1].copy()
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[::-1, :, :].copy()
        #         mask = mask[::-1, :].copy()
        if self.transform is not None:
            img_x = self.transform(pic)
        if self.target_transform is not None:
            img_y = self.target_transform(mask)
        return img_x, img_y,pic_path,mask_path

    def __len__(self):
        return len(self.pics)

class LungKaggleDataset(data.Dataset):
    def __init__(self, state, transform=None, target_transform=None):
        self.state = state
        self.aug = True
        self.root = r'E:\datasets\finding-lungs-in-ct-data-kaggle'
        self.img_paths = None
        self.mask_paths = None
        self.train_img_paths, self.val_img_paths,self.test_img_paths = None,None,None
        self.train_mask_paths, self.val_mask_paths,self.test_mask_paths = None,None,None
        self.pics,self.masks = self.getDataPath()
        self.transform = transform
        self.target_transform = target_transform

    def getDataPath(self):
        self.img_paths = glob(self.root + r'\2d_images\*')
        self.mask_paths = glob(self.root + r'\2d_masks\*')
        self.train_img_paths, self.val_img_paths, self.train_mask_paths, self.val_mask_paths = \
            train_test_split(self.img_paths, self.mask_paths, test_size=0.2, random_state=41)
        self.test_img_paths, self.test_mask_paths = self.val_img_paths, self.val_mask_paths
        assert self.state == 'train' or self.state == 'val' or self.state == 'test'
        if self.state == 'train':
            return self.train_img_paths, self.train_mask_paths
        if self.state == 'val':
            return self.val_img_paths, self.val_mask_paths
        if self.state == 'test':
            return self.test_img_paths, self.test_mask_paths

    def __getitem__(self, index):
        pic_path = self.pics[index]
        mask_path = self.masks[index]
        # origin_x = Image.open(x_path)
        # origin_y = Image.open(y_path)
        pic = cv2.imread(pic_path)
        mask = cv2.imread(mask_path,cv2.COLOR_BGR2GRAY)
        pic = pic.astype('float32') / 255
        mask = mask.astype('float32') / 255
        # if self.aug:
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[:, ::-1, :].copy()
        #         mask = mask[:, ::-1].copy()
        #     if random.uniform(0, 1) > 0.5:
        #         pic = pic[::-1, :, :].copy()
        #         mask = mask[::-1, :].copy()
        if self.transform is not None:
            img_x = self.transform(pic)
        if self.target_transform is not None:
            img_y = self.target_transform(mask)
        return img_x, img_y,pic_path,mask_path

    def __len__(self):
        return len(self.pics)