"""
AWS Lambda handler for image classification using a pre-trained CNN model.
This module provides functionality to classify images into 10 different categories
using a TensorFlow model stored in S3 or locally.
"""

import json
import base64
import numpy as np
import tensorflow as tf
import boto3
import os

# Initialize S3 client for model retrieval
s3 = boto3.client('s3')

# Define the possible classification categories
CLASS_NAMES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']

# Global variable to store the loaded model
model = None

# Common CORS headers for all responses
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
    'Access-Control-Allow-Methods': 'POST,OPTIONS'
}

def load_model():
    """
    Load the trained CNN model either from local storage or S3 bucket.
    
    The function implements a singleton pattern to avoid reloading the model
    on every request. It checks if the model is already loaded and only loads
    it if necessary.
    
    Returns:
        tf.keras.Model: The loaded TensorFlow model
        
    Raises:
        Exception: If there's an error loading the model
    """
    global model
    if model is None:
        try:
            if os.getenv('IS_OFFLINE'):
                # Load model from local storage when running offline
                model_path = "models/TL_DN201_M4.keras"
                model = tf.keras.models.load_model(model_path)
            else:
                # Load model from S3 when running in AWS Lambda
                bucket_name = "project-image-classification-models"
                object_key = "TL_DN201_M4.keras"
                
                response = s3.get_object(Bucket=bucket_name, Key=object_key)
                model_data = response['Body'].read()
                
                # Save model temporarily to disk (required for Lambda)
                with open("/tmp/model.keras", "wb") as f:
                    f.write(model_data)
                
                model = tf.keras.models.load_model("/tmp/model.keras")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    return model

def process_image(image_data):
    """
    Process and classify an input image using the loaded model.
    
    Args:
        image_data (bytes): Raw image data to be processed
        
    Returns:
        list: List of dictionaries containing top 3 predictions with their confidence scores
        
    Raises:
        Exception: If there's an error during image processing
    """
    try:
        # Decode and preprocess the image
        image = tf.image.decode_image(image_data, channels=3)
        image = tf.image.resize(image, [224, 224])  # Resize to model's expected input size
        image = tf.expand_dims(image, 0)  # Add batch dimension
        image = image / 255.0  # Normalize pixel values
        
        # Load model and make predictions
        model = load_model()
        predictions = model.predict(image)
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        
        # Format results
        results = [
            {
                "class": CLASS_NAMES[idx],
                "confidence": round(float(predictions[0][idx]), 4)
            }
            for idx in top_3_idx
        ]
        
        return results
    except Exception as e:
        raise Exception(f"Error during image processing: {str(e)}")

def lambda_handler(event, context):
    """
    AWS Lambda handler function that processes incoming HTTP requests.
    
    This function handles the main request flow:
    1. Validates the incoming request
    2. Extracts and decodes the image data
    3. Processes the image and gets predictions
    4. Returns the results in a standardized format
    
    Args:
        event (dict): The event data from AWS Lambda
        context (LambdaContext): The runtime information from AWS Lambda
        
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code
            - headers: CORS and other HTTP headers
            - body: JSON string containing predictions or error message
    """
    # Handle OPTIONS request for CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': ''
        }

    try:
        # Validate and extract image data from request
        if 'body' in event:
            body = json.loads(event['body'])
            if 'image' in body:
                image_data = base64.b64decode(body['image'])
            else:
                return {
                    'statusCode': 400,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'error': 'No image found in the request'})
                }
        else:
            return {
                'statusCode': 400,
                'headers': CORS_HEADERS,
                'body': json.dumps({'error': 'Invalid request format'})
            }
        
        # Process image and get predictions
        result = process_image(image_data)
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'predictions': result})
        }
    
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        } 