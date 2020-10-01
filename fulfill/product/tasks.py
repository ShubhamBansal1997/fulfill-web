# Standard Library
import csv
import logging

# Third Party Stuff
from celery import shared_task
from celery_progress.websockets.backend import WebSocketProgressRecorder
from django.core.files.storage import default_storage

# fulfill Stuff
from fulfill.product.services import add_or_update_product


@shared_task(bind=True)
def product_upload_task(self, file):
    progress_recorder = WebSocketProgressRecorder(self)
    file = default_storage.open(file, 'r').read()
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
    except Exception as e:
        logging.error(f"Error while running the task {e}")
    return result
