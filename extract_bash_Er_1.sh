#!/bin/sh
ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_091_VID001.mp4 -ss 00:11:40 -to 00:11:50 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_091_VID001_trim1.mp4

ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_095_VID001.mp4 -ss 00:00:01 -to 00:00:30 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_095_VID001_trim1.mp4
ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_095_VID004.mp4 -ss 00:02:30 -to 00:02:40 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_095_VID004_trim1.mp4

ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_096_VID001.mp4 -ss 00:21:30 -to 00:21:58 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_096_VID001_trim1.mp4
ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_096_VID002.mp4 -ss 00:08:28 -to 00:08:48 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_096_VID002_trim1.mp4

ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_098_VID001.mp4 -ss 00:13:28 -to 00:13:36 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_098_VID001_trim1.mp4
ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_098_VID001.mp4 -ss 00:15:56 -to 00:16:22 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_098_VID001_trim2.mp4

ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_099_VID001.mp4 -ss 00:10:30 -to 00:10:45 -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_099_VID001_trim1.mp4
ffmpeg -i /data/Videos/endodata/orig/bsp1_GY_20230601_099_VID001.mp4 -ss  -to  -c:v copy /data/Videos/endodata/sequ/bsp1_GY_20230601_099_VID001_trim2.mp4
