from flask import Blueprint, jsonify, request
from app.models import *
from app import db
import json

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=["POST"])
def register_api():
    if request.method == "POST":
        if User.query.all():
            q = User.query.get(1)
            db.session.delete(q)
            db.session.commit()
        data = request.json
        try:
            q = User(name=data["name"],age=data["age"],sex=data["sex"],allergy=json.dumps(data["allergy"],ensure_ascii=False),hate=json.dumps(data["hate"],ensure_ascii=False),weight=data["weight"],height=data["height"])
            db.session.add(q)
            db.session.commit()
        except:
            return json.dumps({'code': 500})
        return json.dumps({'code': 200})