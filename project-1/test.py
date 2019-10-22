from util import PriorityQueue
queue_xy = PriorityQueue()

queue_xy.push((1,"abc"), 0)
queue_xy.push((2,"abcd"), 3)
queue_xy.push((3,"abcde"), 2)
queue_xy.push((4,"abcdef"), 1)
a = ["1","2","3","4"]

print(a.count())
