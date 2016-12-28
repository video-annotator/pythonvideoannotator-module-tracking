from pysettings import conf
import cv2, numpy as np, os, math
import base64

def points_angle(p1, p2): 
	x1, y1 = p1
	x2, y2 = p2
	rads = math.atan2(-(y2-y1),x2-x1)
	rads %= 2*np.pi
	return rads

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

		
		boundingrect_treenode = self.tree.create_child('bounding rect', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour)

		boundingrect_leftx_treenode = self.tree.create_child('left x', icon=conf.ANNOTATOR_ICON_X, parent=boundingrect_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_boundingbox_leftx_to_timeline_event, item=boundingrect_leftx_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_topy_treenode = self.tree.create_child('top y', icon=conf.ANNOTATOR_ICON_Y, parent=boundingrect_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_boundingbox_topy_to_timeline_event, item=boundingrect_topy_treenode,icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_width_treenode = self.tree.create_child('width', icon=conf.ANNOTATOR_ICON_WIDTH, parent=boundingrect_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_boundingbox_width_to_timeline_event, item=boundingrect_width_treenode,icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_height_treenode = self.tree.create_child('height', icon=conf.ANNOTATOR_ICON_HEIGHT, parent=boundingrect_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_boundingbox_height_to_timeline_event, item=boundingrect_height_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_aspectration_treenode = self.tree.create_child('aspect ratio', icon=conf.ANNOTATOR_ICON_ASPECT_RATIO, parent=boundingrect_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_aspect_ratio_to_timeline_event, item=boundingrect_aspectration_treenode,icon=conf.ANNOTATOR_ICON_TIMELINE)
		
		boundingrect_extend_treenode = self.tree.create_child('extend', icon=conf.ANNOTATOR_ICON_INFO, parent=boundingrect_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_extend_to_timeline_event, item=boundingrect_extend_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		boundingrect_treenode.win = boundingrect_extend_treenode.win = \
		boundingrect_width_treenode.win = boundingrect_height_treenode.win = \
		boundingrect_aspectration_treenode.win = boundingrect_leftx_treenode.win = \
		boundingrect_topy_treenode.win = self


	################# BOUNDING RECT ###################################################
		
	def __send_boundingbox_leftx_to_timeline_event(self):
		data = [(i,self.get_bounding_box(i)[0]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_graph('{0} bounding box - left x'.format(self.name), data)

	def __send_boundingbox_topy_to_timeline_event(self):
		data = [(i,self.get_bounding_box(i)[1]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_graph('{0} bounding box - top y'.format(self.name), data)

	def __send_boundingbox_width_to_timeline_event(self):
		data = [(i,self.get_bounding_box(i)[2]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_graph('{0} bounding box - width'.format(self.name), data)

	def __send_boundingbox_height_to_timeline_event(self):
		data = [(i,self.get_bounding_box(i)[3]) for i in range(len(self)) if self.get_bounding_box(i) is not None]
		self.mainwindow.add_graph('{0} bounding box - height'.format(self.name), data)









	################# EXTREME POINTS ####################################################
		
	def create_tracking_extremepoints_tree_nodes(self):

		extremepoints_treenode = self.tree.create_child('extreme points', 
			icon=conf.ANNOTATOR_ICON_ELLIPSE, parent=self.treenode_countour )

		
		p1_treenode = self.tree.create_child('p1', 
			icon=conf.ANNOTATOR_ICON_POINT, parent=extremepoints_treenode )

		p1_x_treenode = self.tree.create_child('x', icon=conf.ANNOTATOR_ICON_X, parent=p1_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', 
			function_action=self.__send_extremepts_p1_x_to_timeline_event, 
			item=p1_x_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		
		p1_y_treenode = self.tree.create_child('y', icon=conf.ANNOTATOR_ICON_Y, parent=p1_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', 
			function_action=self.__send_extremepts_p1_y_to_timeline_event, 
			item=p1_y_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		


		p2_treenode = self.tree.create_child('p2', 
			icon=conf.ANNOTATOR_ICON_POINT, parent=extremepoints_treenode )
				
		p2_x_treenode = self.tree.create_child('x', icon=conf.ANNOTATOR_ICON_X, parent=p2_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', 
			function_action=self.__send_extremepts_p2_x_to_timeline_event, 
			item=p2_x_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		
		p2_y_treenode = self.tree.create_child('y', icon=conf.ANNOTATOR_ICON_Y, parent=p2_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', 
			function_action=self.__send_extremepts_p2_y_to_timeline_event, 
			item=p2_y_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		

		angle_treenode = self.tree.create_child('angle', 
			icon=conf.ANNOTATOR_ICON_ANGLE, parent=extremepoints_treenode )
		self.tree.add_popup_menu_option(label='View on the timeline', 
			function_action=self.__send_extremepts_angle_to_timeline_event, 
			item=angle_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)


		extremepoints_treenode.win = angle_treenode.win = \
		p1_treenode.win = p1_x_treenode.win = p1_y_treenode.win = \
		p2_treenode.win = p2_x_treenode.win = p2_y_treenode.win = \
		angle_treenode.win = self
		

	################# FIT ELLISPSE ####################################################
	
	def __send_extremepts_p1_x_to_timeline_event(self):
		data = [(i,self.get_extreme_points(i)[0][0]) for i in range(len(self)) if self.get_extreme_points(i)[0] is not None]
		self.mainwindow.add_graph('{0} - extreme point p1 - x'.format(self.name), data)

	def __send_extremepts_p1_y_to_timeline_event(self):
		data = [(i,self.get_extreme_points(i)[0][1]) for i in range(len(self)) if self.get_extreme_points(i)[0] is not None]
		self.mainwindow.add_graph('{0} - extreme point p1 - y'.format(self.name), data)

	def __send_extremepts_p2_x_to_timeline_event(self):
		data = [(i,self.get_extreme_points(i)[1][0]) for i in range(len(self)) if self.get_extreme_points(i)[1] is not None]
		self.mainwindow.add_graph('{0} - extreme point p2 - x'.format(self.name), data)

	def __send_extremepts_p2_y_to_timeline_event(self):
		data = [(i,self.get_extreme_points(i)[1][1]) for i in range(len(self)) if self.get_extreme_points(i)[1] is not None]
		self.mainwindow.add_graph('{0} - extreme point p2 - x'.format(self.name), data)

	def __send_extremepts_angle_to_timeline_event(self):
		data = []
		for i in range(len(self)):
			p1, p2 = self.get_extreme_points(i)
			if p1 is not None and p2 is not None:
				data.append( (i, math.degrees(points_angle(p2, p1)) ) )
		self.mainwindow.add_graph('{0} - extreme points - angle - degrees'.format(self.name), data)













	################# FIT ELLISPSE ####################################################
		
	def create_tracking_fitellipse_tree_nodes(self):

		fitellipse_treenode = self.tree.create_child('fit ellipse', icon=conf.ANNOTATOR_ICON_ELLIPSE, parent=self.treenode_countour )
		
		fitellipse_centerx_treenode = self.tree.create_child('center x', icon=conf.ANNOTATOR_ICON_X, parent=fitellipse_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_fitellipse_centerx_to_timeline_event, item=fitellipse_centerx_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_centery_treenode = self.tree.create_child('center y', icon=conf.ANNOTATOR_ICON_Y, parent=fitellipse_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_fitellipse_centery_to_timeline_event, item=fitellipse_centery_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_majoraxis_treenode = self.tree.create_child('Major axis size', icon=conf.ANNOTATOR_ICON_HEIGHT, parent=fitellipse_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_fitellipse_majoraxis_to_timeline_event, item=fitellipse_majoraxis_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_minoraxis_treenode = self.tree.create_child('Minor axis size', icon=conf.ANNOTATOR_ICON_WIDTH, parent=fitellipse_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_fitellipse_minoraxis_to_timeline_event, item=fitellipse_minoraxis_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_angle_treenode = self.tree.create_child('Angle', icon=conf.ANNOTATOR_ICON_ANGLE, parent=fitellipse_treenode)
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_fitellipse_angle_to_timeline_event, item=fitellipse_angle_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		fitellipse_treenode.win = fitellipse_centerx_treenode.win = \
		fitellipse_centery_treenode.win = fitellipse_majoraxis_treenode.win = \
		fitellipse_minoraxis_treenode.win = fitellipse_angle_treenode.win = self


	################# FIT ELLISPSE ####################################################
	
	def __send_fitellipse_centerx_to_timeline_event(self):
		data = [(i,self.get_fit_ellipse(i)[0]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_graph('{0} fit ellipse - center x'.format(self.name), data)

	def __send_fitellipse_centery_to_timeline_event(self):
		data = [(i,self.get_fit_ellipse(i)[1]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_graph('{0} fit ellipse - center y'.format(self.name), data)

	def __send_fitellipse_majoraxis_to_timeline_event(self):
		data = [(i,self.get_fit_ellipse(i)[2]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_graph('{0} fit ellipse - major axis'.format(self.name), data)

	def __send_fitellipse_minoraxis_to_timeline_event(self):
		data = [(i,self.get_fit_ellipse(i)[3]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_graph('{0} fit ellipse - minor axis'.format(self.name), data)

	def __send_fitellipse_angle_to_timeline_event(self):
		data = [(i,self.get_fit_ellipse(i)[3]) for i in range(len(self)) if self.get_fit_ellipse(i) is not None]
		self.mainwindow.add_graph('{0} fit ellipse - angle'.format(self.name), data)








	def create_tracking_tree_nodes(self):		
		self.treenode_countour 	= self.tree.create_child('countour', icon=conf.ANNOTATOR_ICON_CONTOUR, parent=self.treenode )
		
		################# CONTOUR #########################################################
		
		area_treenode = self.tree.create_child('area', icon=conf.ANNOTATOR_ICON_AREA, parent=self.treenode_countour )
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_area_to_timeline_event, item=area_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)

		equivalentdiameter_treenode = self.tree.create_child('equivalent diameter', icon=conf.ANNOTATOR_ICON_CIRCLE, parent=self.treenode_countour )
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_equivalent_diameter_to_timeline_event, item=equivalentdiameter_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		

		self.create_tracking_boundingrect_tree_nodes()		
		self.create_tracking_fitellipse_tree_nodes()
		self.create_tracking_extremepoints_tree_nodes()
		
		################# CONVEX HULL #####################################################
		
		convexhull_treenode = self.tree.create_child('convex hull', icon=conf.ANNOTATOR_ICON_HULL, parent=self.treenode_countour )
		

		solidity_treenode = self.tree.create_child('solidity', icon=conf.ANNOTATOR_ICON_BLACK_CIRCLE, parent=convexhull_treenode )
		self.tree.add_popup_menu_option(label='View on the timeline', function_action=self.__send_solidity_to_timeline_event, item=solidity_treenode, icon=conf.ANNOTATOR_ICON_TIMELINE)
		

		
		solidity_treenode.win = equivalentdiameter_treenode.win = \
		convexhull_treenode.win = \
		self.treenode_countour.win = area_treenode.win = self


	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	################# CONTOUR #########################################################
		
	def __send_area_to_timeline_event(self):
		data = [(i,self.get_area(i)) for i in range(len(self)) if self.get_area(i) is not None]
		self.mainwindow.add_graph('{0} area'.format(self.name), data)

	def __send_equivalent_diameter_to_timeline_event(self):
		data = [(i,self.get_equivalent_diameter(i)) for i in range(len(self)) if self.get_equivalent_diameter(i) is not None]
		self.mainwindow.add_graph('{0} equivalent diameter'.format(self.name), data)

	
	
	def __send_aspect_ratio_to_timeline_event(self):
		data = [(i,self.get_aspect_ratio(i)) for i in range(len(self)) if self.get_aspect_ratio(i) is not None]
		self.mainwindow.add_graph('{0} aspect ratio'.format(self.name), data)

	def __send_extend_to_timeline_event(self):
		data = [(i,self.get_extend(i)) for i in range(len(self)) if self.get_extend(i) is not None]
		self.mainwindow.add_graph('{0} extend'.format(self.name), data)

	def __send_solidity_to_timeline_event(self):
		data = [(i,self.get_solidity(i)) for i in range(len(self)) if self.get_solidity(i) is not None]
		self.mainwindow.add_graph('{0} solidity'.format(self.name), data)

	

	######################################################################
	### DATA ACCESS FUNCTIONS ############################################
	######################################################################

	def get_bounding_box(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		return cv2.boundingRect(cnt)
		
	def get_fit_ellipse(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		return cv2.fitEllipse(cnt)
		
	def get_convex_hull(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		pass


	def get_extend(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		x,y,w,h = cv2.boundingRect(cnt)
		rect_area = w*h
		return float(area)/float(rect_area)

	def get_solidity(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		hull = cv2.convexHull(cnt)
		hull_area = cv2.contourArea(hull)
		return float(area)/float(hull_area)

	def get_equivalent_diameter(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		return np.sqrt(4*area/np.pi)


	def get_aspect_ratio(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		x,y,w,h = cv2.boundingRect(cnt)
		return float(w)/float(h)

	def get_area(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		return cv2.contourArea(cnt)


	def get_extreme_points(self, index):
		centroid = self.get_position(index)
		contour  = self.get_contour(index)

		if centroid is not None and contour is not None:
			dists = map( lambda p: self.__lin_dist( p[0], centroid ), contour )
			ndx = dists.index(max(dists))			
			head = tuple(contour[ndx][0])
			
			dists = map( lambda p: self.__lin_dist( p[0], contour[ndx][0] ), contour )
			ndx = dists.index(max(dists))
			tail = tuple(contour[ndx][0])
			
			return head, tail
		else:
			return None, None


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

		head, tail = self.get_extreme_points(frame_index)
		if head is not None:
			cv2.circle(frame, head, 5, (255,255,255), -1)
			cv2.circle(frame, head, 3, (100,0,100), -1)
		if tail is not None:
			cv2.circle(frame, tail, 5, (255,255,255), -1)
			cv2.circle(frame, tail, 3, (100,100,0), -1)

	def __lin_dist(self, p1, p2): return np.linalg.norm( (p1[0]-p2[0], p1[1]-p2[1]) )






	######################################################################################
	#### IO FUNCTIONS ####################################################################
	######################################################################################


	def save(self, data, datasets_path=None):
		data = super(TrackingPath, self).save(data, datasets_path)
		dataset_path = data['path']
		
		contours_file = os.path.join(dataset_path, 'contours.csv')
		with open(contours_file, 'wb') as outfile:
			outfile.write(';'.join(['frame','contour','shape'])+'\n' )
			for index in range(len(self._path)):
				contour = self.get_contour(index)
				row = [index] + ([None, None] if contour is None else [base64.b64encode(contour), contour.shape])
				outfile.write(';'.join( map(str,row) ))
				outfile.write('\n')

		return data

	def load(self, data, dataset_path=None):
		super(TrackingPath, self).load(data, dataset_path)		
		contours_file = os.path.join(dataset_path, 'contours.csv')
		
		if os.path.exists(contours_file):
			with open(contours_file, 'r') as infile:
				infile.readline()
				for i, line in enumerate(infile):
					csvrow = line[:-1].split(';')
					
					if csvrow[1] is None or csvrow[2] is None: 		continue
					if len(csvrow[1])==0 or len(csvrow[2])==0: 		continue
					if csvrow[1] == 'None' or csvrow[2] == 'None': 	continue
					
					frame = int(csvrow[0])
					shape = eval(csvrow[2])
					contour = np.frombuffer(base64.decodestring(csvrow[1]), np.int32)
					contour = contour.reshape(shape)
					self.set_contour(frame, contour)