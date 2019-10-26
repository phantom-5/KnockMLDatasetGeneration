import librosa
import numpy as np

def removeNans(np_arr):
    ret=[]
    for i in np_arr:
        l=[]
        for j in i:
            if not np.isnan(j):
                l.append(j)
        ret.append(l)
    return np.array(ret)


y, sr = librosa.load('not1.wav')
x, xr = librosa.load('not1.wav')
y=librosa.stft(y)
freqs = np.abs(y)
phases = np.angle(y)
amps = librosa.power_to_db(freqs**2, ref=np.max)
amps=removeNans(amps)
freqs=removeNans(freqs)
phases=removeNans(phases)
ffsum=0
fasum=0
fpsum=0

for bins in freqs:
    fsums=0
    fmin=np.min(bins)
    fran=np.ptp(bins)
    for i in bins:
        if fran != 0:
            i=(i-fmin)/fran
        else:
            i=1
        fsums=fsums+i
    ffsum=ffsum+fsums
print('Freq',ffsum/len(freqs))


for bins in amps:
    asums=0
    amin=np.min(bins)
    aran=np.ptp(bins)
    for i in bins:
        if aran != 0:
            i=(i-amin)/aran
        else:
            i=1
        asums=asums+i
    fasum=fasum+asums
print('Amps',fasum/len(amps))

for bins in phases:
    psums=0
    pmin=np.min(bins)
    pran=np.ptp(bins)
    for i in bins:
        if pran != 0:
            i=(i-pmin)/pran
        else:
            i=1
        psums=psums+i
    fpsum=fpsum+psums
print('Phases',fpsum/len(phases))

print('Pitch',librosa.beat.tempo(y=x,sr=xr))