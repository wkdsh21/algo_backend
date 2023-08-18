from flask import Blueprint, jsonify, request
from PIL import Image  # 변경 필요
import json
import datetime
import requests
import re
from app.ai.stock.stock import stock
from difflib import SequenceMatcher


bp = Blueprint('ai_stock', __name__, url_prefix='/ai_stock')

@bp.route('/', methods=["POST"])
def ai_stock_api():
    print("dddddddd")
    if request.method == "POST":
        if 'image' in request.files:
            print("dddddddd")
            image = request.files['image']
        else:
            return "image null"
        print("dddddddd")
        image=Image.open(image)
        print("dddddddd")
        row=stock(image)
        if not row:
            return "이미지 탐색불가 OCR 사용"
        row=list(row)[0]
        responsedata={}
        responsedata["nutrition"]={
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
        responsedata["allergy"]="알수없음"
        responsedata["material"]="알수없음"
        # nutrition='{"1회제공량":"2.1","총내용량(g)":"86","총내용량(mL)":"0","에너지(㎉)":"205","단백질(g)":"0","지방(g)":"0","탄수화물(g)":"2","총당류(g)":"0","총 식이섬유(g)":"0","칼슘(㎎)":"0","철(㎍)":"0","마그네슘(㎎)":"카페인(㎎)":"0"0","칼륨(㎎)":"0","나트륨(㎎)":"0","비타민":"10","콜레스테롤(㎎)":"0","총 지방산(g)":"0",}'
        nutrition=row[3]
        # responsedata["name"]='롯데)자일리톨베타비타D용기86G'
        responsedata["name"]=row[2]
        # match = re.search(r'\d', responsedata["name"])
        # if match:
        #     # 숫자가 발견된 경우, 해당 위치부터 문자열의 끝까지를 삭제합니다.
        #     index = match.start()
        #     responsedata["name"] = responsedata["name"][:index]
        responsedata["date"]=str(datetime.date.today())
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
            return "이미지 탐색불가 OCR 사용"
        max=0
        with open('./app/ai/stock/output.txt', 'r') as f:
            for line in f:  # 한 줄씩 읽기
                prob=SequenceMatcher(None, responsedata["name"], line.strip()).ratio()
                if max<prob:  # 줄 바꿈 문자 제거 후 출력
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
                allergy=data["body"]["items"][0]["item"]["allergy"]
                rawmtrl
                if rawmtrl=="알수없음" and allergy=="알수없음":
                    return json.dumps(responsedata)
                else:
                    print(rawmtrl)
                    parts=rawmtrl.split(",") if rawmtrl!="알수없음" else []
                    if parts!=[]:
                        #(,) 괄호 안에 쉼표는 무시하는 코드
                        processed_parts = []

                        inside_parentheses = False
                        current_part = ""

                        for part in parts:
                            if '(' in part and ')' in part:
                                processed_parts.append(part)
                            elif '(' in part:
                                inside_parentheses = True
                                current_part = part
                            elif ')' in part:
                                inside_parentheses = False
                                current_part += ',' + part
                                processed_parts.append(current_part)
                            elif inside_parentheses:
                                current_part += ',' + part
                            else:
                                processed_parts.append(part)
                        print(processed_parts)
                        #괄호밖은 삭제 괄호안에있는 원재료들 리스트에추가
                        for idx,val in enumerate(processed_parts):
                            if "(" in val:
                                start=val.find("(")
                                end=val.find(")")
                                processed_parts.pop(idx)
                                for i in val[start+1:end].split(","):
                                    processed_parts.insert(idx,i)
                    print(processed_parts)
                    responsedata["material"]=processed_parts
                    responsedata["allergy"]=allergy.split(",") if allergy!="알수없음" else []
            else:
                return json.dumps(responsedata)
        else:
            print("API 요청 실패:", response.status_code)
        print(responsedata)
        return json.dumps(responsedata)
