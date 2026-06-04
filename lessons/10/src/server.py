from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/chat")
def chat(query: str = Query(..., description="The chat query of user")):
    job = queue.enqueue(process_query, query)
    return {"status": "queued", "job_id": job.id}


@app.get("/job-status")
def get_result(job_id: str = Query(..., description="The ID of the job")):
    job = queue.fetch_job(job_id)
    result = job.return_value()
    return {"status": "completed", "result": result}
