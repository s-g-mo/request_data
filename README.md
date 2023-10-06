# A simple script to download seismic data as .SAC files.
## Stephen Mosher (2020)

### Short description

The main script is *download_data_SAC.py* which calls the function *request().py*. The code relies on the ObsPy client module and is thus great for requesting data from web servers that implement the FDSN webservice definitions.

### Dependencies

  - python 3.5
  - obspy
  - numpy

### Instructions

  1) Open *download_data_SAC.py* and edit the request parameters.
  2) Close and run.
  3) See data appear.

### Further details

Available clients are (from the ObsPy documentation https://docs.obspy.org/packages/obspy.clients.fdsn.html):
  
- BGR     http://eida.bgr.de
- EMSC    http://www.seismicportal.eu
- ETH     http://eida.ethz.ch
- GEONET  http://service.geonet.org.nz
- GFZ     http://geofon.gfz-potsdam.de
- INGV    http://webservices.rm.ingv.it
- IPGP    http://eida.ipgp.fr
- IRIS    http://service.iris.edu
- ISC     http://isc-mirror.iris.washington.edu
- KOERI   http://eida.koeri.boun.edu.tr
- LMU     http://erde.geophysik.uni-muenchen.de
- NCEDC   http://service.ncedc.org
- NIEP    http://eida-sc3.infp.ro
- NOA     http://eida.gein.noa.gr
- ODC     http://www.orfeus-eu.org
- ORFEUS  http://www.orfeus-eu.org
- RESIF   http://ws.resif.fr
- SCEDC   http://service.scedc.caltech.edu
- USGS    http://earthquake.usgs.gov
- USP     http://sismo.iag.usp.br