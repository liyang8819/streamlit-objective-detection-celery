#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   app.py
@Time    :   2022/7/6 10:04:25
@Author  :   Li Yang
@Version :   1.0.0
@Contact :   yang.li@honeywell.com
@License :   (C)Copyright, Honeywell
@Desc    :   项目的主函数
@Update  :   Liyang，2022/7/6
"""

import streamlit as st
import os
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager, ImageDirManager
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import yaml
from functions import *


def label(img_dir, labels):
    
    """"针对文件夹内的图片信息进行统计，总数，标注数，当前图片索引，图片切换和导航，图片展示
        设置一些标注按钮实现图片的标注
    输入：
    img_dir，标注图片路径，str
    labels，标注的类别，list
    
    返回：current_img：当前图片名称，石头人、
    """
    
    st.set_option("deprecation.showfileUploaderEncoding", False)#弃用警告
    idm = ImageDirManager(img_dir)
    
    # session_state保存文件夹内的文件标注信息
    if "files" not in st.session_state:
        st.session_state["files"] = idm.get_all_files()
        st.session_state["annotation_files"] = idm.get_exist_annotation_files()
        st.session_state["image_index"] = 0  #当前图片
    else:
        idm.set_all_files(st.session_state["files"])
        idm.set_annotation_files(st.session_state["annotation_files"])
    
    def refresh():
        # 刷新文件夹信息
        st.session_state["files"] = idm.get_all_files()
        st.session_state["annotation_files"] = idm.get_exist_annotation_files()
        st.session_state["image_index"] = 0

    def next_image():
        # 切换到下一张图片
        image_index = st.session_state["image_index"]
        if image_index < len(st.session_state["files"]) - 1:
            st.session_state["image_index"] += 1
        else:
            st.warning('This is the last image.')
        
    def previous_image():
        # 切换到前一张图片
        image_index = st.session_state["image_index"]
        if image_index > 0:
            st.session_state["image_index"] -= 1
        else:
            st.warning('This is the first image.')

    def next_annotate_file():
        # 切换到下一张未标注的图片
        image_index = st.session_state["image_index"]
        next_image_index = idm.get_next_annotation_image(image_index)
        if next_image_index:
            st.session_state["image_index"] = idm.get_next_annotation_image(image_index)
        else:
            st.warning("All images are annotated.")
            next_image()
                               
    def go_to_image():
        # 切换到选择的图片
        file_index = st.session_state["files"].index(st.session_state["file"])
        st.session_state["image_index"] = file_index
        
    # Sidebar: show status
    n_files = len(st.session_state["files"])
    n_annotate_files = len(st.session_state["annotation_files"])
    col1,col2,col3=st.columns(3)
    
    col1.write("全部图片:  "+str(n_files))
    col2.write("已标注图片:  "+str(n_annotate_files))
    col3.write("未标注图片:  "+str( n_files - n_annotate_files))

    col1, col2, col3, col4= st.columns([2,2,2,2])
    current_img=col1.selectbox(
                            "Files",
                            st.session_state["files"],
                            index=st.session_state["image_index"],
                            on_change=go_to_image,
                            key="file",
                        )   
    
    with col2:
        st.write("*")
        st.button(label="刷新文件夹", on_click=refresh)
        
        
    #设置自动标注利用的模型    
    with col3:    
        model_ok,model_num=model_sel(st)           
        if model_ok:
            with open(model_sel_config_path,'w', encoding='utf-8') as f:
                 f.write(model_num)
        if not model_ok:
            st.caption("*")
            st.caption('当前无训练好的模型')  
           
    with col4: 
       col4.write("*")         
       if col4.button("全部自动标注"):
           st.info('自动标注开始')
           auto_label_allunlabeled(img_dir)
           st.info('标注成功,请刷新文件夹')
           

    # Main content: annotate images
    img_file_name = idm.get_image(st.session_state["image_index"])
    img_path = os.path.join(img_dir, img_file_name)

    im = ImageManager(img_path)
    img = im.get_img()
    resized_img = im.resizing_img()
    resized_rects = im.get_resized_rects()
    rects = st_img_label(resized_img, box_color="red", rects=resized_rects)
    
    
    #标注信息保存
    def annotate():
        im.save_annotation()
        image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
        if image_annotate_file_name not in st.session_state["annotation_files"]:
            st.session_state["annotation_files"].append(image_annotate_file_name)
        next_annotate_file()
        
        
        
    col1, col2 , col3, col4, col5= st.columns([1,1,2,2,2])      
    with col1:
        st.button(label="上一张", on_click=previous_image)        
    with col2:        
        st.button(label="下一张", on_click=next_image)  
    with col3:
        st.button(label="未标注的下一张", on_click=next_annotate_file)
    with col4: 
       if col4.button("自动标注"):
           st.info('自动标注开始')
           auto_label(img_dir,current_img)
           st.success('自动标注成功')
           st.button('刷新')                                 
    with col5:           
        st.button(label="保存标注", on_click=annotate)                         
    preview_imgs = im.init_annotation(rects)  
    for i, prev_img in enumerate(preview_imgs):
        prev_img[0].thumbnail((200, 200))
        col1, col2 = st.columns(2)
        with col1:
            col1.image(prev_img[0])
        with col2:
            default_index = 0
            # if prev_img[1]:
            #     default_index = labels.index(prev_img[1])

            select_label = col2.selectbox(
                "Label", labels, key=f"label_{i}", index=default_index
            )
            im.set_annotation(i, select_label)
    
    return current_img
    
 
    
    
if __name__ == "__main__":
    
    st.set_page_config(page_title="HCE图像目标平台", 
                        page_icon="random" , 
                        # layout="wide",
                        initial_sidebar_state="auto")
    #隐藏脚注
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: visiable;}
                footer {visibility: hidden;}
                </style>               
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    
    
    
    st.markdown(""" <style> .font3 {
    font-size:20px ; font-family: 'Cooper Black'; color: red;} 
    </style> """, unsafe_allow_html=True)
    
    st.markdown(""" <style> .font1 {
    font-size:25px ; font-family: 'Cooper Black'; color: #red;} 
    </style> """, unsafe_allow_html=True)
    
    from PIL import Image
    image = Image.open('./logo/Honeywell_Logo_RGB_Red.png')    
    col1,col2=st.columns([5,7])
    col1.image(image, width=300) 
    col2.write("")
    col2.write("")
    col2.markdown('<p class="font3">企业智联 | 目标检测助手</p>', unsafe_allow_html=True)

    # st.sidebar.image('./image/honeywell.png',width=150)    
    
    with st.sidebar:    
        choose = option_menu("功能栏", ["图片标注","训练模型"],                             
                             icons=[
                                    'gear-fill',
                                    'plus-lg'], 
                             menu_icon="list", default_index=0)
    if choose =="图片标注":
        i=0
        label_task = stx.stepper_bar(steps=["Step1:配置", "Step2:标注", "Step3:增强"], is_vertical=0, lock_sequence=False)
        
        # """标注环境配置"""
        if label_task==0:
            
            # st.header("step1，图片路径配置")
            img_dir_prev=get_config(path='./config/imgpath_config.txt')  
            img_dir=st.text_input('图片路径',value=img_dir_prev) 
                                
            # st.header("step2，创建Label")
            st.write("")
            st.write("")
            st.write("")
            label_exist=get_config()               
            label_new=st.text_input('创建label',value=label_exist) 
            st.write('当前label :   ',label_new)
            st.write("")
            st.write("")
            st.write("") 
            
            col1,col2=st.columns([7,1])
            config_button=col2.button("确认")            
            if config_button and img_dir!="":
                os.remove(imgpath_config_path)
                with open(imgpath_config_path,'w', encoding='utf-8') as f:
                    f.write(img_dir)
                st.info('创建路径 '+str(img_dir)+' 成功')
            if config_button and label_new!="":
                os.remove(label_config_path)
                with open(label_config_path,'w', encoding='utf-8') as f:
                    f.write(label_new) 
                st.info('创建label '+str(label_new)+' 成功')   
                
        # """标注界面"""            
        if label_task==1:
            img_dir=get_config(path=imgpath_config_path)
            labels=get_config().split(',')
            current_img=label(img_dir,labels)
        
    if choose =="训练模型": 
        
        # '''part 1 设备信息,gpu信息，cpu信息'''       
        st.write("设备信息：")
        with st.expander("-："):
            gpu_info(st) 
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
        
        # '''part 2 图片和标注文件的路径，默认=上次保存的结果'''                        
        img_dir_prev=get_config(path=imgpath_config_path) 
        
        img_dir=st.text_input('训练集路径：',value=img_dir_prev) 
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
    
        
        # '''part 3 模型命名，没有默认值'''         
        expname=st.text_input('模型命名：') 

        if len(expname)>0:  #模型名称保存到txt
            with open(train_name_config_path,'w', encoding='utf-8') as f:
                f.write(expname)  
                
        with open(train_name_config_path,'r', encoding='utf-8') as f:
            expname=f.readlines()[0] 
        st.caption('上个模型：'+expname)
                             
        # '''part 4 训练相关按钮'''                                                                
        col1,col2,col3=st.columns(3)
        with col1:
            start=st.button("开始训练",key='start')
        with col3:
            record=st.button("训练记录",key='record')

        # '''part 5 训练提示'''           
        if start and len(expname)==0: 
            st.warning('请先对模型命名') 
            
        # '''part 5 训练状态'''  
        with open(train_state_config_path,'r', encoding='utf-8') as f:
            train_state=f.readlines()[0]          
        if train_state=="trainning_in_process":
            st.warning(expname+'模型训练中...')
            
        # '''part 5 训练开始'''                                     
        if start and len(expname)>0 and train_state!="trainning_in_process": 
            with open(train_state_config_path,'w', encoding='utf-8') as f:
                f.write("trainning_in_process")  
                
            # """配置模型类型文件""""
            with open(label_config_path, 'r', encoding='utf-8') as f:
                label_exist=list(f.readlines()[0].split(','))     
                
            yolov5l_yaml_path=os.path.join(yolo_path,'models\\yolov5l.yaml')
            with open(yolov5l_yaml_path,'r',encoding='utf8') as file:
                yolov5l_yaml=yaml.safe_load(file)   
            yolov5l_yaml['nc']=len(label_exist)     
            yolov5l_yaml['depth_multiple']=1.0
            yolov5l_yaml['width_multiple']=1.0
            with open(yolov5l_yaml_path,'w') as f:
                yaml.dump(yolov5l_yaml,f)  
                
            st.warning(expname+'模型训练中...')
            
            # from send_task import app
            # app.send_task('send_task.train_yolo',queue='for_one')
            
            #celery启动任务异步执行
            from tasks import train_yolo
            result=train_yolo.delay(train_state_config_path,
                           imgpath_config_path,
                           yolo_path,
                           base_path,
                           label_config_path)
            
        if record:#获取训练日志
            get_model_training_logs(st,n_lines = 10)         