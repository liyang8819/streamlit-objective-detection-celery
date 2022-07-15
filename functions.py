#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   functions.py
@Time    :   2022/7/6 10:04:25
@Author  :   Li Yang
@Version :   1.0.0
@Contact :    yang.li@honeywell.com
@License :   (C)Copyright, Honeywell
@Desc    :   app.py调用的函数库
@Update  :   Liyang，2022/7/6
"""

import os
import shutil
from streamlit_img_label.manage import ImageManager, ImageDirManager
import time
import os
from PIL import Image
import cv2
import numpy as np

"""设置路径变量"""
base_path=os.path.dirname(os.path.abspath('app.py'))
config_path=os.path.join(base_path,'config')
imgpath_config_path=os.path.join(base_path,'config\\imgpath_config.txt')
label_config_path=os.path.join(base_path,'config\\label_config.txt')
model_sel_config_path=os.path.join(base_path,'config\\model_sel_config.txt')
train_name_config_path=os.path.join(base_path,'config\\train_name.txt')
train_state_config_path=os.path.join(base_path,'config\\train_state.txt')
yolo_path=os.path.join(base_path,'yolov5_master')
yolo_train_path=os.path.join(base_path,'yolov5_master\\runs\\train')
yolo_detect_path=os.path.join(base_path,'yolov5_master\\runs\\detect')
images_detect_path=os.path.join(yolo_path,'data\\images_detect')

labels=['helmet',',mask']
with open(label_config_path,'r', encoding='utf-8') as f:
     labels=f.readlines()[0] 

"""txt转xml函数，将标注文件从txt转xml"""
'''人为构造xml文件的格式'''
out0 ='''<annotation>
    <folder>%(folder)s</folder>
    <filename>%(name)s</filename>
    <path>%(path)s</path>
    <source>
        <database>None</database>
    </source>
    <size>
        <width>%(width)d</width>
        <height>%(height)d</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
'''
out1 = '''    <object>
        <name>%(class)s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%(xmin)d</xmin>
            <ymin>%(ymin)d</ymin>
            <xmax>%(xmax)d</xmax>
            <ymax>%(ymax)d</ymax>
        </bndbox>
    </object>
'''

out2 = '''</annotation>
'''

'''txt转xml函数'''
def translate(fdir,lists): 
    source = {}
    label = {}

    for jpg in lists:
        # print(jpg)
        if jpg[-4:] == '.jpg':
            image= cv2.imread(jpg)#路径不能有中文
            h,w,_ = image.shape #图片大小
            
            fxml = jpg.replace('.jpg','.xml')
            fxml = open(fxml, 'w')
            imgfile = jpg.split('/')[-1]
            source['name'] = imgfile 
            source['path'] = jpg
            source['folder'] = os.path.basename(fdir)

            source['width'] = w
            source['height'] = h
            
            fxml.write(out0 % source)
            txt = jpg.replace('.jpg','.txt')
            
            lines = np.loadtxt(txt)#读入txt存为数组,坐标位置信息
            
            #print(type(lines))
            print('lines',lines.shape)
            
            
            if lines.shape == (5,):
                box = lines   
                label_index = int(box[0]) #类别索引从1开始
                label['class']=labels[label_index]
                '''把txt上的数字（归一化）转成xml上框的坐标'''
                xmin = float(box[1] - 0.5*box[3])*w
                ymin = float(box[2] - 0.5*box[4])*h
                xmax = float(xmin + box[3]*w)
                ymax = float(ymin + box[4]*h)
                
                label['xmin'] = xmin
                label['ymin'] = ymin
                label['xmax'] = xmax
                label['ymax'] = ymax                    
                fxml.write(out1 % label)
                fxml.write(out2)
                                
            else:      
                for box in lines:   
                    '''把txt上的第一列（类别）转成xml上的类别
                       我这里是labelimg标1、2、3，对应txt上面的0、1、2'''
                    label_index = int(box[0]) #类别索引从1开始                                
                    label['class']=labels[label_index]
                    print(label)
                    '''把txt上的数字（归一化）转成xml上框的坐标'''
                    xmin = float(box[1] - 0.5*box[3])*w
                    ymin = float(box[2] - 0.5*box[4])*h
                    xmax = float(xmin + box[3]*w)
                    ymax = float(ymin + box[4]*h)
                    
                    label['xmin'] = xmin
                    label['ymin'] = ymin
                    label['xmax'] = xmax
                    label['ymax'] = ymax
                           
                    fxml.write(out1 % label)
                fxml.write(out2)
                
    
def get_config(path=label_config_path):
    
    """获取目标类别"""
    with open(path, 'r', encoding='utf-8') as f:
        label_exist=f.readlines()[0]  
    return label_exist

def model_sel(st):
    
    """获取和选择训练好的标注模型"""
    
    models=os.listdir(yolo_train_path)
    if len(models)>=1:
        model_num=st.selectbox('选择自动标注模型：', models)
        model_ok=1
    else:        
        model_ok=0
        model_num=None           
    return model_ok,model_num
    
    

def auto_label(img_dir,current_img):
        """基于选择训练好的标注模型，对当前图片进行自动标注"""        
        current_img_abs=os.path.join(base_path,img_dir+'\\'+current_img)
        shutil.copy(current_img_abs, images_detect_path)
        os.chdir(yolo_path)
        os.system("python detect.py --save-txt") 
        os.chdir(base_path)
        run_dirlist=os.listdir(yolo_detect_path)
        exp_num='exp'+str(max([int(x[3:]) if x[3:]!="" else 0 for x in run_dirlist])) 
        
        current_img_abs=os.path.join(yolo_detect_path,exp_num+'\\'+current_img)
        dest=os.path.join(yolo_detect_path,exp_num+'\\labels')
        shutil.copy(current_img_abs,dest)
        
        file_dir = dest
        lists=[]
        for i in os.listdir(file_dir):
            if i[-3:]=='jpg':
                lists.append(file_dir+'/'+i) 
        translate(file_dir,lists)
        detect_xml=os.path.join(dest,current_img[0:-3]+'xml')
        shutil.copy(detect_xml,img_dir) 
        
        
    
def auto_label_allunlabeled(img_dir):
    
    """基于选择训练好的标注模型，对当前文件夹未标注的图片进行自动标注"""  
    idm = ImageDirManager(img_dir)
    all_pic= idm.get_all_files()
    xml_files = idm.get_exist_annotation_files()
    labeled_pic=[x.strip('.xml')+'.jpg' for x in xml_files]
    unlabeled_pic=set(all_pic)-set(labeled_pic)

    for unlabeled_picx in unlabeled_pic:
        current_img=os.path.join(base_path,img_dir+'\\'+unlabeled_picx)        
        shutil.copy(current_img, images_detect_path)
             
    os.chdir(yolo_path)
    os.system("python detect.py --save-txt") 
    os.chdir(base_path)
    
    run_dirlist=os.listdir(yolo_detect_path)
    exp_num='exp'+str(max([int(x[3:]) if x[3:]!="" else 0 for x in run_dirlist]))  
    
    for unlabeled_picx in unlabeled_pic:
        current_img=os.path.join(yolo_detect_path,exp_num+'\\'+unlabeled_picx)
        dest=os.path.join(yolo_detect_path,exp_num+'\\labels')
        shutil.copy(current_img,dest)

    
    file_dir = dest
    lists=[]
    for i in os.listdir(file_dir):
        if i[-3:]=='jpg':
            lists.append(file_dir+'/'+i) 
    translate(file_dir,lists)
    for unlabeled_picx in unlabeled_pic:
        detect_xml=os.path.join(dest,unlabeled_picx[0:-3]+'xml')               
        shutil.copy(detect_xml,img_dir)                        

def gpu_info(st):     
    
    """获取当前机器的硬件信息，cuda安装情况"""      
    import torch
    import torchvision
    st.write('torch版本号:',torch.__version__)
    st.write('cuda是否可用:',torch.cuda.is_available())
    st.write('torchvision版本号:',torchvision.__version__)    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    st.write('设备:',device)
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            st.write('第'+str(i)+'块gpu设备名:',torch.cuda.get_device_name(i))
        st.write('cuda版本号:',torch.version.cuda)
        st.write('cudnn版本号:',torch.backends.cudnn.version())
        st.write('cuda计算测试:',torch.rand(3,3).cuda()) 
        
def cp_tree_ext(exts,src,dest):
  """
  Rebuild the director tree like src below dest and copy all files like XXX.exts to dest 
  exts:exetens seperate by blank like "jpg png gif"
  """
  fp={}
  extss=exts.lower().split()
  for dn,dns,fns in os.walk(src):
    for fl in fns:
      if os.path.splitext(fl.lower())[1][1:] in extss:
        if dn not in fp.keys():
          fp[dn]=[]
        fp[dn].append(fl)
  for k,v in fp.items():
      relativepath=k[len(src)+1:]
      newpath=os.path.join(dest,relativepath)
      for f in v:
        oldfile=os.path.join(k,f)
        print("拷贝 ["+oldfile+"] 至 ["+newpath+"]")
        if not os.path.exists(newpath):
          os.makedirs(newpath)
        shutil.copy(oldfile,newpath)

    
def get_model_training_logs(st,n_lines = 1):
    
    """获取模型训练日志"""       
    train_log_path=os.path.join(yolo_path,'train_log.log')
    file = open(train_log_path, 'r')
    lines = file.read().splitlines()[-n_lines:][::-1]

    for line in lines:
        st.markdown(line)
    file.close()
    
  