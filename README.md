# ArUco-Based Assistive Navigation — 2022 MeiChu Hackathon

**3rd Place · PixArt Imaging Track · Two-day team prototype**

An experimental assistive-navigation concept for people with visual impairments. Our team explored how printed **ArUco visual markers**, a smartphone camera, and spoken prompts might help pedestrians identify locations, estimate distance to landmarks, receive directional guidance, and become aware of environmental hazards.

> **Project status:** Historical hackathon prototype, not a validated mobility aid. This repository preserves the original code; documented features do not imply a production-ready or safety-tested navigation system.

## Motivation and concept

Tactile paving and public-space signage can be difficult to use when damaged, obstructed, or wet. We proposed placing durable, camera-readable markers near landmarks and route features, allowing an inexpensive phone-based interface to provide contextual spoken guidance. The long-term placement and accessibility ideas were *proposals*, not an installed or evaluated public infrastructure system.

## Prototype architecture

```text
Android smartphone
  |-- Iriun Webcam (camera feed) --------> Computer / OpenCV
  |                                          |-- ArUco marker detection
  |                                          |-- pose and distance estimate
  |                                          |-- marker-ID lookup / direction rules
  |
  +-- AudioRelay (microphone input) ------> Python SpeechRecognition
                                             |
                                   gTTS / local audio playback
```

The team used **Iriun Webcam** to provide the phone camera feed and **AudioRelay** for phone-to-computer microphone audio, according to team recollection. The historical Python scripts use `cv.VideoCapture(0)`, `SpeechRecognition`, and `gTTS`. The repository does **not** establish whether synthesized output audio was routed back to the handset; playback is currently implemented as a local operating-system command.

## What the code contains

- **Marker detection and pose estimation:** `DISTANCE-ESTIMATION-master/distance.py` and `combine.py` use OpenCV's ArUco APIs, camera calibration data, and an 8 cm reference marker size to estimate marker-relative distance and position.
- **Basic directional cues:** `location_detect()` compares horizontal translation against thresholds to select left/right audio cues; it is not a complete route-planning algorithm.
- **Location and hazard messages:** marker IDs map to sample building and hazard descriptions in `DISTANCE-ESTIMATION-master/sound_output.json`, including construction, traffic, and standing-water warnings.
- **Speech input experiments:** `Speech.py`, `old.py`, and `test.py` demonstrate microphone capture, Google-backed speech recognition, and text-to-speech experiments.

Weather reports and autonomous emergency response were discussed as potential additions but are **not demonstrated by the current source**. There is also no native Android application source code in the repository.

## My contributions

My primary responsibility was the **voice-input and mobile-to-computer audio integration**:

- Prototyped speech recognition in Python using third-party libraries and services.
- Experimented with Android audio-routing apps, including AudioRelay, to make mobile microphone input available to the computer.
- Built and tested voice-input and spoken-response workflows.
- Participated in team brainstorming and filming the original demonstration.

Other teammates primarily developed ArUco detection, distance estimation, broader system integration, and the presentation. This repository represents a **team project**, not solely my individual implementation.

## Repository map

| Path | Role |
| --- | --- |
| `DISTANCE-ESTIMATION-master/combine.py` | Combined marker detection and speech-output prototype |
| `DISTANCE-ESTIMATION-master/distance.py` | Marker position/distance and printed guidance experiments |
| `DISTANCE-ESTIMATION-master/sound_output.json` | Sample marker-to-message mapping used by combined prototype |
| `calib_data/MultiMatrix.npz` | Historical camera calibration values |
| `Speech.py` | SpeechRecognition + gTTS experiment |
| `test.py`, `old.py`, `utils.py` | Early speech experiments and helper content |
| `DISTANCE-ESTIMATION-master/play.py` | Separate speech experiment |
| `example.mp3`, `DISTANCE-ESTIMATION-master/*.mp3` | Historical sample audio artifacts |
| `requirements.txt` | Inferred Python dependencies; not a verified environment lock |

Original filenames and paths are retained to preserve the history and avoid silently breaking relative paths.

## Reproducing and limitations

The original demonstration used an **Android phone**, a computer, and physical printed ArUco markers placed on a test route. The recorded demo is no longer available.

To explore the legacy code:

1. Clone the repository and create a Python virtual environment.
2. Review `requirements.txt` and install compatible legacy dependencies. Versions are **not historically verified**, and newer OpenCV releases may have a different ArUco API.
3. Install and configure Iriun Webcam and, if testing speech input, AudioRelay on the phone and computer.
4. Ensure the camera is correctly calibrated for the device in use; the committed `.npz` file is historical and is not appropriate for arbitrary cameras.
5. Review the code and marker IDs before running any live demonstration.

**Important:** This is **not a tested one-command installation guide**. Running it may require compatible historical OpenCV, Windows audio configuration, microphone permissions, network access for speech services, and modification of relative paths. The scripts have not been revalidated on current environments. Do not use this prototype for real-world mobility decisions.

### Known issues

- `combine.py` can retrigger speech continuously while a marker remains visible.
- Two different `sound_output.json` files contain different ID mappings; the combined script expects the one in its own directory.
- Some audio playback paths use Windows-specific `os.system("start ...")`; others are incomplete.
- `test.py` has a missing `datetime` import and a problematic conditional.
- The camera calibration and positional thresholds are illustrative; no accuracy or accessibility evaluation is provided.
- The complete Android-to-PC-to-Android audio return path has not been verified.

## Credits and provenance

Created by a student team for the **2022 MeiChu Hackathon — PixArt Imaging Track**, where the project received **third place**. The repository was uploaded in 2023. This documentation was added later to explain the original work and its limitations; it is not evidence that later fixes or features were present at the hackathon.

Dependencies, mobile applications, and any external snippets remain the property of their respective authors. No blanket license is asserted for the historical repository.
