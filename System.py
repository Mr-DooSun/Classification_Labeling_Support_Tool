from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QGridLayout, QPushButton, QLineEdit, QDialog, QFileDialog, QButtonGroup
from PyQt5.QtGui import QPixmap

import os

import shutil

from PIL import Image

class OptionWindow(QDialog):
	def __init__(self,parent):
		super(OptionWindow,self).__init__(parent)
		self.setWindowTitle("Do Not Name")
		self.resize(950, 950)

	def main(self,dir_path,folder_list):
		self.dir_path = dir_path
		self.folder_list = folder_list
		
		self.grid = QGridLayout()
		self.setLayout(self.grid)
		
		self.button_num = 0
		self.btnGroup = QButtonGroup()
		self.btnGroup.setExclusive(False)
		self.btnGroup.buttonClicked[int].connect(self.Move_Data)
		for folder in folder_list :
			folder = folder.strip()
			if len(folder) > 0 :
				self.Create_Classification_Dir(dir_path,folder)
				self.button = QPushButton(folder)
				self.btnGroup.addButton(self.button,self.button_num)
				self.grid.addWidget(self.button,self.button_num,1)
				self.button_num+=1

		self.remove = QPushButton('삭제',self)
		self.remove.clicked.connect(self.Remove_Data)
		self.grid.addWidget(self.remove,self.button_num,1)

		self.image_label = QLabel(self)
		self.grid.addWidget(self.image_label, 0,0,self.button_num+1,1)

		file_list = os.listdir(dir_path)
		self.file_list_img = [file for file in file_list if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')]
		
		self.image_number = 0
		
		if len(self.file_list_img) < 1 :
			self.image_label.setText('Image file not found')
		else :
			self.now_image_path = self.dir_path+'/'+self.file_list_img[self.image_number]
			width, height = Image.open(self.now_image_path).size
			if width > 950 or height > 950 :
				width, height = self.Image_Size_Ratio(width, height)
			self.image_label.setPixmap(QPixmap(self.now_image_path).scaled(width,height))

		self.show()

	def Create_Classification_Dir(self,dir_path,folder):	
		try :
			os.mkdir(dir_path+'/'+folder)
		except FileExistsError as e :
			print('The folder is already created.')

	def Move_Data(self,id):
		for btn in self.btnGroup.buttons():
			if btn is self.btnGroup.button(id):
				self.after_image_path = self.dir_path+'/'+self.folder_list[id]+'/'+self.file_list_img[self.image_number]
				shutil.move(self.now_image_path,self.after_image_path)

				self.image_number += 1

				try :
					self.now_image_path = self.dir_path+'/'+self.file_list_img[self.image_number]
					width, height = Image.open(self.now_image_path).size
					if width > 950 or height > 950 :
						width, height = self.Image_Size_Ratio(width, height)
					self.image_label.setPixmap(QPixmap(self.now_image_path).scaled(width, height))
				except IndexError as e:
					self.image_label.setText('Image file not found')
					print(e)
					

	def Remove_Data(self):
		os.remove(self.now_image_path)

		self.image_number += 1

		self.now_image_path = self.dir_path+'/'+self.file_list_img[self.image_number]
		width, height = Image.open(self.now_image_path).size
		if width > 950 or height > 950 :
			width, height = self.Image_Size_Ratio(width, height)
		self.image_label.setPixmap(QPixmap(self.now_image_path).scaled(width, height))

	def Image_Size_Ratio(self,width,height):
		if width-height > 0 :
			big_bee = round(width/height,2)
			small_bee = 950 / big_bee
			big_bee = small_bee * big_bee

			return int(big_bee), int(small_bee)
		else :
			big_bee = round(height/width,2)
			small_bee = 950 / big_bee
			big_bee = small_bee * big_bee

			return int(small_bee), int(big_bee)


class Ui_MainWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.dir_path = 'C:/'

		self.setWindowTitle("Do Not Name")
		# self.resize(600, 500)

		self.grid = QGridLayout()
		self.setLayout(self.grid)

		self.dir_path_label = QLabel('C:/',self)
		self.choose_dir_button = QPushButton('...',self)
		self.choose_dir_button.clicked.connect(self.Choose_Dir_Path)

		self.input_directory = QLineEdit(self)
		self.start_button = QPushButton('Start',self)
		self.start_button.clicked.connect(self.Start_Button_Event)
		
		self.grid.addWidget(self.dir_path_label,0,0)
		self.grid.addWidget(self.choose_dir_button,0,1)
		self.grid.addWidget(self.input_directory,1,0)
		self.grid.addWidget(self.start_button,1,1)

		self.show()

	def Start_Button_Event(self):
		self.folder_list = self.input_directory.text().split(",")
		self.folder_list = [folder.strip() for folder in self.folder_list]
		if len(self.folder_list) > 1 and self.dir_path is not '' :
			main_ui = OptionWindow(self)
			main_ui.main(self.dir_path,self.folder_list)

	def Choose_Dir_Path(self):
		self.dir_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
		self.dir_path_label.setText(self.dir_path)

		return self.dir_path


if __name__=="__main__":
	import sys
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()
	ui = Ui_MainWindow()

	sys.exit(app.exec_())
