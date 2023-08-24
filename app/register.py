from flask import Blueprint, jsonify, request
from app.models import *
from app import db
import json

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('', methods=["POST"])
def register_api():
    if request.method == "POST":
        if User.query.all():
            q = User.query.get(1)
            db.session.delete(q)
            db.session.commit()
        data = request.json
        try:
            if 12<=data["age"]<=19:
                data["kcal"]=135.3-30.8*data["age"]+1.23*(10.0*data["weight"]+934*data["height"])
            elif 20<=data["age"]:
                if data["sex"]=='M':
                    data["kcal"]=662-9.53*data["age"]+1.18*(15.91*data["weight"]+539.6*data["height"])
                else:
                    data["kcal"]=354-6.91*data["age"]+1.20*(9.36*data["weight"]+726*data["height"])
            q = User(name=data["name"],age=data["age"],sex=data["sex"],allergy=json.dumps(data["allergy"],ensure_ascii=False),hate=json.dumps(data["hate"],ensure_ascii=False),weight=data["weight"],height=data["height"],kcal=data["kcal"])
            db.session.add(q)
            db.session.commit()
        except:
            return json.dumps({'code': 500})
        return json.dumps({'code': 200})