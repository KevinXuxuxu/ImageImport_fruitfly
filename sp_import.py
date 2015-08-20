# -*- coding: utf-8 -*-
__author__ = "Xu Fangzhou"
__email__ = "kevin.xu.fangzhou@gmail.com"

import os
import scipy.io as sio

class SPImageSet:

    def __init__(self, _name):
        self.name = _name
        if _name not in os.listdir('.'):
            raise Exception("No such image set in dir: "+os.getcwd())
        self.name_list = []
        for name in os.listdir(_name):
            if not name.startswith('.'):
                self.name_list.append(name)
        self.i = 0
        self.n = len(self.name_list)


    def __iter__(self):
        return self

    def next(self):
        d = {}
        if self.i < self.n:
            i = self.i
            self.i += 1
            d['name'] = self.name_list[i]
            d['id'] = str(i)
            d['sp'] = []
            mat_contents = sio.loadmat(self.name + '/' + self.name_list[i])
            for i in range(1,len(mat_contents['gcs'])+1):
                dd = {'id': i,
                      'gc': mat_contents['gcs'][i-1],
                      'boundary': mat_contents['boundaries'][i-1][0]}
                d['sp'] += [dd]
            return d
        else:
            raise StopIteration()
