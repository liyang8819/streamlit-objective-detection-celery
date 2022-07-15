# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:32:52 2022

@author: zhufei
"""
##not used
from kombu import Queue
BROKER_URL="redis://localhost:6379/1"
CELERY_RESULT_BACKEND="redis://localhost:6379/2"
CELERY_TIMEZONE='Asia/shanghai'
CELERY_DEFAULT_QUEUE='default'

CELERY_QUEUES=(
    Queue('default',routing_key='default'),
    Queue('for_one',routing_key='for_one')
    )

CELERY_ROUTES={
    'send_task.tasks.train_yolo':{"queue":"for_one","routing_key":"for_one"}
        }