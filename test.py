import tkinter
from tkinter import filedialog

import os

def Choose_Dir_Path():
    root = tkinter.Tk()
    # root.withdraw()

    dirPath = filedialog.askdirectory(parent=root, initialdir="/", title='폴더를 선택해주세요.')
    return dirPath

def Create_Classification_Dir(folder_list):
    for folder in folder_list:
        try :
            os.mkdir(dirPath+'/'+folder)
        except FileExistsError as e :
            print('The folder is already created.')

if __name__ == '__main__' :
    dirPath = Choose_Dir_Path()
    folder_list = ['보류']
    Create_Classification_Dir(folder_list)
    

    file_list = os.listdir(dirPath)
    file_list_img = [file for file in file_list if file.endswith('.png') or file.endswith('.jpg')]

    # print(file_list_img)