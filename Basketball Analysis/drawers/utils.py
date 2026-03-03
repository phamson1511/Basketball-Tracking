import cv2
import sys
sys.path.append("../")
from utils.bbox_utils import get_center_of_bbox,get_bbox_width

def draw_ellipse(frame,bbox, color, track_id = None):
    y2 =  int(bbox[3])
    x_center,_ = get_center_of_bbox(bbox)
    width = get_bbox_width(bbox)
    cv2.ellipse(frame,center = (x_center,y2), axes = (int(width), int(0.35*width)),
                                                            angle = 0,
                                                            startAngle = -45,
                                                            endAngle = 235,
                                                            color = color,
                                                            thickness = 2,
                                                            lineType = cv2.LINE_AA)
    
    rectangle_width = 40
    rectangle_height = 20
    x1_rec = x_center - rectangle_width//2
    x2_rec = x_center - rectangle_width//2
    y1_rec = (y2-rectangle_height//2)+15
    y2_rec = (y2+rectangle_height//2)+15

    if track_id is not None:
        # Vẽ hình chữ nhật (background cho ID)
        cv2.rectangle(
            frame,
            (int(x1_rec), int(y1_rec)),
            (int(x2_rec), int(y2_rec)),
            color,
            cv2.FILLED
        )

        # Tính vị trí chữ
        x1_text = x1_rec + 12

        # Nếu ID >= 100 thì lùi chữ lại 1 chút
        if track_id > 99:
            x1_text -= 10

        # Vẽ text ID
        cv2.putText(
            frame,
            str(track_id),
            (int(x1_text), int(y1_rec - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            2
        )
    
    return frame
