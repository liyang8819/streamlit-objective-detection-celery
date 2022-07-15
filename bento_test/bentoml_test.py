# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 09:45:46 2022

@author: zhufei
"""

from sklearn import svm
from sklearn import datasets
import bentoml

# Load training data
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Model Training
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

# 调用`bentoml.<FRAMEWORK>.save_model(<MODEL_NAME>, model)` 为了在本地模型存储中保存为 BentoML 的标准格式
bentoml.sklearn.save_model("iris_clf", clf)

# 然后，您可以使用bentoml.<FRAMEWORK>.load_model(<TAG>) 加载要在线运行的模型。
# 同时，您也可以使用 bentoml.<FRAMEWORK>.load_runner(<TAG>) API 使用性能优化的运行器。
##验证模型是否可以作为运行器加载
runner = bentoml.sklearn.load_model("iris_clf:latest")
print(runner.predict(iris.data[0].reshape(1, -1))) 