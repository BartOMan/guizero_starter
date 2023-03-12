
# REFERENCES
#   https://www.gaussianwaves.com/2015/11/interpreting-fft-results-complex-dft-frequency-bins-and-fftshift/
#   http://bme.elektro.dtu.dk/31610/notes/complex.signals.pdf
#   https://www.analog.com/media/en/technical-documentation/dsp-book/dsp_book_Ch31.pdf
#   https://www.dspguide.com/ch12/1.htm
#   https://www.quora.com/Why-complex-signal-doesnt-exhibit-any-symmetric-around-mid-point-DC-frequency-after-Fourier-analysis-while-real-signal-exhibit
# 

t = np.arange(0,1,0.01)
f = 3
x = cos(2*np.pi*f*t)
plot(t,x)
grid()

#############################################
# HOMEBUILT REAL-VALUED DFT FUNCTION
# PASS IN t, f, x & Compute the REAL DFT
# (for real-valued sequence, 'x'
#############################################

N = len(t)
Nover2 = np.int64(N/2)
if ( np.mod(N,2) ):
    raise ValueError("\n\nERROR:   This requires N to be EVEN!!\n\n")

# Discrete freq array:   0 ==> N/2  (has N/2+1 points)
k = np.arange(0,Nover2+1,1)

Xre = np.zeros([Nover2+1,])    # Real part of X[k]
Xim = np.zeros([Nover2+1,])    # Imag part of X[k]
for kv in k:
    Xre[kv] = 0         
    Xim[kv] = 0 
    for n in range(N):
        Xre[kv] += x[n]*cos(2*np.pi*kv*n/N)
        Xim[kv] += x[n]*sin(2*np.pi*kv*n/N)        
    Xre[kv] *=  (2.0/N)         
    Xim[kv] *= -(2.0/N)         


print(Xre)

# Plot Xre vs freq  (Xre is the real(X(f)) )
# If the original 'f' was 3, then there will be one spike at 3
stem(k,Xre)
grid()
#############################################
# HOMEBUILT REAL-VALUED DFT FUNCTION
# PASS IN t, f, x & Compute the REAL DFT
# (for real-valued sequence, 'x'
#############################################
