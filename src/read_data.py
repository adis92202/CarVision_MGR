import cv2


def load_video(file_path: str) -> cv2.VideoCapture:
    """Loads the video and return VideoCapture object

    Raises:
        ValueError: Raised when cannot open the file

    Returns:
        cv2.VideoCapture: VideoCapture object
    """
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open the file: {file_path}")
    return cap


def play_video(file_path: str, scale: float = 0.5):
    """Plays the video frame by frame

    Args:
        file_path (str): Path to the video
        scale (float, optional): Parameter that is changing the scale of the player. Defaults to 0.5.
    """
    cap = load_video(file_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # EOF

        # Changing the scale
        frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        cv2.imshow(file_path, frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
