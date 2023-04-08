#!/usr/bin/env python
# coding: utf-8

# # Demo LoFTR-DS on a single pair of images in an outdoor environment
# ### (This is a copy of the code in demo_single_pair.ipynb)
# 
# 
# This notebook shows how to use the loftr matcher with default config(dual-softmax) and the pretrained weights.

# In[15]:


import os
# os.chdir("..")
from copy import deepcopy

import torch
import cv2
import numpy as np
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, imshow, subplots
from src.utils.plotting import make_matching_figure


# ## Outdoor Example

# In[16]:


from src.loftr import LoFTR, default_cfg

# The default config uses dual-softmax.
# The outdoor and indoor models share the same config.
# You can change the default values like thr and coarse_match_type.
matcher = LoFTR(config=default_cfg)
matcher.load_state_dict(torch.load("weights/outdoor_ds.ckpt")['state_dict'])
# matcher = matcher.eval().cuda()
matcher = matcher.eval()


# Load example images
img0_pth = "assets/phototourism_sample_images/st_pauls_cathedral_30776973_2635313996.jpg"
img1_pth = "assets/phototourism_sample_images/st_pauls_cathedral_37347628_10902811376.jpg"
img0_raw = cv2.imread(img0_pth, cv2.IMREAD_GRAYSCALE)
img1_raw = cv2.imread(img1_pth, cv2.IMREAD_GRAYSCALE)
img0_raw = cv2.resize(img0_raw, (img0_raw.shape[1]//8*8, img0_raw.shape[0]//8*8))  # input size shuold be divisible by 8
img1_raw = cv2.resize(img1_raw, (img1_raw.shape[1]//8*8, img1_raw.shape[0]//8*8))

# img0 = torch.from_numpy(img0_raw)[None][None].cuda() / 255.
# img1 = torch.from_numpy(img1_raw)[None][None].cuda() / 255.

""" Display both images: """
if(0):
    fig, ax = subplots(1, 2, figsize=(19.2, 10.8))
    ax[0].set_title("Img0 Raw")
    ax[0].imshow(img0_raw, cmap="gray")
    ax[1].set_title("Img1 Raw")
    ax[1].imshow(img1_raw, cmap="gray")
    show()
    exit()

img0 = torch.from_numpy(img0_raw)[None][None] / 255.
img1 = torch.from_numpy(img1_raw)[None][None] / 255.

batch = {'image0': img0, 'image1': img1}

# Inference with LoFTR and get prediction
with torch.no_grad():
    matcher(batch)
    # print(batch.keys())
    mkpts0 = batch['mkpts0_f'].cpu().numpy()
    mkpts1 = batch['mkpts1_f'].cpu().numpy()
    mconf = batch['mconf'].cpu().numpy()


# In[7]:


# Draw
color = cm.jet(mconf)
text = [
    'LoFTR',
    'Matches: {}'.format(len(mkpts0)),
]
fig = make_matching_figure(img0_raw, img1_raw, mkpts0, mkpts1, color, text=text)
show()