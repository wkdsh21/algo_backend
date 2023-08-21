from flask import Blueprint, jsonify, request
from app.models import *
from app.models import *
from app import db
import json
import wikipediaapi
import openai

bp = Blueprint('wiki', __name__, url_prefix='/material')

@bp.route('', methods=["GET"])
def login_api():
    if request.method == "GET":
        name=request.args.get("name")
        wiki = wikipediaapi.Wikipedia("ko")
        page = wiki.page(name)  # 검색어에 해당되는 페이지 전체 가져오기
        if page.exists() == False:
            return None
        # print("제목: ", page.title)  # 제목확인, 요약, url 확인
        # print("요약: ", page.summary)
        # print("url: ", page.fullurl)
        # print(page.text)  # 전체 페이지 내용 보여주기
        return page.summary
