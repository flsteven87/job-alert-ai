"""
Crawler API endpoints for testing and triggering crawls.
"""
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import AnyHttpUrl, BaseModel

from app.services.crawler.crawler_service import CrawlerService

router = APIRouter()


class CrawlRequest(BaseModel):
    """
    Request model for crawling a URL.
    """
    url: AnyHttpUrl
    description: Optional[str] = None


class CrawlResponse(BaseModel):
    """
    Response model for crawl results.
    """
    url: str
    title: Optional[str] = None
    content_preview: str
    status: str
    processing_status: str


@router.post("/crawl", response_model=CrawlResponse, status_code=status.HTTP_200_OK)
async def crawl_url(request: CrawlRequest):
    """
    Crawl a URL and extract its content.
    
    This endpoint is for testing the crawler functionality and extraction logic.
    """
    crawler_service = CrawlerService()
    
    try:
        # 執行爬取和處理
        result = await crawler_service.crawl_and_process(str(request.url))
        
        # 準備回應
        response = CrawlResponse(
            url=str(result["url"]),
            title=result.get("title"),
            content_preview=result["content"],
            status=result["status"],
            processing_status=result["processing_status"]
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Crawl operation failed: {str(e)}"
        )


@router.get("/test", status_code=status.HTTP_200_OK)
async def test_crawler():
    """
    Simple endpoint to test if crawler API is working.
    """
    return {"status": "Crawler API is operational"} 