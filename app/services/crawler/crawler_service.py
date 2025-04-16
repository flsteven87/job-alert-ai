"""
Crawler service factory for job posting extraction.
"""
import logging
from typing import Dict, List, Optional

from app.services.crawler.jina_reader import JinaReaderResponse, JinaReaderService

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
        # 初始化 Jina Reader 服務
        self.jina_reader = JinaReaderService()
    
    async def crawl_page(self, url: str) -> JinaReaderResponse:
        """
        Crawl a job posting page and extract its content.
        
        Args:
            url: URL of the job posting page.
            
        Returns:
            JinaReaderResponse: Structured response with extracted content.
        """
        logger.info(f"Crawling job posting page: {url}")
        
        # 使用 Jina AI Reader API 提取頁面內容
        response = await self.jina_reader.extract_content(url)
        
        logger.info(f"Successfully crawled page: {url}")
        return response
    
    async def process_extracted_content(self, response: JinaReaderResponse) -> Dict:
        """
        Process the extracted content to structure job posting data.
        This is a placeholder for future LLM-based extraction logic.
        
        Args:
            response: The response from Jina AI Reader API.
            
        Returns:
            Dict: Structured job posting data.
        """
        # 這裡只是一個基本的實現，未來會整合 LLM 來提取結構化的職缺數據
        return {
            "url": response.url,
            "title": response.title or "Unknown Job Title",
            "content": response.content[:200] + "..." if len(response.content) > 200 else response.content,
            "status": "extracted",
            "processing_status": "pending"
        }
    
    async def crawl_and_process(self, url: str) -> Dict:
        """
        Crawl a job posting page and process its content.
        
        Args:
            url: URL of the job posting page.
            
        Returns:
            Dict: Structured job posting data.
        """
        # 爬取頁面
        response = await self.crawl_page(url)
        
        # 處理提取的內容
        result = await self.process_extracted_content(response)
        
        return result 