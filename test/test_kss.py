txt ='우리 생일을 만들어 주신 분들이 알 수 있다면 감사하고 싶어 너무 감사하다고 고맙다고 10분 백번 천번 만번 말하고 싶어'
# import time

# # 사용 input_text
# with open('/mnt/c/Users/kooli/mrmind/chatbot/v.0.0.2_2022.08.24/wiboe_dev_v2/user_input_text.txt', 'r', encoding='utf-8') as f:
#     sentences = f.readlines()

# ##############################################################################################################################################################
# for txt in sentences:

#     start = time.time()
#     import kss

#     print("------Kks-----")

#     for index, sent in enumerate(kss.split_sentences(txt)):
#         print(index,':', sent)

#     print("time :", time.time() - start)

#     ##############################################################################################################################################################

#     start = time.time()
#     from kiwipiepy import Kiwi

#     kiwi = Kiwi()

#     print("------kiwipiepy-----")

#     for index, sent in enumerate(kiwi.split_into_sents(txt)):
#         print(index,':', sent[0])

#     print("time :", time.time() - start, '\n')

import mecab

mec = mecab.MeCab()

text = ['안녕하세요',
        '그러세요',
        '내가 말하잖아', 
        '더이상 그럴일은 없겠어', 
        '그런게 더 많겠지', 
        '걘 아직도 잘살잖아', 
        '그렇게 살다가 죽겠지', 
        '그러면 와이프가 싫겠지', 
        '나한테 말하겠군',
        '더이상 그럴일은 없겠군',
        '그런게 더 많겠군',
        '그렇게 살다가 죽겠군'
        ]

for txt in text:
    print(mec.pos(txt))



