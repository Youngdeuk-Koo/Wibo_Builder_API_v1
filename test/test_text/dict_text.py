path = "C:/Users/kooli/mrmind/chatbot/v.0.0.1_2022.08.23/wiboe_dev_v2/test/text_trim_test.txt"

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')

    except OSError:
        print(f'경로를 열 수 없습니다: {profile_path}')
        raise

# class Pictures(dict):
#     def __missing__(self, key):
#         value = open_picture(key)
#         self[key] = value
#         return value

# pictures = Pictures()
# handle = pictures[path]
# handle.seek(0)
# image_data = handle.read()

print(open_picture(path))