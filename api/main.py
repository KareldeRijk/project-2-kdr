from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import boto3
import base64
from pydantic import BaseModel

app = FastAPI()

# CORS-Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client('s3')

CLASS_NAMES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

def load_model():
    try:
        bucket_name = "project-image-classification-models"
        object_key = "vgg16_model.keras"
        
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        model_data = response['Body'].read()
        
        with open("/tmp/temp_model.keras", "wb") as f:
            f.write(model_data)
        
        model = tf.keras.models.load_model("/tmp/temp_model.keras")
        return model
    except Exception as e:
        raise Exception(f"Error loading the model: {str(e)}")

model = load_model()

def process_image(image_data):
    try:
        image = tf.image.decode_image(image_data, channels=3)
        image = tf.image.resize(image, [32, 32])
        image = tf.expand_dims(image, 0) 
        image = image / 255.0
        
        predictions = model.predict(image)
        
        top_5_idx = np.argsort(predictions[0])[-5:][::-1]
        
        results = [
            {
                "class": CLASS_NAMES[idx],
                "confidence": round(float(predictions[0][idx]), 4)
            }
            for idx in top_5_idx
        ]
        
        return results
    except Exception as e:
        raise Exception(f"Fehler bei der Bildverarbeitung: {str(e)}")

class ImageRequest(BaseModel):
    image: str

@app.post("/classify")
async def predict_image(request: ImageRequest):
    try:
        image_data = base64.b64decode(request.image)
        result = process_image(image_data)
        
        return {"predictions": result}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
