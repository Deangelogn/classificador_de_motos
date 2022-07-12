
import torch
import json
import numpy as np
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms


class Model_Handler():
  def __init__(self, model=None):
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
  
    if model == 'motorcycle':
      self.model = torch.load('models/resnet18_pytorch.pth', map_location=self.device)
      self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
          ])
      self.sm = torch.nn.Softmax()
      self.classes = json.load(open("models/classes/motorcycle.json", 'r'))
      
  def inference(self, image):
    image_tensor = self.transform(image).float() 
    image_tensor = image_tensor.unsqueeze_(0)
    input_tensor = Variable(image_tensor)
    input_tensor = input_tensor.to(self.device)
    output = self.model(input_tensor)
    probs = self.sm(output)
    probs = probs.data.cpu().numpy()[0]
    probs_round = [round(num, 5) for num in probs]

    return probs_round

  def get_classes(self):
    return self.classes