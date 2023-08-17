# from flask import Blueprint, jsonify, request
# import torch
# from torchvision import transforms
# from PIL import Image  # 변경 필요
# import torch.nn as nn
# from torch.cuda.amp import autocast
# from timm.models import create_model
# import sqlite3
import json
import datetime
import requests
# # 데이터베이스 파일 생성 또는 연결
# conn = sqlite3.connect('algo.db')
# # 커서 생성
# cursor = conn.cursor()

# bp = Blueprint('ai_stock', __name__, url_prefix='/ai_stock')

# @bp.route('/', methods=['GET', 'POST'])
# def form_list():
#     if request.method == "GET":

# class LotteNet(nn.Module):
#     def __init__(self, cfg):
#         super(LotteNet, self).__init__()
#         self.model = create_model(
#             model_name=cfg.model.model_name,
#             pretrained=cfg.model.pretrained,
#             num_classes=cfg.model.num_classes,
#             drop_rate=cfg.model.drop_rate,
#             drop_path_rate=cfg.model.drop_path,
#         )

#     @autocast()
#     def forward(self, x):
#         output = self.model(x)
#         return output

# # 모델 로드
# a = torch.load(
#     r"C:\Users\sh\Desktop\algohack/best_top1_validation.pth",
#     map_location=torch.device("cpu"),
# )

# model = LotteNet(a["cfg"])
# model.load_state_dict(a["model"])
# model.eval()

# # 이미지 전처리 함수 정의
# preprocess = transforms.Compose(
#     [
#         transforms.Resize((224, 224)),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ]
# )

# # 이미지 불러오기 및 전처리
# image_path = "C:/Users/sh/Desktop/상품 이미지(가공식품ai)/최종_Lotte-MEGA/pretrained/base/checkpoint/10100_0_s_2.jpg"  # 테스트할 이미지의 경로
# image = Image.open(image_path)
# input_tensor = preprocess(image)
# input_batch = input_tensor.unsqueeze(0)  # 모델 입력 형태로 변환

# # 추론
# with torch.no_grad():
#     output = model(input_batch)

# # 확률값 계산
# probabilities = torch.nn.functional.softmax(output[0], dim=0)

# # 가장 확률이 높은 클래스 인덱스와 확률값 찾기
# max_prob, max_idx = torch.max(probabilities, dim=0)

# # 클래스 인덱스와 확률값 출력
# print("Predicted class index:", max_idx.item())
# print("Predicted class probability:", max_prob.item())
# print("Predicted class itemcode:",a["label_to_name"][max_idx.item()])
# labels=a["label_to_name"][max_idx.item()]
# # SQL 쿼리 작성
# select_query = f"SELECT * FROM Stock WHERE itemCode='{labels}'" # WHERE 뒤엔 '' 무조건 붙이기

# cursor.execute(select_query)
responsedata=dict()
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
# 결과 가져오기
# result = cursor.fetchall()

# 결과 출력
# for row in result:
#     print(row)
# nutrition=list(result[0])[3]


responsedata["name"]='롯데)자일리톨베타비타D용기86G'
responsedata["date"]=str(datetime.date.today())
nutrition='{"1회제공량":"2.1","총내용량(g)":"86","총내용량(mL)":"0","에너지(㎉)":"205","단백질(g)":"0","지방(g)":"0","탄수화물(g)":"2","총당류(g)":"0","총 식이섬유(g)":"0","칼슘(㎎)":"0","철(㎍)":"0","마그네슘(㎎)":"카페인(㎎)":"0"0","칼륨(㎎)":"0","나트륨(㎎)":"0","비타민":"10","콜레스테롤(㎎)":"0","총 지방산(g)":"0",}'
start=nutrition.find('"마그네슘(㎎)"')
end=nutrition.find('"칼륨(㎎)"')
nutrition=nutrition[:start]+nutrition[end:-2]+nutrition[-1]
request=dict(json.loads(nutrition))

print(dict(json.loads(nutrition))) #삭제

dict={"에너지(㎉)":"kcal","단백질(g)":"protein","지방(g)":"fat","탄수화물(g)":"glucide","총당류(g)":"sugar","총 식이섬유(g)":"dietaryfiber","칼슘(㎎)":"calcium","철(㎍)":"Iron","마그네슘(㎎)":"magnesium","카페인(㎎)":"caffeine","칼륨(㎎)":"Potassium","나트륨(㎎)":"Natrium","비타민":"vitamin","콜레스테롤(㎎)":"cholesterol","총 지방산(g)":"fatty","트랜스지방(g)":"transfat"}
for i in request:
    if i in dict:
        if dict[i] in responsedata["nutrition"]:
            responsedata["nutrition"][dict[i]]=float(request[i])

# API 엔드포인트 URL
# url = f"https://apis.data.go.kr/B553748/CertImgListServiceV2/getCertImgListServiceV2?serviceKey=VR%2F13txmreE9yEgJXJq34c1S37YXK%2Fg3vy9gzqJA3NsillraiJuAW6QheGbVl7WZTL3etaxdvJpCz%2FjhDKQ5Iw%3D%3D&prdlstNm={responsedata['name']}&returnType=json&pageNo=1&numOfRows=10"
url = "https://apis.data.go.kr/B553748/CertImgListServiceV2/getCertImgListServiceV2?serviceKey=VR%2F13txmreE9yEgJXJq34c1S37YXK%2Fg3vy9gzqJA3NsillraiJuAW6QheGbVl7WZTL3etaxdvJpCz%2FjhDKQ5Iw%3D%3D&prdlstNm=새우깡&returnType=json&pageNo=1&numOfRows=10"
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
            print("OCR ㄱㄱ")
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
        print("OCR ㄱㄱ")
else:
    print("API 요청 실패:", response.status_code)
    
print(responsedata) #삭제
