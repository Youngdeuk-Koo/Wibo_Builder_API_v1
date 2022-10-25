
import os

path = './test/ebs'

if not os.path.exists(path):
    os.makedirs(path)
    print(f'[{path}] 폴더가 생성되었습니다')

else:
    print(f'[{path}] 폴더가 이미 있습니다')
    pass