import numpy as np
import serial,re

class recDataBase:
    '''
        recData base
        override: func __init__() to add pattern to fetch useful data
        override: func insert() to realize other ways of transmission
    '''
    def __init__(self, slide_size):
        self.__slide_size = slide_size
        self.__data = np.zeros(slide_size, float)

    def insert(self, data):
        self.__data[:-1] = self.__data[1:]
        try:
            data = float(data)
        except:
            data = self.__data[-2]
            self.log("data convert to float failed:"+str(data))
        self.__data[-1] = data

    def get(self):
        return self.__data

    def size(self):
        return self.__slide_size

    def clear(self):
        self.__data = np.zeros(self.__slide_size)

    def log(self,str):
        print(str)

class recDataBySerial(recDataBase):
    '''
        by serial
    '''
    def __init__(self, com, baudrate, slide_size, pattern, data_index):
        super.__init__(slide_size)
        self.ser=serial.Serial(com, baudrate)
        self.__pattern = pattern
        self.__data_index = data_index

    def insert(self, data):
        data_str = self.ser.readline()
        data = re.split(self.__pattern, data_str)[self.__data_index]
        super.insert(data)

if __name__ == "__main__":
    size = 200
    ex = recDataBase(size)
    for i in range(1,size):
        import math
        ex.insert(math.cos(i))
    print(ex.get())