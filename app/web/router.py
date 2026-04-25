from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.query_service import QueryService
from app.core.logging_config import logger
import os

# Setup templates directory
templates_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_path)

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main search page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    """
    Process search query and render results page.
    """
    logger.info(f"Web Search Query: {query}")
    
    # Use the same QueryService as the API
    response = QueryService.process_query(query)
    
    # Convert WhatsApp-style bold/italic to HTML-style if needed
    # (Actually Jinja2 | safe and keeping markdown-ish style for simplicity, 
    # but could replace here)
    formatted_reply = response.reply.replace("*", "<strong>").replace("<strong>", "</strong>", 0) # Simple hack
    # Let's do a better replacement for *
    import re
    html_reply = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', response.reply)
    html_reply = html_reply.replace('\n', '<br>')

    return templates.TemplateResponse(
        "results.html", 
        {
            "request": request, 
            "query": query, 
            "reply": html_reply, 
            "intent": response.intent
        }
    )
