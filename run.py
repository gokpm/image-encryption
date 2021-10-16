import os
import json
import cv2 as cv
import numpy as np
from random import shuffle
import sys
np.set_printoptions(threshold=sys.maxsize)

class Image:
    def __init__(self, path: str)-> None:
        self.path = path
        self.levels = 256
        self.values = np.arange(self.levels, dtype = np.uint8)
        self.img = cv.imread(self.path)
        self.rows, self.columns, self.channels = self.img.shape
        return

    def encrypt(self)-> None:
        self.encrypted = np.zeros((self.rows, self.columns, self.channels), dtype = np.uint8)
        self.key = Database(os.path.splitext(self.path)[0] + '_key' + '.json')
        self.key.data = np.zeros((self.rows, self.columns, self.levels), dtype = np.uint8)
        
        for i in range(self.rows):
            for j in range(self.columns):
                shuffle(self.values)
                self.key.data[i, j] = self.values
                for k in range(self.channels):
                    self.encrypted[i, j, k] = self.values[self.img[i, j, k]]
                    
        self.key.write(self.key.data.tolist())        
        cv.imwrite(os.path.splitext(self.path)[0] + '_encrypted' + '.tif', self.encrypted)
        return

    def decrypt(self)-> None:
        self.decrypted = np.zeros((self.rows, self.columns, self.channels), dtype = np.uint8)
        self.name = (os.path.splitext(self.path)[0].split('_', 1))[0]
        self.key = Database(self.name + '_key' + '.json')
        
        for i in range(self.rows):
            for j in range(self.columns):
                self.values = self.key.data[i,j]
                for k in range(self.channels):
                    self.decrypted[i, j, k] = np.where(self.values==self.img[i, j, k])[0][0]
                    
        cv.imwrite(self.name + '_decrypted' + '.tif', self.decrypted)
        return

class Database:
    def __init__(self, path: str)-> None:
        self.path = path
        if os.path.isfile(self.path):
            self.read()
        else:
            self.write([])
            
    def read(self)-> None:
        with open(self.path, 'r') as file:
            self.data = np.array(json.load(file), dtype = np.uint8)
        return

    def write(self, data: list)-> None:
        self.data = data
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent = 4)
        return

def main()-> None:
    return

if __name__ == '__main__':
    main()
