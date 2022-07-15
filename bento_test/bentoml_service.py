# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:23:51 2022

@author: zhufei
"""

import numpy as np
import bentoml
from bentoml.io import NumpyNdarray

# 加载我们刚刚保存的最新 ScikitLearn 模型的运行器
iris_clf_runner = bentoml.sklearn.get("iris_clf:latest").to_runner()

# 使用 ScikitLearn 运行器创建 iris_classifier 服务
# 如果需要，可以在runners数组中指定多个运行器
# 当包装为bento时，运行器（runners）也会被包括在里面
svc = bentoml.Service("iris_classifier", runners=[iris_clf_runner])

# 使用“svc”注解创建具有预处理和后处理逻辑的 API 函数
@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray) -> np.ndarray:
    # 定义预处理逻辑
    result = iris_clf_runner.run(input_series)
    # 定义后处理逻辑
    return result