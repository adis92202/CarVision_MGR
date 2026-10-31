# CarVision: Road Bump Detection for Vehicle Suspension Assistance

> **Master's thesis, AGH University of Krakow (M.Sc. Geoinformatics, Data Analysis specialization)**
> *Analysis of the possibility of using Machine Vision in vehicle suspension assistance systems for road bumps based on images from a digital camera.*

![Python](https://img.shields.io/badge/Python-3.11.9-blue)
![YOLO](https://img.shields.io/badge/Models-YOLOv5s%20%7C%20YOLOv8n-orange)
![Domain](https://img.shields.io/badge/Domain-ADAS%20%7C%20Computer%20Vision-green)

![Dashcam image with annotations](assets/via.png)

## Why this project

Modern vehicles increasingly use **camera-based perception to prepare the chassis for what is ahead**. If a forward-facing camera can recognise a speed bump or road defect early enough, the suspension can be adjusted *before* the wheels reach it. This is the same perception-to-action principle behind many ADAS functions.

This project investigates whether a **single monocular dashcam**, with no LiDAR and no radar, provides enough information to detect road bumps reliably with modern object detectors.

## What I built

- **Custom dataset** built from **50+ hours of real dashcam recordings** captured on real roads
- **Manual annotation** of thousands of road defects with bounding boxes
- **Training and comparison of YOLOv5 and YOLOv8** detectors on the custom data
- **Evaluation of detection quality** and analysis of model behaviour
- Reproducible environment (`conda-lock`) and a modular codebase (`src/`, `notebooks/`)

## Pipeline

```
Dashcam video  ->  Frame extraction  ->  Annotation (bounding boxes)
                                                  |
                                                  v
          Evaluation  <-  Training (YOLOv5 / YOLOv8)  <-  Dataset (YOLO format)
```

## Results

Single class (`pothole`), 640x640 input, batch size 32, default Ultralytics training regime. Split stratified per domain: **10,483 training / 2,866 validation images**.

| Model   | Precision | Recall | AP@0.5 | mAP@0.5:0.95 | Best F1 (conf. threshold) | Weights |
|---------|-----------|--------|--------|--------------|---------------------------|---------|
| YOLOv5s | 0.597     | 0.522  | 0.524  | 0.224        | 0.56 (0.276)              | 14.35 MB |
| YOLOv8n | 0.612     | 0.482  | 0.511  | 0.232        | 0.54 (0.204)              | 6.22 MB  |

Trained on a laptop GPU (RTX 3050, 4 GB), so this is a deliberately lightweight, prototype-level setup. Inference latency / FPS on target hardware was **not** measured.

**Key findings:** 

- **The two models are close, with different trade-offs.** AP@0.5 is about 0.52 vs 0.51. YOLOv8n has higher precision and slightly better mAP@0.5:0.95 (better localisation across IoU thresholds) and is **2.3x smaller**. YOLOv5s has higher recall, so it misses fewer small potholes. For a suspension system where a false alarm is costly, YOLOv8n with a higher confidence threshold is the safer choice. If detection coverage matters more and a post-filter is available, YOLOv5s is better.
- **Failure cases are domain-driven, not random.** Most errors are false negatives on small, low-contrast defects. At night and in rain, light reflections on wet asphalt produce false positives. Saliency maps confirm this: in night-rain frames, activation concentrates on reflections instead of road defects. Those domains are also the least represented in the data, so some of this is epistemic uncertainty (missing training data) rather than a model limit.
- **A cheap ROI mask helps without touching the model.** Restricting saliency to a trapezoid over the ego lane suppresses activations from kerbs, signs, buildings and oncoming lanes. The effect is moderate in daylight and clear at night in rain.
- **Data analysis mattered.** Pothole density and shape depend strongly on road type (Kruskal-Wallis, p < 1e-5): mountain roads have the most events per hour, motorways the fewest but the widest, flattest defects. Weather affects mostly signal quality and sample counts rather than defect size. Per-domain reporting and class-balanced sampling are therefore needed.
- **What it would take to go to production** (also my own listed limitations): temporal tracking and vehicle-speed fusion to estimate time-to-impact, a real measurement of end-to-end latency on automotive hardware, more night/rain data, segmentation instead of bounding boxes, a dynamic ROI that follows lane geometry, and calibrated per-domain confidence thresholds.

## Repository structure

```
.
├── src/             # Core code: data processing, training, evaluation
├── notebooks/       # Exploration, analysis and visualisation
├── yolov5/          # YOLOv5 framework
├── dataset.yaml     # Dataset configuration (YOLO format)
├── environment.yml  # Conda environment
├── conda-lock.yml   # Locked dependencies for reproducibility
└── __main__.py      # Entry point
```

## Getting started

```bash
# 1. Clone
git clone https://github.com/adis92202/CarVision_MGR.git
cd CarVision_MGR

# 2. Create the environment
conda env create -f environment.yml
conda activate <car_vision>

# 3. Run - remember to (un)comment appropriate sections
python __main__.py
```

## Dataset

The dataset is a **private, self-collected dashcam collection**. It is not published in this repository because the footage shows public roads, other vehicles and licence plates, and no anonymisation pipeline was implemented for the prototype. **It can be shared on request** for research or evaluation purposes; please contact me (see [Author](#author)).

| | |
|---|---|
| **Source** | Single Xblitz Tango 4K dashcam behind the rear-view mirror, one vehicle (Suzuki Vitara MY2022), fixed mounting position and viewing angle |
| **Collection period** | 8 March - 29 May 2024, recorded during my own trips |
| **Region** | Poland, mostly the Lesser Poland and Silesian voivodeships |
| **Volume** | 3,277 clips (each under 1 min), about 55 hours |
| **Format** | Original 2K `.ts`, transcoded to Full HD `.mp4` with HandBrake |
| **Annotation** | Manual rectangular bounding boxes in VIA Video Annotator, single class `pothole`, exported as normalised coordinates with timestamps (JSON) |
| **Training data** | Frames with annotated defects cropped out and converted to YOLO format, 10,483 train / 2,866 validation images, split stratified per domain (about 80/20) |

**16 domains** are defined by road type x time of day x weather: city, motorway, mountain roads and roadworks, each in day, day + rain, night and night + rain, plus a separate "complex" category (tunnels, underground car parks, parking). The data is strongly imbalanced: city and motorway in good weather dominate, while night and rain are rare and mountain roads at night in rain are not represented at all. That imbalance is the main source of the weaker results in those conditions (see Key findings).

**Known limitations of the data:** one camera and one car only, no calibration, unannotated defects may remain in some frames (label noise), and transcoding from 2K to Full HD may introduce compression artefacts.

## Skills demonstrated

| Area | What this project shows |
|------|-------------------------|
| **Computer Vision** | Object detection with YOLOv5 / YOLOv8, bounding box annotation, detector comparison |
| **Data work** | Building a dataset from raw video, labeling, quality control |
| **ML workflow** | Training, evaluation, error analysis, reproducible environments |
| **Automotive context** | Camera-based perception for vehicle systems (ADAS-adjacent use case) |

## Related work

This thesis is part of a broader interest in automotive AI. See also my earlier work on **ADAS performance analysis**: real-world data from Blind Spot Monitoring (BSM) and Lane Departure Warning (LDW) systems, analysed statistically under different driving conditions. <!-- TODO: link to the AGH graduate work's repo -->

## Possible next steps

- Temporal modelling (video-based detection / tracking instead of single frames)
- Depth or distance estimation to give the suspension controller a time-to-impact
- Optimisation for embedded inference (quantisation, TensorRT / ONNX)
- Fusion with IMU or vehicle signals to validate detections against real suspension response

## Author

**Adam Piwowarski**, Data Scientist
[LinkedIn](https://www.linkedin.com/in/adam-piwowarski-ba56bb238/) | [GitHub](https://github.com/adis92202)
