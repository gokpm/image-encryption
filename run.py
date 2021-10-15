import os
import json
import cv2 as cv
import numpy as np
from random import shuffle

class Image:
    def __init__(self, path) -> None:
        self.levels = 256
        self.values = np.arange(self.levels)
        self.path = path
        self.img = cv.imread(self.path)
        self.rows, self.columns, self.channels = self.img.shape
        return

    def encrypt(self) -> None:
        self.key = Database(os.path.splitext(self.path)[0] + '_encrypted' + '_key' + '.json')
        self.key.data = np.zeros((self.rows, self.columns, self.levels), dtype = np.uint8)
        self.encrypted = np.zeros((self.rows, self.columns, self.channels), dtype = np.uint8)
        for i in range(self.rows):
            for j in range(self.columns):
                shuffle(self.values)
                self.key.data[i,j] = self.values
                for k in range(self.channels):
                    self.encrypted[i,j,k] = self.values[self.img[i,j,k]]
        self.key.write(self.key.data.tolist())
        cv.imwrite(os.path.splitext(self.path)[0] + '_encrypted' + '.jpg', self.encrypted)
        return

    def decrypt(self) -> None:
        self.key = Database(os.path.splitext(self.path)[0] + '_key' + '.json')
        self.decrypted = np.zeros((self.rows, self.columns, self.channels), dtype = np.uint8)
        for i in range(self.rows):
            for j in range(self.columns):
                self.values = self.key.data[i,j]
                for k in range(self.channels):
                    self.decrypted[i, j, k] = np.uint8(np.where(self.values==self.img[i,j,k])[0][0])
        b = self.decrypted[:, :, 0]
        g = self.decrypted[:, :, 1]
        r = self.decrypted[:, :, 2]
        self.img = cv.merge((b,g,r), 3)
        cv.imwrite(os.path.splitext(self.path)[0] + '_decrypted' + '.jpg', self.img)
        return

class Database:
    def __init__(self, path) -> None:
        self.path = path
        if os.path.isfile(self.path):
            self.read()
        else:
            self.write([])
            
    def read(self) -> None:
        with open(self.path, 'r') as file:
            self.data = np.array(json.load(file))
        return

    def write(self, data) -> None:
        self.data = data
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent = 4)
        return

def main():
    b = Image('#16_encrypted.jpg')
    b.decrypt()

if __name__ == '__main__':
    main()
