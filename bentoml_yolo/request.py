# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:29:00 2022

@author: zhufei
"""

# http_request.py
import requests
from sklearn import datasets
iris = datasets.load_iris()

print(requests.post(
    "http://127.0.0.1:3000/yolo_detect",
    headers={"content-type": "application/json"},
    data="[[5.1, 3.5, 1.4, 0.2]]").text)