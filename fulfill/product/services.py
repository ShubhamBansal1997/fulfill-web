# fulfill Stuff
# Standard Library
import uuid

# Third Party Stuff
import boto3
from botocore.config import Config
from django.conf import settings
from django.db import IntegrityError

from fulfill.product.models import Product

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_S3_HOST = getattr(settings, 'AWS_S3_HOST', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_REGION_NAME = getattr(settings, 'AWS_S3_REGION_NAME', '')


def add_or_update_bulk_product(rows, cols):
    """
    Add product to db if doesn't exists
    Sku is used to identify if the product exists or not
    Args:
        rows(array): list of the products
        cols(str): list of the product columns

    Returns:
        None
    """
    s_index = cols.index('sku')
    d_index = cols.index('description')
    n_index = cols.index('name')
    products = [
        Product(sku=data[s_index].lower(), description=data[d_index], name=data[n_index]) for data in rows
    ]
    try:
        Product.objects.bulk_create(products, ignore_conflicts=True)
    except IntegrityError:
        for product in products:
            try:
                product.save()
            except IntegrityError:
                continue


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
