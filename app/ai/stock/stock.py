import torch
from torchvision import transforms
from PIL import Image  # 변경 필요
import torch.nn as nn
from torch.cuda.amp import autocast
from timm.models import create_model
import sqlite3

def stock(img):
    class LotteNet(nn.Module):
        def __init__(self, cfg):
            super(LotteNet, self).__init__()
            self.model = create_model(
                model_name=cfg.model.model_name,
                pretrained=cfg.model.pretrained,
                num_classes=cfg.model.num_classes,
                drop_rate=cfg.model.drop_rate,
                drop_path_rate=cfg.model.drop_path,
            )

        @autocast()
        def forward(self, x):
            output = self.model(x)
            return output

    # 모델 로드
    a = torch.load(
        "./app/ai/stock/weight/best_top1_validation.pth",
        map_location=torch.device("cpu"),
    )

    model = LotteNet(a["cfg"])
    model.load_state_dict(a["model"])
    model.eval()

    # 이미지 전처리 함수 정의
    preprocess = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    # 이미지 불러오기 및 전처리
    image = img
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)  # 모델 입력 형태로 변환

    # 추론
    with torch.no_grad():
        output = model(input_batch)

    # 확률값 계산
    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    # 가장 확률이 높은 클래스 인덱스와 확률값 찾기
    max_prob, max_idx = torch.max(probabilities, dim=0)

    # 클래스 인덱스와 확률값 출력
    print("Predicted class index:", max_idx.item())
    print("Predicted class probability:", max_prob.item())
    print("Predicted class itemcode:",a["label_to_name"][max_idx.item()])
    labels=a["label_to_name"][max_idx.item()]
    # SQL 쿼리 작성
    conn = sqlite3.connect('algo.db')
    # 커서 생성
    cursor = conn.cursor()
    select_query = f"SELECT * FROM Stock WHERE itemCode='{labels}'" # WHERE 뒤엔 '' 무조건 붙이기

    cursor.execute(select_query)
    # 결과 가져오기
    result = cursor.fetchall()

    # 결과 출력
    for row in result:
        print(row)
    
    return result