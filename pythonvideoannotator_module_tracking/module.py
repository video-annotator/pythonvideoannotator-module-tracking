import cv2
from pysettings import conf
from pythonvideoannotator_module_tracking.tracking_window import TrackingWindow


class Module(object):

	def __init__(self):
		"""
		This implements the Path edition functionality
		"""
		super(Module, self).__init__()


		self.tracking_window = TrackingWindow(self)


		self.mainmenu[1]['Modules'].append(
			{'Tracking': self.tracking_window.show, 'icon':conf.ANNOTATOR_ICON_PATH },			
		)


	def video_changed_evt(self):
		super(Module, self).video_changed_evt()
		self.tracking_window.video_filename = self._video.value
	

	def add_dataset_evt(self, dataset):
		super(Module, self).add_dataset_evt(dataset)
		self.tracking_window.add_dataset_evt(dataset)

	def remove_dataset_evt(self, dataset):
		super(Module, self).remove_dataset_evt(dataset)
		self.tracking_window.remove_dataset_evt(dataset)

	def remove_object_evt(self, obj):
		super(Module, self).remove_object_evt(obj)
		self.tracking_window.remove_object_evt(obj)


	
	######################################################################################
	#### IO FUNCTIONS ####################################################################
	######################################################################################

	
	def save(self, data, project_path=None):
		data = super(Module, self).save(data, project_path)
		data['tracking-settings'] = self.tracking_window.save({})
		return data

	def load(self, data, project_path=None):
		super(Module, self).load(data, project_path)
		if 'tracking-settings' in data: self.tracking_window.load(data['tracking-settings'])
