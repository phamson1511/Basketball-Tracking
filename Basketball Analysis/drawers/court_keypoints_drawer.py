import supervision as sv
import numpy as np

class CourtKeypointDrawer:
    def __init__(self, conf_threshold=0.5):
        self.keypoint_color = "#ff2c2c"
        self.conf_threshold = conf_threshold

    def draw(self, frames, court_keypoints):
        vertex_annotator = sv.VertexAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            radius=9
        )
        vertex_label_annotator = sv.VertexLabelAnnotator(
            color=sv.Color.from_hex(self.keypoint_color),
            text_color=sv.Color.WHITE,
            text_scale=0.5,
            text_thickness=1
        )

        output_frames = []
        for index, frame in enumerate(frames):
            annotated_frame = frame.copy()
            keypoints = court_keypoints[index]

            # Lấy data: shape (N, K, 3) — [x, y, conf]
            kp_data = keypoints.data.cpu().numpy()  # (N, K, 3)

            if kp_data.shape[0] == 0:
                output_frames.append(annotated_frame)
                continue

            xy = kp_data[..., :2]          # (N, K, 2)
            conf = kp_data[..., 2]          # (N, K)

            # Mask keypoint có confidence thấp — đặt về (0,0) để supervision bỏ qua
            low_conf_mask = conf < self.conf_threshold
            xy[low_conf_mask] = 0

            # Tạo supervision KeyPoints object để 2 annotator dùng cùng 1 source
            sv_keypoints = sv.KeyPoints(xy=xy, confidence=conf)

            # Labels: chỉ hiện index của keypoint có conf cao
            labels = []
            for k in range(conf.shape[1]):
                avg_conf = conf[:, k].mean()
                labels.append(str(k) if avg_conf >= self.conf_threshold else "")

            annotated_frame = vertex_annotator.annotate(
                scene=annotated_frame, key_points=sv_keypoints
            )
            annotated_frame = vertex_label_annotator.annotate(
                scene=annotated_frame, key_points=sv_keypoints, labels=labels
            )

            output_frames.append(annotated_frame)

        return output_frames