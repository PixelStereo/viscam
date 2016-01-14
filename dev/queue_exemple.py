import Queue
from time import sleep
q = Queue.Queue()

print '1'

for i in range(5):
    q.put(i)

for i in range(100,105):
    q.put(i)