#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   tasks.py
@Time    :   2022/7/6 10:04:25
@Author  :   Li Yang
@Version :   1.0.0
@Contact :   yang.li@honeywell.com
@License :   (C)Copyright, Honeywell
@Desc    :   celery task for 异步训练yolov5模型
@Update  :   Liyang，2022/7/6
"""
from celery import Celery
import pickle
import time
import yaml
import os
import shutil
from functions import cp_tree_ext
app=Celery('tasks',backend='redis://localhost',broker='redis://127.0.0.1:6379')
# or
# app=Celery('tasks')
# app.config_from_object('celeryconfig_send')

@app.task()
def train_yolo(train_state_config_path,
               imgpath_config_path,
               yolo_path,
               base_path,
               label_config_path):


    """"训练yolov5
    输入：
    各个文件的路径
    返回：current_img：当前图片名称，石头人、
    """
    
    # step1,训练状态
    with open(train_state_config_path,'r', encoding='utf-8') as f:
        train_state=f.readlines()[0] 
              
        
    if train_state=="trainning_in_process":           
    # step2,获取训练集路径    
        with open(imgpath_config_path,'r', encoding='utf-8') as f:
            img_dir=f.readlines()[0]
        print("训练集路径:",img_dir)
                      
    # step3,进入yolov5_master文件夹,img_dir下的图片和标注xml，分别拷贝到yolov5_master下特定的文件夹 
        os.chdir(yolo_path) 
        src=os.path.join(base_path,img_dir)
        dest_img=os.path.join(yolo_path,'data\\images')
        dest_xml=os.path.join(yolo_path,'data\\Annotations')
        cp_tree_ext('xml',src,dest_xml)
        cp_tree_ext('jpg',src,dest_img)

    
    # step4,进入yolov5_master文件夹，生成配置文件
        os.system("python makeTxt.py")  
        os.system("python voc_label.py")  
        
        ori_yaml_path=os.path.join(yolo_path,'data\\ori.yaml')
        with open(ori_yaml_path,'r',encoding='utf8') as file:
            config_yaml=yaml.safe_load(file)
               
        with open(label_config_path, 'r', encoding='utf-8') as f:
            label_exist=list(f.readlines()[0].split(',')) 
            classes=label_exist
        
        config_yaml['nc']=len(classes)#几个目标类别
        config_yaml['names']=classes #目标类别list
        name_yaml='_'.join(str(x) for x in classes)#用目标类别名称，定义yaml文件的名称
        dest_yaml_path=os.path.join(yolo_path,'data\\'+name_yaml+'.yaml')
        with open(dest_yaml_path,'w') as f:
            yaml.dump(config_yaml,f)  
            
      
    # step5,进入yolov5_master文件夹，加载训练参数，训练模型（执行opt=parse_opt()会报错，所以在下面执行parse_opt函数中将参数存为pkl再加载pkl）
        # from yolov5_master.train import main
        # from yolov5_master.argparse_opt import parse_opt   
        # opt=parse_opt()
        os.system("python argparse_opt.py") 
        with open('../config/'+name_yaml+'_opt.pkl','rb') as f:
            opt=pickle.load(f)
            
    # step6,进入yolov5_master文件夹，训练模型
        from yolov5_master.train import main
        main(opt)
            
    # step7,更新训练进度       
        with open(train_state_config_path,'w', encoding='utf-8') as f:
            f.write("finished")  

if __name__ == "__main__":
    from functions import *
    train_yolo(train_state_config_path,
                   imgpath_config_path,
                   yolo_path,
                   base_path,
                   label_config_path)
    