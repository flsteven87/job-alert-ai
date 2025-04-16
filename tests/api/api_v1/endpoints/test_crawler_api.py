"""
Tests for crawler API endpoints.
"""
import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.services.crawler.crawler_service import CrawlerService


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_crawl_result():
    """Mock crawl result fixture."""
    return {
        "url": "https://example.com/jobs",
        "title": "Example Job Posting",
        "content": "This is an example job posting content...",
        "status": "extracted",
        "processing_status": "pending"
    }


def test_test_crawler_endpoint(client):
    """Test the crawler test endpoint."""
    # Arrange & Act
    response = client.get("/api/v1/crawler/test")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Crawler API is operational"}


def test_crawl_url_endpoint_success(client, mock_crawl_result):
    """Test successful crawl URL endpoint."""
    # Arrange
    test_url = "https://example.com/jobs"
    
    # Mock the crawler service
    with patch("app.services.crawler.crawler_service.CrawlerService.crawl_and_process", 
               new_callable=AsyncMock) as mock_crawl:
        # Setup the mock
        mock_crawl.return_value = mock_crawl_result
        
        # Act
        response = client.post(
            "/api/v1/crawler/crawl",
            json={"url": test_url}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["url"] == test_url
        assert result["title"] == mock_crawl_result["title"]
        assert result["content_preview"] == mock_crawl_result["content"]
        assert result["status"] == mock_crawl_result["status"]
        assert result["processing_status"] == mock_crawl_result["processing_status"]
        
        # Verify service was called correctly
        mock_crawl.assert_called_once_with(test_url)


def test_crawl_url_endpoint_error(client):
    """Test error handling in crawl URL endpoint."""
    # Arrange
    test_url = "https://example.com/jobs"
    error_message = "Simulated error"
    
    # Mock the crawler service to raise an exception
    with patch("app.services.crawler.crawler_service.CrawlerService.crawl_and_process", 
               new_callable=AsyncMock) as mock_crawl:
        # Setup the mock
        mock_crawl.side_effect = Exception(error_message)
        
        # Act
        response = client.post(
            "/api/v1/crawler/crawl",
            json={"url": test_url}
        )
        
        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert error_message in response.json()["detail"] 