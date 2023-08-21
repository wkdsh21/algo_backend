import xml.etree.ElementTree as ET
import csv
import pandas as pd
from app.ai.food.testgo import return_weight
from app.ai.food.detect_1231 import detect 
from datetime import datetime
import re

#필요한 것 음식 판단 모델, 중량 예상 모델
#영양데이터, 'name' : '음식이름' 데이터

#이미지 분석 후 저장
def detect_image():
    cfg = r'app\ai\food\cfg\yolov3-spp-403cls.cfg'
    names = r'app\ai\food\data\403food.names'
    weights = r'app\ai\food\weights\best_403food_e200b150v2.pt'
    source = r'app\ai\food\data\samples'
    output = r'app\ai\food\output'
    img_size = 255
    conf_thres = 0.3
    iou_thres = 0.5
    half = False
    view_img = False
    save_txt = False
    save_xml = True
    classes = None
    agnostic_nms = False
    augment = False

    detect(cfg, names, weights, source, output, img_size, conf_thres, iou_thres, half, view_img, save_txt, save_xml, classes, agnostic_nms, augment)


#xml 에서 name(id) 받아오기
def get_name(path):
    
    # XML 파일을 파싱하여 ElementTree 객체 생성
    tree = ET.parse(path)
    root = tree.getroot()

    
    # name 태그의 값을 가져오기
    names = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        names.append(name)
    
    return names    

#xml에서 받은 중량값 리턴 
def get_food_weight(path):
    weight_num = return_weight(path)
    weight_dict = {
        0 : 0.25,
        1 : 0.50,
        2 : 0.75,
        3 : 1.00,
        4 : 1.25,
    }
    return weight_dict.get(weight_num)


#xml에서 받아온 name을 이용해서 음식이름을 return
def get_food_name(names):    
    foodnames = {
        '01011001':'쌀밥',
        '01012003':'보리밥',
        '01012002':'콩밥',
        '01012001':'잡곡밥',
        '01013002':'곤드레밥',
        '01013001':'감자밥',
        '01014004':'일반비빔밥',
        '01014003':'볶음밥',
        '01014002':'주먹밥',
        '01014001':'김치볶음밥',
        '01012004':'돌솥밥',
        '01014005':'전주비빔밥',
        '01014006':'삼선볶음밥',
        '01014007':'새우볶음밥',
        '01014008':'알밥',
        '01014009':'산채비빔밥',
        '01014010':'오므라이스',
        '01014011':'육회비빔밥',
        '01014012':'해물볶음밥',
        '01014013':'열무비빔밥',
        '01015002':'불고기덮밥',
        '01015003':'소고기국밥',
        '01015004':'송이덮밥',
        '01015005':'오징어덮밥',
        '01015006':'자장밥',
        '01015007':'잡채밥',
        '01015008':'잡탕밥',
        '01015009':'장어덮밥',
        '01015010':'제육덮밥',
        '01015011':'짬뽕밥',
        '01015012':'순대국밥',
        '01015013':'카레라이스',
        '01015014':'전주콩나물국밥',
        '01015015':'해물덮밥',
        '01015016':'회덮밥',
        '01015017':'소머리국밥',
        '01015018':'돼지국밥',
        '01016001':'김치김밥',
        '01016002':'농어초밥',
        '01016003':'문어초밥',
        '01016004':'새우초밥',
        '01016005':'새우튀김롤',
        '01016006':'샐러드김밥',
        '01016007':'광어초밥',
        '01016008':'소고기김밥',
        '01016009':'갈비삼각김밥',
        '01016010':'연어롤',
        '01016011':'연어초밥',
        '01016012':'유부초밥',
        '01016013':'장어초밥',
        '01016014':'참치김밥',
        '01016015':'참치마요삼각김밥',
        '01016016':'충무김밥',
        '01016017':'치즈김밥',
        '01016018':'캘리포니아롤',
        '01016019':'한치초밥',
        '02011001':'간자장',
        '02011002':'굴짬뽕',
        '02011003':'기스면',
        '02011004':'김치라면',
        '02011005':'김치우동',
        '02011006':'김치말이국수',
        '02011007':'닭칼국수',
        '02011008':'들깨칼국수',
        '02011009':'떡라면',
        '02011010':'라면',
        '02011011':'막국수',
        '02011012':'메밀국수',
        '02011013':'물냉면',
        '02011014':'비빔국수',
        '02011015':'비빔냉면',
        '02011016':'삼선우동',
        '02011017':'삼선자장면',
        '02011018':'삼선짬뽕',
        '02011019':'수제비',
        '02011020':'쌀국수',
        '02011021':'열무김치국수',
        '02011023':'오일소스스파게티',
        '02011024':'일식우동',
        '02011025':'볶음우동',
        '02011027':'자장면',
        '02011028':'잔치국수',
        '02011029':'짬뽕',
        '02011030':'짬뽕라면',
        '02011031':'쫄면',
        '02011032':'치즈라면',
        '02011033':'콩국수',
        '02011034':'크림소스스파게티',
        '02011035':'토마토소스스파게티',
        '02011036':'해물칼국수',
        '02011037':'회냉면',
        '02011038':'떡국',
        '02011039':'떡만둣국',
        '02012001':'고기만두',
        '02012002':'군만두',
        '02012003':'김치만두',
        '02012004':'물만두',
        '02012005':'만둣국',
        '03011001':'게살죽',
        '03011002':'깨죽',
        '03011003':'닭죽',
        '03011004':'소고기버섯죽',
        '03011005':'어죽',
        '03011006':'잣죽',
        '03011007':'전복죽',
        '03011008':'참치죽',
        '03011009':'채소죽',
        '03011010':'팥죽',
        '03011011':'호박죽',
        '03012001':'콘스프',
        '03012002':'토마토스프',
        '04011001':'굴국',
        '04011002':'김치국',
        '04011003':'달걀국',
        '04011004':'감자국',
        '04011005':'미역국',
        '04011006':'바지락조개국',
        '04011007':'소고기무국',
        '04011008':'소고기미역국',
        '04011009':'소머리국밥',
        '04011010':'순대국',
        '04011011':'어묵국',
        '04011012':'오징어국',
        '04011013':'토란국',
        '04011014':'탕국',
        '04011015':'홍합미역국',
        '04011016':'황태해장국',
        '04012001':'근대된장국',
        '04012002':'미소된장국',
        '04012003':'배추된장국',
        '04012004':'뼈다귀해장국',
        '04012005':'선지(해장)국',
        '04012006':'콩나물국',
        '04012007':'시금치된장국',
        '04012008':'시래기된장국',
        '04012009':'쑥된장국',
        '04012010':'아욱된장국',
        '04012011':'우거지된장국',
        '04012012':'우거지해장국',
        '04012013':'우렁된장국',
        '04013002':'갈비탕',
        '04013003':'감자탕',
        '04013004':'곰탕',
        '04013005':'매운탕',
        '04013006':'꼬리곰탕',
        '04013007':'꽃게탕',
        '04013008':'낙지탕',
        '04013009':'내장탕',
        '04013010':'닭곰탕',
        '04013011':'닭볶음탕',
        '04013012':'지리탕',
        '04013013':'도가니탕',
        '04013014':'삼계탕',
        '04013015':'설렁탕',
        '04013017':'알탕',
        '04013018':'연포탕',
        '04013019':'오리탕',
        '04013020':'추어탕',
        '04013021':'해물탕',
        '04013022':'닭개장',
        '04013023':'육개장',
        '04014001':'미역오이냉국',
        '04015001':'고등어찌개',
        '04015002':'꽁치찌개 ',
        '04015003':'동태찌개',
        '04016001':'부대찌개',
        '04017001':'된장찌개',
        '04017002':'청국장찌개',
        '04018001':'두부전골',
        '04018002':'곱창전골',
        '04018003':'소고기전골',
        '04018004':'국수전골',
        '04019001':'돼지고기김치찌개',
        '04019002':'버섯찌개',
        '04019003':'참치김치찌개',
        '04019004':'순두부찌개',
        '04019005':'콩비지찌개',
        '04019006':'햄김치찌개',
        '04019007':'호박찌개',
        '05011001':'대구찜',
        '05011002':'도미찜',
        '05011004':'문어숙회',
        '15011020':'test4',
        '05011008':'아귀찜',
        '15011019':'test3',
        '05011010':'조기찜',
        '05011011':'참꼬막',
        '05011012':'해물찜',
        '16011007':'test2',
        '06012001':'닭갈비',
        '06012002':'닭꼬치',
        '06012003':'돼지갈비',
        '06012004':'떡갈비',
        '06012005':'불고기',
        '06012006':'소곱창구이',
        '06012007':'소양념갈비구이',
        '06012008':'소불고기',
        '06012009':'양념왕갈비',
        '06012010':'햄버거스테이크',
        '06012011':'훈제오리',
        '06012012':'치킨데리야끼',
        '06012013':'치킨윙',
        '06013001':'더덕구이',
        '06013002':'양배추구이',
        '06013003':'두부구이',
        '07011001':'가자미전',
        '07011002':'굴전',
        '07011003':'동태전',
        '07011004':'해물파전',
        '07012001':'동그랑땡',
        '07012002':'햄부침',
        '07012003':'육전',
        '07013001':'감자전',
        '07013002':'고추전',
        '07013003':'김치전',
        '07013004':'깻잎전',
        '07013005':'녹두빈대떡',
        '07013006':'미나리전',
        '07013007':'배추전',
        '07013008':'버섯전',
        '07013009':'부추전',
        '07013010':'야채전',
        '07013011':'파전',
        '07013012':'호박부침개',
        '07013013':'호박전',
        '07014001':'달걀말이',
        '07014002':'두부부침',
        '07014003':'두부전',
        '08011001':'건새우볶음',
        '08011002':'낙지볶음',
        '08011003':'멸치볶음',
        '08011004':'어묵볶음',
        '08011005':'오징어볶음',
        '08011006':'오징어채볶음',
        '08011007':'주꾸미볶음',
        '08011008':'해물볶음',
        '08012001':'감자볶음',
        '08012002':'김치볶음',
        '08012003':'깻잎나물볶음',
        '08012004':'느타리버섯볶음',
        '08012005':'두부김치',
        '08012006':'머위나물볶음',
        '08012007':'양송이버섯볶음',
        '08012008':'표고버섯볶음',
        '08012009':'고추잡채',
        '08012010':'호박볶음',
        '08013001':'돼지고기볶음',
        '08013002':'돼지껍데기볶음',
        '08013003':'소세지볶음',
        '08013004':'순대볶음',
        '08013005':'오리불고기',
        '08013006':'오삼불고기',
        '08014001':'떡볶이',
        '08014002':'라볶이',
        '08014003':'마파두부',
        '09011001':'가자미조림',
        '09011002':'갈치조림',
        '09011003':'고등어조림',
        '09011004':'꽁치조림',
        '09011005':'동태조림',
        '09011006':'북어조림',
        '09011007':'조기조림',
        '09011008':'코다리조림',
        '09012001':'달걀장조림',
        '09012002':'메추리알장조림',
        '09013001':'돼지고기메추리알장조림',
        '09013002':'소고기메추리알장조림',
        '09014001':'고추조림',
        '09014002':'감자조림',
        '09014003':'우엉조림',
        '09014004':'알감자조림',
        '09015001':'(검은)콩조림',
        '09015002':'콩조림',
        '09015003':'두부고추장조림',
        '10011001':'미꾸라지튀김',
        '10011002':'새우튀김',
        '10011003':'생선가스',
        '10011004':'쥐포튀김',
        '10011005':'오징어튀김',
        '10012001':'닭강정',
        '10012002':'닭튀김',
        '10012003':'돈가스',
        '10012004':'모래집튀김',
        '10012005':'양념치킨',
        '10012006':'치즈돈가스',
        '10012007':'치킨가스',
        '10012008':'탕수육',
        '10012009':'깐풍기',
        '10014001':'감자튀김',
        '10014002':'고구마맛탕',
        '10014003':'고구마튀김',
        '10014004':'고추튀김',
        '10014005':'김말이튀김',
        '10014006':'채소튀김',
        '11011001':'노각무침',
        '11011002':'단무지무침',
        '11011003':'달래나물무침',
        '11011004':'더덕무침',
        '11011005':'도라지생채',
        '11011006':'도토리묵',
        '11011007':'마늘쫑무침',
        '11011008':'무생채',
        '11011009':'무말랭이',
        '11011010':'오이생채',
        '11011011':'파무침',
        '11012001':'상추겉절이',
        '11012002':'쑥갓나물무침',
        '11012003':'청포묵무침',
        '11012004':'해파리냉채',
        '11013001':'가지나물',
        '11013002':'고사리나물',
        '11013003':'도라지나물',
        '11013004':'무나물',
        '11013005':'미나리나물',
        '11013006':'숙주나물',
        '11013007':'시금치나물',
        '11013009':'취나물',
        '11013010':'콩나물',
        '11013011':'고구마줄기나물',
        '11013012':'우거지나물무침',
        '11014001':'골뱅이무침',
        '11014002':'김무침',
        '11014003':'미역초무침',
        '11014004':'북어채무침',
        '11014005':'회무침',
        '11014006':'쥐치채',
        '11014007':'파래무침',
        '11014008':'홍어무침',
        '11015001':'잡채',
        '11015002':'탕평채',
        '12011001':'갓김치',
        '12011002':'고들빼기',
        '12011003':'깍두기',
        '12011004':'깻잎김치',
        '12011005':'나박김치',
        '12011006':'동치미',
        '12011007':'배추겉절이',
        '12011008':'배추김치',
        '12011009':'백김치',
        '12011010':'부추김치',
        '12011011':'열무김치',
        '12011012':'열무얼갈이김치',
        '12011013':'오이소박이',
        '12011014':'총각김치',
        '12011015':'파김치',
        '13011001':'간장게장',
        '13011002':'마늘쫑장아찌',
        '13011003':'고추장아찌',
        '13011004':'깻잎장아찌',
        '13011005':'마늘장아찌',
        '13011006':'무장아찌',
        '13011007':'양념게장',
        '13011008':'양파장아찌',
        '13011009':'오이지',
        '13011010':'무피클',
        '13011011':'오이피클',
        '13011012':'단무지',
        '13012001':'오징어젓갈',
        '13012002':'명란젓',
        '14011001':'생연어',
        '14011002':'생선물회',
        '15011018':'test1',
        '14011004':'광어회',
        '14011005':'훈제연어',
        '14012001':'육회',
        '14012002':'육사시미',
        '15011002':'경단',
        '15011001':'가래떡',
        '15011003':'꿀떡',
        '15011004':'시루떡',
        '15011005':'메밀전병',
        '15011006':'찰떡',
        '15011007':'무지개떡',
        '15011008':'백설기',
        '15011009':'송편',
        '15011010':'수수부꾸미',
        '15011011':'수수팥떡',
        '15011012':'쑥떡',
        '15011013':'약식',
        '15011014':'인절미',
        '15011015':'절편',
        '15011016':'증편',
        '15011017':'찹쌀떡',
        '16011001':'매작과',
        '16011002':'다식',
        '16011003':'약과',
        '16011004':'유과',
        '16011005':'산자',
        '16011006':'깨강정',
        '09016001':'땅콩조림',
        '01016020':'일반김밥',
        '01015019':'하이라이스',
        '02011040':'짜장라면',
        '11014009':'골뱅이국수무침',
        '11014010':'오징어무침',
        '04013024':'뼈해장국',
        '04019008':'고추장찌개',
        '05012001':'소갈비찜',
        '05012002':'돼지갈비찜',
        '05012003':'돼지고기수육',
        '05012004':'찜닭',
        '05012005':'족발',
        '05013001':'달걀찜',
        '06014001':'삼치구이'    
    }
    
    food_list = []
    for name in names:
        foodname = foodnames.get(name)
        food_list.append(foodname)

    return food_list
    


#음식이름과 중량값을 이용해서 영양정보 return(json format)
def get_nutritional_information(food_name, weight, nutritional_path):
    
    # 엑셀 파일 읽기
    df = pd.read_excel(nutritional_path)

    # 찾고자 하는 키(key)
    target_key = "name"
    target_value = food_name
    result_rows = df[df[target_key] == target_value]

    #영양성분에 weigt 값 곱하기
    final_nutritional = result_rows.applymap(lambda x: multiply_numeric(x, weight))
  
    return final_nutritional

#값 넣기
def food_response_dto(nutritional):
    #dict로 변환
    nutritional_dict = nutritional.to_dict(orient='index')
    
    #1번쨰 키값 변경 000 -> "nutrition", (idx, name) 변수 저장
    new_key = "nutrition"
    idx = next(iter(nutritional_dict))
    name = nutritional_dict[next(iter(nutritional_dict))]["name"]
    nutritional_dict[new_key] = nutritional_dict.pop(next(iter(nutritional_dict)))
    
    #dict 덮어쓰기, (name,idx) 값 넣기
    nutritional_dict = update_dict(nutritional_dict)
    # nutritional_dict["idx"] = idx
    nutritional_dict["name"] = name
    
    #date 넣기
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    nutritional_dict["date"] =formatted_date 

    #재료 넣기
    material = get_material(nutritional_dict["name"])
    nutritional_dict["material"] = material

    allergy = get_allergy(material)
    nutritional_dict["allergy"] = allergy

    print(nutritional_dict)
    return nutritional_dict

#재료 가져오기
def get_material(food_name):
    db_path = r"app\AI\food\data\TB_RECIPE_SEARCH-220701 (1).csv"
    with open(db_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # 첫 번째 행은 헤더로 가정
        headers = next(reader)
    
        # 컬럼 인덱스 찾기
        ckg_nm_idx = headers.index("CKG_NM")
        ckg_mtrl_cn_idx = headers.index("CKG_MTRL_CN")
        
        # 데이터 찾기
        for row in reader:
            if row[ckg_nm_idx] == food_name:
                ckg_mtrl_cn_value = row[ckg_mtrl_cn_idx]
                break  # 찾았으면 더 이상 검색하지 않음


    # '[재료]'와 '[숙주나물양념]' 등의 패턴을 찾아 재료 정보 추출
    pattern = r'\[.*?\]\s*(.*?)(?=\s*\[|$)'
    matches = re.findall(pattern, ckg_mtrl_cn_value)

    # 재료 정보를 다시 파싱하여 추출하고 '|'로 나눈 후 숫자 앞에서 자름
    ingredients_list = []
    for match in matches:
        ingredients = match.split('|')
        for ingredient in ingredients:
            cleaned_ingredient = ingredient.strip()
            if cleaned_ingredient:
                cleaned_ingredient = re.sub(r'\d+.*|약간', '',  cleaned_ingredient).rstrip()
                ingredients_list.append(cleaned_ingredient)
                
    #print(ingredients_list)
    return ingredients_list


#알레르기 성분 검출
def get_allergy(material):
    allergy_list =[
        "옥수수", "참깨", "콩", "감자", "사과", "카카오",
        "복숭아", "토마토", "키위", "망고", "바나나", "라임",
        "오렌지", "레몬", "땅콩", "호두", "밤", "밀", "보리",
        "쌀", "메밀", "마늘", "양파", "샐러리", "오이", "효모",
        "버섯", "계란", "우유", "게", "새우", "고등어", "돼지고기",
        "소고기", "치즈", "닭고기", "대구", "홍합", "참치", "연어",
        "조개", "오징어", "멸치"
    ]
    #print(material)

    allergy = []
    for material_value in material:
        for allergy_value in allergy_list:
            shortened_allergy_value = allergy_value[:2]
            if shortened_allergy_value in material_value:
                allergy.append(allergy_value)

    #print(allergy)
    return allergy




#스트링 제외 곱연산
def multiply_numeric(x, factor):
    if isinstance(x, (int, float)):
        return x * factor
    else:
        return x

#dict 덮어쓰기
def update_dict(other_dict):
    key_dict = {
        "idx": 0,
        "name": 0.0,
        "nutrition": {
            "kcal": 0.0,
            "protein": 0.0,
            "fat": 0.0,
            "glucide": 0.0,
            "sugar": 0.0,
            "dietaryfiber": 0.0,
            "calcium": 0.0,
            "Iron": 0.0,
            "magnesium": 0.0,
            "caffeine": 0.0,
            "Potassium": 0.0,
            "Natrium": 0.0,
            "vitamin": 0.0,
            "cholesterol": 0.0,
            "fatty": 0.0,
            "transfat": 0.0
        },
        "date": "YYYY-MM-DD",
        "hate": [],
        "allergy": [],
        "material": []
    }
    data = {
        key: other_dict.get(key, value) if isinstance(value, (int, float, str, list))
        else {k: other_dict["nutrition"].get(k, v) for k, v in value.items()}
        for key, value in key_dict.items()
    }
    return data

    
    


if __name__ == '__main__':
    #img 분석
    detect_image()
    #xml에서 name(id) 받아오기
    names = get_name(r"app\ai\food\output\__1.xml")
    #print(names)
    
    #id를 통해 food list 추출
    food_names = get_food_name(names)
    #print(food_names)
    
    #음식 무게 추출
    food_weight = get_food_weight(r"app\AI\food\data\samples\__3.jpg")
    #print(food_weight)

    #음식 영양소 추출
    nut_path = r"app\AI\food\data\음식분류 AI 데이터 영양DB.xlsx"
    nutritional = get_nutritional_information(food_names[0],food_weight,nut_path)
    #print(nutritional)

    food_dict = food_response_dto(nutritional)

   
   

