import os
import xml.etree.ElementTree as ET
import sqlite3
# 주어진 폴더 경로
main_folder = r'C:\Users\sh\Desktop\상품 이미지(가공식품ai)\상품 이미지\Validation'
# 데이터베이스 파일 생성 또는 연결
conn = sqlite3.connect('algo.db')
# 커서 생성
cursor = conn.cursor()
# 주어진 폴더 안에 있는 모든 폴더 불러오기
subfolders = [f.path for f in os.scandir(main_folder) if f.is_dir()]

# 각 폴더에서 두 번째 파일의 텍스트 불러오기
for subfolder in subfolders:
    files = [f.name for f in os.scandir(subfolder) if f.is_file()]
    if len(files) >= 2:
        second_file_path = os.path.join(subfolder, files[1])
        try:
            with open(second_file_path, 'r',encoding='utf-8') as file:
                file_contents = file.read()
                # XML 파싱
                root = ET.fromstring(file_contents)

                # 원하는 정보 추출
                for stock in root.findall('div_cd'):
                    name = stock.find('img_prod_nm').text
                    itemCode = stock.find('item_cd').text
                    nutrition = stock.find('nutrition_info').text
                    # SQL 쿼리 작성
                    insert_query = "INSERT INTO Stock (itemCode, name, nutrition) VALUES (?, ?, ?)"
                    # 데이터 삽입
                    data_to_insert = (itemCode, name, nutrition)
                    cursor.execute(insert_query, data_to_insert)
                    # 변경사항 저장
                    conn.commit()
        except Exception as e:
            print(f"Error reading file '{second_file_path}': {e}")
    else:
        print(f"Not enough files in '{subfolder}' to retrieve second file.\n")


# import sqlite3
# conn = sqlite3.connect('algo.db')
# cursor = conn.cursor()
# insert_query = "DELETE FROM Stock where idx!=0"
# cursor.execute(insert_query)
# conn.commit()