"""
Tests for Jina AI Reader service.
"""
import pytest
import requests
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.crawler.jina_reader import JinaReaderResponse, JinaReaderService


@pytest.fixture
def mock_response():
    """Mock response fixture for requests."""
    response = MagicMock()
    response.text = "# Example Page Title\n\nThis is an example page content."
    response.status_code = 200
    return response


@pytest.mark.asyncio
async def test_extract_content_success(mock_response):
    """Test successful content extraction."""
    # Arrange
    url = "https://example.com/jobs"
    
    # Mock requests.get to return our mock_response
    with patch("requests.get", return_value=mock_response):
        service = JinaReaderService(api_key="test_api_key")
        
        # Act
        result = await service.extract_content(url)
        
        # Assert
        assert isinstance(result, JinaReaderResponse)
        assert result.content == mock_response.text
        assert result.url == url
        assert result.status_code == 200
        assert result.title == "Example Page Title"


@pytest.mark.asyncio
async def test_extract_content_http_error():
    """Test handling of HTTP errors."""
    # Arrange
    url = "https://example.com/jobs"
    
    # Mock requests.get to raise an exception
    with patch("requests.get", side_effect=requests.RequestException("Connection error")):
        service = JinaReaderService(api_key="test_api_key")
        
        # Act & Assert
        with pytest.raises(HTTPException) as excinfo:
            await service.extract_content(url)
        
        assert excinfo.value.status_code == 500
        assert "Failed to extract content" in excinfo.value.detail


@pytest.mark.asyncio
async def test_extract_title():
    """Test title extraction from content."""
    # Arrange
    service = JinaReaderService(api_key="test_api_key")
    
    # Act & Assert - Content with title
    content_with_title = "# Job Opening\n\nSome content"
    assert service._extract_title(content_with_title) == "Job Opening"
    
    # Act & Assert - Content without title
    content_without_title = "No title here. Just content."
    assert service._extract_title(content_without_title) is None 