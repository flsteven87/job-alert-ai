"""
Jina AI Reader API service for web content extraction.
"""
import logging
from typing import Dict, Optional, Union

import requests
from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl

from app.core.config import settings

# 設置日誌記錄器
logger = logging.getLogger(__name__)


class JinaReaderResponse(BaseModel):
    """
    Jina AI Reader API response model.
    """
    content: str
    url: HttpUrl
    title: Optional[str] = None
    status_code: int


class JinaReaderService:
    """
    Service for extracting content from web pages using Jina AI Reader API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Jina AI Reader service.
        
        Args:
            api_key: Jina AI API key, defaults to the one in settings.
        """
        # 總是使用配置中的 API key
        self.api_key = api_key or settings.JINA_AI_API_KEY
        
        # 只顯示 API key 的前幾個字符，保護安全性
        masked_key = self.api_key[:8] + "..." if self.api_key else "None"
        logger.info(f"Using Jina AI API key: {masked_key}")
        
        self.base_url = "https://r.jina.ai/"
        
        # 設置授權頭
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        logger.info("Jina AI Reader Service initialized")
    
    async def extract_content(self, url: str) -> JinaReaderResponse:
        """
        Extract content from a web page using Jina AI Reader API.
        
        Args:
            url: The URL of the web page to extract content from.
            
        Returns:
            JinaReaderResponse: Structured response with extracted content.
            
        Raises:
            HTTPException: If the API request fails.
        """
        try:
            # 構建完整的 API URL
            api_url = f"{self.base_url}{url}"
            logger.info(f"Extracting content from URL: {url}")
            logger.info(f"API URL: {api_url}")
            
            # 發送請求
            logger.info("Sending request to Jina AI Reader API...")
            response = requests.get(api_url, headers=self.headers)
            logger.info(f"Response status code: {response.status_code}")
            
            # 如果狀態碼為 401，提供更具體的錯誤訊息
            if response.status_code == 401:
                error_msg = "Authentication failed with 401 Unauthorized."
                logger.error(f"{error_msg} Please check your API key format and validity.")
                logger.error(f"Response content: {response.text[:200]}...")
                
                raise HTTPException(
                    status_code=401,
                    detail=f"Authentication failed: {error_msg} Response: {response.text[:100]}"
                )
            
            response.raise_for_status()
            
            # 解析回應
            logger.info(f"Successfully received response, content length: {len(response.text)}")
            result = JinaReaderResponse(
                content=response.text,
                url=url,
                status_code=response.status_code,
                title=self._extract_title(response.text)
            )
            
            logger.info(f"Successfully extracted content from URL: {url}")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Error extracting content from URL {url}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract content: {str(e)}"
            )
    
    def _extract_title(self, content: str) -> Optional[str]:
        """
        Extract title from HTML content (if available).
        
        Args:
            content: HTML content.
            
        Returns:
            Optional[str]: Title if found, None otherwise.
        """
        # 簡單的標題提取實現，可以在將來改進
        try:
            if "# " in content:
                return content.split("# ", 1)[1].split("\n", 1)[0].strip()
        except Exception:
            pass
        return None 
    

# main
if __name__ == "__main__":
    import asyncio
    import os
    
    async def main():
        print("Starting Jina Reader Service...")
        jina_reader = JinaReaderService()
        url = "https://supabase.com/careers#positions"
        content = await jina_reader.extract_content(url)
        
        # 確保 data 目錄存在
        os.makedirs("./data", exist_ok=True)
        
        # 創建並保存檔案(使用 url 的 domain 作為文件名)
        file_name = url.split("/")[2]
        with open(f"./data/{file_name}.md", "w") as f:
            f.write(content.content)
        print(f"Saved content to ./data/{file_name}.md")
    
    # 執行異步主程序
    asyncio.run(main())
