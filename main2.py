from flask import Flask, request, jsonify
import server
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename
import skimage.draw
import imageio
import cv2
from io import BytesIO
from urllib import parse
# import cStringIO as StringIO
app = Flask(__name__)


@app.route('/')
def home():
    return '연결 성공!'


# localhost:5000/image
# 갤러리에서 이미지를 보내면 분석을 해서 다시 리턴해주는 부분.
# 분석하는 코드는 없음.
@app.route('/image', methods=['POST', 'GET'])
def image():
    import base64
    import json
    # image = request.files['file']
    # imgdata = base64.b64decode(str(image))
    # image_str = request.args.get('image')
    # url_decode = parse.unquote(image_str)
    # image_str = url_decode.replace("data:image/png;base64,", "");
    # image_bytes = base64.b64decode(image_str)

    image_str = request.form['image']
    url_decode = parse.unquote(image_str)
    image_str = url_decode.replace("data:image/png;base64,", "");
    image_bytes = base64.b64decode(image_str)

    print(type(image_str))
    print(type(url_decode))
    print(type(image_str))
    print(type(image_bytes))
    print(image_bytes)


    # filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    # with open("imageToSave.jpg", "wb") as fh:
    #     fh.write(base64.decodebytes(imgdata))
    # stream = StringIO.StringIO(image_bytes)
    # img = Image.open(stream)
    # img.show()

    # image_bytes = image_bytes.read()
    im = Image.open(BytesIO(image_bytes))
    # im.show()
    im.save('test.jpg')


    # image_string = base64.b64encode(image.read())
    # tmp = Image.open(image)
    # tmp.show()
    # tmp.save('test.jpg')
    # image_string 을 분석기에 보내서 분석하는 코드가 필요
    # if image:
    #     filename = secure_filename(image.filename)
    model = "C:/Users/user/PycharmProjects/maskrcnn-custom/logs/mask_rcnn_experiment_0096.h5"
    #1. 이미지 저장후 보내기
    color, shape = server.get_img_inform(model, "C:/Users/user/PycharmProjects/maskrcnn-custom/23.python_server/test.jpg")
    #2. 저장없이 보내기
    # color, shape = server.get_img_inform(model, image)
    print(shape, color)
    # shape = "circle"
    # color = "black"
    return jsonify(
        shape=shape,
        color=color
    )

# localhost:5000/image
# 갤러리에서 이미지를 보내면 분석을 해서 다시 리턴해주는 부분.
# 분석하는 코드는 없음.
@app.route('/image1', methods=['POST', 'GET'])
def image2():
    import base64
    import json
    # image_string 을 분석기에 보내서 분석하는 코드가 필요
    shape = "circle"
    color = "black"
    return jsonify(
        shape=shape,
        color=color
    )


# 앱에서 사용자가 데이터를 수정해주면 그 정보를 바탕으로 크롤링 하는 부분
@app.route('/crawl', methods=['POST', 'GET'])
def crawl():
    #POST방식
    # shape = request.form['shape']
    # color = request.form['color']
    # text = request.form['text']

    #GET방식
    shape = request.args.get('shape')
    color = request.args.get('color')
    text = request.args.get('text')
    # image_string 을 분석기에 보내서 분석하는 코드가 필요

    # shape = 'circle'
    # color = 'white'
    print(shape, color, text)
    total = server.crawling_get_link_img_name(shape, color, text)

    # tmp = {'medicine_name' : '인데놀정10mg',
    #        'medicine_image' : 'https://terms.naver.com/entry.naver?docId=2141123&cid=51000&categoryId=51000',
    #        'link' : 'https://dbscthumb-phinf.pstatic.net/3323_000_20/20210803233503184_NG6OQL73C.jpg/A11ABBBBB090302.jpg?type=m250&wm=N'}
    # tmp2 = {'medicine_name' : '소론도정',
    #         'medicine_image' : 'https://terms.naver.com/entry.naver?docId=2140285&cid=51000&categoryId=51000',
    #         'link' : 'https://dbscthumb-phinf.pstatic.net/3323_000_9/20171126022112845_RQZOH3G3T.jpg/A11A4290B001503.jpg?type=m250&wm=N'}
    # total = [tmp,tmp2]

    # 서버에서 string값 두개 리턴하는 코드 여기다가 넣어야함.
    return jsonify(
        total = total
    )


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True,host="220.125.156.59",port=5000)
