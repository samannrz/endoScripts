import torch
import torch.nn as nn
import torch.optim as optim

checkpoint = torch.load('glenda_model/checkpoint', map_location="cpu")
