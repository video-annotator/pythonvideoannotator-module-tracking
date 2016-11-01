from pysettings import conf
import cv2, numpy as np

class TrackingPath(object):

	def __init__(self, name=None):
		super(TrackingPath, self).__init__(name)

		self._contours = []
		
	######################################################################
	### EVENTS ###########################################################
	######################################################################

	def name_updated(self, newname):
		super(TrackingPath, self).name_updated(newname)
		if hasattr(self,'mainwindow'): self.mainwindow.tracking_window.update_datasets()













	################# BOUNDING RECT ###################################################
		
	def create_tracking_boundingrect_tree_nodes(self):

		
		boundingrect_treenode = self.tree.createChild('bounding rect', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour)

		boundingrect_leftx_treenode = self.tree.createChild('left x', icon=conf.ANNOTATOR_ICON_AREA, parent=boundingrect_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_boundingbox_leftx_to_timeline_evt, item=boundingrect_leftx_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_topy_treenode = self.tree.createChild('top y', icon=conf.ANNOTATOR_ICON_AREA, parent=boundingrect_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_boundingbox_topy_to_timeline_evt, item=boundingrect_topy_treenode,icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_width_treenode = self.tree.createChild('width', icon=conf.ANNOTATOR_ICON_AREA, parent=boundingrect_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_boundingbox_width_to_timeline_evt, item=boundingrect_width_treenode,icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_height_treenode = self.tree.createChild('height', icon=conf.ANNOTATOR_ICON_AREA, parent=boundingrect_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_boundingbox_height_to_timeline_evt, item=boundingrect_height_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_aspectration_treenode = self.tree.createChild('aspect ratio', icon=conf.ANNOTATOR_ICON_AREA, parent=boundingrect_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_aspect_ratio_to_timeline_evt, item=boundingrect_aspectration_treenode,icon=conf.ANNOTATOR_ICON_TIMELINE)
		
		boundingrect_extend_treenode = self.tree.createChild('extend', icon=conf.ANNOTATOR_ICON_AREA, parent=boundingrect_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_extend_to_timeline_evt, item=boundingrect_extend_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_treenode.win = boundingrect_extend_treenode.win = \
		boundingrect_width_treenode.win = boundingrect_height_treenode.win = \
		boundingrect_aspectration_treenode.win = boundingrect_leftx_treenode.win = \
		boundingrect_topy_treenode.win = self


	################# BOUNDING RECT ###################################################
		
	def __send_boundingbox_leftx_to_timeline_evt(self):
		data = [(i,self.get_bounding_box(i)[0]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_chart('{0} bounding box - left x'.format(self.name), data)

	def __send_boundingbox_topy_to_timeline_evt(self):
		data = [(i,self.get_bounding_box(i)[1]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_chart('{0} bounding box - top y'.format(self.name), data)

	def __send_boundingbox_width_to_timeline_evt(self):
		data = [(i,self.get_bounding_box(i)[2]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_chart('{0} bounding box - width'.format(self.name), data)

	def __send_boundingbox_height_to_timeline_evt(self):
		data = [(i,self.get_bounding_box(i)[3]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_chart('{0} bounding box - height'.format(self.name), data)









	################# FIT ELLISPSE ####################################################
		
	def create_tracking_fitellipse_tree_nodes(self):

		fitellipse_treenode = self.tree.createChild('fit ellipse', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour )
		
		fitellipse_centerx_treenode = self.tree.createChild('center x', icon=conf.ANNOTATOR_ICON_AREA, parent=fitellipse_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_fitellipse_centerx_to_timeline_evt, item=fitellipse_centerx_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_centery_treenode = self.tree.createChild('center y', icon=conf.ANNOTATOR_ICON_AREA, parent=fitellipse_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_fitellipse_centery_to_timeline_evt, item=fitellipse_centery_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_majoraxis_treenode = self.tree.createChild('Major axis size', icon=conf.ANNOTATOR_ICON_AREA, parent=fitellipse_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_fitellipse_majoraxis_to_timeline_evt, item=fitellipse_majoraxis_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_minoraxis_treenode = self.tree.createChild('Minor axis size', icon=conf.ANNOTATOR_ICON_AREA, parent=fitellipse_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_fitellipse_minoraxis_to_timeline_evt, item=fitellipse_minoraxis_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_angle_treenode = self.tree.createChild('Angle', icon=conf.ANNOTATOR_ICON_AREA, parent=fitellipse_treenode)
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_fitellipse_angle_to_timeline_evt, item=fitellipse_angle_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)


	################# FIT ELLISPSE ####################################################
	
	def __send_fitellipse_centerx_to_timeline_evt(self):
		data = [(i,self.get_fit_ellipse(i)[0]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_chart('{0} fit ellipse - center x'.format(self.name), data)

	def __send_fitellipse_centery_to_timeline_evt(self):
		data = [(i,self.get_fit_ellipse(i)[1]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_chart('{0} fit ellipse - center y'.format(self.name), data)

	def __send_fitellipse_majoraxis_to_timeline_evt(self):
		data = [(i,self.get_fit_ellipse(i)[2]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_chart('{0} fit ellipse - major axis'.format(self.name), data)

	def __send_fitellipse_minoraxis_to_timeline_evt(self):
		data = [(i,self.get_fit_ellipse(i)[3]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_chart('{0} fit ellipse - minor axis'.format(self.name), data)

	def __send_fitellipse_angle_to_timeline_evt(self):
		data = [(i,self.get_fit_ellipse(i)[3]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_chart('{0} fit ellipse - angle'.format(self.name), data)








	def create_tracking_tree_nodes(self):		
		self.treenode_countour 	= self.tree.createChild('countour', icon=conf.ANNOTATOR_ICON_CONTOUR, parent=self.treenode )
		
		################# CONTOUR #########################################################
		
		area_treenode = self.tree.createChild('area', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour )
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_area_to_timeline_evt, item=area_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		equivalentdiameter_treenode = self.tree.createChild('equivalent diameter', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour )
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_equivalent_diameter_to_timeline_evt, item=equivalentdiameter_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		

		self.create_tracking_boundingrect_tree_nodes()		
		self.create_tracking_fitellipse_tree_nodes()
		
		################# CONVEX HULL #####################################################
		
		convexhull_treenode = self.tree.createChild('convex hull', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour )
		

		solidity_treenode = self.tree.createChild('solidity', icon=conf.ANNOTATOR_ICON_AREA, parent=convexhull_treenode )
		self.tree.addPopupMenuOption(label='View on the timeline', functionAction=self.__send_solidity_to_timeline_evt, item=solidity_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		

		
		solidity_treenode.win = equivalentdiameter_treenode.win = \
		self.treenode_countour.win = area_treenode.win = self


	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	################# CONTOUR #########################################################
		
	def __send_area_to_timeline_evt(self):
		data = [(i,self.get_area(i)) for i in range(len(self))]
		self.mainwindow.add_chart('{0} area'.format(self.name), data)

	def __send_equivalent_diameter_to_timeline_evt(self):
		data = [(i,self.get_equivalent_diameter(i)) for i in range(len(self))]
		self.mainwindow.add_chart('{0} equivalent diameter'.format(self.name), data)

	
	
	def __send_aspect_ratio_to_timeline_evt(self):
		data = [(i,self.get_aspect_ratio(i)) for i in range(len(self))]
		self.mainwindow.add_chart('{0} aspect ratio'.format(self.name), data)

	def __send_extend_to_timeline_evt(self):
		data = [(i,self.get_extend(i)) for i in range(len(self))]
		self.mainwindow.add_chart('{0} extend'.format(self.name), data)

	def __send_solidity_to_timeline_evt(self):
		data = [(i,self.get_solidity(i)) for i in range(len(self))]
		self.mainwindow.add_chart('{0} solidity'.format(self.name), data)

	

	######################################################################
	### DATA ACCESS FUNCTIONS ############################################
	######################################################################

	def get_bounding_box(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		return cv2.boundingRect(cnt)
		
	def get_fit_ellipse(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		return cv2.fitEllipse(cnt)
		
	def get_convex_hull(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		pass


	def get_extend(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		area = cv2.contourArea(cnt)
		x,y,w,h = cv2.boundingRect(cnt)
		rect_area = w*h
		return float(area)/float(rect_area)

	def get_solidity(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		area = cv2.contourArea(cnt)
		hull = cv2.convexHull(cnt)
		hull_area = cv2.contourArea(hull)
		return float(area)/float(hull_area)

	def get_equivalent_diameter(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		area = cv2.contourArea(cnt)
		return np.sqrt(4*area/np.pi)


	def get_aspect_ratio(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		x,y,w,h = cv2.boundingRect(cnt)
		return float(w)/float(h)

	def get_area(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return 0
		return cv2.contourArea(cnt)





	def get_contour(self, index):
		if index<0 or index>=len(self._contours): return None
		return self._contours[index] if self._contours[index] is not None else None

	def set_contour(self, index, contour):
		if not hasattr(self, 'treenode_countour'): self.create_tracking_tree_nodes()
		# add contours in case they do not exists
		if index >= len(self._contours):
			for i in range(len(self._contours), index + 1): self._contours.append(None)
		self._contours[index] = contour
	
	def set_data_from_blob(self,index, blob):
		x,y = blob._centroid
		self.set_position(index, x, y)

		self.set_contour(index, blob._contour)


	def draw(self, frame, frame_index):
		super(TrackingPath, self).draw(frame, frame_index)

		cnt = self.get_contour(frame_index)
		if cnt is not None: cv2.polylines(frame, np.array( [cnt] ), True, (0,255,0), 2)