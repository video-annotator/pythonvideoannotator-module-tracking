import pyforms, math, cv2
from pysettings import conf
from pyforms import BaseWidget
from pyforms.Controls import ControlNumber
from pyforms.Controls import ControlList
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCheckBox
from pyforms.Controls import ControlCheckBoxList
from pyforms.Controls import ControlEmptyWidget
from pyforms.Controls import ControlProgress

from mcvgui.dialogs.simple_image_filter_workflow import SimpleImageFilterWorkflow
from mcvapi.blobs.order_by_position import combinations

import json

class TrackingWindow(BaseWidget):

	def __init__(self, parent=None):
		super(TrackingWindow, self).__init__('Tracking', parentWindow=parent)
		self.mainwindow = parent

		self.layout().setMargin(5)
		self.setMinimumHeight(800)
		self.setMinimumWidth(900)

		self._start 		= ControlNumber('Start on frame',0)
		self._end 			= ControlNumber('End on frame', 10)
		self._objects 		= ControlCheckBoxList('Select the objects to track')
		self._filter_panel 	= ControlEmptyWidget('Filter')
		self._progress  	= ControlProgress('Progress')
		self._apply 		= ControlButton('Apply', checkable=True)

		self._formset = [
			('_objects',['_start','_end']), 
			'_filter_panel',
			'_apply',
			'_progress'
		]

		self.load_order = ['_start', '_end', '_filter_panel']


		self._filter 				= SimpleImageFilterWorkflow(video=self.mainwindow._video.value)
		self._filter_panel.value 	= self._filter
		self._apply.value			= self.__apply_evt
		self._apply.icon 			= conf.ANNOTATOR_ICON_PATH
		
		self._progress.hide()


	

	###########################################################################
	### AUX FUNCTIONS #########################################################
	###########################################################################

	def update_datasets(self):
		items = self._objects.items
		self._objects.clear()
		self._objects.value = items
	
	###########################################################################
	### INTERFACE FUNCTIONS ###################################################
	###########################################################################

	def add_dataset_evt(self, dataset):
		dataset.tracking_window = self		
		self._objects+= [dataset, True]

	def remove_dataset_evt(self, dataset):
		self._objects -= dataset

	def remove_object_evt(self, obj):
		items2remove = []
		for i, (item, checked) in enumerate(self._objects.items):
			if item.object2d==obj: items2remove.append(i)
		for i in sorted(items2remove,reverse=True): self._objects -= i

	
	###########################################################################
	### PROPERTIES ############################################################
	###########################################################################


	@property
	def player(self):
		return self._filter._player
	
	@property
	def video_filename(self): return self._video_filename if hasattr(self,'_video_filename') else None
	@video_filename.setter
	def video_filename(self, value):  
		self._filter.filename = value
		self._start.max = self.player.max
		self._end.max = self.player.max
	

	def __apply_evt(self):

		if self._apply.checked:
			self._start.enabled = False
			self._end.enabled = False
			self._objects.enabled = False
			self._filter_panel.enabled = False
			self._apply.label = 'Cancel'


			start = int(self._start.value)
			end   = int(self._end.value)
			self._progress.min = start
			self._progress.max = end
			self._progress.show()

			self._filter.clear()

			objects = self.objects
			paths 	= None
			
			capture = self.player.value
			capture.set(cv2.CAP_PROP_POS_FRAMES, start); 
			
			for index in range(start, end+1):
				res, frame = capture.read()
				if not res: break
				if not self._apply.checked: break

				paths = self._filter.processflow(frame)

				"""
				step = 16581375 / (len(paths)+1)
				for i, path in enumerate(paths): 


					rgb_int = step*(i+1)
					blue 	= rgb_int & 255
					green 	= (rgb_int >> 8) & 255
					red 	= (rgb_int >> 16) & 255
					c 		= (blue, green, red)
					path.draw(frame, color=c)
				
				self.player.image 	 = frame"""
				self._progress.value = index

			if paths is not None and self._apply.checked:

				objects = self.objects
				if len(paths)>len(objects):
					objects += [None for i in range(len(paths)-len(objects))]
				elif len(paths)<len(objects):
					paths += [None for i in range(len(objects)-len(paths))]

				classifications = []
				for comb in combinations( paths, objects):

					classification = 0
					for path, obj in comb:
						if not path or not obj: continue

						distances = []
						for i, b in enumerate(path.path):
							if b is None: continue 
							pos = obj.get_position(start + i)
							if pos is None: continue 

							p0   = pos
							p1 	 = path.centroid
							dist = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
							
							distances.append( dist )

						classification += sum(distances)/len(distances)
					
					classifications.append( (classification, comb) )
					
				classifications = sorted(classifications, key=lambda x: x[0])
				for path, obj in classifications[0][1]:
					if obj is None: continue
					for frame_index in range(start, end+1):
						blob = path[frame_index-start]
						if blob: obj.set_data_from_blob(frame_index, blob)
							

			self._start.enabled = True
			self._end.enabled = True
			self._objects.enabled = True
			self._filter_panel.enabled = True
			self._apply.label = 'Apply'
			self._apply.checked = False
			self._progress.hide()

		
	@property
	def objects(self): return self._objects.value
			
		
	


if __name__ == '__main__': 
	pyforms.startApp(TrackingWindow)
