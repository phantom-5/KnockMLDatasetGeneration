import librosa
import numpy as np
import xlsxwriter as xl

workbook = xl.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1','Frequency')
worksheet.write('B1','Amplitude')
worksheet.write('C1','Phase')
worksheet.write('D1','Tempo')
worksheet.write('E1','Label')

def removeNans(np_arr):
    ret=[]
    for i in np_arr:
        l=[]
        for j in i:
            if not np.isnan(j):
                l.append(j)
        ret.append(l)
    return np.array(ret)

Freq=0
Amps=0
Phases=0
Pitch=0

def cal(filename):
    global Freq,Amps,Phases,Pitch
    y, sr = librosa.load(filename)
    x, xr = librosa.load(filename)
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
    Freq=ffsum/len(freqs)


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
    Amps=fasum/len(amps)

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
    Phases=fpsum/len(phases)

    Pitch=librosa.beat.tempo(y=x,sr=xr)

row=116
col=0

for item in range(1,19):
    print("Writing to workbook...")
    cal('Nots//not'+str(item)+'.wav')
    vals=[Freq,Amps,Phases,Pitch[0],0]
    print(vals)
    for stuff in vals:
        worksheet.write(row,col,stuff)
        col+=1
    row+=1
    col=0
    print("Inserted ",row)

for item in range(7,27):
    print("Writing to workbook...")
    cal('Knocks//Knock'+str(item)+'.wav')
    vals=[Freq,Amps,Phases,Pitch[0],1]
    print(vals)
    for stuff in vals:
        worksheet.write(row,col,stuff)
        col+=1
    row+=1
    col=0
    print("Inserted ",row)

workbook.close()
