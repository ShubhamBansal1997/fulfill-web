# Standard Library
import csv
import logging

# Third Party Stuff
from celery import shared_task
from celery_progress.websockets.backend import WebSocketProgressRecorder
from django.conf import settings
from django.core.files.storage import default_storage
from rest_hooks.tasks import DeliverHook

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


def deliver_hook_wrapper(target, payload, instance, hook):
    # instance is None if using custom event, not built-in
    if instance is not None:
        instance_id = instance.id
    else:
        instance_id = None
    # pass ID's not objects because using pickle for objects is a bad thing
    kwargs = dict(target=target, payload=payload,
                  instance_id=instance_id, hook_id=hook.id)
    DeliverHook.apply_async(kwargs=kwargs)
