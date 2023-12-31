from flask import Blueprint, jsonify, request
from app.models import *
from app import db
import json
import datetime

bp = Blueprint('todayfood', __name__, url_prefix='/todayfood')

@bp.route('', methods=["GET"])
def todayfood_api():
    if request.method == "GET":
        query = Food.query.filter(Food.date==datetime.date.today()).all()
        res={"foods":[]}
        for i in query:
            q=i.__dict__
            q.pop("_sa_instance_state")
            q.pop("idx")
            q.pop("useridx")
            for j in q:
                try:
                    q[j]=json.loads(q[j])
                except:
                    pass
            res["foods"].append(q)
            
        return json.dumps(res,ensure_ascii=False)