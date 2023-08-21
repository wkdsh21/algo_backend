from flask import Blueprint, jsonify, request
from app.models import *
from app.models import *
from app import db
import json
bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('', methods=["GET"])
def login_api():
    if request.method == "GET":
        q = User.query.get(1)
        q=q.__dict__
        q.pop("_sa_instance_state")
        for j in q:
            try:
                q[j]=json.loads(q[j])
            except:
                pass
        return json.dumps(q)