from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response #will render data in json
from rest_framework.decorators import api_view
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

import base64 
from base64 import b64decode
from http import HTTPStatus
import time
import subprocess
from django.http import HttpResponse

from rest_framework import status
from http import HTTPStatus
from django.http import HttpResponse

# GLOBALS (horrible practices)
mat_file = "ECG.mat"

put_command = f"/home/rivercard/oscar-cli service put-file dislib-rf minio ./{mat_file} dislib-rf/in/{mat_file}"
check_command_1 = f"/home/rivercard/oscar-cli service logs list dislib-rf -s Running,Pending"
check_command_2 = f"/home/rivercard/oscar-cli service logs list dislib-rf"
get_log_command = f"/home/rivercard/oscar-cli service logs get dislib-rf"

# HELPER FUNCTIONS
# Returns job state of specific job 
def get_job_state(job_id):
    run_object = subprocess.run(f"{check_command_2} | grep {job_id}", shell=True, capture_output=True, text=True)
    check_str = str(run_object.stdout)
    job_items = check_str.split()
    return str(job_items[1])

# Returns job id of (hopefully) last sent job
def get_job_id():
    run_object = subprocess.run(check_command_1, shell=True, capture_output=True, text=True)
    check_str = str(run_object.stdout)

    check_lines = check_str.splitlines()
    print(check_lines)
    last_job = check_lines[1]
    last_job_items = last_job.split()
    return last_job_items[0]

# Return job log of specific job
def get_job_log(job_id):
    run_object = subprocess.run(f"{get_log_command} {job_id}", shell=True, capture_output=True, text=True)
    log_str = str(run_object.stdout)
    return log_str


# BACKEND FUNCTIONS
@api_view(['GET']) 
def getData(request):
    person = {'name':'Dennis', 'age':'28'}
    return Response(person)

@api_view(['POST'])
def iktus(request):
    if request.method == 'POST':
        body = request.body
        bytes = b64decode(body, validate=True)
        f= open('file.pdf','wb')
        f.write(bytes)
        f.close()
        if bytes[0:4] != b'%PDF':
            print('Missing the PDF file signature')
        
        # Convert PDF to final mat file
        pdfToECG()
        treureColumna()
        csvToMat()

        # Send job and wait until we have a log file
        # IT'S MORBING TIME
        # Send mat file
        global put_command
        print(put_command)
        run_object = subprocess.run(put_command, shell=True, capture_output=True, text=True)
        time.sleep(3) # To ensure that the job is running when we poll

        # Start the state polling
        job_id = get_job_id()
        print(f"Job sent is {job_id}")

        #Check when the job finishes and get its log and inference result
        while get_job_state(job_id) != "Succeeded":
            time.sleep(2)
            print(f"Job {job_id} still running...")
        print("JOB FINSHED!")
        log_str = get_job_log(job_id)

        # Parse the result!
        log_list = log_str.splitlines()
        pos = log_list.index('------------------------------------------------------------')
        result_str = log_list[pos-4]

        print(f"Result of inference is {result_str}")

        # Return respone to app 
        person = {'value':result_str}

        return Response(
        person,
        status=status.HTTP_200_OK,
    )




# WALL OF SHAME

# Handle file upload
#    if request.method == 'POST':
#        form = DocumentForm(request.POST, request.FILES)
#        if form.is_valid():
#            newdoc = Document(docfile = request.FILES['docfile'])
#            newdoc.save()

            # Redirect to the document list after POST
#            return HttpResponseRedirect(reverse('myapp.views.list'))
#    else:
#        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
#    documents = Document.objects.all()

    # Render list page with the documents and the form
#    return render_to_response(
#        'myapp/list.html',
#        {'documents': documents, 'form': form},
#        context_instance=RequestContext(request)
#    )
#@api_view(['POST'])
#def UploadCSV(request):
#    if request.method = 'POST':
#        file = request.FileField()
#    else
#        pass
#    return render(request, 'administrator')

from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image, ImageOps
import numpy as np
from numpy import asarray
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 5]

from scipy.io import savemat
import scipy.io as sio
from scipy.ndimage import label

def pdfToECG():
    image = convert_from_path('file.pdf')
    # convert the image to grayscale
    im = ImageOps.grayscale(image[0])

# crop the image and paste the pieces together
    width, height = im.size

    n = 319
    left = 49
    right = 1662

    top1, bottom1 = 393, 638
    top2, bottom2 = top1 + n, bottom1 + n
    top3, bottom3 = top2 + n, bottom2 + n
    top4, bottom4 = top3 + n, bottom3 + n

    im1 = im.crop((left, top1, right, bottom1))
    im2 = im.crop((left, top2, right, bottom2))
    im3 = im.crop((left, top3, right, bottom3))
    im4 = im.crop((left, top4, 1258, bottom4))

    imgs = [im1, im2, im3, im4]
    imgs_comb = np.hstack(imgs)
    imgs_comb = Image.fromarray(imgs_comb)

    imgs_comb.save('test_cropped.jpg')

    # convert the image to an array, keep only the ECG line, and save the csv
    data = np.array(imgs_comb.transpose(Image.FLIP_TOP_BOTTOM))
    print(data.shape)

    #data.setflags(write=1)


    n = 111
    data[data < 100] = 255
    data[data < n] = 0
    data[data >= n] = 255
    im = Image.fromarray(data)
    mat = list()
    for i in range(data.shape[1]):
        l = np.where(data.T[i]==0)[0]
        if len(l) > 0:
            mat.append([i, np.mean(l)]) # average of multiple vertical pixels
        else:
            mat.append([i, np.nan])

    df = pd.DataFrame.from_records(mat)
    df.columns = ['x','y']
    df['y'] = df['y'] - (250/30)*10 # set zero

    df.to_csv('test.csv')

def treureColumna():
    df = pd.read_csv('test.csv')
    # If you know the name of the column skip this
    first_column = df.columns[0]
    # Delete first
    df = df.drop([first_column], axis=1)
    df.to_csv('test.csv', index=False)


freq = 511
secs = 30

def csvToMat():
    #drive.mount('/content/gdrive')
    df = pd.read_csv("test.csv",error_bad_lines=False)
    df = df.iloc[8:]
    df = df.set_axis(["unit","amplitude"], axis=1)
    df['unit'] = pd.to_numeric(df['unit'])
    df['amplitude'] = pd.to_numeric(df['amplitude'])
    df = df.dropna()
    time = np.arange(df.size/2)/freq
    plt.plot(time, df.unit * df.amplitude)
    plt.xlabel("time[S]")
    plt.ylabel("scaled Amplitude")
    plt.title("apple watch ECG")
    plt.show()

    arr =(df.unit * df.amplitude).to_numpy()

    mydic = {"val":arr}
    savemat(mat_file, mydic)