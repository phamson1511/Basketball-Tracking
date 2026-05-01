def get_center_of_bbox(bbox):
    x1,y1,x2,y2 = bbox

    return int((x1+x2)/2), int((y1+y2)/2)

def get_bbox_width(bbox):
    x1,y1,x2,y2 = bbox
    return bbox[2] - bbox[0]

def get_foot_position(bbox):
    """Lấy vị trí chân cầu thủ (điểm giữa cạnh dưới bbox)"""
    x1, y1, x2, y2 = bbox
    return (int((x1 + x2) / 2), int(y2))

def measure_distance(p1, p2):
    """Tính khoảng cách Euclidean giữa 2 điểm"""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def measure_xy_distance(p1,p2):
    """
    Calculate the separate x and y distances between two points.

    Args:
        p1 (tuple): First point coordinates (x, y).
        p2 (tuple): Second point coordinates (x, y).

    Returns:
        tuple: The (x_distance, y_distance) between the points.
    """
    return p1[0]-p2[0],p1[1]-p2[1]