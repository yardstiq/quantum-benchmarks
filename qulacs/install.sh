#!/bin/sh
conda create -y --prefix=env python=3.8
conda activate ./env
conda install -p env -y numpy mkl-service pytest pybind11 pytest-benchmark cffi
./env/bin/pip install qulacs-gpu
