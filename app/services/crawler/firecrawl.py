"""
FireCrawl API service for web content extraction and job posting crawling.
"""
import json
import logging
import os
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl

from app.core.config import settings

# 設置日誌記錄器
logger = logging.getLogger(__name__)

# 導入 FireCrawl 庫
from firecrawl import FirecrawlApp


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


class JobPostingsResponse(BaseModel):
    """
    Response model for job postings extraction.
    """
    job_postings: List[JobPosting]
    url: str
    status_code: int = 200


class FirecrawlService:
    """
    Service for extracting job postings using FireCrawl API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FireCrawl service.
        
        Args:
            api_key: FireCrawl API key, defaults to the one in settings.
            
        Raises:
            ValueError: If no valid API key is provided or configured.
        """
        # 使用傳入的 API key 或從設置取得
        self.api_key = api_key or settings.FIRECRAWL_API_KEY
        
        # 驗證 API 密鑰格式
        if not self.api_key or not self.api_key.startswith('fc-'):
            raise ValueError(
                "Invalid or missing FireCrawl API key. "
                "Please set a valid FIRECRAWL_API_KEY in your .env file. "
                "The key should start with 'fc-'."
            )
        
        # 初始化 FireCrawl 客戶端
        self._client = FirecrawlApp(api_key=self.api_key)
        logger.info("FireCrawl client initialized successfully")
    
    async def extract_job_postings(self, url: str, company_name: Optional[str] = None, debug_mode: bool = False, 
                           append_positions_tag: bool = False) -> JobPostingsResponse:
        """
        Extract job postings from a company's career page.
        
        Args:
            url: The URL of the career page to extract job postings from.
            company_name: The name of the company. If not provided, will be extracted from the URL domain.
            debug_mode: If True, save raw responses to file for analysis.
            append_positions_tag: If True, append "#positions" to the URL to improve crawling success for some sites.
            
        Returns:
            JobPostingsResponse: Structured response with extracted job postings.
            
        Raises:
            HTTPException: If the API request fails.
        """
        try:
            # 如果沒有提供公司名稱，從 URL 中提取域名作為公司名稱
            if not company_name:
                company_name = self._extract_company_from_url(url)
                logger.info(f"Company name not provided, using domain name: {company_name}")
            
            # 可選：添加 #positions 標籤以提高爬取成功率
            original_url = url
            if append_positions_tag and "#positions" not in url:
                url = url + "#positions"
                logger.debug(f"Appended #positions tag to URL: {url}")
            
            logger.info(f"Extracting job postings from URL: {url}")
            
            # 直接使用成功的測試檔案中的模型和參數
            class NestedModel1(BaseModel):
                job_title: str
                job_url: str

            class ExtractSchema(BaseModel):
                jobs: list[NestedModel1]
            
            # 構建請求選項
            options = {
                'prompt': 'Extract job titles and their corresponding URLs from all career pages.',
                'schema': ExtractSchema.model_json_schema(),
            }
            
            # 發送請求到 FireCrawl API
            logger.info("Sending request to FireCrawl API...")
            response = self._client.extract([url], options)
            
            # Debug 模式：保存原始回應到檔案
            if debug_mode:
                self._save_debug_response(url, json.dumps(response, indent=2))
            
            # 處理回應並轉換結構
            job_postings = []
            
            # 檢查回應是否有效 (參考測試檔案的成功回應格式)
            if response and 'data' in response and 'jobs' in response['data']:
                jobs = response['data']['jobs']
                
                for job in jobs:
                    job_posting = JobPosting(
                        company=company_name,
                        title=job.get('job_title', ''),
                        url=job.get('job_url', ''),
                        description=None,
                        location=None,
                        department=None
                    )
                    job_postings.append(job_posting)
            
            logger.info(f"Successfully extracted {len(job_postings)} job postings from URL: {url}")
            
            # 構建回應
            return JobPostingsResponse(
                job_postings=job_postings,
                url=original_url
            )
            
        except Exception as e:
            logger.error(f"Error extracting job postings from URL {url}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract job postings: {str(e)}"
            )
    
    def _save_debug_response(self, url: str, response_text: str) -> None:
        """
        Save response to a debug file for analysis.
        
        Args:
            url: The URL of the requested page.
            response_text: The response text to save.
        """
        try:
            # 確保 data 目錄存在
            data_dir = "./data"
            os.makedirs(data_dir, exist_ok=True)
            
            # 從 URL 提取文件名
            domain = url.split("//")[-1].split("/")[0]
            filename = f"{data_dir}/{domain}_firecrawl_debug.json"
            
            # 保存回應
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response_text)
                
            logger.info(f"Saved debug response to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save debug response: {str(e)}")
    
    def _extract_company_from_url(self, url: str) -> str:
        """
        Extract company name from URL domain.
        
        Args:
            url: The URL to extract company name from.
            
        Returns:
            str: Extracted company name.
        """
        try:
            # 從 URL 中提取域名
            domain = url.split("//")[-1].split("/")[0]
            
            # 移除 www. 前綴和頂級域名
            parts = domain.split(".")
            if parts[0] == "www":
                parts = parts[1:]
            
            # 取出可能的公司名稱部分
            company = parts[0]
            
            # 將首字母大寫
            return company.capitalize()
            
        except Exception as e:
            logger.warning(f"Failed to extract company name from URL {url}: {str(e)}")
            return "Unknown"


# main
if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("Starting FireCrawl Service test...")
        firecrawl_service = FirecrawlService()
        
        # 測試職位提取功能
        test_url = "https://supabase.com/careers#positions"
        
        # 啟用 debug 模式保存原始回應
        print(f"Extracting job postings from {test_url}...")
        try:
            result = await firecrawl_service.extract_job_postings(test_url, debug_mode=True)
            
            # 確保 data 目錄存在
            os.makedirs("./data", exist_ok=True)
            
            # 保存提取的職位資訊為 JSON 檔案
            domain = test_url.split("/")[2]
            
            # 使用與 pydantic v1/v2 兼容的序列化方法
            try:
                # pydantic v2
                jobs_data = [job.model_dump() for job in result.job_postings]
            except AttributeError:
                # pydantic v1
                jobs_data = [job.dict() for job in result.job_postings]
            
            output_data = {
                "jobs": jobs_data,
                "url": str(result.url),
                "total": len(result.job_postings)
            }
            
            with open(f"./data/{domain}_jobs.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully extracted {len(result.job_postings)} job postings.")
            print(f"Results saved to ./data/{domain}_jobs.json")
            
            # 顯示提取的職位
            for i, job in enumerate(result.job_postings, 1):
                print(f"{i}. {job.title} - {job.url}")
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
    
    # 執行異步主程序
    asyncio.run(main()) 