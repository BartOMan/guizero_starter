#########################################################################################################################
# REFERENCES
#   https://www.gaussianwaves.com/2015/11/interpreting-fft-results-complex-dft-frequency-bins-and-fftshift/
#   http://bme.elektro.dtu.dk/31610/notes/complex.signals.pdf
#   https://www.analog.com/media/en/technical-documentation/dsp-book/dsp_book_Ch31.pdf
#   https://www.dspguide.com/ch12/1.htm
#   https://www.quora.com/Why-complex-signal-doesnt-exhibit-any-symmetric-around-mid-point-DC-frequency-after-Fourier-analysis-while-real-signal-exhibit
#########################################################################################################################

# CRITICALLY IMPORTANT!!
# ALWAYS ALWAYS ALWAYS CHOOSE YOUR STEP SIZE WITH THIS CRITERIA:
#   1) Step size must be <= HALF the period of your highest frequency
#       (Nyquist-Shannon Sampling Theorem).  
#       i.e. Pick the highest frequency in your signal and make sure it has >= 2 points/period in it
#
#   2) Don't be a dumb-ass and shoot yourself in the foot if you have a choice about the
#       sampling size.  For maximizing the quality of the DFT and getting EXACT (not close, but EXACT)
#       amplitudes & frequency values, choose a sampling time (dt) to have an INTEGER number of points
#       in ALL frequency components of interest.  
#       Example:   Suppose you're sampling a digitial signal running at 10 Gbps.
#                  The basic bit width is T=1/10e9, so instead of being a dumbass and picking
#                  dt values out of thin air, choose an INTEGER NUMBER OF SAMPLES PER BIT.
#
#       Example:   Suppose you're sampling tones at 10 Hz & 20 Hz.    
#                  The highest freq is 20 Hz, with a period of 0.05 sec.   
#                  Nyquist/Shannon requires dt to be dt <= 0.025 sec, and that is perfectly adequate
#                  for extracting BOTH frequency components and BOTH amplitudes EXACTLY.
#                  The DFT should pick up 2 pure tones @ 2 precise amplitudes.
#                  This works, because dt=0.025 sec evenly divides the 10, and 20 Hz periods.
#                       Freq    Period      dt      Samples/Period
#                       10      0.1         0.025       4
#                       20      0.05        0.025       2
#                   
#   3) If you are building a time domain signal with equations, you must understand the effect
#       that a phase delay has on your time domain signals.
#       Example:   cos(2*pi*f*t + pi/3))  and   cos(2*pi*f*t) look like the same signal, with a simple
#                   phase shift in it.   But the pi/3 shift will reduce your spectral components by 
#                   cos(pi/3) or 0.5.
#

#####################################################
# KEY RELATIONSHIPS:
#   1) Frequency step:  df = 1/Tend  
#      Therefore, adjust your df freq step so that freq samples
#      land on all freq components you might have.
#   2) 
#####################################################


f = np.array( [10.0,  15.0, 20.0] )     # 2 freq components (Hz)
A = np.array( [1.0,    1.0,  1.0] )     # 2 amplitude components

maxF = np.max(f)                        # Highest freq component
minF = np.min(f)                        # Lowest freq component


############################################################
# ONE CRITERIAL FOR CHOOSING TEND:
#   Force Tend to be an integer multiple of the longest
#   period (lowest freq).  This produces a smaller df
#   value that also helps hitting integer freq values
#   on the higher freq end
############################################################
NumPeriods = 4
Tend = NumPeriods*(1/minF)              # Make Tend be an integer multiple of the longest period (lowest freq)


############################################################
# TWO CRITERIAL FOR CHOOSING SAMPLING TIME, DT:
#   1) Nyquist/Shannon sampling theorem:  
#       Need >= 2 samples/period in the smallest period (highest freq)
#   2) dt should have an integer number of points in the longest period
#       (lowest freq) or else Tend will not end up as an even multiple 
#       of the longest period
############################################################
Tshortest = 1/maxF                      # Shortest period (highest freq component)]

# dtMax = (1/maxF)/2                    # Nyquist/Shannon sampling theorem requires >= 2 samples/period, so the MAX
                                        # sampling time is half the shortest period.  But it's always good to choose
                                        # some value well below the max value
dtMax = Tshortest/(2*5)                 # Choose a max sampling time 5X smaller than the Nyquist/Shannon limit or
                                        # 1/10th the shortest period


Tlongest = 1/minF                       # Longest period (lowest freq component)
Np   = np.int64(np.ceil(Tlongest/dtMax))# Number of sample points to use in the longest period

dt   = Tlongest/Np                      # Set dt so that there are an integer number of dt points in the
                                        # longest period (lowest freq).  If you don't do this, then Tend won't
                                        # end up at the value you intended.
                                        # HOWEVER, dt is also constrained (by Nyquist/Shannon) to be <= half the period
                                        # of the shortest period (fastest freq)

# Plot the time-domain sinusoid
t = np.arange(0, Tend, dt)
# f = np.array( [7.0,  12.0] )   # 2 freq components (Hz)
# A = np.array( [0.75, 1.4] )    # 2 amplitude components

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

