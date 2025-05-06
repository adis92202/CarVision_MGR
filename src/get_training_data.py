import cv2
import json
import os


def load_annotations(json_path: str) -> dict:
    """Loads VIA annotations from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_and_save_frames(json_data: dict, video_path: str, output_dir: str):
    """Extracts frames at given timestamps and crops rectangles defined in JSON metadata."""
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    metadata = json_data["metadata"]
    # fname = json_data["file"]["1"]["fname"]
    ix = 1

    for key, entry in metadata.items():
        timestamp = entry["z"][0]  # sekunda
        x, y, w, h = entry["xy"][1:]
        x1, y1 = int(x), int(y)
        x2, y2 = int(x + w), int(y + h)

        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()
        if not ret:
            print(f"Cannot read frame at {timestamp}s (frame {frame_number})")
            continue

        crop = frame[y1:y2, x1:x2]
        output_path = os.path.join(output_dir, f"{ix}_{key}.jpg")
        cv2.imwrite(output_path, crop)
        print(f"Saved: {output_path}")
        ix += 1

    cap.release()
