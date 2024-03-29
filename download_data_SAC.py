'''
SCRIPT download_data_SAC.py

A script to download seismic data as .SAC files and write them into a given 
output directory. The main function that gets called is request.data().

Important Notes:
  1) You must specify how many channels (N) are being requested.

  2) Network code, stations, and channels support Unix-style wildcard characters
  
  3) Quality control in request.data() throws out zero/constant-valued traces.

Stephen Mosher (2020) - updated 2022
'''
# Import modules and functions
import request, setup
from obspy import UTCDateTime 

############################## Request parameters ##############################

clnt = 'IRIS'                     # client
name = 'YL'                       # network name
code = 'YL'                       # network code
chns = 'LH1,LH2,LHZ,LDH'          # channel(s)
N = 4                             # number of channels being requested
stns = 'A02W'                     # station(s)
sT = UTCDateTime(2009, 11, 21, 00)# request interval start time
eT = UTCDateTime(2010, 11, 19, 00)# request interval end time
dlen = 60. * 60. * 24             # length of data segments [seconds]
strict_dlen = True                # if length of segment < dLen, throw out
fname_fmt = 'default'             # file name format (default is %Y.%j.%H.%M)
preproc = True                    # optional preprocessing on downloaded data

# Specify directory to save .SAC files.
out_dir = '/Users/stephenmosher/Seismo/raw_data/' + code + '_LH/'

##################################### Main #####################################
                           
# Set up directory for .SAC files.
setup.directory(out_dir)

# Request data.
request.data(clnt,
             sT,
             eT,
             dlen, 
             code, 
             chns, 
             stns, 
             N,
             strict_dlen,
             fname_fmt,
             out_dir,
             preproc)
