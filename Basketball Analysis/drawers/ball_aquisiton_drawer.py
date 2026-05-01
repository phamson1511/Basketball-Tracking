import cv2 
import numpy as np

class BallAquisitionDrawer:
    def __init__(self):
        pass

    def get_team_ball_control(self,player_assignment,ball_aquisition):
        """
        Tính toán đội nào kiểm soát bóng ở mỗi frame.

        Tham số:
            player_assignment (list): Danh sách các dictionary cho biết mỗi player thuộc đội nào tương ứng với từng frame.
            ball_aquisition (list): Danh sách cho biết player nào đang giữ bóng ở mỗi frame.

        Trả về:
            numpy.ndarray: Một mảng cho biết đội nào đang kiểm soát bóng ở mỗi frame
        (1 cho Team 1, 2 cho Team 2, -1 nếu không có đội nào kiểm soát).
        """

        team_ball_control = []
        for player_assignment_frame,ball_aquisition_frame in zip(player_assignment,ball_aquisition):
            if ball_aquisition_frame == -1:
                team_ball_control.append(-1)
                continue
            if ball_aquisition_frame not in player_assignment_frame:
                team_ball_control.append(-1)
                continue
            if player_assignment_frame[ball_aquisition_frame] == 1:
                team_ball_control.append(1)
            else:
                team_ball_control.append(2)

        team_ball_control= np.array(team_ball_control) 
        return team_ball_control

    def draw(self,video_frames,player_assignment,ball_aquisition):
        """
        Vẽ thống kê kiểm soát bóng của các đội lên danh sách các frame video.

        Tham số:
            video_frames (list): Danh sách các frame (dưới dạng mảng NumPy hoặc đối tượng ảnh) để vẽ lên.
            player_assignment (list): Danh sách các dictionary cho biết mỗi player thuộc đội nào
                tương ứng với từng frame.
            ball_aquisition (list): Danh sách cho biết player nào đang giữ bóng ở mỗi frame.

        Trả về:
            list: Danh sách các frame đã được vẽ thêm thống kê kiểm soát bóng của các đội.
        """
        
        team_ball_control = self.get_team_ball_control(player_assignment,ball_aquisition)

        output_video_frames= []
        for frame_num, frame in enumerate(video_frames):
            if frame_num == 0:
                continue

            frame_drawn = self.draw_frame(frame,frame_num,team_ball_control)
            output_video_frames.append(frame_drawn)
        return output_video_frames
    
    def draw_frame(self,frame,frame_num,team_ball_control):
        """
        Vẽ một lớp phủ (overlay) bán trong suốt hiển thị % kiểm soát bóng của các đội lên một frame.

        Tham số:
            frame (numpy.ndarray): Frame video hiện tại để chi so.
            frame_num (int): Chỉ số của frame hiện tại.
            team_ball_control (numpy.ndarray): Mảng đội kiểm soát bóng ở mỗi frame.

        Trả về:
            numpy.ndarray: Frame đã được thêm thống kê.
        """
        
        # Draw a semi-transparent rectaggle 
        overlay = frame.copy()
        font_scale = 0.7
        font_thickness=2
        
        # Overlay Position
        frame_height, frame_width = overlay.shape[:2]
        rect_x1 = int(frame_width * 0.60) 
        rect_y1 = int(frame_height * 0.75)
        rect_x2 = int(frame_width * 0.99)  
        rect_y2 = int(frame_height * 0.90)
        # Text positions
        text_x = int(frame_width * 0.63)  
        text_y1 = int(frame_height * 0.80)  
        text_y2 = int(frame_height * 0.88)


        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), (255,255,255), -1 )
        alpha = 0.8
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        team_ball_control_till_frame = team_ball_control[:frame_num+1]
        # Get the number of time each team had ball control
        team_1_num_frames = team_ball_control_till_frame[team_ball_control_till_frame==1].shape[0]
        team_2_num_frames = team_ball_control_till_frame[team_ball_control_till_frame==2].shape[0]
        team_1 = team_1_num_frames/(team_ball_control_till_frame.shape[0])
        team_2 = team_2_num_frames/(team_ball_control_till_frame.shape[0])

        cv2.putText(frame, f"Ti le kiem soat doi 1: {team_1*100:.2f}%",(text_x, text_y1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), font_thickness)
        cv2.putText(frame, f"Ti le kiem soat doi 2: {team_2*100:.2f}%",(text_x, text_y2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), font_thickness)

        return frame