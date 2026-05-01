from utils.video_utils import read_video, save_video
from trackers import PlayerTracker,BallTracker
from drawers import (PlayerTracksDrawer,
                     BallTracksDrawer,
                     CourtKeypointDrawer,
                     TacticalViewDrawer,
                     BallAquisitionDrawer)
from team_assigner import TeamAssigner
from court_keypoint_detector import CourtKeypointDetector
from tactical_view_converter import TacticalViewConverter
from ball_aquisition.ball_aquisition_detector import BallAquisitionDetector


def main():
    print("Start")
    video_frames = read_video("input_videos/video_1.mp4")

    
    player_tracker = PlayerTracker("models/player_detector.pt")
    ball_tracker = BallTracker("models/ball_detector.pt")
    court_keypoint_detector = CourtKeypointDetector("models/court_keypoint_detector.pt")


    player_tracks = player_tracker.get_object_tracks(video_frames,
                                                     read_from_stub = True,
                                                     stub_path = "stubs/player_track_stub.pkl"
                                                     )
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                     read_from_stub = True,
                                                     stub_path = "stubs/ball_track_stub.pkl"
                                                     )
    
    court_keypoints = court_keypoint_detector.get_court_keypoints(video_frames,
                                                                    read_from_stub = True,
                                                                    stub_path = "stubs/court_keypoints_stub.pkl"
                                                                    )
    
    print(court_keypoints)
    
    print("Processing ball tracking...")
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)


    team_assigner = TeamAssigner()
    
    ball_aquisition_detector = BallAquisitionDetector()
    ball_aquisition = ball_aquisition_detector.detect_ball_possession(player_tracks,ball_tracks)

    player_assignment = team_assigner.get_player_teams_across_frames(video_frames, player_tracks, read_from_stub=False, stub_path="stubs/player_assignment_stub.pkl")


    tactical_view_converter = TacticalViewConverter(court_image_path="./image/basketball-court.png")
    court_keypoints = tactical_view_converter.validate_keypoints(court_keypoints)
    tactical_player_positions = tactical_view_converter.transform_players_to_tactical_view(court_keypoints, player_tracks)

    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    tactical_view_drawer = TacticalViewDrawer()
    court_keypoint_drawer = CourtKeypointDrawer()
    ball_aquisition_drawer = BallAquisitionDrawer()
    
    output_video_frames =  player_tracks_drawer.draw(video_frames,player_tracks,player_assignment)
    output_video_frames =  ball_tracks_drawer.draw(output_video_frames,ball_tracks)
    output_video_frames =  court_keypoint_drawer.draw(output_video_frames,court_keypoints)
    output_video_frames = ball_aquisition_drawer.draw(output_video_frames,player_assignment,ball_aquisition)
    output_video_frames = tactical_view_drawer.draw(output_video_frames,
                                                    tactical_view_converter.court_image_path,
                                                    tactical_view_converter.width,
                                                    tactical_view_converter.height,
                                                    tactical_view_converter.key_points,
                                                    tactical_player_positions,
                                                    player_assignment
                                                    )

    
    

    print("Saving video...")
    save_video(output_video_frames,"output_videos/output_video.avi")    

    print("DONE")

if __name__ == "__main__":
        main()