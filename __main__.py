from src.read_data import play_video
from src.get_training_data import load_annotations, extract_and_save_frames


def main():
    video_path = "data/recordings/20240308 143701F C D.mp4"
    json_path = "data/metadata/20240308_143701F_c_d.json"
    output_dir = "data/training_set"
    data = load_annotations(json_path)
    extract_and_save_frames(data, video_path, output_dir)
    # play_video(video_path)


if __name__ == "__main__":
    main()
