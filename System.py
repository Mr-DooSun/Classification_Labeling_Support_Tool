from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QGridLayout, QPushButton, QLineEdit, QDialog, QFileDialog, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap

import os

import shutil

from PIL import Image

import threading

from pynput.keyboard import Listener, Key

class OptionWindow(QDialog):
	def __init__(self,parent):
		super(OptionWindow,self).__init__(parent)
		self.setWindowTitle("Do Not Name")
		self.resize(950, 950)
	
	def closeEvent(self, event):
		self.listener.stop()

	def main(self,dir_path,folder_list,move_remove):
		self.move_remove = move_remove
		self.dir_path = dir_path
		self.folder_list = folder_list
		
		self.grid = QGridLayout()
		self.setLayout(self.grid)
		
		self.button_num = 0
		self.btnGroup = QButtonGroup()
		self.btnGroup.setExclusive(False)

		if self.move_remove :
			self.btnGroup.buttonClicked[int].connect(self.Move_Data)
		else :
			self.btnGroup.buttonClicked[int].connect(self.Copy_Data)

		for folder in folder_list :
			folder = folder.strip()
			if len(folder) > 0 :
				self.Create_Classification_Dir(dir_path,folder)
				self.button = QPushButton(folder)
				self.btnGroup.addButton(self.button,self.button_num)
				self.grid.addWidget(self.button,self.button_num,1)
				self.button_num+=1

		if self.move_remove :
			self.remove_or_pass = QPushButton('삭제',self)
			self.remove_or_pass.clicked.connect(self.Remove_Data)
		else :
			self.remove_or_pass = QPushButton('다음',self)
			self.remove_or_pass.clicked.connect(self.Show_Next_Image)

		self.grid.addWidget(self.remove_or_pass,self.button_num,1)

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

		self.KeyClickEvent_Thread()

		self.show()
	
	def Image_Size_Ratio(self,width,height):
		if width-height > 0 :
			big_bee = width/height
			small_bee = 950 / big_bee
			big_bee = small_bee * big_bee

			return int(big_bee), int(small_bee)
		else :
			big_bee = height/width
			small_bee = 950 / big_bee
			big_bee = small_bee * big_bee

			return int(small_bee), int(big_bee)

	def Create_Classification_Dir(self,dir_path,folder):	
		try :
			os.mkdir(dir_path+'/'+folder)
		except FileExistsError as e :
			print(folder + ' folder is already created.')

	# 다음 데이터 보기
	def Show_Next_Image(self):
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

	# 데이터 삭제
	def Remove_Data(self):
		try:
			os.remove(self.now_image_path)
		except FileNotFoundError as e:
			print(e)

		self.Show_Next_Image()
	
	# 데이터 보류
	def Move_Hold(self):
		if os.path.isdir(self.dir_path+'/보류'):
			try :
				shutil.move(self.now_image_path,self.dir_path+'/보류')
			except :
				print('"보류" folder is not found')
				return None

			self.Show_Next_Image()
		
	# 데이터 이동
	def Move_Data(self,id):
		for btn in self.btnGroup.buttons():
			if btn is self.btnGroup.button(id):
				self.after_image_path = self.dir_path+'/'+self.folder_list[id]+'/'+self.file_list_img[self.image_number]
				shutil.move(self.now_image_path,self.after_image_path)

				self.Show_Next_Image()
	
	# 데이터 복사
	def Copy_Data(self,id):
		for btn in self.btnGroup.buttons():
			if btn is self.btnGroup.button(id):
				self.after_image_path = self.dir_path+'/'+self.folder_list[id]+'/'+self.file_list_img[self.image_number]
				shutil.copy2(self.now_image_path,self.after_image_path)

				self.Show_Next_Image()

	def on_release(self,key):  # The function that's called when a key is released
		if key == Key.end:
			if self.move_remove :
				self.Remove_Data()
				print('삭제')
			else :
				self.Show_Next_Image()
				print('다음')

		elif key == Key.home:
			if not self.move_remove :
				self.Move_Hold()
				print('보류')
			else :
				self.Copy_Data()
				print('복사')
		else :
			pass

	def KeyClickEvent(self):
		with Listener(on_release=self.on_release) as self.listener:  # Create an instance of Listener
			self.listener.join()  # Join the listener thread to the main thread to keep waiting for keys

	def KeyClickEvent_Thread(self):
		thread = threading.Thread(target=self.KeyClickEvent)
		thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
		thread.start()
		thread.do_run = False


class Ui_MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		
		self.dir_path=''

		self.setWindowTitle("Do Not Name")
		# self.resize(600, 500)

		self.grid = QGridLayout()
		self.setLayout(self.grid)

		self.rbtn1 = QRadioButton('Move / Remove',self)
		self.rbtn1.move(50, 50)
		self.rbtn1.setChecked(True)

		self.rbtn2 = QRadioButton('Copy / Pass',self)
		self.rbtn2.move(50, 70)

		self.dir_path_label = QLabel('',self)
		self.choose_dir_button = QPushButton('...',self)
		self.choose_dir_button.clicked.connect(self.Choose_Dir_Path)

		self.input_directory = QLineEdit(self)
		self.start_button = QPushButton('Start',self)
		self.start_button.clicked.connect(self.Start_Button_Event)
		
		self.grid.addWidget(self.rbtn1,0,0)
		self.grid.addWidget(self.rbtn2,1,0)
		self.grid.addWidget(self.dir_path_label,0,1)
		self.grid.addWidget(self.choose_dir_button,0,2)
		self.grid.addWidget(self.input_directory,1,1)
		self.grid.addWidget(self.start_button,1,2)
		

		self.show()

	def Start_Button_Event(self):
		self.folder_list = self.input_directory.text().split(",")
		self.folder_list = [folder.strip() for folder in self.folder_list]
		if len(self.folder_list) > 0 and self.dir_path != '' :
			main_ui = OptionWindow(self)
			main_ui.main(self.dir_path,self.folder_list,self.rbtn1.isChecked())

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