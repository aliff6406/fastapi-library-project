import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Message" : "Home Page"}
    
def main():
    """Launched with `poetry run start`"""
    uvicorn.run("fastapi_project.main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()