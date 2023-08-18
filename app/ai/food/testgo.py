# import torch

# checkpoint = torch.load(r"C:\Users\sh\Desktop\음식이미지 및 영양성분 aihub\음식양추정\quantity_est\weights\new_opencv_ckpt_b84_e200.pth",map_location='cpu')
# model = checkpoint['model_ft']
# model.load_state_dict(checkpoint['state_dict'], strict=False)
# model.class_to_idx = checkpoint['class_to_idx']
# optimizer_ft = checkpoint['optimizer_ft']
# epochs = checkpoint['epochs']

import torch
from torch.autograd import Variable
from torchvision import transforms
from PIL import Image  # 변경 필요
import torch.nn as nn
from torch.cuda.amp import autocast
import torch.nn.functional as F
#from timm.models import create_model
import numpy as np

def return_weight(path):
        # 모델 로드
        checkpoint = torch.load(r"app\ai\food\weights\new_opencv_ckpt_b84_e200.pth",map_location='cpu')
        model = checkpoint['model_ft']
        model.load_state_dict(checkpoint['state_dict'], strict=False)
        model.eval()

        # 이미지 전처리 함수 정의
        preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])])

        # 이미지 불러오기 및 전처리
        image_path = path  # 테스트할 이미지의 경로
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        image = Image.open(image_path)
        image = preprocess(image)
        image = np.expand_dims(image, 0)
        image = torch.from_numpy(image)
        inputs = Variable(image).to(device)
        logits = model.forward(inputs)
        #print(logits)
        ps = F.softmax(logits, dim=1)
        topk = ps.cpu().topk(5)
        probs, classes=(e.data.numpy().squeeze().tolist() for e in topk)
        #print(probs,classes)
        return classes[0]
