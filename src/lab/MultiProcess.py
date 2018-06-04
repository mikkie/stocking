# -*-coding=utf-8-*-

#多进程与多线程测试，通过lock保证一个事物的原子性

import multiprocessing as mp
import threading
import os


def async(f):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=f,args = args, kwargs = kwargs)
        t.start()
    return wrapper    

@async
def run2(value,lock):
    lock.acquire()
    value.value = value.value - 1
    for i in range(10):
        print('thread name = %s, pid = %s, value = %s' % (threading.current_thread().name,os.getpid(),value.value))
    lock.release()    

def run(value,lock):
    for i in range(3):
        run2(value,lock)

if __name__ == '__main__':
   pool = mp.Pool(3)
   manager = mp.Manager()
   value = manager.Value('i',5)
   lock = manager.Lock()
   for i in range(3):
       pool.apply_async(run, args=(value,lock))
   input('please enter to exit')   


