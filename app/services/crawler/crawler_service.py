"""
Crawler service factory for job posting extraction.
"""
import logging
from typing import Dict, List, Optional

from app.services.crawler.firecrawl import FirecrawlService, JobPostingsResponse

# 設置日誌記錄器
logger = logging.getLogger(__name__)


class CrawlerService:
    """
    Factory service for crawling job postings from various sources.
    """
    
    def __init__(self):
        """
        Initialize the crawler service with required dependencies.
        """
        # 初始化 FireCrawl 服務
        self.firecrawl = FirecrawlService()
    
    async def crawl_job_postings(self, url: str, company_name: Optional[str] = None, 
                            append_positions_tag: bool = False) -> JobPostingsResponse:
        """
        Crawl job postings from a career page using FireCrawl.
        
        Args:
            url: URL of the career page.
            company_name: Name of the company. If not provided, will be extracted from URL.
            append_positions_tag: If True, append "#positions" to the URL (useful for some career sites).
            
        Returns:
            JobPostingsResponse: Extracted job postings.
        """
        logger.info(f"Crawling job postings from URL: {url}")
        
        # 使用 FireCrawl 爬取職缺
        try:
            response = await self.firecrawl.extract_job_postings(
                url=url, 
                company_name=company_name,
                append_positions_tag=append_positions_tag
            )
            logger.info(f"Successfully extracted {len(response.job_postings)} job postings using FireCrawl")
            return response
        except Exception as e:
            logger.error(f"Error using FireCrawl for URL {url}: {str(e)}")
            raise
            
    async def crawl_and_process(self, url: str) -> Dict:
        """
        Crawl a page and extract its basic content using FireCrawl.
        
        This is a simplified method for general content extraction, useful for testing and
        for scenarios where full job posting extraction is not needed.
        
        Args:
            url: URL of the page to crawl.
            
        Returns:
            Dict: Basic extracted information about the page.
        """
        logger.info(f"Performing basic crawl of URL: {url}")
        
        try:
            # 嘗試基本提取，這裡我們先只獲取職缺作為內容示例
            job_response = await self.firecrawl.extract_job_postings(
                url=url, 
                debug_mode=True,
                append_positions_tag=False  # 對通用爬取，不添加 #positions 標籤
            )
            
            # 將提取的資訊轉換為簡單的頁面內容
            content = "Job postings found on page:\n"
            if job_response.job_postings:
                for i, job in enumerate(job_response.job_postings, 1):
                    content += f"{i}. {job.title} - {job.url}\n"
            else:
                content = "No structured content could be extracted from the page."
                
            result = {
                "url": url,
                "title": f"Page from {url}",
                "content": content,
                "status": "successful" if job_response.job_postings else "partial",
                "processing_status": "completed"
            }
            
            logger.info(f"Basic crawl completed for URL: {url}")
            return result
            
        except Exception as e:
            logger.error(f"Error performing basic crawl for URL {url}: {str(e)}")
            # 返回錯誤信息而不是拋出異常，便於API處理
            return {
                "url": url,
                "title": None,
                "content": f"Error extracting content: {str(e)}",
                "status": "failed",
                "processing_status": "error"
            } 