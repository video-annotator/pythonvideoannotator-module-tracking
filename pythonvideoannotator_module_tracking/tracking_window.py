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

from mcvgui.dialogs.simple_filter import SimpleFilter
from mcvapi.blobs.order_by_position import combinations

from pythonvideoannotator_models_gui.dialogs.paths_and_intervals_selector import PathsAndIntervalsSelectorDialog

import json

class TrackingWindow(BaseWidget):

	def __init__(self, parent=None):
		super(TrackingWindow, self).__init__('Tracking', parent_win=parent)
		self.mainwindow = parent

		self.layout().setMargin(5)
		self.setMinimumHeight(800)
		self.setMinimumWidth(1100)

		self._paths_panel	= ControlEmptyWidget('Paths')
		self._start 		= ControlNumber('Start on frame',0)
		self._end 			= ControlNumber('End on frame', 10)		
		self._filter_panel 	= ControlEmptyWidget('Filter')
		self._progress  	= ControlProgress('Progress')
		self._apply 		= ControlButton('Apply', checkable=True)
		
		self._formset = [			
			'_paths_panel',
			'=',
			'_filter_panel',
			'_apply',
			'_progress'
		]

		self.paths_dialog = PathsAndIntervalsSelectorDialog(self)
		self.paths_dialog.video_selection_changed_event = self.__video_selection_changed_event
		self._paths_panel.value = self.paths_dialog

		self.load_order = ['_paths_panel','_filter_panel']


		self._filter 				= SimpleFilter(parent=self, video=self.mainwindow.video)
		self._filter_panel.value 	= self._filter
		self._apply.value			= self.__apply_event
		self._apply.icon 			= conf.ANNOTATOR_ICON_PATH

		self._progress.hide()

	def init_form(self):
		super(TrackingWindow, self). init_form()
		self.paths_dialog.project = self.mainwindow.project
		

	###########################################################################
	### EVENTS ################################################################
	###########################################################################

	def __video_selection_changed_event(self):
		video = self.paths_dialog.current_video
		self.player.stop()			
		self._filter.clear()
		self._filter.video_capture = video.video_capture if video is not None else None
		self._filter.clear()
		self.player.update_frame()

			

	###########################################################################
	### PROPERTIES ############################################################
	###########################################################################

	@property
	def paths(self): return self.paths_dialog.paths
	

	@property
	def player(self): return self._filter._player
	
	def __apply_event(self):

		if self._apply.checked:
			self._start.enabled 		= False
			self._end.enabled 			= False
			self._paths_panel.enabled 	= False
			self._filter_panel.enabled 	= False
			self._apply.label 			= 'Cancel'

			#try:

			total_2_analyse  = 0
			for video, (begin, end), paths in self.paths_dialog.selected_data:
				capture 		 = video.video_capture
				total_2_analyse += end-begin

			self._progress.min = 0
			self._progress.max = total_2_analyse
			self._progress.show()

			count = 0
			for video, (begin, end), paths in self.paths_dialog.selected_data:
				if len(paths)==0: continue
				begin, end = int(begin), int(end)

				self._filter.clear()
				self._filter.video_capture = capture = video.video_capture
				

				capture.set(cv2.CAP_PROP_POS_FRAMES, begin); 
				
				blobs_paths = None

				for index in range(begin, end+1):
					res, frame = capture.read()
					if not res: break
					if not self._apply.checked: break

					blobs_paths = self._filter.processflow(frame)
					self._progress.value = count
					count += 1

				if blobs_paths is not None and self._apply.checked:
					
					print video, begin, end, paths
				
					if len(paths)>len(paths):
						paths += [None for i in range(len(blobs_paths)-len(paths))]
					elif len(paths)<len(paths):
						paths += [None for i in range(len(paths)-len(blobs_paths))]

					classifications = []
					for comb in combinations( blobs_paths, paths):
						print comb
				
						classification = 0
						for blob_path, obj in comb:
							if not blob_path or not obj: continue

							distances = []
							for i, p1 in enumerate(blob_path.path):
								if p1 is None: continue 
								pos = obj.get_position(begin + i)
								if pos is None: continue 

								p0   = pos
								dist = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
								
								distances.append( dist )

							classification += sum(distances)/len(distances)
						
						classifications.append( (classification, comb) )
						
					classifications = sorted(classifications, key=lambda x: x[0])
					if len(classifications)>0:
						for blob_path, path in classifications[0][1]:
							if obj is None: continue
							for frame_index in range(begin, end+1):
								blob = blob_path[frame_index-begin]
								if blob: path.set_data_from_blob(frame_index, blob)

			#except Exception as e:
			#	print("Error", e)
								

			self._start.enabled 		= True
			self._end.enabled 			= True
			self._paths_panel.enabled 	= True
			self._filter_panel.enabled 	= True
			self._apply.label 			= 'Apply'
			self._apply.checked 		= False
			self._progress.hide()





	


if __name__ == '__main__': 
	pyforms.startApp(TrackingWindow)
