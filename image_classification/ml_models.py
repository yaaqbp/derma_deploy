from torch import load as torch_load
from torchvision import transforms
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
        self.classes = ['akiec', 'bcc', 'bkl', 'df', 'nv', 'vasc','mel']
        img = Image.open(io.BytesIO(image_bytes))
        tensor_img = self.basic_transform(img).unsqueeze(0)
        outputs = self.model(tensor_img)
        prediction = outputs.max(1, keepdim=True)[1]
        disease = self.lesion_type_dict.get(self.classes[int(prediction)], {
        })
    
        return disease