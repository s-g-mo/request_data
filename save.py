'''
FUNCTION save.py

A function to save trace objects contained in a downloaded stream to disk.

Stephen Mosher (2020)
'''

def SAC_data(tr, fname_fmt, data_dir):
  # Grab station name and build file name.
  stn = tr.stats.station
  if fname_fmt == 'default':
    time_stamp = tr.stats.starttime.strftime(format='%Y.%j.%H.%M:%S.%f')+'.'
  else:
    time_stamp = tr.stats.starttime.strftime(format=fname_fmt)+'.'
  
  # Write.
  print('\n Writing file ' + stn + ' ' + time_stamp + tr.stats.channel +' ...')
  tr.write(data_dir + time_stamp + tr.id + '.SAC' , format='SAC')