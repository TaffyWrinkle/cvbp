# -*- coding: utf-8 -*-

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@microsoft.com
#
# A script to classify an image into one of 1000 know objects.
#
# ml tag cvbp <path>
#
# From the Microsoft Best Practices Suite: Computer Vision
# https://github.com/microsoft/ComputerVision

import sys
import os
import urllib.request
import argparse

from mlhub.pkg import is_url
from mlhub.utils import get_cmd_cwd

import fastai
from fastai.vision import models, open_image, load_learner, untar_data

# Until this is pip installable we use a local copy!

from utils_cv.common.data import data_path
from utils_cv.common.gpu import which_processor
from utils_cv.classification.data import imagenet_labels
from utils_cv.classification.model import IMAGENET_IM_SIZE, model_to_learner

# ----------------------------------------------------------------------
# Parse command line arguments
# ----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'path',
    help='path or url to image')

#option_parser.add_argument(
#    '--model',
#    help="use this model instead of '{}'.".format(RESNET18))


args = option_parser.parse_args()

# ----------------------------------------------------------------------

labels = imagenet_labels()

# Convert a pretrained imagenet model into Learner for prediction. 
# You can load an exported model by learn = load_learner(path) as well.
# --model=
# models.BasicBlock 	models.Darknet 	models.DynamicUnet
# models.ResLayer 	models.ResNet 	models.SqueezeNet
# models.UnetBlock 	models.WideResNet 	models.XResNet
# models.alexnet 	models.darknet 	models.densenet121
# models.densenet161 	models.densenet169 	models.densenet201
# models.resnet101 	models.resnet152 	models.resnet18
# models.resnet34 	models.resnet50 	models.squeezenet1_0
# models.squeezenet1_1 	models.unet 	models.vgg16_bn
# models.vgg19_bn 	models.wrn 	models.wrn_22
# models.xception 	models.xresnet 	models.xresnet101
# models.xresnet152 	models.xresnet18 	models.xresnet34
# models.xresnet50
learn = model_to_learner(models.resnet18(pretrained=True), IMAGENET_IM_SIZE)
#learn = model_to_learner(models.resnet152(pretrained=True), IMAGENET_IM_SIZE)
#learn = model_to_learner(models.xresnet152(pretrained=True), IMAGENET_IM_SIZE)

# Want to load from local copy rather than from ~/.torch? Maybe
#learn = load_learner(file="resnet18-5c106cde.pth")

#model = untar_data("resnet18-5c106cde.pth")
#learn = load_learner(model)

url = args.path

if is_url(url):
    # Download an example image
    # IM_URL = "https://cvbp.blob.core.windows.net/public/images/cvbp_cup.jpg"
    imfile = os.path.join(data_path(), "temp.jpg")
    urllib.request.urlretrieve(url, imfile)
else:
    imfile = os.path.join(get_cmd_cwd(), url)
    
im = open_image(imfile, convert_mode='RGB')

# Predict the class label.

_, ind, prob = learn.predict(im)
sys.stdout.write(f"{prob[ind]:.2f},{labels[ind]}\n")

