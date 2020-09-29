# fulfill Stuff
# Standard Library
import uuid

# Third Party Stuff
import boto3
from botocore.config import Config
from django.conf import settings

from fulfill.product.models import Product

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_S3_HOST = getattr(settings, 'AWS_S3_HOST', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_REGION_NAME = getattr(settings, 'AWS_S3_REGION_NAME', '')


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


def get_presigned_url():
    """
    Give pre signed url used to upload files from the frontend
    Returns:
        url(str): pre signed url
        filename(str): filename

    """
    file_name = f'{str(uuid.uuid4())}.csv'
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=AWS_S3_REGION_NAME,
                            endpoint_url=f'https://{AWS_S3_HOST}',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            config=Config(signature_version='s3'))
    url = client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': f"{AWS_STORAGE_BUCKET_NAME}/{file_name}",
            'ContentType': 'text/csv'
        })
    return url, file_name
