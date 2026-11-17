# Automated Multi-Platform Posting System

A Python FastAPI service that automatically publishes a short message across multiple third-party platforms independently.

## Features
- **Strict Input Validation**: Enforces a 200-character limit and verifies the presence of exactly one HTTP/HTTPS CTA link.
- **5 Platform Integrations**: X (Twitter), LinkedIn, DEV.to, Mastodon, and Reddit.
- **Fault-Tolerant Concurrent Execution**: Uses `asyncio.gather` so failures on one platform never block posting to others.

## Local Setup & Execution

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 4000
   ```

5. Run unit tests:
   ```bash
   pytest
   ```

## API Documentation
Open `http://localhost:4000/docs` after starting the server.

## Sample Request & Response

### Request
```http
POST http://localhost:4000/posting
Content-Type: application/json

{
  "message": "Check out our latest business platform and grow your online visibility. https://example.com"
}
```

### Response
```json
{
  "success": true,
  "results": [
    {
      "platform": "X (Twitter)",
      "status": "success",
      "posted_url": "https://x.com/i/web/status/1234567890",
      "public_access": true,
      "date": "2026-11-17",
      "time": "11:27:00",
      "error": null
    },
    {
      "platform": "LinkedIn",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": null,
      "time": null,
      "error": "Missing LinkedIn credentials."
    }
  ]
}
```
