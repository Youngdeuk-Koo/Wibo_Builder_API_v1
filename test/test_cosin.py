import os
import pandas as pd
from collections import defaultdict, Counter


def core_text_process(text):
    
    text = text.split()

    word_dict = defaultdict(lambda:[])
    
    for i, v in enumerate(text):        
    
        if v in ['으면', '지만', '하지만', '으니깐', '으니까', '근데', '그리고', '그런데', '거니까', '그래갖고', '그래가지고', '하는데', '말하는데', '자꾸', ]:
            
            word_dict['word'].append(i)

            if len(word_dict['word']) >= 2:
                if word_dict['word'][-1] >= (len(text) * 0.95):
                    print('process sucess.1')
                    join_text = ' '.join(text[word_dict['word'][len(word_dict['word'])-2]+1:])
                    return join_text, 'process sucess.1'
                else:    
                    print('process sucess.2')
                    join_text = ' '.join(text[word_dict['word'][-1]+1:])
                    return join_text, 'process sucess.2'
            else:
                if word_dict['word'][-1] >= (len(text) * 0.95):
                    print('process sucess.3')
                    join_text = ' '.join(text)
                    return join_text, 'process sucess.3'
                else:
                    print('process sucess.4')
                    join_text = ' '.join(text[word_dict['word'][-1]+1:])
                    return join_text, 'process sucess.4'  

        else:
            print('process fail')
            return ' '.join(text), 'process fail'


    

df = pd.DataFrame()

path_dir = '/mnt/c/Logs/nlp_log'
# file_list = os.listdir(path_dir)
# print(file_list)
with open(path_dir + '/' + 'nlp_2022-08-21.txt', 'r', encoding='utf-8') as f:
    text = f.readlines()


with open('/mnt/c/Users/kooli/mrmind/wiboe_dev_v2/test_text/user_input_text.txt', 'w+', encoding='utf-8') as f:
    for i, v in enumerate(text[:200]): 
        f.write(v.split('    ')[3] + '\n')          
            # input_text = v.split('    ')[3]
            
            # join_text, pro_type = core_text_process(input_text)
            # print(i)

            # with open('text_trim_test' + '.txt', 'a+') as f:
            #     f.write(str(i) + '        ' + pro_type + '        ' + str(input_text) + '        ' + str(join_text) + '\n')


# test_text = '나도 끝난다 뒤에가 그거 하나 갖고 말하는데 먼지 말하는데 깜빡'

# print(core_text_process(test_text))

