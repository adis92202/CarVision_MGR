import os
import glob
from src.get_training_data import load_annotations, extract_and_save_frames

# Lista kategorii
categories = [
    "city_daylight",
    "city_daylight_rain",
    "city_night",
    "city_night_rain",
    "highway_daylight",
    "highway_daylight_rain",
    "highway_night",
    "highway_night_rain",
    "mountain_roads_daylight",
    "mountain_roads_daylight_rain",
    "mountain_roads_night",
    "mountain_roads_night_rain",
    "roadworks_daylight",
    "roadworks_daylight_rain",
    "roadworks_night",
    "roadworks_night_rain",
]

# Bazowe ścieżki
base_input_path = r"D:\MGR\Master\recordings"
base_output_path = r"data/training_set"


def convert_json_name_to_mp4(json_name):
    """
    Konwersja nazwy pliku JSON na odpowiadający mu plik mp4:
    np. 20240308_143701F_c_d.json -> 20240308 143701F C D.mp4
    """
    base_name = os.path.splitext(json_name)[0]
    mp4_name = base_name.replace("_", " ").upper() + ".mp4"
    return mp4_name


def process_all_videos():
    for category in categories:
        mp4_dir = os.path.join(base_input_path, category, "mp4")
        metadata_dir = os.path.join(base_input_path, category, "metadata")
        output_dir = os.path.join(base_output_path, category)

        os.makedirs(output_dir, exist_ok=True)

        json_files = glob.glob(os.path.join(metadata_dir, "*.json"))
        for json_path in json_files:
            json_name = os.path.basename(json_path)
            corresponding_mp4_name = convert_json_name_to_mp4(json_name)
            video_path = os.path.join(mp4_dir, corresponding_mp4_name)

            if not os.path.exists(video_path):
                print(
                    f"[WARN] Video not found for {json_name} -> {corresponding_mp4_name}"
                )
                continue

            try:
                data = load_annotations(json_path)
                extract_and_save_frames(data, video_path, output_dir)
                print(f"[OK] Processed: {corresponding_mp4_name}")
            except Exception as e:
                print(f"[ERROR] {corresponding_mp4_name}: {e}")


if __name__ == "__main__":
    process_all_videos()
