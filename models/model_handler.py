
import torch
import json
from torch.autograd import Variable
from torchvision import transforms


class Model_Handler():
  def __init__(self, model=None):
    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
  
    if model == 'motorcycle':
      self.model = torch.load('models/pytorch_motorcycle.pth', map_location=self.device)
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
    return probs

  def get_classes(self):
    return self.classes