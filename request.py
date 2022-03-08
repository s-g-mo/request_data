'''
FUNCTION request.py

This function queries a seismic client for data and downloads it if available.

Stephen Mosher (2020)
'''
# Import modules and functions.
import os
import save
import numpy as np
from obspy import Stream, UTCDateTime
from obspy.clients.fdsn import Client
from obspy.io.sac.util import obspy_to_sac_header

def data(clnt,tstart,tend,dlen,ntwrk,chns,stns,N,sD,fname_fmt,data_dir,preproc):
  
  # Check dlen doesn't exceed length of request interval.
  if dlen > (tend - tstart):
    print('\n Requested segment length exceeds length of request interval ...')
    raise SystemExit
  
  # Establish client.
  print('\n Initializing client ...')
  client = Client(clnt)

  inv = client.get_stations(starttime=tstart,
                            endtime=tend,
                            network=ntwrk,
                            station=stns,
                            level='response')

  # Download data station by station.
  for stn in [stn.code for stn in inv[0]]:

    # Initialize the running time variables.
    t1 = tstart
    t2 = tstart + dlen
    
    # Proceed by downloading seismograms within [tstart, tend].
    while t2 <= tend:

      # Try and get waveforms from the client.
      try:
        print('\n Fetching waveforms @'+stn+': '+str(t1).split('.')[0]+' ...')
        
        st = client.get_waveforms(ntwrk,
                                  stn,
                                  '*',
                                  chns,
                                  t1,
                                  t2,
                                  attach_response=True)

        # Perform quality control on traces in stream. Run this first because it
        # catches empty streams which, otherwise, bug up the next check.
        QC_pass = quality_control(st, sD, dlen)
        if QC_pass == False:
          t1, t2 = advance_segment(t1, t2, dlen)
          continue

        # If num unique channels in st != the number being requested, continue.
        if len( set( [tr.stats.channel for tr in st.traces] )) != N:
          print('\n Requested channels unavailable. Continuing ...')
          t1, t2 = advance_segment(t1, t2, dlen)
          continue 

        # Imprint stn lat, lon, elv, and comp orientations into each tr.
        for tr in st:
          imprint_stats(tr, inv[0])
          
        # Optional pre-processing. Values hardcoded for now. Generalize later.
        if preproc:
          for tr in st:
            if (tr.stats.channel == np.array(chns.split(',')[0:3])).any():
              tr.detrend('demean')
              tr.detrend('linear')
              tr.filter('lowpass', freq=0.5 * 5.0, corners=2, zerophase=True)
              tr.resample(1.0)
              tr.remove_response(pre_filt=[0.001, 0.005, 45., 50.], output='DISP')
            elif tr.stats.channel == chns.split(',')[3]:
              tr.detrend('demean')
              tr.detrend('linear')
              tr.filter('lowpass', freq=0.5 * 5.0, corners=2, zerophase=True)
              tr.resample(1.0)
              tr.remove_response(pre_filt=[0.001, 0.005, 45., 50.])

        # Optional pre-processing. Values hardcoded for now. Generalize later.
        if preproc:
          preprocessing(st)

        # Write to disk.
        for tr in st:
          save.SAC_data(tr, fname_fmt, data_dir)

        # Shift to next segment.
        t1, t2 = advance_segment(t1, t2, dlen)
      
      except Exception as e:
        print('\n Exception occurred: ' + str(e))
        print('\n Continuing ...')
        
        # Shift to the next data segment.
        t1, t2 = advance_segment(t1, t2, dlen)
        continue

def preprocessing(st):
  for tr in st:
    channel_codes = [char for char in tr.stats.channel]
    # Pre-processing for seismic components.
    if channel_codes[1] == 'H':
      tr.detrend('demean')
      tr.detrend('linear')
      #tr.filter('lowpass', freq=0.5 * 5.0, corners=2, zerophase=True)
      #tr.resample(1.0)
      tr.remove_response(pre_filt=[0.001, 0.005, 45., 50.], output='DISP')
    # Pre-processing for pressure component.
    elif channel_codes[1] == 'D':
      tr.detrend('demean')
      tr.detrend('linear')
      #tr.filter('lowpass', freq=0.5 * 5.0, corners=2, zerophase=True)
      #tr.resample(1.0)
      tr.remove_response(pre_filt=[0.001, 0.005, 5., 10.])

def quality_control(st, strict_dlen, dlen):

  QC_pass = True

  # Remove any zero-valued and constant-valued traces.
  rejects = [t for t in st if np.all(t.detrend(type='demean').data == 0)]

  if rejects:
    print('\n Constant-valued traces. Continuing ...')
    QC_pass = False
    return QC_pass

  elif not rejects:
    # Are traces segmented? If they're segmented maybe it's easy to put them
    # back together? Figure this out another time.

    # Assess if length of trace's data < strict_dlen.
    if strict_dlen:
      rejects = [t for t in st if dlen * t.stats.sampling_rate - len(t.data) > 1]

    if rejects:
      print('\n Traces dont have the correct length. Continuing ...')
      QC_pass = False
      return QC_pass

def imprint_stats(tr, network_obj):
  # Write some stats into sac header of trace.
  stn_obj = network_obj.select(station=tr.stats.station)
  tr.stats.sac = obspy_to_sac_header(tr.stats)
  tr.stats.sac.stla = stn_obj[0][0].latitude
  tr.stats.sac.stlo = stn_obj[0][0].longitude
  tr.stats.sac.stel = stn_obj[0][0].elevation
  tr.stats.sac.cmpaz = stn_obj[0][0].azimuth
  tr.stats.sac.cmpinc = stn_obj[0][0].dip + 90. # conversion to .SAC convention
  return None

def advance_segment(t1, t2, dlen):
  t1 += dlen
  t2 += dlen
  return t1, t2
