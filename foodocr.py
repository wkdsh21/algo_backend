import requests
import uuid
import time
import json

api_url = 'https://dru0jyamtv.apigw.ntruss.com/custom/v1/24333/588d160384902c3d25c0b2e6f81fed5b4d7430703bec6b924e528c922c1c4690/general'
secret_key = 'WmVycWdsZnNzSU9FdXBkV3VmWlhpRmprQVJQQ0RNS2o='
image_file = './4.jpg'

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
    ('file', open(image_file, 'rb'))
]
headers = {
    'X-OCR-SECRET': secret_key
}

response = requests.request(
    "POST", api_url, headers=headers, data=payload, files=files)
if response.status_code == 200:
    check = 0
    result = response.json()
    for item in result['images'][0]['fields']:
        print(f"{item['inferText']} ")
    for item in result['images'][0]['fields']:
        if "제품명" in item['inferText'] and check == 0:
            check = 1
        else:
            print(f"제품명은 {item['inferText']} 입니다.")
            break
    al = input("가지고있는 알러지 입력: ")
    for item in result['images'][0]['fields']:
        if al in item['inferText']:
            print(f"{al}함유 섭취금지!!")
            break
else:
    print(f"API 요청 에러: {response.status_code}")
