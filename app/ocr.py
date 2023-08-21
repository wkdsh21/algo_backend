from flask import Blueprint, jsonify, request
from PIL import Image
import json
import datetime
import requests
import re
from app.ai.stock.stock import stock
from difflib import SequenceMatcher
import os
import uuid
import time
from app.models import *
from app import db
import sqlite3

bp = Blueprint('ocr', __name__, url_prefix='/ocr')

@bp.route('', methods=["POST"])
def ocr_api():
    if request.method == "POST":
        responsedata={  "useridx":1,
                        "hate":[],
                        "idx":1,
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
        
        if 'image' in request.files:
            image = request.files['image']
        else:
            return "image null"
        
        api_url = 'https://dru0jyamtv.apigw.ntruss.com/custom/v1/24333/588d160384902c3d25c0b2e6f81fed5b4d7430703bec6b924e528c922c1c4690/general'
        secret_key = 'WmVycWdsZnNzSU9FdXBkV3VmWlhpRmprQVJQQ0RNS2o='

        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }

        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
            ('file', image)
        ]
        headers = {
            'X-OCR-SECRET': secret_key
        }

        response = requests.request(
            "POST", api_url, headers=headers, data=payload, files=files)
        if response.status_code == 200:
            check = 0
            result = response.json()
            for item in result['images'][0]['fields']:
                print(f"{item['inferText']} ")
            max=0
            check=0
            for item in result['images'][0]['fields']:
                if check==0:
                    pattern = r'[^0-9%가-힣 ]+'
                    row = re.split(pattern, item['inferText'])
                    with open('./app/ai/stock/name.txt', 'r') as f:
                        for line in f:  # 한 줄씩 읽기
                            if check==0:
                                li=line.strip()
                                if li.find('(')!=-1 and li.find(')')!=-1:
                                    li=li[:li.find('(')]
                                for i in row:
                                    prob=SequenceMatcher(None, i, li).ratio()
                                    if li and i and max<prob:
                                        max=prob
                                        maxword=li
                                        print(prob)
                                        print(maxword)
                                        if prob>0.9:
                                            check=1
                                            break
                            else:
                                break
                else:
                    break
            if max>0.8:
                responsedata["name"]=maxword
                print(maxword)
        else:
            print(f"API 요청 에러: {response.status_code}")
        conn = sqlite3.connect('./app/ai/stock/ocr.db')

        # 커서 생성
        cursor = conn.cursor()
        select_query = f"SELECT nutrition FROM Ocr WHERE name LIKE'%{maxword}%'" # WHERE 뒤엔 '' 무조건 붙이기

        cursor.execute(select_query)
        # 결과 가져오기
        result = cursor.fetchall()
        print(result)
        if result: 
            responsedata["nutrition"]=json.loads(result[-1][0])

        # 응답 확인 및 JSON 데이터 파싱
        url = f"https://apis.data.go.kr/B553748/CertImgListServiceV2/getCertImgListServiceV2?serviceKey=VR%2F13txmreE9yEgJXJq34c1S37YXK%2Fg3vy9gzqJA3NsillraiJuAW6QheGbVl7WZTL3etaxdvJpCz%2FjhDKQ5Iw%3D%3D&prdlstNm={responsedata['name']}&returnType=json&pageNo=1&numOfRows=10"
        response = requests.get(url)
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
                    if responsedata["allergy"]:
                        responsedata["allergy"][-1]=responsedata["allergy"][-1][:-2]
            else:
                q = Food(useridx=1,name=responsedata["name"],nutrition=json.dumps(responsedata["nutrition"],ensure_ascii=False),date=datetime.date.today(),hate=json.dumps(responsedata["hate"],ensure_ascii=False),material=json.dumps(responsedata["material"],ensure_ascii=False))
                db.session.add(q)
                db.session.commit()
                return json.dumps(responsedata,ensure_ascii=False)
        else:
            print("API 요청 실패:", response.status_code)

        q = Food(useridx=1,name=responsedata["name"],nutrition=json.dumps(responsedata["nutrition"],ensure_ascii=False),date=datetime.date.today(),hate=json.dumps(responsedata["hate"],ensure_ascii=False),material=json.dumps(responsedata["material"],ensure_ascii=False))
        db.session.add(q)
        db.session.commit()
        return json.dumps(responsedata,ensure_ascii=False)
        # return "200"