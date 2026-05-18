from utils.video_utils import read_video, save_video
import os
import argparse
from trackers import PlayerTracker,BallTracker
from drawers import (PlayerTracksDrawer,
                     BallTracksDrawer,
                     BallAquisitionDrawer,
                     PassInterceptionDrawer)
from team_assigner import TeamAssigner
from ball_aquisition.ball_aquisition_detector import BallAquisitionDetector
from pass_and_interception_detector import PassAndInterceptionDetector
import os
def parse_args():
    parser = argparse.ArgumentParser(description='Basketball Video Analysis')
    parser.add_argument('input_video', type=str, help='Path to input video file')
    return parser.parse_args()
      


def main():
    args = parse_args()
    print("Start")
    input_path = args.input_video
    video_frames = read_video(input_path)
    input_name = os.path.splitext(os.path.basename(input_path))[0]

    
    player_tracker = PlayerTracker("models/player_detector.pt")
    ball_tracker = BallTracker("models/ball_detector.pt")


    player_tracks = player_tracker.get_object_tracks(video_frames,
                                                     read_from_stub = True,
                                                     stub_path = "stubs/player_track_stub.pkl"
                                                     )
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                     read_from_stub = True,
                                                     stub_path = "stubs/ball_track_stub.pkl"
                                                     )
    
   
    
    print("Processing ball tracking...")
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)


    team_assigner = TeamAssigner()
    
    #Quyen kiem soat bong
    ball_aquisition_detector = BallAquisitionDetector()
    ball_aquisition = ball_aquisition_detector.detect_ball_possession(player_tracks,ball_tracks)

    #Chia cau thu 2 doi
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames, player_tracks, read_from_stub=False, stub_path="stubs/player_assignment_stub.pkl")

    #Duong chuyen va cat bong
    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(ball_aquisition,player_assignment)
    interception = pass_and_interception_detector.detect_interceptions(ball_aquisition,player_assignment)


    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    ball_aquisition_drawer = BallAquisitionDrawer()
    pass_and_interception_drawer = PassInterceptionDrawer()
    
    output_video_frames =  player_tracks_drawer.draw(video_frames,player_tracks,player_assignment)
    output_video_frames =  ball_tracks_drawer.draw(output_video_frames,ball_tracks)
    output_video_frames = ball_aquisition_drawer.draw(output_video_frames,player_assignment,ball_aquisition)
    output_video_frames = pass_and_interception_drawer.draw(output_video_frames,passes,interception)
 
    print("Saving video...")
    output_path = f"output_videos/output_{input_name}.avi"  
    save_video(output_video_frames, output_path) 

    print("DONE")

if __name__ == "__main__":
        main()