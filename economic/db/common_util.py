# encoding=utf-8
import numpy as np

class CommonUtil:

    def tuple_to_list(self,demo):#将从数据库中的元祖转为数列，并将其中unicode编码转为float
        size = len(demo)
        result = [0]*size
        new_image = np.zeros((3, 5))
        if size == 0:
            return demo
        if size == 1:
            result[0] = float(''.join(demo[0]).encode("utf-8"))
            return result
        if size > 1:
            for i in range(size):
                result[i] = float(''.join(demo[i]).encode("utf-8"))
            return result

if __name__ == '__main__':
    fc = CommonUtil()
    tup1 = (u'19.97',);
    print (fc.tuple_to_list(tup1))