from flask import Flask, request
import numpy as np
from  tensorflow import keras
from tensorflow.keras.models import model_from_json
from plantDisease import plantDiseaseClasses
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)
baseDirectory= os.path.join(os.getcwd(),'Model')
print(baseDirectory)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
jsonFile = open(os.path.join(baseDirectory,'trainedModel.json'),'r')
plantModelJson = jsonFile.read()
plantModel = model_from_json(plantModelJson)
plantModel.load_weights(os.path.join(baseDirectory,'modelweight.h5'))
jsonFile.close()

def predictDisease(postImage):
    imagePath = os.path.join(baseDirectory,'localImage')
    postImage.save(imagePath)
    newImg =keras.utils.load_img(imagePath, target_size=(256, 256))
    os.remove(imagePath)
    testImage = keras.utils.img_to_array(newImg)
    testImage = np.expand_dims(testImage, axis=0)
    testImage = testImage/255
    prediction = plantModel.predict(testImage)
    index=prediction.argmax(axis=-1)[0]
    className = plantDiseaseClasses[index]
    return className

@app.route('/')
def index():

    return

@cross_origin()

@app.route('/predict',methods=['POST'])
def predict():
    if 'formIMAGE' in request.files:
        postImage = request.files['formIMAGE']

        return predictDisease(postImage)
    else:
        return 'No image file received'
    diseaseName=predictDisease()

if __name__ == '__main__': #Server running
    app.run()


