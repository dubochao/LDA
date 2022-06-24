import sys
import time
import math
 
def progress_bar(start, end):
    if math.ceil(start*100/end)!=math.ceil((start-1)*100/end):
        print("\rDownload progress: {}%: ".format(math.ceil(start*100/end)), "▋" * (math.ceil( start*10/end)), end="")

if __name__ == '__main__':
    for i in range(100):
        progress_bar(i, 100)
        time.sleep(0.1)

