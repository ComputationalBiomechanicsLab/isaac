# ChangeLog

All notable changes to this project will be documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 2023/11/13

- `README.md` was updated with a user-facing walkthrough, relevant sections, etc.
- This `CHANGELOG.md` was added to the repo to track changes over time
- SCONE was downloaded from SimTK and installed via `sudo apt install ./scone_2.2.1_amd64.deb` (#16)
- FEBio 4.3 was downloaded from the official site and ran (installed) as-is as sudo. Confirmed that GUI boots and renders basic scene (#17)
- Tensorflow was installed onto the base system with:
  - Installed Nvidia CUDA compiler with `apt-get install nvidia-cuda-toolkit` (Build cuda_11.5.r11.5/compiler.30672275_0)
  - Installed Nvidia cuDNN for Ubuntu22 (x86_64): https://developer.nvidia.com/rdp/cudnn-download
    - Then copied it over
    - Then installed it
    - But it doesn't actually install the necessary binaries, just unpacks *other* deb files into `/var`
    - So those three needed to be manually installed:
      - sudo apt-get install /var/cudnn-local-repo-ubuntu2204-8.9.6.50/libcudnn8_8.9.6.50-1+cuda11.8_amd64.deb
      - sudo apt-get install /var/cudnn-local-repo-ubuntu2204-8.9.6.50/libcudnn8-dev_8.9.6.50-1+cuda11.8_amd64.deb
      - sudo apt-get install /var/cudnn-local-repo-ubuntu2204-8.9.6.50/libcudnn8-samples_8.9.6.50-1+cuda11.8_amd64.deb
  - Installed Nvidia TensorRT accelerator:
    - https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-723/quick-start-guide/index.html#install
    - Download here: https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html#downloading
    - Got version 8: https://developer.nvidia.com/nvidia-tensorrt-8x-download
    - Specifically, 8.6 GA: nv-tensorrt-local-repo-ubuntu2204-8.6.1-cuda-11.8_1.0-1_amd64.deb
  - python code: https://www.tensorflow.org/install/pip
  - GPU setup: https://www.tensorflow.org/install/gpu
  - `python3 -m pip install tensorflow[and-cuda]`
