import pyforms, cv2, base64, numpy as np
from pyforms import BaseWidget
from pyforms.Controls import ControlEmptyWidget
from mcvapi.masks.polygons_mask import PolygonsMask as Class
from pythonvideoannotator_models_gui.models.video.objects.geometry import Geometry

from pythonvideoannotator_models_gui.dialogs import ObjectsDialog

class PolygonsMask(Class, BaseWidget):
	
	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Polygons Mask')
		Class.__init__(self, **kwargs)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(150)

		self._panel	= ControlEmptyWidget('Panel', ObjectsDialog() )
		self._panel.value.objects_filter = lambda x: isinstance(x, Geometry)
		self._panel.value.objects_changed_event = self.__objects_changed_event

	def destroy(self, destroyWindow = True, destroySubWindows = True):
		self._panel.value.destroy(destroyWindow, destroySubWindows)
		super(PolygonsMask, self).destroy(destroyWindow, destroySubWindows)

	def __objects_changed_event(self):
		polygons_list = []
		for video, polygons_set in self._panel.value.selected_data:
			print video.video_capture,'==',self._video
			if video.video_capture==self._video: 
				for polygons in polygons_set:
					polygons_list += [p for l, p in polygons.geometry]
				break
		self._param_polygons_mask = None
		self._param_polygons_polys = np.int32(polygons_list)

	@property
	def video(self): return None
	@video.setter 
	def video(self, value):
		self._video = value
		self.__objects_changed_event()



if __name__ == '__main__': 
	pyforms.start_app(PolygonsMask)