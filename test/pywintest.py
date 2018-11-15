import os
import time
from multiprocessing import Process
from pywinauto import application


def run_proc():
    app = application.Application()
    window_name = u"Untitled - Notepad"
    menulist = u"Help->About Notepad"
    app.connect(title = window_name)
    app[window_name].menu_select(menulist)
    app[u'About Notepad'][u'OK'].click()

def open_notepad():
    os.popen(r'notepad.exe')    

if __name__ == '__main__':
   p1 = Process(target=open_notepad)
   p2 = Process(target=run_proc)
   p1.start()
   time.sleep(1)
   p2.start()
   p1.join()
   p2.join()