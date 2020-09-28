# fulfill Stuff
from fulfill.product.models import Product, ProductFile


def update_product_file_status(id, status, task_id=None):
    """
    Used to change the file upload status
    Args:
        id(str): pk
        status(str): RUNNING, ADDED, COMPLETED
        task_id(str): celery task id

    Returns:
        None
    """
    file = ProductFile.objects.get(pk=id)
    file.status = status
    if task_id:
        file.task_id = task_id
    file.save()


def add_or_update_product(sku, description, name):
    """
    Add product to db if doesn't exists
    Sku is used to identify if the product exists or not
    Args:
        sku(str): sku of the product
        description(str): description of the product
        name(str): name of the product

    Returns:
        None
    """
    try:
        p = Product.objects.get(sku=sku.lower())
        p.description = description
        p.name = name
        p.save()
    except Product.DoesNotExist:
        p = Product(sku=sku.lower(), description=description, name=name)
        p.save()
