import queue_exemple as qq
from time import sleep
print '2'
print 'X',qq.q

sleep(1)

for i in range(333,339):
    qq.q.put(i)


if __name__ == '__main__':
	print qq.q
	while not qq.q.empty():
		print qq.q.get()