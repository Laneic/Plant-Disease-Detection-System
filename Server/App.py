from flask import Flask
import numpy as np
from  tensorflow import keras
from tensorflow.keras.models import model_from_json
from plantDisease import plantDiseaseClasses
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
jsonFile = open("E:/Plant-Disease-Detection-System/model/trainedModel.json",'r')
plantModelJson = jsonFile.read()
plantModel = model_from_json(plantModelJson)
plantModel.load_weights("E:/Plant-Disease-Detection-System/model/modelWeight.h5")
jsonFile.close()

def predictDisease():
    
    imagePath="E:/Plant-Disease-Detection-System/server/image.jpeg"
    newImg =keras.utils.load_img(imagePath, target_size=(256, 256))
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

@app.route('/predict')
def predict():
    diseaseName=predictDisease()
    return diseaseName

if __name__ == '__main__': #Server running
    app.run()


