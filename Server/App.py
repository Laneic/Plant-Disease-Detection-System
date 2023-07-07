from flask import Flask, request
import numpy as np
from  tensorflow import keras
from tensorflow.keras.models import model_from_json
from plantDisease import plantDiseaseClasses
from flask_cors import CORS, cross_origin
import os
import requests
from dotenv.main import load_dotenv

app = Flask(__name__)
CORS(app)
baseDirectory= os.path.join(os.getcwd(),'Model')
app.config['CORS_HEADERS'] = 'Content-Type'
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
    diseasedesc = openAIAPI(className[1])
    output={
        "plantName": className[0],
        "disease": className[1],
        "diseaseDesc": diseasedesc
    }

    return output

def openAIAPI(diseaseName):
    load_dotenv()
    apiKey = os.environ['API_KEY']
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {apiKey}',
        'Content-Type': 'application/json'
    }
    data = {
        'messages': [
            {'role': 'user', 'content': f'Give me information about {diseaseName}'},        
        ],"model": "gpt-3.5-turbo",
    }
    response = requests.post(url, headers=headers, json=data)
    jsonResponse = response.json()
    generatedResponse = jsonResponse['choices'][0]['message']['content']
    return generatedResponse

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    if 'formIMAGE' in request.files:
        postImage = request.files['formIMAGE']

        return predictDisease(postImage)
    else:
        return 'No image file received'

if __name__ == '__main__': #Server running
    app.run()




