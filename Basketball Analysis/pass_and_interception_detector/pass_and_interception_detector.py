from copy import deepcopy

class PassAndInterceptionDetector():
    
    def __init__(self):
        pass 

    def detect_passes(self,ball_acquisition,player_assignment):
        
        passes = [-1] * len(ball_acquisition)
        prev_holder=-1
        previous_frame=-1

        for frame in range(1, len(ball_acquisition)):
            if ball_acquisition[frame - 1] != -1:
                prev_holder = ball_acquisition[frame - 1]
                previous_frame= frame - 1
            
            current_holder = ball_acquisition[frame]
            
            if prev_holder != -1 and current_holder != -1 and prev_holder != current_holder:
                prev_team = player_assignment[previous_frame].get(prev_holder, -1)
                current_team = player_assignment[frame].get(current_holder, -1)
                print(f"[Frame {frame}] {prev_holder}(team {prev_team}) → {current_holder}(team {current_team})")
                if prev_team == current_team and prev_team != -1:
                    passes[frame] = prev_team
                
            
        return passes

    def detect_interceptions(self, ball_acquisition, player_assignment):
        interceptions = [-1] * len(ball_acquisition)
        prev_controlling_team = -1  # đội đang kiểm soát bóng trước đó

        for frame in range(len(ball_acquisition)):
            current_holder = ball_acquisition[frame]
            if current_holder == -1:
                continue  # không ai cầm bóng → bỏ qua, KHÔNG reset controlling team

            current_team = player_assignment[frame].get(current_holder, -1)
            if current_team == -1:
                continue

            # Chỉ tính khi đội kiểm soát bóng thực sự đổi
            if prev_controlling_team != -1 and current_team != prev_controlling_team:
                interceptions[frame] = current_team

            # Cập nhật đội đang kiểm soát
            prev_controlling_team = current_team

        return interceptions