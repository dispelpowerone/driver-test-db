from fastapi import FastAPI
from .models.tests import GetTestsRequest, GetTestsResponse
from .service import DatabaseService

service = DatabaseService(
    "/Users/d.vasilyev/Workspace/quiz-dataset-tools/output/ny_positions/build/main.db"
)
app = FastAPI()


@app.post("/tests/get")
async def get_tests(req: GetTestsRequest) -> GetTestsResponse:
    return service.get_tests(req)