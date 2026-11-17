from fastapi import FastAPI, HTTPException
from app.schemas import PostRequest, PostResponse
from app.services.posting_service import PostingService

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="FastAPI service to automatically publish short messages across multiple platforms.",
    version="1.0.0",
)

posting_service = PostingService()

@app.post("/posting", response_model=PostResponse)
async def post_message(payload: PostRequest):
    try:
        results = await posting_service.broadcast(payload.message)
        return PostResponse(success=True, results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Automated Multi-Platform Posting System"}
