# Project-2
This repository contains a deep learning project implementing Convolutional Neural Networks (CNNs) for image classification. Trained on CIFAR-10 dataset, which consists of 60,000 32x32 color images in 10 classes, with 6,000 images per class. The model achieves high accuracy in recognizing and categorizing images across multiple animal classes. Built using TensorFlow/Keras, with data preprocessing, model training, evaluation, and visualization included.

## Project Overview

### Project Structure
```
File Structure:
├── data/                   # License free test images
├── api/                    # API implementation for model serving
├── web/                    # Web interface for model interaction
├── notebooks/              # Jupyter notebooks containing model development, training, and evaluation
│   ├── Base CNN Model/     # Basic CNN implementation and training
│   ├── VGG16/              # VGG16 transfer learning implementation
│   ├── DenseNet201/        # DenseNet201 transfer learning implementation
│   └── preprocessing.ipynb # Data preprocessing and preparation
```

### Model Architecture
The project implements three different approaches:

1. **Custom CNN Model**
   - Basic convolutional neural network
   - Data augmentation with random flips and rotations
   - Achieved accuracy: ~85%

2. **VGG16 Transfer Learning**
   - Pre-trained VGG16 model as base
   - Fine-tuned for CIFAR-10 classification
   - Achieved accuracy: ~85%
   - Best performance without freezing layers

3. **DenseNet201 Transfer Learning**
   - Pre-trained DenseNet201 model as base
   - Fine-tuned for CIFAR-10 classification
   - Achieved accuracy: ~93%
   - Best overall performance with optimized hyperparameters

### Key Features
- Data preprocessing and normalization
- Data augmentation techniques
- Model training and evaluation
- Performance visualization
- AWS Lambda deployment for inference
- Model storage in AWS S3

### Technical Implementation
- Built with TensorFlow/Keras
- Python-based implementation
- AWS integration for deployment
- Comprehensive evaluation metrics (accuracy, precision, recall, F1-score)

## Deployment
The model is deployed as an AWS Lambda function with the following features:
- REST API endpoint for image classification
- S3 integration for model storage
- Support for base64 encoded image input
- CORS enabled for cross-origin requests

## Model Tracking
Track model performance and experiments:
https://docs.google.com/spreadsheets/d/1v45NI5V2AYiYLz7QQBh2qrkOevQ912NchR29SLfgEtc/edit?usp=sharing

## Final Models
DenseNet201<br />
https://project-image-classification-models.s3.eu-central-1.amazonaws.com/TL_DN201_M4.keras<br /><br />

VGG16<br />
https://project-image-classification-models.s3.eu-central-1.amazonaws.com/vgg16_model.keras

## Getting Started
1. Clone the repository
2. Install dependencies
3. Run the preprocessing notebook
4. Train the model using either approach
5. Deploy to AWS Lambda for inference

## Dependencies
- TensorFlow
- NumPy
- Matplotlib
- Seaborn
- scikit-learn
- AWS SDK (boto3)