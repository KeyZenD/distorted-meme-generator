import numpy as np
import sys
import struct
import wave

wavf = 'audio.wav'
wr = wave.open(wavf, 'r')

ch = wr.getnchannels()
width = wr.getsampwidth()
fr = wr.getframerate()
fn = wr.getnframes()
bdata = wr.readframes(wr.getnframes())
wr.close()
data = np.frombuffer(bdata, dtype=np.int16)

min_freq = 3
max_freq = 6
min_amp = 100
max_amp = 150

xround=lambda x:(x*2+1)//2

def getofs(amp, freq, x):
  return int(amp*(np.cos(np.pi*freq*1/(fr/2)*x)+1)//2)

def main(l):
  
  x = 0
  length = len(l)/2
  first = True
  
  for midx in range(0, len(l), 2):
    
    pre = 1-(x+1)/length
    post = (x+1)/length
    freq = min_freq*pre + max_freq*post
    amp = min_amp*pre + max_amp*post
    sidx = midx + getofs(amp, freq, x)*2

    if first:
      array = np.array(l[sidx:sidx+2])
    else:
      array = np.append(array, l[sidx:sidx+2])
    first = False

    x+=1

    state = x/length*100

    print("\r{:.2f}%".format(state), end="")
    
  return array

array = main(data)

print(array)

'''
for l in blocks:
  pre = (x+1)/length
  post = 1-(x+1)/length
  freq = min_freq*pre + max_freq*post
  amp = min_amp*pre + max_amp*post
  idx = getofs(amp, freq, x)
  #array = np.vstack([array, l[idx]])
  print("\r{0}".format(l[idx]), end="")
  x+=1
'''


outf = 'out_audio.wav'
outd = struct.pack("h" * len(array), *array)

ww = wave.open(outf, 'w')
ww.setnchannels(ch)
ww.setsampwidth(width)
ww.setframerate(fr)
ww.writeframes(outd)
ww.close()


'''
spl = x%8
pre = (x+1)/length
post = 1-(x+1)/length
freq = min_freq*pre + max_freq*post
amp = min_amp*pre + max_amp*post
idx = getofs(amp, freq, x)
if spl == idx:
  np.append(array, i)
x += 1
print("\r{0} {1}".format(idx,spl), end="")
'''
