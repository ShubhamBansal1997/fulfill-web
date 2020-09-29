# Standard Library
import csv
import logging

# Third Party Stuff
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.core.files.storage import default_storage

# fulfill Stuff
from fulfill.product.models import ProductFile
from fulfill.product.services import add_or_update_product, update_product_file_status


@shared_task(bind=True)
def product_upload_task(self, id):
    progress_recorder = ProgressRecorder(self)
    file = ProductFile.objects.get(pk=id)
    file = default_storage.open(str(file.file), 'r').read()
    update_product_file_status(id, 'RUNNING', self.request.id)
    csv_reader = csv.reader(file.strip().split('\n'))
    data = list(csv_reader)
    cols, data = data[0], data[1:]
    total_count = len(data)
    result = 0
    try:
        for i in range(total_count):
            sku = data[i][cols.index('sku')]
            description = data[i][cols.index('description')]
            name = data[i][cols.index('name')]
            add_or_update_product(sku, description, name)
            result += i
            progress_recorder.set_progress(i + 1, total_count)
        update_product_file_status(id, 'COMPLETED')
    except Exception as e:
        update_product_file_status(id, 'FAILED')
        logging.error(f"Error while running the task {e}")
    return result
