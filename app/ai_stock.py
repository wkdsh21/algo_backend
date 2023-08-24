from flask import Blueprint, jsonify, request
from PIL import Image  # 변경 필요
import json
import datetime
import requests
import re
from app.ai.stock.stock import stock
from difflib import SequenceMatcher
import os
from app.models import *
from app import db

bp = Blueprint('ai_stock', __name__, url_prefix='/stockcnn')

@bp.route('', methods=["POST"])
def ai_stock_api():
    print("dddddddd")
    if request.method == "POST":
        if 'image' in request.files:
            image = request.files['image']
        else:
            return "image null"
        image_path = os.path.join("./", "image.jpg")

        # 이미지 데이터를 파일에 저장
        with open(image_path, "wb") as image_file:
            image_file.write(image.read())
        image=Image.open(image)
        row,prob=stock(image)
        if prob<0.5:
            return json.dumps({"idx":-1})
        if not row:
            return json.dumps({"idx":-1})
        row=list(row)[0]
        responsedata={  "hate":[],
                        "idx":0,
                        "allergy":[],
                        "material":[],
                        "name":"",
                        "date":str(datetime.date.today()),
                        "nutrition":{
                        "kcal": 0,
                        "protein": 0,
                        "fat": 0,
                        "glucide": 0,
                        "sugar": 0,
                        "dietaryfiber": 0,
                        "calcium": 0,
                        "Iron": 0,
                        "magnesium": 0,
                        "caffeine": 0,
                        "Potassium": 0,
                        "Natrium": 0,
                        "vitamin": 0,
                        "cholesterol": 0,
                        "fatty": 0,
                        "transfat": 0
                        }
                    }
        # nutrition='{"1회제공량":"2.1","총내용량(g)":"86","총내용량(mL)":"0","에너지(㎉)":"205","단백질(g)":"0","지방(g)":"0","탄수화물(g)":"2","총당류(g)":"0","총 식이섬유(g)":"0","칼슘(㎎)":"0","철(㎍)":"0","마그네슘(㎎)":"카페인(㎎)":"0"0","칼륨(㎎)":"0","나트륨(㎎)":"0","비타민":"10","콜레스테롤(㎎)":"0","총 지방산(g)":"0",}'
        nutrition=row[3]
        # responsedata["name"]='롯데)자일리톨베타비타D용기86G'
        responsedata["name"]=row[2]
        # match = re.search(r'\d', responsedata["name"])
        # if match:
        #     # 숫자가 발견된 경우, 해당 위치부터 문자열의 끝까지를 삭제합니다.
        #     index = match.start()
        #     responsedata["name"] = responsedata["name"][:index]
        start=nutrition.find('"마그네슘(㎎)"')
        end=nutrition.find('"칼륨(㎎)"')
        nutrition=nutrition[:start]+nutrition[end:-2]+nutrition[-1]
        nutrition=json.loads(nutrition)


        dict={"에너지(㎉)":"kcal","단백질(g)":"protein","지방(g)":"fat","탄수화물(g)":"glucide","총당류(g)":"sugar","총 식이섬유(g)":"dietaryfiber","칼슘(㎎)":"calcium","철(㎍)":"Iron","마그네슘(㎎)":"magnesium","카페인(㎎)":"caffeine","칼륨(㎎)":"Potassium","나트륨(㎎)":"Natrium","비타민":"vitamin","콜레스테롤(㎎)":"cholesterol","총 지방산(g)":"fatty","트랜스지방(g)":"transfat"}
        try:
            for i in nutrition:
                if i in dict:
                    if dict[i] in responsedata["nutrition"]:
                        responsedata["nutrition"][dict[i]]=float(nutrition[i])
        except:
            return json.dumps({"idx":-1})
        max=0
        with open('./app/ai/stock/name.txt', 'r') as f:
            for line in f:  # 한 줄씩 읽기
                prob=SequenceMatcher(None, responsedata["name"], line.strip()).ratio()
                if max<prob:
                    max=prob
                    maxword=line.strip()
        if max>0.5:
            responsedata["name"]=maxword
            print(max,maxword)
        print(max,maxword)
        # API 엔드포인트 URL
        url = f"https://apis.data.go.kr/B553748/CertImgListServiceV2/getCertImgListServiceV2?serviceKey=VR%2F13txmreE9yEgJXJq34c1S37YXK%2Fg3vy9gzqJA3NsillraiJuAW6QheGbVl7WZTL3etaxdvJpCz%2FjhDKQ5Iw%3D%3D&prdlstNm={responsedata['name']}&returnType=json&pageNo=1&numOfRows=10"
        # url = "https://apis.data.go.kr/B553748/CertImgListServiceV2/getCertImgListServiceV2?serviceKey=VR%2F13txmreE9yEgJXJq34c1S37YXK%2Fg3vy9gzqJA3NsillraiJuAW6QheGbVl7WZTL3etaxdvJpCz%2FjhDKQ5Iw%3D%3D&prdlstNm=새우깡&returnType=json&pageNo=1&numOfRows=10"
        # GET 요청 보내기
        response = requests.get(url)

        # 응답 확인 및 JSON 데이터 파싱
        if response.status_code == 200:
            data = response.json()
            if data["body"]["totalCount"]!='0':
                rawmtrl=data["body"]["items"][0]["item"]["rawmtrl"]
                rawmtrl=rawmtrl if rawmtrl!="알수없음" else []
                allergy=data["body"]["items"][0]["item"]["allergy"]
                allergy=allergy if allergy!="알수없음" else []
                if not(rawmtrl or allergy):
                    q = Food(useridx=1,name=responsedata["name"],nutrition=json.dumps(responsedata["nutrition"],ensure_ascii=False),date=datetime.date.today(),hate=json.dumps(responsedata["hate"],ensure_ascii=False),material=json.dumps(responsedata["material"],ensure_ascii=False))
                    db.session.add(q)
                    db.session.commit()
                    responsedata["idx"]=q.idx
                    return json.dumps(responsedata,ensure_ascii=False)
                else:
                    if rawmtrl:
                        print(rawmtrl)
                        pattern = r'[^0-9%.]'
                        rawmtrl = ''.join(re.findall(pattern, rawmtrl))
                        print(rawmtrl)
                        pattern = r'[^가-힣]+'
                        rawmtrl = re.split(pattern, rawmtrl)
                        rawmtrl=list(set(rawmtrl))
                        print(rawmtrl)
                        with open('./app/ai/stock/material.txt', 'r', encoding='utf-8') as f:
                            responsedata["material"]=[line.strip() for line in f if line.strip() in rawmtrl]
                        print(responsedata["material"])
                        with open('./app/ai/stock/hate.txt', 'r', encoding='utf-8') as f:
                            responsedata["hate"]=[line.strip() for line in f if line.strip() in responsedata["material"]]
                    responsedata["allergy"]=allergy.split(",") if allergy else []
                    response["allergy"][-1]=response["allergy"][-1][:-2]
                    # for i in rawmtrl:
                    #     max=0
                    #     with open('./app/ai/stock/material.txt', 'r', encoding='utf-8') as f:
                    #         for line in f:
                    #             if i in line.strip():
                    #                 prob=SequenceMatcher(None, i, line.strip()).ratio()
                    #                 if max<prob:
                    #                     max=prob
                    #                     maxword=line.strip()
                    #     responsedata["material"].append(maxword)
                    # responsedata["material"]=list(set(responsedata["material"]))
                    # print(responsedata["material"])
                    # parts=rawmtrl.split(",") if rawmtrl!="알수없음" else []
                    # if parts!=[]:
                    #     #(,) 괄호 안에 쉼표는 무시하는 코드
                    #     processed_parts = []

                    #     inside_parentheses = False
                    #     current_part = ""

                    #     for part in parts:
                    #         if '(' in part and ')' in part:
                    #             processed_parts.append(part)
                    #         elif '(' in part:
                    #             inside_parentheses = True
                    #             current_part = part
                    #         elif ')' in part:
                    #             inside_parentheses = False
                    #             current_part += ',' + part
                    #             processed_parts.append(current_part)
                    #         elif inside_parentheses:
                    #             current_part += ',' + part
                    #         else:
                    #             processed_parts.append(part)
                    #     print(processed_parts)
                    #     #괄호밖은 삭제 괄호안에있는 원재료들 리스트에추가
                    #     for idx,val in enumerate(processed_parts):
                    #         if "(" in val:
                    #             start=val.find("(")
                    #             end=val.find(")")
                    #             processed_parts.pop(idx)
                    #             for i in val[start+1:end].split(","):
                    #                 processed_parts.insert(idx,i)
                    # print(processed_parts)
                    # responsedata["material"]=processed_parts
                    # responsedata["allergy"]=allergy.split(",") if allergy!="알수없음" else []
            else:
                q = Food(useridx=1,name=responsedata["name"],nutrition=json.dumps(responsedata["nutrition"],ensure_ascii=False),date=datetime.date.today(),hate=json.dumps(responsedata["hate"],ensure_ascii=False),material=json.dumps(responsedata["material"],ensure_ascii=False))
                db.session.add(q)
                db.session.commit()
                responsedata["idx"]=q.idx
                return json.dumps(responsedata,ensure_ascii=False)
        else:
            print("API 요청 실패:", response.status_code)
        print(responsedata)
        q = Food(useridx=1,name=responsedata["name"],nutrition=json.dumps(responsedata["nutrition"],ensure_ascii=False),date=datetime.date.today(),hate=json.dumps(responsedata["hate"],ensure_ascii=False),material=json.dumps(responsedata["material"],ensure_ascii=False))
        db.session.add(q)
        db.session.commit()
        responsedata["idx"]=q.idx
        return json.dumps(responsedata,ensure_ascii=False)
