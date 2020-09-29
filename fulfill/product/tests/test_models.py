# Third Party Stuff
from django.test import TestCase

# fulfill Stuff
from fulfill.product.models import Product
from fulfill.product.services import add_or_update_product


class ProductTestCase(TestCase):
    def setUp(self):
        Product(name="product 1 name", sku="product-1-sku", description="Product 1 description").save()
        Product(name="product 2 name", sku="product-2-sku", description="Product 2 description").save()

    def test_create_products(self):
        initial_count = Product.objects.all().count()
        Product(name="product 3 name", sku="product-3-sku", description="Product 2 description").save()
        p = Product.objects.get(sku="product-3-sku")
        self.assertEqual(p.sku, "product-3-sku")
        self.assertEqual(p.name, "product 3 name")
        self.assertEqual(p.description, "Product 2 description")
        self.assertEqual(str(p), str(p.sku))
        self.assertEqual(Product.objects.all().count(), initial_count + 1)

    def test_update_product(self):
        p = Product.objects.get(sku="product-1-sku")
        p.description = "Product 1 description New"
        p.save()
        u_p = Product.objects.get(sku="product-1-sku")
        self.assertEqual(u_p.sku, p.sku)
        self.assertEqual(u_p.name, p.name)
        self.assertNotEqual(u_p.description, "Product 2 description")

    def test_add_or_create_product(self):
        p = Product.objects.get(sku="product-1-sku")
        sku = p.sku
        name = p.name
        description = p.description
        add_or_update_product(sku, "New Name", "New Description")
        u_p = Product.objects.get(sku=sku)
        self.assertEqual(u_p.sku, sku)
        self.assertNotEqual(u_p.name, name)
        self.assertNotEqual(u_p.description, description)

    def test_delete_product(self):
        Product.objects.get(sku="product-1-sku").delete()
        self.assertEqual(Product.objects.all().count(), 1)

    def tearDown(self):
        Product.objects.all().delete()
