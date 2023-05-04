import base64
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .ml_models import clf
clf = clf()

def index(request):
    image_ori = None
    #graph = None
    output = 0

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            image_bytes = image.file.read()
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            image_ori = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
            try:
                output = clf.predict(image_bytes = image_bytes)
            except RuntimeError as re:
                print(re)
    else:
        form = ImageUploadForm()

    context = {
        'form': form,
        'image_ori': image_ori,
        'output': output
        #'quantity': quantity,
        #'graph': graph
    }
    return render(request, 'image_classification/index.html', context)


def about(request):
    return render(request, 'image_classification/about.html')

def diseases(request):
    return render(request, 'image_classification/diseases.html')