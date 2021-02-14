from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def order_KB():
    # 1. 클라이언트가 준 name, num, address, phone 가져오기.
    name_receive = request.form['name_give']
    num_receive = request.form['num_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone-give']

    # 2. DB에 정보 삽입하기
    doc = {
        'name': name_receive,
        'num': num_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    db.order_list.insert_one(doc)
    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문이 완료되었습니다!'})


@app.route('/order', methods=['GET'])
def read_orders():
    order_list = list(db.order_list.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'data': order_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
