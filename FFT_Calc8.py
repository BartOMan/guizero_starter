#########################################################################################################################
# REFERENCES
#   https://www.gaussianwaves.com/2015/11/interpreting-fft-results-complex-dft-frequency-bins-and-fftshift/
#   http://bme.elektro.dtu.dk/31610/notes/complex.signals.pdf
#   https://www.analog.com/media/en/technical-documentation/dsp-book/dsp_book_Ch31.pdf
#   https://www.dspguide.com/ch12/1.htm
#   https://www.quora.com/Why-complex-signal-doesnt-exhibit-any-symmetric-around-mid-point-DC-frequency-after-Fourier-analysis-while-real-signal-exhibit
#########################################################################################################################
f   = 12
T   = 1/f
phi = 0.0

# Plot the time-domain sinusoid
t = np.arange(0, 4*T, T/50)
# f = np.array( [7.0,  12.0] )    # 2 freq components (Hz)
# A = np.array( [0.75, 1.4] )    # 2 amplitude components
f = np.array( [12.0] )    # 2 freq components (Hz)
A = np.array( [1.4] )    # 2 amplitude components

x = 0.0
for ii,fv in enumerate(f):
    x += A[ii]*cos(2*np.pi*f[ii]*t + phi)
    
plot(t,x, '-*b')
grid()

#############################################
# HOMEBUILT REAL-VALUED DFT FUNCTION
# PASS IN t, f, x & Compute the REAL DFT
# (for real-valued sequence, 'x')
#############################################
N = len(t)                      # # points in the sequence
dt = np.mean(np.diff(t))        # time step
T  = dt*N                       # Total sequence duration
df = 1/T                        # Sampling freq

# Define constants
Nover2 = np.int64(N/2)
twoPi  = 2.0*np.pi


k = np.arange(0,Nover2+1,1)     # Discrete, normalized frequency array:   
                                #   Values:  0 ==> N/2  (N/2 + 1 points)
K = k*df                        # The REAL, positive (non-normalized or ACTUAL) frequency axis, Hertz


# This version requires that N is even
if ( np.mod(N,2) ):
    raise ValueError("\n\nERROR:   This requires N to be EVEN!!\n\n")


Xre = np.zeros([Nover2+1,])    # Real part of X[k]
Xim = np.zeros([Nover2+1,])    # Imag part of X[k]
for kv in k:
    for n in range(N):
        Xre[kv] +=  x[n]*cos(twoPi*kv*n/N)
        Xim[kv] += -x[n]*sin(twoPi*kv*n/N)        


# Reduce the spectral amplitudes to compensate for the artificial processing gain of N/2.
# Raw spectral amplitudes are proportional to # samples (N), so we must compensate.
Xre /=  (N/2)             
Xim /=  (N/2)         

Xre[0]      /= 2             # Adjust DC & Nyquist freq components.  
Xre[Nover2] /= 2



# print(Xim)
print(Xre)


# Plot the freq-domain DFT( x[t] )
# Plot Xre vs freq  (Xre is the real(X(f)) )
# If the original 'f' was 3, then there will be one spike at 3
stem(K,Xre)
grid()
# stem(k,Xim)
# grid()

K = k + 0.0     # Make a copy of the discrete freq array

#############################################
# HOMEBUILT REAL-VALUED INVERSE DFT FUNCTION
# PASS IN L, Xre and Xim & Compute the REAL IDFT
# (for real-valued sequence, 'x')
#############################################
del(x)

Nover2 = len(K)-1
N      = 2*Nover2
if ( np.mod(N,2) ):
    raise ValueError("\n\nERROR:   This requires N to be EVEN!!\n\n")

# Discrete freq array:   0 ==> N/2  (has N/2+1 points)
k = np.arange(0,Nover2+1,1)
x = np.zeros([N,])    # Time domain signal, x[n]
for n in range(N):
    for kv in k:
        x[n] += Xre[kv]*cos(2*np.pi*kv*n/N)
        x[n] -= Xim[kv]*sin(2*np.pi*kv*n/N)        


# Plot the freq-domain DFT( x[t] )
# Plot Xre vs freq  (Xre is the real(X(f)) )
# If the original 'f' was 3, then there will be one spike at 3
plot(t,x, '--dr')
#############################################

