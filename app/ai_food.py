from flask import Blueprint, jsonify, request
import torch
from torchvision import transforms
from PIL import Image  # 변경 필요
import torch.nn as nn
from torch.cuda.amp import autocast
from timm.models import create_model
import io
import json
import datetime
import requests
import re
from app import db
from app.models import *

#from app.ai.stock.stock import stock
import os

from app.ai.food import food_analyse


bp = Blueprint('ai_food', __name__, url_prefix='/foodcnn')

@bp.route('/', methods=['POST'])
def ai_stock_api():
    if request.method == "POST":
        image_data = request.files['image'].read()
        image = Image.open(io.BytesIO(image_data))

        try:

            #이미지 저장
            delete_and_save_image(r"app\ai\food\data\samples", image_data)

            #이미지 분석
            food_analyse.detect_image()
            
            #이름 받아오기
            names = food_analyse.get_name(r"app\ai\food\output\__image.xml")
            # print(names)

            food_names = food_analyse.get_food_name(names)
            # print(food_names)
            #음식 무게 추출
            food_weight = food_analyse.get_food_weight(r"C:\AI\fooddata\yolov3\456.jpg")
            # print(food_weight)
            
            #음식 영양소 추출
            nut_path = r"C:\AI\fooddata\yolov3\음식분류 AI 데이터 영양DB.xlsx"
            nutritional = food_analyse.get_nutritional_information(food_names[0],food_weight,nut_path)
            
            #딕셔너리 형태로 저장
            food_dict = food_analyse.food_response_dto(nutritional)
            #print(food_dict)
            
            #db 저장
            db_pull_data = store_db(food_dict)  
            
            #json 변환
            json_string = json.dumps(db_pull_data, ensure_ascii=False, indent=4)  # indent 옵션으로 가독성을 높일 수 있음

            
        except Exception:
            error = {"idx" : -1}
            return json.dumps(error, ensure_ascii=False, indent=4)

       
          
        return json_string

    return "post 오류"



def delete_and_save_image(folder_path, image_data):
    # 기존 "__"로 시작하는 파일들을 삭제
    delete_files_with_prefix(folder_path, "__")

    # 이미지 파일 저장 경로 생성
    image_path = os.path.join(folder_path, "__image.jpg")

    # 이미지 데이터를 파일에 저장
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)

    print("Image saved successfully.")

def delete_files_with_prefix(folder_path, prefix):
    file_list = os.listdir(folder_path)

    for filename in file_list:
        if filename.startswith(prefix):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Deleted: {filename}")


def store_db(responsedata):
    q = Food(useridx=1,name=responsedata["name"],nutrition=json.dumps(responsedata["nutrition"],ensure_ascii=False),date=datetime.date.today(),hate=json.dumps(responsedata["hate"],ensure_ascii=False),material=json.dumps(responsedata["material"],ensure_ascii=False))
    db.session.add(q)
    db.session.commit()
    
    responsedata["idx"] = q.idx
    return responsedata


def compare_food_and_standard_value(food_dict):
    3