# Streamlit Image Labelling - Blog post
streamlit-img-label is a graphical image annotation tool using streamlit. Annotations are saved as XML files in PASCAL VOC format.

## Installation
In your python virtual environment, run:

```sh
pip install streamlit-img-label
```

## Example
```sh
streamlit run app.py，
进入redis目录，执行 redis-cli.exe -h 127.0.0.1 -p 6379
进入redis目录，执行 redis-server.exe redis.windows.conf
进入./streamlit-objective-detection-celery,执行python -m celery -A tasks worker --loglevel=info -P solo
```

## Demo
![Demo](asset/st_img_label.gif)

## Reference
Streamlit Image Labelling
- [streamlit-cropper](https://github.com/turner-anderson/streamlit-cropper)


Train a YOLOv5 model on a custom dataset.
Models and datasets download automatically from the latest YOLOv5 release.
- [Models](https://github.com/ultralytics/yolov5/tree/master/models)
- [Datasets](https://github.com/ultralytics/yolov5/tree/master/data)
- [Tutorial](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data)
-Usage:
    $ python path/to/train.py --data coco128.yaml --weights yolov5s.pt --img 640  # from pretrained (RECOMMENDED)
    $ python path/to/train.py --data coco128.yaml --weights '' --cfg yolov5s.yaml --img 640  # from scratch
    
## Bentoml说明(bentoml_test文件夹)
- [BentoML](https://github.com/bentoml/BentoML)
Path(__file__).resolve()
```sh
     $ 保存和加载模型：bentoml_test.py, 在终端执行python bentoml_test.py
     $ 创建服务：bentoml_service.py, 在终端执行 bentoml serve ./bentoml_service.py:svc --reload （windows下 --reload 会报错）
     $          使用 --reload 选项允许服务显示对 bentoml_service.py 模块所做的任何更改，而无需重新启动（热更新）
     $ 服务提供给http调用：bentoml_http_request.py, 在终端执行bentoml_http_request.py
     $ 构建和部署 Bentos，创建一个名为 bentofile.yaml 的文件，在终端执行bentoml build


     $ 查看保存的模型：bentoml models list
     $ 构建的Bentos将保存在本地bento商店中bentoml list
     $ 从bento商店提供bentos服务。其中，--production 选项将在生产模式下提供bento服务：bentoml serve iris_classifier:veshoxfq3wzyqhqa --production
     $ 容器化部署：bentoml containerize iris_classifier:veshoxfq3wzyqhqa，
     $ 运行容器：docker run -p 5000:5000 iris_classifier:invwzzsw7li6zckb2ie5eubhd 
```     
## Bentoml yolov5
- [BentoML-yolov5](https://github.com/serberoos/bentoml-yolov5-model-service-test)    
