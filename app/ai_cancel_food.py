from app import db
from app.models import *
from flask import Blueprint, jsonify, request
import json



bp = Blueprint('ai_cancel_food', __name__, url_prefix='/delete')

@bp.route('', methods=['GET'])
def get_param():
    code = {"code" : 200}
    try:
        get_idx = request.args.get('idx')  # 'param_name'에 원하는 파라미터 이름을 넣어주세요
        q= Food.query.get(get_idx)    
        db.session.delete(q)
        db.session.commit()
        
        Food.query.all()
    except Exception:
        code['code'] = 500
        return json.dumps(code, ensure_ascii=False, indent=4)

    return json.dumps(code, ensure_ascii=False, indent=4)

