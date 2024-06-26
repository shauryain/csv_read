from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def handle_uploaded_file(f):
    data = pd.read_csv(f)
    print(data,"********************************************")
    analysis_result = data.describe()
    return analysis_result

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            analysis_result = handle_uploaded_file(request.FILES['file'])
            fig, ax = plt.subplots()
            analysis_result.plot(kind='bar', ax=ax)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            return render(request, 'analysis/result.html', {
                'analysis_result': analysis_result.to_html(),
                'image_base64': image_base64,
            })
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})
