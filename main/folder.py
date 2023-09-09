import os
import shutil


#用于创建文件夹
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

#删除文件夹
def delete_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

#删除文件
def delete_file(filename):
    if (os.path.exists(filename)):
        os.remove(filename)
