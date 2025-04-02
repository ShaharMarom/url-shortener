import os
import sys
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_shorten_valid_url():
    response = client.post(
        "/shorten",
        json={"url": "https://www.example.com"}
    )
    assert response.status_code == 200
    assert response.text.startswith('"http://localhost:8000/shorten/')

def test_shorten_invalid_url():
    response = client.post(
        "/shorten",
        json={"url": "not-a-valid-url"}
    )
    assert response.status_code == 400
    assert response.json() == "Invalid URL as a parameter"

def test_shorten_missing_url():
    response = client.post(
        "/shorten",
        json={}
    )
    assert response.status_code == 422 

def test_get_nonexistent_url():
    response = client.get("/shorten/nonexistent")
    assert response.status_code == 404
    assert response.json() == "URL doesn't exists"

def test_shorten_and_retrieve_url():
    original_url = "https://www.example.com/test"
    shorten_response = client.post(
        "/shorten",
        json={"url": original_url}
    )
    assert shorten_response.status_code == 200
    
    shortened_url = shorten_response.json()
    shortened_id = shortened_url.split("/")[-1]
    
    get_response = client.get(f"/shorten/{shortened_id}")
    assert get_response.status_code == 200
    assert get_response.json() == original_url

def test_shorten_same_url_twice():
    test_url = "https://www.example.com/same"
    
    response1 = client.post(
        "/shorten",
        json={"url": test_url}
    )
    assert response1.status_code == 200
    short_url1 = response1.json()
    
    response2 = client.post(
        "/shorten",
        json={"url": test_url}
    )
    assert response2.status_code == 200
    short_url2 = response2.json()
    
    assert short_url1 == short_url2

