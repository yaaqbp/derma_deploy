from torch import load as torch_load
from torchvision import transforms
from torch.nn import Softmax
import numpy as np
from PIL import Image
import io
from image_classification.descriptions import descriptions

class clf():
    def __init__(self):

        self.model = torch_load('image_classification/saved_models/model_20_epochs.pt')
        self.model.eval()

        input_size= 224
        norm_mean,norm_std = ([0.7853635, 0.5307834, 0.5485232], [0.13058408, 0.14806533, 0.16119444])
        self.basic_transform = transforms.Compose([transforms.Resize((input_size,input_size)), transforms.ToTensor(),
                                        transforms.Normalize(norm_mean, norm_std)])
    
        self.lesion_type_dict = descriptions

    def predict(self, image_bytes):
        self.classes = ['akiec', 'bcc', 'bkl', 'df', 'nv', 'vasc','mel', 'unkown']
        img = Image.open(io.BytesIO(image_bytes))
        tensor_img = self.basic_transform(img).unsqueeze(0)
        outputs = self.model(tensor_img)
        softmax = Softmax(dim=1)
        probabilities = softmax(outputs).data.numpy()[0]
        prediction = np.argmax(probabilities) if max(probabilities) >0.7 else -1
        disease = self.lesion_type_dict.get(self.classes[int(prediction)], {
        })
        if disease: disease['prob'] = int(max(probabilities)*100)
    
        return disease