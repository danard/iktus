import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import savemat
import scipy.io as sio
from scipy.ndimage import label

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
    savemat("ECG.mat", mydic)