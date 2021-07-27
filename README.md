# Automatic-Brain-Tumor-Segmentation
Brain Tumor Segmentation of MRI T1-weighted images is done using [U-Net Architecture](https://arxiv.org/abs/1505.04597)

## Dataset Used
Dataset used in this project was provided by Jun Cheng.
[This](https://figshare.com/articles/dataset/brain_tumor_dataset/1512427) dataset contains 3064 T1-weighted contrast-enhanced images with three kinds of brain tumor. Version 5 of this dataset is used in this project. Each image is of dimension 512 x 512 x 1 , these are black and white images thus having a single channel.

## Installation
This project uses python3.
Clone the project.
`git clone https://github.com/Jeetu95/Brain-Tumor-Segmentation.git`
Install Pytorch from this [link](https://pytorch.org/get-started/locally/)
Use pip to install all the dependencies
`pip install -r requirements.txt`
To open the notebook
`jupyter lab`
