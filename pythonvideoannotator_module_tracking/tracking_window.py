import pyforms, math, cv2
from pysettings import conf
from pyforms import BaseWidget
from pyforms.Controls import ControlNumber
from pyforms.Controls import ControlList
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlToolBox
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlCheckBox
from pyforms.Controls import ControlCheckBoxList
from pyforms.Controls import ControlEmptyWidget
from pyforms.Controls import ControlProgress

from mcvapi.blobs.order_by_position 						import combinations
from pythonvideoannotator_module_tracking.tracking_filter 	import TrackingFilter

from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.contours import Contours
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path
from pythonvideoannotator_models.models.video.objects.object2d import Object2D


from pythonvideoannotator_models_gui.dialogs import DatasetsDialog

import simplejson as json

class TrackingWindow(BaseWidget):

	def __init__(self, parent=None):
		super(TrackingWindow, self).__init__('Tracking', parent_win=parent)
		self.mainwindow = parent

		if conf.PYFORMS_USE_QT5:
			self.layout().setContentsMargins(5,5,5,5)
		else:
			self.layout().setMargin(5)
			

		self.setMinimumHeight(800)
		self.setMinimumWidth(1100)

		self._toggle_btn    = ControlButton('Hide datasets list', checkable=True)
		self._input			= ControlEmptyWidget('Videos to process')
		
		self._filter_panel 	= ControlEmptyWidget('Tracking filter')
		self._progress  	= ControlProgress('Progress')
		self._apply 		= ControlButton('Apply', checkable=True)
		
		self._formset = [
			'_toggle_btn',
			'_input',
			'_filter_panel',
			'_apply',
			'_progress'
		]

		self.input_dialog = DatasetsDialog(self)
		self.input_dialog.objects_filter  = lambda x: isinstance(x, Object2D)
		self.input_dialog.datasets_filter = lambda x: isinstance(x, (Contours,Path) )
		self.input_dialog.video_selection_changed_event = self.__video_selection_changed_event
		self._input.value = self.input_dialog

		self.load_order = ['_input','_filter_panel']


		self._filter 				= TrackingFilter(parent=self, video=self.mainwindow.video)
		self._filter_panel.value 	= self._filter
		self._apply.value			= self.__apply_event
		self._apply.icon 			= conf.ANNOTATOR_ICON_PATH

		self._toggle_btn.value = self.__toggle_btn_click_event
		self._toggle_btn.checked = True


		self._progress.hide()

	def init_form(self):
		super(TrackingWindow, self). init_form()
		self.input_dialog.project = self.mainwindow.project
		
	def __toggle_btn_click_event(self):
		if self._input.visible:
			self._toggle_btn.label = 'Show datasets list'
			self._input.hide()
		else:
			self._toggle_btn.label = 'Hide datasets list'
			self._input.show()

	###########################################################################
	### EVENTS ################################################################
	###########################################################################

	def __video_selection_changed_event(self):
		video = self.input_dialog.selected_video
		self.player.stop()			
		self._filter.clear()
		self._filter.video = video
		self._filter.clear()
		self.player.update_frame()

	###########################################################################
	### PROPERTIES ############################################################
	###########################################################################

	@property
	def videos(self): return self.input_dialog.videos
	
	@property
	def player(self): return self._filter._player
	
	def __apply_event(self):

		if self._apply.checked:
			self._input.enabled 		= False
			self._filter_panel.enabled 	= False
			self._apply.label 	  		= 'Cancel'
			self.player.stop()
			
			# calculate the total number of frames to analyse
			total_2_analyse  = 0
			for video, (begin, end), datasets_list in self.input_dialog.selected_data:
				total_2_analyse += end-begin+1

			self._progress.min = 0
			self._progress.max = total_2_analyse
			self._progress.show()

			count = 0
			for video, (begin, end), datasets_list in self.input_dialog.selected_data:
				capture = cv2.VideoCapture(video.filepath)
				capture.set(cv2.CAP_PROP_POS_FRAMES, begin)

				self._filter.video = video
				self._filter.clear()
				
				begin, end = int(begin), int(end)+1

				#set the video in the one frame before and read the frame.
				#I use this technique because for some formats of videos opencv does not jump immediately to the requested frame
				blobs_paths = None

				for index in range(begin, end):
					res, frame = capture.read()
					
					if not res: break
					if not self._apply.checked: break

					blobs_paths = self._filter.processflow(frame)

					self._progress.value = count
					count += 1


				if blobs_paths is not None and self._apply.checked:

					if   len(blobs_paths)>len(datasets_list):
						datasets_list += [None for i in range(len(blobs_paths)-len(datasets_list))]
					elif len(blobs_paths)<len(datasets_list):
						blobs_paths += [None for i in range(len(datasets_list)-len(blobs_paths))]

					classifications = []
					for comb in combinations( blobs_paths, datasets_list):
						classification = 0
						for blob_path, dataset in comb:
							if not blob_path or not dataset: continue
							print(comb)

							distances = []
							for i, p1 in enumerate(blob_path.path):
								if p1 is None: continue 
								pos = dataset.get_position(begin + i)
								if pos is None: continue 

								p0   = pos
								dist = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
								
								distances.append( dist )

							classification += sum(distances)/len(distances)
						
						classifications.append( (classification, comb) )
						

					classifications = sorted(classifications, key=lambda x: x[0])

					if len(classifications)>0:
						for blob_path, dataset in classifications[0][1]:
							if dataset is None: continue
							for frame_index in range(begin, end):
								if blob_path is None:
									dataset.set_data_from_blob(frame_index, None)
								else:
									if len(blob_path)<=(frame_index-begin): continue
									blob = blob_path[frame_index-begin]
									dataset.set_data_from_blob(frame_index, blob)

















			self._input.enabled 		= True
			self._filter_panel.enabled 	= True
			self._apply.label 	  		= 'Apply'
			self._apply.checked   		= False
			self._progress.hide()





	


if __name__ == '__main__': 
	pyforms.startApp(TrackingWindow)
