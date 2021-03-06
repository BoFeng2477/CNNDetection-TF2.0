import math
import os
import numpy as np
import random
import cv2
from PIL import Image
from tensorflow.keras.utils import Sequence
from Data.DataAug import data_augment

# Restructured train-time data generator
class DataGenerator(Sequence):

    def __init__(self, file_index,root_dir='../e4040-proj-data/',  batch_size=256, shuffle=True,blur_prob=0,jpeg_prob=0):
        self.datas = file_index 
        self.root_dir = root_dir
        self.indexes = np.arange(len(file_index))
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()
        self.opt = {'blur_prob':blur_prob,
                    'blur_sig':[0, 3],
                    'jpg_prob':jpeg_prob,
                    'jpg_method':['cv2'],
                    'jpg_qual':[30,100],
                    'rz_interp':'bilinear',
                    'loadSize':256
                  }

        
    def __len__(self):      
        return int(np.floor(len(self.datas) / self.batch_size)) #np.floor / np.ceil
 

    def __getitem__(self, index):
        
        indexs = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        img_path = [self.datas.loc[k]['file'] for k in indexs]
        labels = [self.datas.loc[k]['label'] for k in indexs]
        labels = np.array(labels).astype(np.float32)
        imgs = self.read_img_from_csv(img_path,self.opt)
        return imgs,labels

    def read_img_from_csv(self,img_path, opt):
        imgs = []
        for path in img_path:
            path = self.root_dir +path
            img = cv2.imread(path)   
            img = data_augment(img,opt)
            imgs.append(img)
        imgs = np.array(imgs).astype(np.float32)
        imgs = imgs / 255.0  
        return imgs

# Restructured test-time data generator
class TestDataGenerator(Sequence):

    def __init__(self, file_index,root_dir='../e4040-proj-data/',  batch_size=256, shuffle=True):
        self.datas = file_index 
        self.root_dir = root_dir
        self.indexes = np.arange(len(file_index))
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()

        
    def __len__(self):      
        return int(np.floor(len(self.datas) / self.batch_size)) #np.floor / np.ceil
 

    def __getitem__(self, index):
        
        indexs = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        img_path = [self.datas.loc[k]['file'] for k in indexs]
        labels = [self.datas.loc[k]['label'] for k in indexs]
        labels = np.array(labels).astype(np.float32)
        imgs = self.read_img_from_csv(img_path)
        return imgs,labels

    def read_img_from_csv(self,img_path):
        imgs = []
        for path in img_path:
            path = self.root_dir +path
            img = cv2.imread(path)   
            
            size=224
            h, w = img.shape[:2]
            y = int(h-size/2)
            x = int(w-size/2)
            img = img[y:y+size, x:x+size, :]
            
            imgs.append(img)
        imgs = np.array(imgs).astype(np.float32)
        imgs = imgs / 255.0  
        return imgs