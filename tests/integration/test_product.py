# Standard Library
import json

# Third Party Stuff
import pytest
from django.urls import reverse

# fulfill Stuff
from fulfill.product.models import Product

pytestmark = pytest.mark.django_db


def test_add_product(client):
    url = reverse("product-list")
    product = {
        "sku": "test-sku",
        "name": "Test SKU name",
        "description": "Test SKU description"
    }
    response = client.json.post(url, json.dumps(product))
    assert response.status_code == 201
    expected_keys = ["id", "sku", "name", "description", "created_at", "modified_at"]
    assert set(expected_keys).issubset(response.data.keys())
    assert response.status_code == 201
    assert response.data["sku"] == "test-sku"
    assert response.data["name"] == "Test SKU name"
    assert response.data["description"] == "Test SKU description"


def test_update_product(client):
    p = Product(sku="test-sku", name="Test SKU name", description="Test SKU description")
    p.save()
    url = reverse("product-detail", kwargs={'pk': p.pk})
    product = {
        "sku": "test-sku-new",
        "name": "Test SKU name New",
        "description": "Test SKU description new"
    }
    response = client.json.put(url, json.dumps(product))
    assert response.status_code == 200
    expected_keys = ["id", "sku", "name", "description", "created_at", "modified_at"]
    assert set(expected_keys).issubset(response.data.keys())
    assert response.data["sku"] == "test-sku-new"
    assert response.data["name"] == "Test SKU name New"
    assert response.data["description"] == "Test SKU description new"


def test_list_products(client):
    url = reverse("product-list")
    response = client.json.get(url)
    assert response.status_code == 200
    expected_keys = ["count", "next", "previous", "results"]
    assert set(expected_keys).issubset(response.data.keys())
    assert response.data["count"] == 0
    assert response.data["next"] is None
    assert response.data["previous"] is None


def test_delete_products(client):
    p = Product(sku="test-sku", name="Test SKU name", description="Test SKU description")
    p.save()
    url = reverse("product-detail", kwargs={'pk': p.pk})
    response = client.json.delete(url)
    assert response.status_code == 204
