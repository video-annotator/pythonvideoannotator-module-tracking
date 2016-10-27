

class TrackingPath(object):

	def __init__(self, name=None):
		super(TrackingPath, self).__init__(name)
		
	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def name_updated(self, newname):
		super(TrackingPath, self).name_updated(newname)
		if hasattr(self,'mainwindow'): self.mainwindow.tracking_window.update_datasets()