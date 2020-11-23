![CI CPU testing](https://github.com/ultralytics/yolov5/workflows/CI%20CPU%20testing/badge.svg)

This repository is forked from Ultralytics open-source research into future object detection methods,

<img src="https://user-images.githubusercontent.com/26833433/90187293-6773ba00-dd6e-11ea-8f90-cd94afc0427f.png" width="1000">\*\* GPU Speed measures end-to-end time per image averaged over 5000 COCO val2017 images using a V100 GPU with batch size 32, and includes image preprocessing, PyTorch FP16 inference, postprocessing and NMS. EfficientDet data from [google/automl](https://github.com/google/automl) at batch size 8.

## Pretrained Checkpoints on Different Models

| Model                                                           | AP<sup>val</sup> | AP<sup>test</sup> | AP<sub>50</sub> | Speed<sub>GPU</sub> | FPS<sub>GPU</sub> |     | params | FLOPS  |
| --------------------------------------------------------------- | ---------------- | ----------------- | --------------- | ------------------- | ----------------- | --- | ------ | :----: |
| [YOLOv5s](https://github.com/ultralytics/yolov5/releases)       | 37.0             | 37.0              | 56.2            | **2.4ms**           | **416**           |     | 7.5M   | 13.2B  |
| [YOLOv5m](https://github.com/ultralytics/yolov5/releases)       | 44.3             | 44.3              | 63.2            | 3.4ms               | 294               |     | 21.8M  | 39.4B  |
| [YOLOv5l](https://github.com/ultralytics/yolov5/releases)       | 47.7             | 47.7              | 66.5            | 4.4ms               | 227               |     | 47.8M  | 88.1B  |
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases)       | **49.2**         | **49.2**          | **67.7**        | 6.9ms               | 145               |     | 89.0M  | 166.4B |
|                                                                 |                  |                   |                 |                     |                   |     |        |
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases) + TTA | **50.8**         | **50.8**          | **68.9**        | 25.5ms              | 39                |     | 89.0M  | 354.3B |
|                                                                 |                  |                   |                 |                     |                   |     |        |
| [YOLOv3-SPP](https://github.com/ultralytics/yolov5/releases)    | 45.6             | 45.5              | 65.2            | 4.5ms               | 222               |     | 63.0M  | 118.0B |

** AP<sup>test</sup> denotes COCO [test-dev2017](http://cocodataset.org/#upload) server results, all other AP results in the table denote val2017 accuracy.  
** All AP numbers are for single-model single-scale without ensemble or test-time augmentation. **Reproduce** by `python test.py --data coco.yaml --img 640 --conf 0.001`  
** Speed<sub>GPU</sub> measures end-to-end time per image averaged over 5000 COCO val2017 images using a GCP [n1-standard-16](https://cloud.google.com/compute/docs/machine-types#n1_standard_machine_types) instance with one V100 GPU, and includes image preprocessing, PyTorch FP16 image inference at --batch-size 32 --img-size 640, postprocessing and NMS. Average NMS time included in this chart is 1-2ms/img. **Reproduce** by `python test.py --data coco.yaml --img 640 --conf 0.1`  
** All checkpoints are trained to 300 epochs with default settings and hyperparameters (no autoaugmentation).
** Test Time Augmentation ([TTA](https://github.com/ultralytics/yolov5/issues/303)) runs at 3 image sizes. **Reproduce\*\* by `python test.py --data coco.yaml --img 832 --augment`

## Requirements

Python 3.8 or later with all [requirements.txt](https://github.com/ultralytics/yolov5/blob/master/requirements.txt) dependencies installed, including `torch>=1.6`. To install run:

```bash
$ pip install -r requirements.txt
```

## Inference

detect.py runs inference on a variety of sources, downloading models automatically from the [latest YOLOv5 release](https://github.com/ultralytics/yolov5/releases) and saving results to `inference/output`.

```bash
$ python detect.py --source 0  # webcam
                            file.jpg  # image
                            file.mp4  # video
                            path/  # directory
                            path/*.jpg  # glob
                            rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa  # rtsp stream
                            rtmp://192.168.1.105/live/test  # rtmp stream
                            http://112.50.243.8/PLTV/88888888/224/3221225900/1.m3u8  # http stream
```

To run inference on example images in `inference/images`:

```bash
$ python detect.py --source inference/images --weights yolov5s.pt --conf 0.25

Namespace(agnostic_nms=False, augment=False, classes=None, conf_thres=0.25, device='', img_size=640, iou_thres=0.45, output='inference/output', save_conf=False, save_txt=False, source='inference/images', update=False, view_img=False, weights='yolov5s.pt')
Using CUDA device0 _CudaDeviceProperties(name='Tesla V100-SXM2-16GB', total_memory=16160MB)

Downloading https://github.com/ultralytics/yolov5/releases/download/v3.0/yolov5s.pt to yolov5s.pt... 100%|██████████████| 14.5M/14.5M [00:00<00:00, 21.3MB/s]

Fusing layers...
Model Summary: 140 layers, 7.45958e+06 parameters, 0 gradients
image 1/2 yolov5/inference/images/bus.jpg: 640x480 4 persons, 1 buss, 1 skateboards, Done. (0.013s)
image 2/2 yolov5/inference/images/zidane.jpg: 384x640 2 persons, 2 ties, Done. (0.013s)
Results saved to yolov5/inference/output
Done. (0.124s)
```

<img src="https://user-images.githubusercontent.com/26833433/97107365-685a8d80-16c7-11eb-8c2e-83aac701d8b9.jpeg" width="500">

## Training

Download [COCO](https://github.com/ultralytics/yolov5/blob/master/data/scripts/get_coco.sh) and run command below. Training times for YOLOv5s/m/l/x are 2/4/6/8 days on a single V100 (multi-GPU times faster). Use the largest `--batch-size` your GPU allows (batch sizes shown for 16 GB devices).

```bash
$ python train.py --data coco.yaml --cfg yolov5s.yaml --weights '' --batch-size 64
                                         yolov5m                                40
                                         yolov5l                                24
                                         yolov5x                                16
```

<img src="https://user-images.githubusercontent.com/26833433/90222759-949d8800-ddc1-11ea-9fa1-1c97eed2b963.png" width="900">

## Ultralytics Citation

[![DOI](https://zenodo.org/badge/264818686.svg)](https://zenodo.org/badge/latestdoi/264818686)

## About Ultralytics

Ultralytics is a U.S.-based particle physics and AI startup with over 6 years of expertise supporting government, academic and business clients. We offer a wide range of vision AI services, spanning from simple expert advice up to delivery of fully customized, end-to-end production solutions.

For business inquiries and professional support requests please visit them at https://www.ultralytics.com.

## About me

I am currently a Masters student at The University of Melbourne and this repo is for detecting deepfakes using Yolo

## Scripts in SPARTAN

1. JOB - 21469258 --> rundf is running on spartan-gpgpu060
2. JOB - 21469196 --> runff is running on spartan-gpgpu028
3. JOB - 21496778 --> runfs is running on spartan-gpgpu063
4. JOB - 21469198 --> runnt is running on spartan-gpgpu037
5. JOB - 21540669 --> run_final is running on spartan-gpgpu065 (batch_size - 64)
6. JOB - 21480289 --> run_final is running on spartan-gpgpu065 (batch_size - 32)
7. JOB - 21497230 --> run_final (batch_size - 64 & no weights)
