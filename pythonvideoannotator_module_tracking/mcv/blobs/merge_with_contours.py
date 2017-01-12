from mcvapi.mcvbase import MCVBase
from pyforms import BaseWidget

class MergeWithContours(MCVBase, BaseWidget):
	
	# Group blobs by their path

	def __init__(self, **kwargs):
		BaseWidget.__init__(self, 'Track path')
		
		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(65)

		self.formset = ['Merge the contours']


		self._mergewithcontours_existing_contours = []
	
	def clear(self): self._trackpath_paths = []

	def process(self, paths):
		existing = contours

		
	def processflow(self, contours_list):
		contours_list = super(MergeWithContours, self).processflow(contours_list)
		return self.process(contours_list)

	@property 
	def contours_to_merge_with(self): 			self._mergewithcontours_existing_contours
	@contours_to_merge_with.setter
	def contours_to_merge_with(self, value): 	self._mergewithcontours_existing_contours = value