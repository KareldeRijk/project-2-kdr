import json
import base64
import numpy as np
import tensorflow as tf
import boto3

s3 = boto3.client('s3')

CLASS_NAMES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

model = None

def load_model():
    global model
    if model is None:
        try:
            bucket_name = "project-image-classification-models"
            object_key = "vgg16_model.keras"
            
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            model_data = response['Body'].read()
            
            with open("/tmp/model.keras", "wb") as f:
                f.write(model_data)
            
            model = tf.keras.models.load_model("/tmp/model.keras")
        except Exception as e:
            raise Exception(f"Fehler beim Laden des Modells: {str(e)}")
    return model

def process_image(image_data):
    try:
        # Some images operations
        image = tf.image.decode_image(image_data, channels=3)
        image = tf.image.resize(image, [32, 32])
        image = tf.expand_dims(image, 0)
        image = image / 255.0
        
        model = load_model()
        
        predictions = model.predict(image)
        
        # Find top three predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        
        results = [
            {
                "class": CLASS_NAMES[idx],
                "confidence": round(float(predictions[0][idx]), 4)
            }
            for idx in top_3_idx
        ]
        
        return results
    except Exception as e:
        raise Exception(f"Errors during image processing: {str(e)}")

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event['body'])
            if 'image' in body:
                image_data = base64.b64decode(body['image'])
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No image found in the request'})
                }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid request format'})
            }
        
        result = process_image(image_data)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'predictions': result})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 