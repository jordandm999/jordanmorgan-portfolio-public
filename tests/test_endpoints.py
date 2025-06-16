import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'website'))
sys.path.insert(0, parent_dir)

from website.asgi import application
from fastapi.testclient import TestClient

client = TestClient(application)

def test_api_list_tools():
    response = client.get("/api/mcp_server/list_tools")
    assert response.status_code == 200
