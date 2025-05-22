# API Project

This project provides a REST API developed with Python and based on the Serverless Framework.

## Prerequisites

- Python 3.x
- Node.js and npm
- Docker (optional)
- AWS CLI (for deployment)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies:
```bash
npm install
```

## Development

### Local Development

1. Run the python script
````
python main.py
````

2. Test it
```
curl -X POST http://0.0.0.0:8000/ \
  -H "Content-Type: application/json" \
  -d '{"image": "'"$(base64 < dog.jpeg | tr -d '\n')"'"}'
```

## Deployment

```bash
serverless deploy
```

## Project Structure

- `main.py` - Main application logic
- `handler.py` - Lambda handler for Serverless
- `serverless.yml` - Serverless Framework configuration
- `Dockerfile` - Docker configuration
- `requirements.txt` - Python dependencies

## Test deployed API Endpoint

```
curl -X POST https://zl2pcttxj4.execute-api.eu-central-1.amazonaws.com/dev/classify \
  -H "Content-Type: application/json" \
  -d '{"image": "'"$(base64 < dog.jpeg | tr -d '\n')"'"}'
```

