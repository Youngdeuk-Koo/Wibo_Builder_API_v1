import time

n = time.localtime().tm_wday

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

print(days[n])



