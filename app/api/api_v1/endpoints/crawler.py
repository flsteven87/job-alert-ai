"""
Crawler API endpoints for testing and triggering crawls.
"""
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import AnyHttpUrl, BaseModel, Field

from app.services.crawler.crawler_service import CrawlerService
from app.services.crawler.firecrawl import JobPostingsResponse as FireCrawlJobPostingsResponse
from app.services.crawler.firecrawl import JobPosting as FireCrawlJobPosting

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


class JobPosting(BaseModel):
    """
    Job posting data model.
    """
    company: str
    title: str
    url: str
    description: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None


class JobPostingRequest(BaseModel):
    """
    Request model for extracting job postings.
    """
    url: AnyHttpUrl
    company_name: Optional[str] = None
    append_positions_tag: bool = False


class JobPostingResponse(BaseModel):
    """
    Response model for job posting extraction.
    """
    job_postings: List[JobPosting]
    url: str
    status_code: int
    total: int = Field(..., description="Total number of job postings found")


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


@router.post("/extract-jobs", response_model=JobPostingResponse, status_code=status.HTTP_200_OK)
async def extract_job_postings(request: JobPostingRequest):
    """
    Extract job postings from a career page.
    
    Args:
        request: Job posting extraction request with URL, optional company name,
                and whether to append "#positions" tag to the URL.
    
    Returns:
        List of extracted job postings.
    """
    crawler_service = CrawlerService()
    
    try:
        # 執行爬取職缺
        result = await crawler_service.crawl_job_postings(
            url=str(request.url),
            company_name=request.company_name,
            append_positions_tag=request.append_positions_tag
        )
        
        # 將 FireCrawl 模型轉換為 API 模型
        job_postings = [
            JobPosting(
                company=job.company,
                title=job.title,
                url=job.url,
                description=job.description,
                location=job.location,
                department=job.department
            ) 
            for job in result.job_postings
        ]
        
        # 準備回應
        response = JobPostingResponse(
            job_postings=job_postings,
            url=str(result.url),
            status_code=result.status_code,
            total=len(job_postings)
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job posting extraction failed: {str(e)}"
        )


@router.get("/test", status_code=status.HTTP_200_OK)
async def test_crawler():
    """
    Simple endpoint to test if crawler API is working.
    """
    return {"status": "Crawler API is operational"}