from pysettings import conf
from pythonvideoannotator.utils import tools
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
		self.create_group_node('contour > bounding rect', icon=conf.ANNOTATOR_ICON_AREA)
		self.create_data_node('contour > bounding rect > left x', icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('contour > bounding rect > left y', icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('contour > bounding rect > width',  icon=conf.ANNOTATOR_ICON_WIDTH)
		self.create_data_node('contour > bounding rect > height', icon=conf.ANNOTATOR_ICON_HEIGHT)	
		self.create_data_node('contour > bounding rect > aspect ratio', icon=conf.ANNOTATOR_ICON_ASPECT_RATIO)
		self.create_data_node('contour > bounding rect > area',   icon=conf.ANNOTATOR_ICON_AREA)		
		self.create_data_node('contour > bounding rect > extend', icon=conf.ANNOTATOR_ICON_INFO)

	def get_contour_boundingrect_leftx_value(self, index):
		v = self.get_bounding_box(index)
		return v[0] if v is not None else None

	def get_contour_boundingrect_lefty_value(self, index):
		v = self.get_bounding_box(index)
		return v[1] if v is not None else None

	def get_contour_boundingrect_width_value(self, index):
		v = self.get_bounding_box(index)
		return v[2] if v is not None else None

	def get_contour_boundingrect_height_value(self, index):
		v = self.get_bounding_box(index)
		return v[3] if v is not None else None

	def get_contour_boundingrect_aspectratio_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		x,y,w,h = cv2.boundingRect(cnt)
		return float(w)/float(h)

	def get_contour_boundingrect_area_value(self, index):
		v = self.get_bounding_box(index)
		return v[0]*v[1] if v is not None else None
		
	def get_contour_boundingrect_extend_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		x,y,w,h = cv2.boundingRect(cnt)
		rect_area = w*h
		return float(area)/float(rect_area)

	################# BOUNDING RECT ###################################################









	################# EXTREME POINTS ####################################################
		
	def create_tracking_extremepoints_tree_nodes(self):
		self.create_group_node('contour > extreme points', 			icon=conf.ANNOTATOR_ICON_ELLIPSE)
		
		self.create_group_node('contour > extreme points > p1', 	icon=conf.ANNOTATOR_ICON_POINT)
		self.create_data_node('contour > extreme points > p1 > x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('contour > extreme points > p1 > y', 	icon=conf.ANNOTATOR_ICON_Y)
		
		self.create_group_node('contour > extreme points > p2', 	icon=conf.ANNOTATOR_ICON_POINT)
		self.create_data_node('contour > extreme points > p2 > x', 	icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('contour > extreme points > p2 > y', 	icon=conf.ANNOTATOR_ICON_Y)
		
		self.create_data_node('contour > extreme points > angle', 	icon=conf.ANNOTATOR_ICON_ANGLE)		
		
	def get_contour_extremepoints_p1_x_value(self, index):
		v = self.get_extreme_points(index)
		return v[0][0] if v is not None else None

	def get_contour_extremepoints_p1_y_value(self, index):
		v = self.get_extreme_points(index)
		return v[0][1] if v is not None else None

	def get_contour_extremepoints_p2_x_value(self, index):
		v = self.get_extreme_points(index)
		return v[1][0] if v is not None else None

	def get_contour_extremepoints_p2_y_value(self, index):
		v = self.get_extreme_points(index)
		return v[1][1] if v is not None else None

	def get_contour_extremepoints_angle_value(self, index):
		v = self.get_extreme_points(index)
		return math.degrees(points_angle(v[0], v[1])) if v is not None else None

	################# FIT ELLISPSE ####################################################











	################# FIT ELLIPSE ####################################################
		
	def create_tracking_fitellipse_tree_nodes(self):
		self.create_group_node('contour > fit ellipse', 				 icon=conf.ANNOTATOR_ICON_ELLIPSE)
		self.create_data_node('contour > fit ellipse > center x', 		 icon=conf.ANNOTATOR_ICON_X)
		self.create_data_node('contour > fit ellipse > center y', 		 icon=conf.ANNOTATOR_ICON_Y)
		self.create_data_node('contour > fit ellipse > major axis size', icon=conf.ANNOTATOR_ICON_HEIGHT)
		self.create_data_node('contour > fit ellipse > minor axis size', icon=conf.ANNOTATOR_ICON_WIDTH)
		self.create_data_node('contour > fit ellipse > angle', 			 icon=conf.ANNOTATOR_ICON_ANGLE)
		
	def get_contour_fitellipse_centerx_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[0][0] if v is not None else None

	def get_contour_fitellipse_centery_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[0][1] if v is not None else None

	def get_contour_fitellipse_majoraxissize_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[1][0] if v is not None else None

	def get_contour_fitellipse_minoraxissize_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[1][1] if v is not None else None

	def get_contour_fitellipse_angle_value(self, index):
		v = self.get_fit_ellipse(index)
		return v[2] if v is not None else None

	################# FIT ELLIPSE ####################################################









	################# CONVEX HULL ####################################################
		
	def create_tracking_convexhull_tree_nodes(self):
		self.create_group_node('contour > convex hull', 		  icon=conf.ANNOTATOR_ICON_HULL)
		self.create_data_node('contour > convex hull > solidity', icon=conf.ANNOTATOR_ICON_BLACK_CIRCLE)
		
	def get_contour_convexhull_solidity_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		hull = cv2.convexHull(cnt)
		hull_area = cv2.contourArea(hull)
		return float(area)/float(hull_area)

	################# CONVEX HULL ####################################################








	def create_tracking_tree_nodes(self):
		self.create_group_node('contour', icon=conf.ANNOTATOR_ICON_CONTOUR)
		
		
		################# CONTOUR #########################################################
		self.create_data_node('contour > area', icon=conf.ANNOTATOR_ICON_AREA)
		self.create_data_node('contour > equivalent diameter', icon=conf.ANNOTATOR_ICON_CIRCLE)

		self.create_tracking_boundingrect_tree_nodes()		
		self.create_tracking_fitellipse_tree_nodes()
		self.create_tracking_extremepoints_tree_nodes()
		self.create_tracking_convexhull_tree_nodes()
				
	######################################################################
	### FUNCTIONS ########################################################
	######################################################################

	################# CONTOUR #########################################################

	def get_contour_area_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		return cv2.contourArea(cnt)	

	def get_contour_equivalentdiameter_value(self, index):
		cnt = self.get_contour(index)
		if cnt is None: return None
		area = cv2.contourArea(cnt)
		return np.sqrt(4*area/np.pi)	
		
	

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
		if not hasattr(self, 'treenode_contour'): self.create_tracking_tree_nodes()
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



