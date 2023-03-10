from fastapi import FastAPI

app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'Root': 'please no more ginger 🤮'}

@app.get('/chord_predict')
def index():
    return {'to_implement': True}

# run sudo docker run -e PORT=8000 -p 8080:8000 human1 (local)
# docker run -e PORT=8000 -p 8080:8000 $GCR_MULTI_REGION/$GCP_PROJECT_ID/$DOCKER_IMAGE_NAME .
