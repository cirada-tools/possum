"""
Creates the images for the validation page using the *source* list from selavy. 

Generally one would want to use "pol_validation_components.py" and not this file, which
makes the images from the component list and not the source list.
"""
from validation_utils import *
import numpy as np
from numpy import inf

import pdb
import scipy.stats as stats
import pandas as pd
#from scipy import *
from astropy import units as u
import astropy.io.fits as pf
from astropy.wcs import WCS
import astropy.wcs.utils as wcs
from astropy.coordinates import SkyCoord  # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
import sys


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.ioff()

#define files
#open cubes

path=sys.argv[1]
sb=sys.argv[2] # 7216
base=sys.argv[3] #"SN1006

fluxmin=np.float(sys.argv[4]) #min flux limit in Jy
fluxmax=np.float(sys.argv[5]) #
in_i= path+"image.restored.i."+base+".SB"+str(sb)+".contcube.fits" #image.restored.q.SB4612.contcube.fits"
in_q= path+"image.restored.q."+base+".SB"+str(sb)+".contcube.fits" #image.restored.q.SB4612.contcube.fits"
in_u= path+"image.restored.u."+base+".SB"+str(sb)+".contcube.fits" #"image.restored.u.SB4612.contcube.fits"
in_v= path+"image.restored.v."+base+".SB"+str(sb)+".contcube.fits" #"image.restored.u.SB4612.contcube.fits"

taylor0=path+"image.i."+base+".SB"+str(sb)+".cont.taylor.0.restored.fits" #"image.i.SN1006.SB7216.cont.taylor.0.restored.fits"
taylor1=path+"image.i."+base+".SB"+str(sb)+".cont.taylor.1.restored.fits" #"image.i.SN1006.SB7216.cont.taylor.1.restored.fits"
selavy=path+"selavy-cont-image.i."+base+".SB"+str(sb)+".cont.taylor.0.restored/selavy-image.i."+base+".SB"+str(sb)+".cont.taylor.0.restored.txt"
footfile=path+"metadata/footprintOutput-sb"+str(sb)+"-"+base+".txt" #'../newfootprint.dat'


#distance limits
min_dist=0
max_dist=5

#read selavy input
headerrows=47
#fluxmin=0.1
#fluxmax=10
df = pd.read_fwf(selavy, skiprows=headerrows,  header=None)
df.columns = ["ObjID", "Name", "X", "Y","Z", "RA", "DEC", "RA [deg]", "DEC [deg]", "FREQ [Hz]","MAJ [arcsec]","MIN [arcsec]", "PA [deg]", "w_RA [arcmin]", "w_DEC [arcmin]", "w_50 [Hz]","w_20 [Hz]", "w_FREQ [Hz]", "F_int [Jy]", "F_tot [Jy/beam]", "F_peak [Jy/beam]", "X1", "X2","Y1","Y2", "Z1", "Z2", "Nvoxel", "Nchan", "Nspatpix", "Flag", "X_av", "Y_av", "Z_av", "X_cent", "Y_cent", "Z_cent", "X_peak", "Y_peak", "Z_peak"]
df.sort_values(by=["F_peak [Jy/beam]"])
names= df.loc[(df["F_peak [Jy/beam]"] > fluxmin) & (df["F_peak [Jy/beam]"] < fluxmax)]["Name"].values
cut_ra = df.loc[(df["F_peak [Jy/beam]"] > fluxmin) & (df["F_peak [Jy/beam]"] < fluxmax)]["RA [deg]"].values
cut_dec = df.loc[(df["F_peak [Jy/beam]"] > fluxmin) & (df["F_peak [Jy/beam]"] < fluxmax)]["DEC [deg]"].values
numsources = len(cut_ra)
print("Computing statistics for "+str(numsources)+" source(s).")
#get header and data
f = in_i
head=pf.getheader(f)
w = WCS(f)
t0=pf.getdata(taylor0)[:,0,:,:]
t1=pf.getdata(taylor1)[:,0,:,:]

#get frequencies
if head['ctype3']=='FREQ': freqAx=3
elif head['ctype4']=='FREQ': freqAx=4

nFreq = head["NAXIS"+str(freqAx)]
cdelt = head['cdelt'+str(freqAx)]
crpix = head['crpix'+str(freqAx)]
crval = head['crval'+str(freqAx)]
freq = np.arange(nFreq, dtype = np.float32)
for j in range(nFreq):
    freq[j] = (j + 1 - crpix) * cdelt + crval

#get coords of the mosaic centre
cx=int(head['naxis1']/2)
cy=int(head['naxis2']/2)
centre_coord = wcs.pixel_to_skycoord(cx, cy, w)

#get distaces from beam and mosaic centres
centers1=read_centers(footfile)
coords1=hms2skycoord(centers1)
points1=getpoints(cut_ra,cut_dec)
distances=dists(coords1,points1)
beam_dist,beam_num=mindists(distances)
mosdistances = mosdistance(centre_coord.ra.deg, centre_coord.dec.deg, cut_ra, cut_dec)

#get source statistics

#data=pf.getdata(in_i)[:,0,:,:]
i_vals, i_freqs, i_medians, i_sixteenth, i_eightyforth, i_stdevs, i_skews, i_kurtosi, i_dists, i_bdists, i_bnum, i_sourceras, i_sourcedecs = getSourceStats(in_i, cut_ra, cut_dec, w, mosdistances, beam_dist, beam_num, freq)
#data=pf.getdata(in_v)[:,0,:,:]
v_vals, v_freqs, v_medians, v_sixteenth, v_eightyforth, v_stdevs, v_skews, v_kurtosi, v_dists, v_bdists, v_bnum, v_sourceras, v_sourcedecs = getSourceStats(in_v, cut_ra, cut_dec, w, mosdistances, beam_dist, beam_num, freq)
#data=pf.getdata(in_q)[:,0,:,:]
q_vals, q_freqs, q_medians, q_sixteenth, q_eightyforth, q_stdevs, q_skews, q_kurtosi, q_dists, q_bdists, q_bnum, q_sourceras, q_sourcedecs = getSourceStats(in_q, cut_ra, cut_dec, w, mosdistances, beam_dist, beam_num, freq)
#data=pf.getdata(in_u)[:,0,:,:]
u_vals, u_freqs, u_medians, u_sixteenth, u_eightyforth, u_stdevs, u_skews, u_kurtosi, u_dists, u_bdists, u_bnum, u_sourceras, u_sourcedecs = getSourceStats(in_u, cut_ra, cut_dec, w, mosdistances, beam_dist, beam_num, freq)

#cut values that are not within the distance limits
dist_mask=np.zeros(len(v_dists))
dist_mask[np.logical_and(np.array(v_dists)>min_dist, v_dists<max_dist)]=1
aa=np.argwhere(dist_mask==1)[:,0]
v_vals_cut= [v_vals[i] for i in aa]
i_vals_cut= [i_vals[i] for i in aa]
q_vals_cut= [q_vals[i] for i in aa]
u_vals_cut= [u_vals[i] for i in aa]


numSources=len(i_sourceras)
w0 = WCS(taylor0)
c0 = SkyCoord(cut_ra, cut_dec, frame='fk5',unit='deg')
x0, y0 = wcs.skycoord_to_pixel(c0,w0)
X0=np.rint(x0)
Y0=np.rint(y0)

t0_val=t0[:,np.int_(Y0),np.int_(X0)]
t1_val=t1[:,np.int_(Y0),np.int_(X0)]/t0_val

imsize=20

#plot spectrum for every source
for source in range(0, numSources):
    print("Making plot for "+str(names[source])+" ("+str(source+1)+" of "+ str(numSources) +")")
    makePIImage(path, sb, in_q, in_u, i_sourceras[source], i_sourcedecs[source], names[source], imsize)
    makeSourcePlot(i_vals_cut[source], q_vals_cut[source], u_vals_cut[source], v_vals_cut[source], t0, t0_val[0][source], t1_val[0][source], i_freqs[source], q_freqs[source], u_freqs[source], v_freqs[source], i_sourceras[source], i_sourcedecs[source], w0, path, sb, names[source])



i_vals_cat = np.concatenate(np.array(i_vals_cut))
v_vals_cat = np.concatenate(np.array(v_vals_cut))
q_vals_cat = np.concatenate(np.array(q_vals_cut))
u_vals_cat = np.concatenate(np.array(u_vals_cut))
title = str(numsources)+" sources from "+str(fluxmin)+" to "+str(fluxmax)+" Jy"
ihiststats=makeHistogram(i_vals_cat, "I", title, min_dist, max_dist, path)
vhiststats=makeHistogram(v_vals_cat, "V", title, min_dist, max_dist, path)
qhiststats=makeHistogram(q_vals_cat, "Q", title, min_dist, max_dist, path)
uhiststats=makeHistogram(u_vals_cat, "U", title, min_dist, max_dist, path)

#Stokes V as a function of distance from the mosaic centre
fig, ax = plt.subplots()
plt.fill_between(v_dists[np.argsort(v_dists)], v_sixteenth[np.argsort(v_dists)], v_eightyforth[np.argsort(v_dists)], alpha=0.5)
lm=plt.plot(v_dists[np.argsort(v_dists)],v_medians[np.argsort(v_dists)])
lsd=plt.plot(v_dists[np.argsort(v_dists)],v_stdevs[np.argsort(v_dists)], '-')
plt.ylim(-vhiststats[4], vhiststats[4])
plt.ylabel("Stokes V")
plt.xlabel("Distance from mosaic centre (degrees)")
plt.title("Sources from "+str(fluxmin)+" to "+str(fluxmax)+" Jy")
plt.figlegend( (lm, lsd),('median', 'stdev'),'upper right' )
fig.savefig(path+"/plots/stokesV_vs_dist_from_mosaic_centre.png",bbox_inches='tight')
plt.clf()
plt.cla()
plt.close(fig)

#Stokes V as a function of distance from the beam centre
fig, ax = plt.subplots()
plt.fill_between(v_bdists[np.argsort(v_bdists)], v_sixteenth[np.argsort(v_bdists)], v_eightyforth[np.argsort(v_bdists)], alpha=0.5)
lm=plt.plot(v_bdists[np.argsort(v_bdists)],v_medians[np.argsort(v_bdists)])
lsd=plt.plot(v_bdists[np.argsort(v_bdists)],v_stdevs[np.argsort(v_bdists)], '-')
plt.ylim(-vhiststats[4], vhiststats[4])
plt.ylabel("Stokes V")
plt.xlabel("Distance from beam centre (degrees)")
plt.title("Sources from "+str(fluxmin)+" to "+str(fluxmax)+" Jy")
plt.figlegend( (lm, lsd),('median', 'stdev'),'upper right' )
fig.savefig(path+"/plots/stokesV_vs_dist_from_beam_centre.png",bbox_inches='tight')
plt.clf()
plt.cla()
plt.close(fig)
