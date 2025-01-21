from fastapi import FastAPI

app = FastAPI(title="PyTestCoder")

@app.get("/")
async def root():
    return {"message": "Welcome to PyTestCoder - A Test Development Project"}