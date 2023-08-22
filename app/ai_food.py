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

import os

from app.ai.food import food_analyse
#pip install openai
import openai


bp = Blueprint('ai_food', __name__, url_prefix='/foodcnn')

@bp.route('', methods=['POST'])
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
            print(names)

            food_names = food_analyse.get_food_name(names)
            print(food_names)
            #음식 무게 추출
            food_weight = food_analyse.get_food_weight(r"C:\AI\fooddata\yolov3\456.jpg")
            # print(food_weight)
            
            #음식 영양소 추출
            nut_path = r"C:\AI\fooddata\yolov3\음식분류 AI 데이터 영양DB.xlsx"
            nutritional = food_analyse.get_nutritional_information(food_names[0],food_weight,nut_path)
            
            #딕셔너리 형태로 저장
            food_dict = food_analyse.food_response_dto(nutritional)
            #print(food_dict)
            
            #gpt 답변
            prompt = compare_food_and_standard_value(food_dict)
            food_dict["prompt"] = prompt

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
    #영양분 하루 기준치
    standard_value ={
        "kcal": 0.0,
        "protein": 55.0,
        "fat": 54.0,
        "glucide": 324.0,
        "sugar": 100.0,
        "dietaryfiber": 25.0,
        "calcium": 700.0,
        "Iron": 12.0,
        "magnesium": 315.0,
        "caffeine": 0.0,
        "Potassium": 3500.0,
        "Natrium": 2000.0,
        "vitamin": 0.0,
        "cholesterol": 300.0,
        "fatty": 0.0,
        "transfat": 0.0
    }
    
    json_standard_value =json.dumps(standard_value)
    
    #방금 먹은 음식 영양정보
    json_food_dict = json.dumps(food_dict["nutrition"])

    #지금까지 총 영양소
    today_user_nutrution = today_all_nutrution()
    json_today = json.dumps(today_user_nutrution)    
    
    #오늘 총영양소 + 방금 먹은 음식 영양정보 와 지금까지 오늘 총 영양소 비교
    #gpt?? or 임의 설정?
    prompt =f"""
    하루 기준 영양분 : {json_standard_value}, \n 
    지금까지 먹은 총 영양소: {json_today}, \n 
    이제 먹을 음식 영양소 : {json_food_dict}, \n 
    이제 먹을 음식 영양소와 지금까지 먹을 음식 영양소를 더해서 하루 기준 영양소와 분석해주고 
    이제 먹을 음식 영양소를 섭취했을 때, 위험한 영양소를 0~ 2가지를 알려줘 , 너가 무엇을 했는지 말고 결과값을 답변해줘. 총 답변은 100자 이내로 답변해줘.(한국어로 답변)"""
    
    result = use_gpt_api(prompt)
    return result


def today_all_nutrution():
    all_nutrition = []
    today_nurtition = Food.query.filter(Food.useridx == 1, Food.date == datetime.date.today()).all()
    for food in today_nurtition:
        food_dict = json.loads(food.nutrition)
        all_nutrition.append(food_dict)
    
    sum_dict = {}
    for d in all_nutrition:
        for key, value in d.items():
            if key in sum_dict:
                try:
                    print(type(value))
                    sum_dict[key] += float(value)
                except ValueError:
                    pass  # 변환 실패 시 무시
            else:
                try:
                    sum_dict[key] = float(value)
                except ValueError:
                    pass  # 변환 실패 시 무시

    print(sum_dict)
    return(sum_dict)


def use_gpt_api(prompt):
    OPENAI_YOUR_KEY = "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"
    openai.api_key = OPENAI_YOUR_KEY

    MODEL = "gpt-3.5-turbo"
    USER_INPUT_MSG = prompt

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a Korean nutritionist"},
            {"role": "user", "content": USER_INPUT_MSG}, 
            {"role": "assistant", "content": "Who's there?"},
        ],
        temperature=0,
    )
    return response['choices'][0]['message']['content']
