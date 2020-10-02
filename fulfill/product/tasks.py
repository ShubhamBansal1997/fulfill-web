# Standard Library
import csv
import logging

# Third Party Stuff
from celery import shared_task
from celery_progress.websockets.backend import WebSocketProgressRecorder
from django.conf import settings
from django.core.files.storage import default_storage

# fulfill Stuff
from fulfill.product.services import add_or_update_bulk_product
from fulfill.product.utils import chunked

MAX_DB_INSERTIONS = getattr(settings, 'MAX_DB_INSERTIONS', 1000)


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
        for rows in chunked(data, MAX_DB_INSERTIONS):
            add_or_update_bulk_product(rows, cols)
            result += len(rows)
            progress_recorder.set_progress(result, total_count)
    except Exception as e:
        logging.error(f"Error while running the task {e}")
    return result
