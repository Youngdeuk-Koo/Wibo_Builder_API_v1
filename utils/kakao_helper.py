import pymysql


def check_hotel_reserve(text) :
    text = text.replace(" ", "")
    locals = ["서울", "강원", "제주", "제주도", "강원도"]
    state = 0
    if "추천" in text and "호텔" in text  :
        state = 1
        for local in locals :
            if local in  text  :
                return True, 1, local
    return False, state, ""


def recommend_hotels(local) :
    category_code = 1

    if local == "강원" or local == "강원도" :
        category_code = 4
    elif local == "제주" or local == "제주도" :
        category_code = 7

    conn = pymysql.connect(host='54.180.88.116', port=3306,
                                user='root', passwd='7890uiop', db='wibo', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = "select id, title, img, link, cont from recommend_items where category_id = %s limit 10"
    curs.execute(sql, (category_code))
    rows = curs.fetchall()

    curs.close()
    conn.close()

    results = []
    for row in rows :
        item = {}
        item["title"] = row["title"]
        item["description"] = row["cont"]
        item["thumbnail"] = {"imageUrl": row["img"]}
        item["buttons"] = [{"action": "webLink", "label": "예약하기", "webLinkUrl": row["link"]}]

        results.append(item)
        #break
    return results

def response_list(title, tit_img, more_link, items) :
    
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": title
                           # "imageUrl": tit_img
                        },
                        "items": items,
                        
                        "buttons": [
                            {
                                "label": "더보기",
                                "action": "webLink",
                                "webLinkUrl": more_link
                            }
                        ]
                    }
                }
            ]
        }
    }
    return response
    



def response_card_sel(items) :
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": items
                    }
                }
            ]
        }
    }
    return response