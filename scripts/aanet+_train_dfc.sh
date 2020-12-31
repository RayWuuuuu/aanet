#!/usr/bin/env bash

# Train on Scene Flow training set
CUDA_VISIBLE_DEVICES=0,1,2,3 python train.py \
--mode val \
--checkpoint_dir checkpoints/aanet+_dfc \
--batch_size 4 \
--val_batch_size 4 \
--img_height 960 \
--img_width 960 \
--val_img_height 1056 \
--val_img_width 1056 \
--feature_type ganet \
--feature_pyramid \
--refinement_type hourglass \
--milestones 20,30,40,50,60 \
--max_epoch 64 \
--pretrained_aanet aanet_best.pth \
--learning_rate 1e-4

