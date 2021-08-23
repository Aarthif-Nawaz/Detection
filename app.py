from flask import Flask, request, jsonify
import os
import cv2
import easyocr
import warnings
import shutil
import imutils

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['SECRET_KEY'] = "asadbsjdnsfkslnkslfnmksdfmnaskldasd"


@app.route('/api/getData', methods=['GET', 'POST'])
def readData():
    if request.method == "POST":
        try:
            filename_data = request.files['passport']
        except:
            return jsonify({'Result': 'Please Provide Passport as a key and the Image as Value !'})
        shutil.rmtree('Passport')
        os.mkdir('Passport')
        filename_data.save(os.path.join(os.getcwd(), f'Passport/{filename_data.filename}'))
        try:
            reader = easyocr.Reader(['en'], gpu=True)
            bounds = reader.readtext(os.path.join(os.getcwd(), f'Passport/{filename_data.filename}'))
            for i in bounds:
                if str(i[1]).__contains__("<"):
                    passport = str(i[1]).split("<")
                    passport = list(filter(None, passport))
                    if passport[0] == "P":
                        name = passport[-3:]
                        name = ' '.join([str(elem) for elem in name])
                        country = passport[1][0:3]
                        if name.__contains__(country):
                            name = name.replace(country, '')
                        return jsonify({
                            'Name': name,
                            'Country': country
                        })
            image = cv2.imread(os.path.join(os.getcwd(), f'Passport/{filename_data.filename}'))
            rotated = imutils.rotate_bound(image, 270)
            reader = easyocr.Reader(['en'], gpu=True)
            bounds = reader.readtext(rotated)
            for i in bounds:
                if str(i[1]).__contains__("<"):
                    passport = str(i[1]).split("<")
                    passport = list(filter(None, passport))
                    if passport[0] == "P":
                        name = passport[-3:]
                        name = ' '.join([str(elem) for elem in name])
                        country = passport[1][0:3]
                        if name.__contains__(country):
                            name = name.replace(country, '')
                        return jsonify(
                            {
                                'Name': name,
                                'Country': country
                            }
                        )
            return jsonify({'Result': 'Please Provide A Clear Image Of Passport'})
        except Exception as e:
            print(e)
            return jsonify({'Result': 'An Error Occurred'})

    else:
        return jsonify({'Result': 'Please Provide an Image Of Passport'})


if __name__ == "__main__":
    app.run()
