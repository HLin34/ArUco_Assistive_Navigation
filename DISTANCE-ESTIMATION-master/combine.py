"""Maintained version of the 2022 ArUco + spoken guidance prototype.

Requires a compatible legacy OpenCV ArUco API, a calibrated camera,
and network access for gTTS. Not a safety-tested navigation aid.
"""
from pathlib import Path
import json
import time

import cv2 as cv
from cv2 import aruco
from gtts import gTTS
import numpy as np
from playsound import playsound

from navigation_logic import direction_for_offset, marker_message, should_announce

HERE = Path(__file__).resolve().parent
with (HERE / "sound_output.json").open(encoding="utf-8") as f:
    data = json.load(f)

calib_data = np.load(HERE.parent / "calib_data" / "MultiMatrix.npz")
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

MARKER_SIZE = 8  # centimeters, as in the original prototype
marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create()

last_event = None
last_time = float("-inf")


def play_direction(direction):
    file = HERE / ("turn-left.mp3" if direction == "left" else "turn-right.mp3")
    playsound(str(file))


def speak(text, language):
    if not text:
        return
    output = HERE / "example.mp3"
    gTTS(text=text, lang=language, slow=False).save(str(output))
    playsound(str(output))


def announce(event, direction=None, message="", language="zh-TW"):
    """Play an event only after a state change or the cooldown period."""
    global last_event, last_time
    now = time.monotonic()
    if not should_announce(event, last_event, last_time, now):
        return
    last_event, last_time = event, now
    try:
        if direction is not None:
            play_direction(direction)
        else:
            speak(message, language)
    except Exception as exc:
        # Audio/network failures should not kill the camera loop.
        print(f"Audio playback failed: {exc}")


def main():
    cap = cv.VideoCapture(0)  # Select the Iriun virtual camera if needed.
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera index 0")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            corners_list, marker_ids, _ = aruco.detectMarkers(
                gray, marker_dict, parameters=param_markers
            )
            if marker_ids is not None and len(marker_ids):
                rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
                    corners_list, MARKER_SIZE, cam_mat, dist_coef
                )
                for marker, corners, rvec, tvec in zip(
                    marker_ids.flatten(), corners_list, rvecs, tvecs
                ):
                    marker_id = int(marker)
                    cv.polylines(
                        frame, [corners.astype(np.int32)], True,
                        (0, 255, 255), 4, cv.LINE_AA
                    )
                    points = corners.reshape(4, 2).astype(int)
                    distance = float(np.linalg.norm(tvec[0]))
                    cv.drawFrameAxes(frame, cam_mat, dist_coef, rvec, tvec, 4)
                    cv.putText(
                        frame, f"id: {marker_id} Dist: {distance:.2f}",
                        tuple(points[0]), cv.FONT_HERSHEY_PLAIN,
                        1.3, (0, 0, 255), 2, cv.LINE_AA
                    )
                    cv.putText(
                        frame, f"x:{tvec[0][0]:.1f} y:{tvec[0][1]:.1f}",
                        tuple(points[2]), cv.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 255), 2, cv.LINE_AA
                    )

                    if 10 <= marker_id <= 40:
                        direction = direction_for_offset(float(tvec[0][0]))
                        if direction:
                            announce(("direction", direction), direction=direction)
                        else:
                            print("in the location")
                    else:
                        message, language = marker_message(marker_id, data)
                        if message:
                            announce(("marker", marker_id), message=message, language=language)

                    # Historical diagnostic only, not an emergency-call feature.
                    if distance < 35:
                        print("help")

            cv.imshow("frame", frame)
            if cv.waitKey(1) == ord("q"):
                break
    finally:
        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
