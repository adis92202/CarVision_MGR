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
    base_json_filename = os.path.splitext(
        os.path.basename(json_data["file"]["1"]["fname"])
    )[0]

    # Słownik do liczenia indexu dla każdej sekundy
    timestamp_counter = {}

    for key, entry in metadata.items():
        timestamp = entry["z"][0]  # sekunda

        # Liczymy index w tej sekundzie
        timestamp_key = f"{timestamp:.3f}"
        index = timestamp_counter.get(timestamp_key, 0)
        timestamp_counter[timestamp_key] = index + 1

        # Zamiana kropki na 'd'
        timestamp_str = str(timestamp).replace(".", "d")

        x, y, w, h = entry["xy"][1:]
        x1, y1 = int(round(x)), int(round(y))
        x2, y2 = int(round(x + w)), int(round(y + h))

        frame_number = int(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()
        if not ret:
            print(f"Cannot read frame at {timestamp}s (frame {frame_number})")
            continue

        crop = frame[y1:y2, x1:x2]
        output_filename = f"{base_json_filename}_{timestamp_str}_{index}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, crop)
        print(f"Saved: {output_path}")

    cap.release()
