

class TrackingObject2d(object):

	def __init__(self, objects_set):
		super(TrackingObject2d, self).__init__(objects_set)
		
	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def name_updated(self, newname):
		super(TrackingObject2d, self).name_updated(newname)
		if hasattr(self,'mainwindow'): self.mainwindow.tracking_window.update_datasets()