# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:23:51 2022

@author: zhufei
"""

import numpy as np
import bentoml
from bentoml.io import NumpyNdarray
import os


# # 加载我们刚刚保存的最新模型的运行器
# yolo_runner = bentoml.sklearn.get("iris_clf:latest").to_runner()
# svc = bentoml.Service("yolo_runner", runners=[yolo_runner])

# # 使用“svc”注解创建具有预处理和后处理逻辑的 API 函数
# @svc.api(input=NumpyNdarray(), output=NumpyNdarray())
# def yolo_detect(input_series: np.ndarray) -> np.ndarray:
#     os.system('python detect_bentoml.py')
#     return np.array([0])
yolo_runner = bentoml.pytorch.get("ckptbest.pt:latest").to_runner()
svc = bentoml.Service("yolo_runner", runners=[yolo_runner])
@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def yolo_detect(input_series: np.ndarray) -> np.ndarray:
    yolo_runner.init_local()
    yolo_runner.run(input_series)

    return np.array([0])




# import torch
# import torchvision
# from utils.torch_utils import select_device, time_sync
# from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
#                             increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
# from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
# device = select_device('0')


# # model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
# # model.load_state_dict(torch.load('best.pt'), strict=False)

# model =yolo_runner
# # stride, names, pt = model.stride, model.names, model.pt
# stride,pt=32,True

# imgsz = check_img_size((640, 640), s=stride)  # check image size
# dataset = LoadImages('online_detect_images', img_size=imgsz, stride=stride, auto=pt)
# bs = 1  # batch_size
# vid_path, vid_writer = [None] * bs, [None] * bs   
# dt, seen = [0.0, 0.0, 0.0], 0
# for path, im, im0s, vid_cap, s in dataset:
#     t1 = time_sync()
#     im = torch.from_numpy(im).to(device)
#     # im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
#     im = im.float() 
    
    
#     im /= 255  # 0 - 255 to 0.0 - 1.0
#     if len(im.shape) == 3:
#         im = im[None]  # expand for batch dim
#     t2 = time_sync()
#     dt[0] += t2 - t1

#     # Inference
#     # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
#     # pred = model(im, augment=augment, visualize=visualize)
#     pred = model(im, augment=False)  #liyang
#     # print('im',im)
#     # t3 = time_sync()
#     # dt[1] += t3 - t2

#     # # NMS
#     conf_thres=0.25,  # confidence threshold
#     iou_thres=0.45,  # NMS IOU threshold
#     max_det=1000,  # maximum detections per image
#     classes=['helmet','mask']
#     agnostic_nms=False
    
#     # pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
#     # dt[2] += time_sync() - t3
#     # print('pred',pred)

#     print('im',im)
#     t3 = time_sync()
#     dt[1] += t3 - t2

#     # NMS
#     # pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
#     pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
#     dt[2] += time_sync() - t3
    # print('pred',pred)

  

# @env(infer_pip_packages=True)
# @artifacts([PytorchModelArtifact('yolo_model')]) 
# class YoloPytorchModelService(BentoService): 

#     @api(input=ImageInput(), batch=True) 
#     def predict(self, imgs):
#         outputs = self.artifacts.model(imgs) 
#         return outputs

# svc = YoloPytorchModelService()

# # Pytorch model can be packed directly.
# svc.pack('yolo_model',model)
