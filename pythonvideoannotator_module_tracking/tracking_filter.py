from mcvgui.dialogs.simple_filter import SimpleFilter
import pyforms

from mcvgui.filters.adaptative_threshold 	import AdaptativeThreshold
from mcvgui.masks.polygons_mask 			import PolygonsMask
from mcvgui.masks.path_mask 				import PathMask

from mcvgui.blobs.find_blobs 			import FindBlobs
from mcvgui.blobs.biggests_blobs 		import BiggestsBlobs
from mcvgui.blobs.order_by_position 	import OrderByPosition
from mcvgui.blobs.track_path 			import TrackPath

from pythonvideoannotator_models_gui.dialogs import DatasetsDialog

from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.contours import Contours
from pythonvideoannotator_models_gui.models.video.objects.object2d.datasets.path import Path



class TrackingFilter(SimpleFilter):


	def __init__(self, parent=None, video=None):
		SimpleFilter.__init__(self,parent, video)

		self.paths_2_mask  = None
		self.video_capture = None
		self._video = None
		
		self.__load_blobs_filters()
		self.__load_images_filters()

	########################################################################
	### PRIVATE FUNCTION ###################################################
	########################################################################

	def __create_path_mask(self):
		maskfilter = PathMask()
		maskfilter.pathmask_select_paths_event = self.__select_paths_2_mask_event
		return maskfilter
		
	def __load_images_filters(self):
		# set the available filters for the images
		self.add_image_filters('Adaptative threshold', [
			('Threshold', 	AdaptativeThreshold )
		])

		self.add_image_filters('Adaptative threshold + mask', [
			('Threshold', 	AdaptativeThreshold ),
			('Mask', 		PolygonsMask 		)
		])
		
		self.add_image_filters('Adaptative threshold + path mask', [
			('Threshold', 	AdaptativeThreshold ),
			('Paths', 		self.__create_path_mask  )
		])

		self.add_image_filters('Adaptative threshold + mask + path mask', [
			('Threshold', 	AdaptativeThreshold ),
			('Mask', 		PolygonsMask 		),
			('Paths', 		self.__create_path_mask  )
		])

	def __load_blobs_filters(self):
		# set the available filters for the blobs
		self.add_blobs_filters('Find blobs + track path', [
			('Find the blobs', 		FindBlobs 		),
			('Select the biggests', BiggestsBlobs 	),
			('Sort blobs', 			OrderByPosition ),
			('Tack paths', 			TrackPath		)
		])

	def __update_paths_mask(self):
		# set the paths for the PathMask filters		
		for f in self.image_filters: 
			if isinstance(f, PathMask):
				f.mask_paths = [path for path in self._paths_2_mask if path.object2d.video==self.video]

	########################################################################
	### EVENTS #############################################################
	########################################################################

	def __select_paths_2_mask_event(self):
		# open the datasets dialog for the PathMask filter
		if not hasattr(self, '_paths2mask_dialog'):
			self._paths2mask_dialog = DatasetsDialog()
			self._paths2mask_dialog.interval_visible   = False
			self._paths2mask_dialog.apply_event = self.__paths_2_mask_selected_event
			self._paths2mask_dialog.datasets_filter = lambda x: isinstance(x, (Contours,Path) )

		self._paths2mask_dialog.clear()
		for video in self.parentwindow.videos: self._paths2mask_dialog += video		
		self._paths2mask_dialog.show()

	def __paths_2_mask_selected_event(self):
		# function called when the apply button from the _paths2mask_dialog is pressed
		self._paths2mask_dialog.hide()
		self._paths_2_mask = self._paths2mask_dialog.datasets
		self.__update_paths_mask()


	
	########################################################################
	### PROPERTIES #########################################################
	########################################################################

	@property
	def video(self): return self._video
	@video.setter
	def video(self, value):
		self._video 		= value
		self.video_capture 	= value.video_capture if value is not None else None


	@property
	def parentwindow(self): return self._parent
	

	



if __name__ == '__main__': 
	pyforms.start_app(TrackingFilter)