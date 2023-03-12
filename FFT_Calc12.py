#########################################################################################################################
# REFERENCES
#   https://www.gaussianwaves.com/2015/11/interpreting-fft-results-complex-dft-frequency-bins-and-fftshift/
#   http://bme.elektro.dtu.dk/31610/notes/complex.signals.pdf
#   https://www.analog.com/media/en/technical-documentation/dsp-book/dsp_book_Ch31.pdf
#   https://www.dspguide.com/ch12/1.htm
#   https://www.quora.com/Why-complex-signal-doesnt-exhibit-any-symmetric-around-mid-point-DC-frequency-after-Fourier-analysis-while-real-signal-exhibit
#########################################################################################################################

#########################################################################################################
# CRITICALLY IMPORTANT!!
# ALWAYS ALWAYS ALWAYS CHOOSE YOUR STEP SIZE WITH THIS CRITERIA:
#   1) If building a period signal for experimentation & analysis, use 
#       cosine function, NOT sine functions!!   
# 
#   2) Step size must be <= HALF the period of your highest frequency
#       (Nyquist-Shannon Sampling Theorem).  
#       i.e. Pick the highest frequency in your signal and make sure it has >= 2 points/period in it
#               
#   3) If you are building a time domain signal with equations, you must understand the effect
#       that a phase delay has on your time domain signals.
#       Example:   cos(2*pi*f*t + pi/3))  and   cos(2*pi*f*t) look like the same signal, with a simple
#                   phase shift in it.   But the pi/3 shift will reduce your spectral components by 
#                   cos(pi/3) or 0.5.
#
#       If you require phase shifts, that's fine, but remove them from the cosines using the trig identity:
#           cos(A-B) = cos(A)*cos(B) + sin(A)*sin(B)
#               or
#           cos(A+B) = cos(A)*cos(B) - sin(A)*sin(B)
#########################################################################################################


#####################################################
# KEY RELATIONSHIPS:
#   1) Frequency step:  df = 1/Tend  
#      Therefore, adjust your df freq step so that freq samples
#      land on all freq components you might have.
#   2) Sampling time dt must be small enough so that you get
#      AT LEAST 2 samples/period in your highest freq component
#   3) You must fit an integer number of dt points in your lowest
#      freq component
#   4) All of this works out more easily if you choose the number
#       of samples (N) as an even number.  It does not need to be 2^p
#   5) If analyzing digital signals, follow these simple rules.
#      Digital signals carry data, often signaling at 2 voltage levels,
#      but nearly always with a fixed bit width (bit period), T.  
#      The bit rate is 1/T, and it's usually measured in Gbps or Mbps.
#      If you have control over how to build an artificial bit signal
#      or in how to sample an actual bit signal then:
#       a) ALWAYS build your signal to have a whole number of data bits.
#           If you're using sampled data, don't just use the data raw.
#           Take the sampled values & pre-process them, discarding half data bits
#           that you don't need.
#       b) ALWAYS choose an integer number of samples/bit.  Your bit period
#           is fundamental and you want to make sure your frequency domain df
#           hits the key frequencies associated with the sin(x)/x spectrum of 
#           this bit pattern.  This will allow that to happen.
#           Depending on the level of detail, 20 samples/bit is not bad
#           Going up to 100 samples/bit will work, but it probably doesn't 
#           need to be more than that.
#       c) ALWAYS make sure your first & last bits are at the same voltage level.
#          If you started on a logic 0, then end on a logic 0.  The rational
#          behind this is to avoid time-domain discontinuities that artificially
#          inject high frequency components into the signal in a very bad way.
#          With FFT analysis, there is no first & last point.  Your signal is assumed
#          to be periodic, first point & last points in your sequence are not unique
#          in any way, and the way the DFT sees your signal as one periodic 
#          waveform on an endless loop/repeat.   So a sudden jump from logic 0 to logic 
#          1 in 1 picosecond is quite a jolt of high-frequency energy!
#       
#          You could also splice together first/last points during the transition.
#          In that case, the last point might be transitionining midway from logic 0 to logic 1,
#          just below mid-voltage while your first sequence point might start just above mid-voltage,
#          in the same logic 0 to logic 1 transition.
#   
#       c) ALWAYs use an even number of bits in your time-domain signal.
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
Xre /=  (N/2)               # Same as multipling by (2/N)
Xim /=  (N/2)         

Xre[0]      /= 2            # Adjust DC & Nyquist freq components.  
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

############################################################################
# HOMEBUILT REAL-VALUED INVERSE DFT FUNCTION
# PASS IN L, Xre and Xim & Compute the REAL IDFT
# (for real-valued sequence, 'x')
############################################################################
del(x)              # Delete.... we will be rebuilding it from scratch

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

