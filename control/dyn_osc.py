#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 20:44:09 2021

@author: virati
The Dynamic Oscillation submodule
"""
from DBSpace import nestdict
import DBSpace as dbo

import scipy
import scipy.io as sio
import scipy.signal as sig
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from numpy.random import default_rng
import pyvista as pv

import mne
import pdb
import h5py

import pysindy as ps

from DBSpace.visualizations import EEG_Viz as EEG_Viz



Ephys = nestdict()
Phase = 'TurnOn'
if Phase == 'TurnOn':
    Ephys['901']['OnTarget']['Filename'] = '/home/virati/MDD_Data/BR/901/Session_2014_05_16_Friday/DBS901_2014_05_16_17_10_31__MR_0.txt'
    Ephys['901']['OffTarget']['Filename'] = '/home/virati/MDD_Data/BR/901/Session_2014_05_16_Friday/DBS901_2014_05_16_16_25_07__MR_0.txt'
    Ephys['901']['OnTarget']['segments']['Bilat'] = (600,630)
    Ephys['901']['OnTarget']['segments']['PreBilat'] = (500,530)
    Ephys['901']['OffTarget']['segments']['Bilat'] = (600,630)
    Ephys['901']['OffTarget']['segments']['PreBilat'] = (480,510)
    
    Ephys['903']['OnTarget']['Filename'] = '/home/virati/MDD_Data/BR/903/Session_2014_09_03_Wednesday/DBS903_2014_09_03_14_16_57__MR_0.txt'
    Ephys['903']['OffTarget']['Filename'] = '/home/virati/MDD_Data/BR/903/Session_2014_09_04_Thursday/DBS903_2014_09_04_12_53_09__MR_0.txt' 
    Ephys['903']['OnTarget']['segments']['Bilat'] = (550,580)
    Ephys['903']['OffTarget']['segments']['Bilat'] = (550,580)
    Ephys['903']['OnTarget']['segments']['PreBilat'] = (501,531)
    Ephys['903']['OffTarget']['segments']['PreBilat'] = (501,531)
    
    Ephys['905']['OnTarget']['Filename'] = '/home/virati/MDD_Data/BR/905/Session_2015_09_28_Monday/Dbs905_2015_09_28_13_51_42__MR_0.txt' 
    Ephys['905']['OffTarget']['Filename'] = '/home/virati/MDD_Data/BR/905/Session_2015_09_29_Tuesday/Dbs905_2015_09_29_12_32_47__MR_0.txt' 
    Ephys['905']['OnTarget']['segments']['Bilat'] = (610,640)
    Ephys['905']['OffTarget']['segments']['Bilat'] = (610,640)
    Ephys['905']['OnTarget']['segments']['PreBilat'] = (561,591)
    Ephys['905']['OffTarget']['segments']['PreBilat'] = (561,591)
    
    
    Ephys['906']['OnTarget']['Filename'] = '/home/virati/MDD_Data/BR/906/Session_2015_08_27_Thursday/DBS906_2015_08_27_15_10_44__MR_0.txt'
    Ephys['906']['OffTarget']['Filename'] = '/home/virati/MDD_Data/BR/906/Session_2015_08_27_Thursday/DBS906_2015_08_27_16_20_23__MR_0.txt'
    Ephys['906']['OnTarget']['segments']['Bilat'] = (610,640)
    Ephys['906']['OffTarget']['segments']['Bilat'] = (610,640)
    Ephys['906']['OnTarget']['segments']['PreBilat'] = (561,591)
    Ephys['906']['OffTarget']['segments']['PreBilat'] = (561,591)
    
    #for R stim
    Ephys['906']['OffTarget']['segments']['C1'] = (368,389)
    Ephys['906']['OffTarget']['segments']['C2'] = (389,422)
    Ephys['906']['OffTarget']['segments']['C3'] = (422,475)
    Ephys['906']['OffTarget']['segments']['C4'] = (475,486)
    Ephys['906']['OffTarget']['segments']['C5'] = (488,530)

    #for bilat
    Ephys['906']['OffTarget']['segments']['C1'] = (603,615)
    Ephys['906']['OffTarget']['segments']['C2'] = (615,620)
    Ephys['906']['OffTarget']['segments']['C3'] = (620,627)
    Ephys['906']['OffTarget']['segments']['C4'] = (627,635)
    Ephys['906']['OffTarget']['segments']['C5'] = (635,675)    
    
    Ephys['907']['OnTarget']['Filename'] = '/home/virati/MDD_Data/BR/907/Session_2015_12_16_Wednesday/DBS907_2015_12_16_12_09_04__MR_0.txt'
    Ephys['907']['OffTarget']['Filename'] = '/home/virati/MDD_Data/BR/907/Session_2015_12_17_Thursday/DBS907_2015_12_17_10_53_08__MR_0.txt' 
    Ephys['907']['OnTarget']['segments']['Bilat'] = (640,670)
    Ephys['907']['OffTarget']['segments']['Bilat'] = (625,655)
    Ephys['907']['OnTarget']['segments']['PreBilat'] = (590,620)
    Ephys['907']['OffTarget']['segments']['PreBilat'] = (560,590)
    
    Ephys['908']['OnTarget']['Filename'] = '/home/virati/MDD_Data/BR/908/Session_2016_02_10_Wednesday/DBS908_2016_02_10_13_03_10__MR_0.txt'
    Ephys['908']['OffTarget']['Filename'] = '/home/virati/MDD_Data/BR/908/Session_2016_02_11_Thursday/DBS908_2016_02_11_12_34_21__MR_0.txt'
    Ephys['908']['OnTarget']['segments']['Bilat'] = (611,641)
    Ephys['908']['OffTarget']['segments']['Bilat'] = (611,641)
    Ephys['908']['OnTarget']['segments']['PreBilat'] = (551,581)
    Ephys['908']['OffTarget']['segments']['PreBilat'] = (551,581)
elif Phase == '6Mo':
            #901
    Ephys['901']['OnTarget']['Filename'] = '/run/media/virati/Samsung USB/MDD_Data/BR/901/Session_2014_11_14_Friday/DBS901_2014_11_14_16_46_35__MR_0.txt'
    Ephys['901']['OffTarget']['Filename'] = '/run/media/virati/Samsung USB/MDD_Data/BR/901/Session_2014_11_14_Friday/DBS901_2014_11_14_17_34_35__MR_0.txt'
    Ephys['901']['OnTarget']['segments']['Bilat'] = (670,700)
    Ephys['901']['OnTarget']['segments']['PreBilat'] = (620,650)
    
    Ephys['901']['OffTarget']['segments']['Bilat'] = ()
    Ephys['901']['OffTarget']['segments']['PreBilat'] = ()
    
            #903
    Ephys['903']['OnTarget']['Filename'] = ''
    Ephys['903']['OffTarget']['Filename'] = ''
    
    Ephys['903']['OnTarget']['segments']['PreBilat'] = ()
    Ephys['903']['OnTarget']['segments']['Bilat'] = ()
    Ephys['903']['OffTarget']['segments']['PreBilat'] = ()
    Ephys['903']['OffTarget']['segments']['Bilat'] = ()
    
            #905
    Ephys['905']['OnTarget']['Filename'] = ''
    Ephys['905']['OffTarget']['Filename'] = ''
    Ephys['905']['OnTarget']['segments']['PreBilat'] = ()
    Ephys['905']['OnTarget']['segments']['Bilat'] = ()
    Ephys['905']['OffTarget']['segments']['PreBilat'] = ()
    Ephys['905']['OffTarget']['segments']['Bilat'] = ()
    
            #906
    Ephys['906']['OnTarget']['Filename'] = ''
    Ephys['906']['OffTarget']['Filename'] = ''
    Ephys['906']['OnTarget']['segments']['Bilat'] = (610,640)
    Ephys['906']['OffTarget']['segments']['Bilat'] = (610,640)
    Ephys['906']['OnTarget']['segments']['PreBilat'] = (561,591)
    Ephys['906']['OffTarget']['segments']['PreBilat'] = (561,591)
    
            #907
    Ephys['907']['OnTarget']['Filename'] = ''
    Ephys['907']['OffTarget']['Filename'] = ''
    Ephys['907']['OnTarget']['segments']['Bilat'] = (640,670)
    Ephys['907']['OffTarget']['segments']['Bilat'] = (625,655)
    Ephys['907']['OnTarget']['segments']['PreBilat'] = (590,620)
    Ephys['907']['OffTarget']['segments']['PreBilat'] = (560,590)
    
            #908
    Ephys['908']['OnTarget']['Filename'] = ''
    Ephys['908']['OffTarget']['Filename'] = ''
    Ephys['908']['OnTarget']['segments']['Bilat'] = (611,641)
    Ephys['908']['OffTarget']['segments']['Bilat'] = (611,641)
    Ephys['908']['OnTarget']['segments']['PreBilat'] = (551,581)
    Ephys['908']['OffTarget']['segments']['PreBilat'] = (551,581)
    



def load_raw_mat(fname):
    signal = sio.loadmat(fname)
    
    return signal['EXPORT']['chann'][0][0]

def extract_raw_mat(fname=[]):
    if fname == []:
        pt_dir = 'DBS906/'
        file = 'DBS906_TurnOn_Day1_Sess1_20150827_024013.mat'
        
        data_dir = '/home/virati/B04/'
        Inp = sio.loadmat(data_dir + pt_dir + file)
    else:
        Inp = sio.loadmat(fname)
        

    #Find the key corresponding to the data
    data_key = [key for key in Inp.keys() if key[0:3] == 'DBS']
    
    #Spectrogram of the first channel to see
    chann = 32
    #sg_sig = sig.decimate(Inp[data_key[0]][chann,:],q=10)
    sg_sig = Inp[data_key[0]][chann,:]
    
    #do filtering here
    sos_lpf = sig.butter(10,20,fs=1000,output='sos')
    fsg_sig = sig.sosfilt(sos_lpf,sg_sig)
    
    
    T,F,SG = sig.spectrogram(sg_sig,nfft=2**10,window='blackmanharris',nperseg=1024,noverlap=500,fs=1000)
    fig,ax1 = plt.subplots()
    ax1.pcolormesh(F,T,10*np.log10(SG))
    
    ax2 = ax1.twinx()
    ax2.plot(np.linspace(0,fsg_sig.shape[0]/1000,fsg_sig.shape[0]),fsg_sig)
    
    #Data matrix generation
    Data_matr = Inp[data_key[0]]

    #Spectrogram of the first channel to see
    
    t_bounds = {'Pre_STIM':(760,780), 'BL_STIM':(790,810)}
    t_vect = np.linspace(0,Data_matr.shape[1]/1000,Data_matr.shape[1])
    
    
    signal = defaultdict(dict)
    for ts, tt in t_bounds.items():
        t_loc = np.where(np.logical_and(t_vect > tt[0],t_vect < tt[1]))[0]
        signal[ts] = Inp[data_key[0]][:,t_loc] - np.mean(Inp[data_key[0]][:,t_loc],0)
    
    #Save DataStructure
    sio.savemat('/tmp/test',signal)
    

class EEG_DO:
    #data_dir = '/run/media/virati/Stokes/MDD_Data/hdEEG/Continuous/CHIRPS/'
    data_dir = '/home/virati/MDD_Data/hdEEG/Continuous/CHIRPS/'
    fs = 500
    ds_fact = 4
    def __init__(self,pt='DBS906',condit='OnTarget'):
        self.pt = pt
        self.condit = condit
        
        file = self.data_dir + pt + '_Sample_Chirp_template/' + pt + '_' + condit + '_all.mat'
        signal = load_raw_mat(fname=file)
            
        def EEG_to_Matr(signal):
            data = []
            
            for ch in range(257):
                data.append(signal[:,ch][0][0][0][0][0])
            data = np.array(data)
            
            return data

        self.data = sig.detrend(EEG_to_Matr(signal),type='constant')
        
        # get our LFP here
        if pt == 'DBS906':
            lfp_segment = np.arange(256000,330200)
            pt_side = 'Left'
            self.lfp_template = dbo.load_BR_dict(Ephys[pt[-3:]][condit]['Filename'],sec_offset=0)
            self.chirp_template = self.lfp_template[pt_side][lfp_segment]
            
    
    def calc_psd_stack(self,interval=(0,-1)):
        Pxx = [None] * 257
        sigs = self.import_channels(range(257))
        
        for cc in range(257):
            f,Pxx[cc] = sig.welch(sigs[cc,interval[0]:interval[1]],fs=self.fs/self.ds_fact,window='blackmanharris',nperseg=256,noverlap=0,nfft=2**10)
        
        self.f_vect = f
        return np.array(Pxx)
    
    def map_blips(self,interval=(7000,25000),thresh=1,render=False):   
        all_psd = self.calc_psd_stack(interval=interval)
        frange = np.logical_and(self.f_vect > 2,self.f_vect < 10)
        mask = np.sum(all_psd[:,frange],axis=1)
        print('Mean EEG blip power ' + str(np.mean(mask)))
        plt.figure();plt.hist(mask,range=(0,100),bins=50);print(mask);plt.vlines(thresh,0,100)
        if render:
            EEG_Viz.maya_band_display(mask > thresh)
        EEG_Viz.plot_3d_scalp(mask>thresh,unwrap=True)
        
        self.mask = mask
        
    def map_templates(self,interval=(7000,25000),thresh=1,render=False):
        # Get our data prepared first
        # EEG data here
        
        # LFP template here
        
        
        frange = np.logical_and(self.f_vect > 2,self.f_vect < 10)
        mask = np.sum(all_psd[:,frange],axis=1)
        print('Mean EEG blip power ' + str(np.mean(mask)))
        plt.figure();plt.hist(mask,range=(0,100),bins=50);print(mask);plt.vlines(thresh,0,100)
        if render:
            EEG_Viz.maya_band_display(mask > thresh)
        EEG_Viz.plot_3d_scalp(mask>thresh,unwrap=True)
        
        self.mask = mask
        
    def import_channels(self,chs):
        display_sigs = [None] * len(chs)
        for ii in range(len(chs)):
            display_sigs[ii] = sig.decimate(self.data[chs[ii]][:],self.ds_fact,zero_phase=True)
        
        sigs = np.array(display_sigs)
        
        return sigs
    
    def sgs(self,chs=[32,255]):
        #two-channel display
        sigs = self.import_channels(chs)
        fig = plt.figure()
        plt.subplot(211)
        plt.plot(sigs.T)
        
        for ii in range(len(chs)):
            plt.subplot(2,len(chs),len(chs)+ii+1)
            F,T,SG = sig.spectrogram(sigs[ii,:],nperseg=256,noverlap=200,window=sig.get_window('blackmanharris',256),fs=self.fs/self.ds_fact,nfft=512)
            #plt.plot(sigs[ii,:])
            plt.pcolormesh(T,F,10*np.log10(SG),rasterized=True)
        
        return fig
    
    def regimePlot(self,**kwargs):
        fig_handle = self.sgs(**kwargs)
        regimes = self.regimes
        for rr in range(len(regimes) -1):
            rect = patches.Rectangle((regimes[rr],1),regimes[rr+1]-regimes[rr],1,linewidth=1,edgecolor='r')
            fig_handle.add_patch(rect)
            
    def multiphase(self,chs=[32,255,256],interval=(9000,9800),plot=False):
        if len(chs) > 3:
            raise Exception()
        
        raw_sigs = self.import_channels(chs)[:,interval[0]:interval[1]]
        
        ## Filter here
        sos_lpf = sig.butter(15,10,output='sos',fs = self.fs/self.ds_fact)
        sigs = np.array([sig.sosfilt(sos_lpf,raw_sigs[ii,:]) for ii in range(3)])
        
        model = ps.SINDy()
        model.fit(sigs.T,t=1/self.fs)
        model.print()
        t_test = np.arange(0,50,1/self.fs)
        sim = model.simulate(sigs[:,0],t_test)
        
        if plot:
            plt.figure()
            point_cloud = pv.PolyData(sigs.T)
            point_cloud.plot(eye_dome_lighting=True)
            
    def phase(self,chs=[32,255],interval=(9000,9800),plot=False):
        if len(chs) > 2:
            raise Exception()
            
        raw_sigs = self.import_channels(chs)[:,interval[0]:interval[1]]
        
        ## Filter here
        sos_lpf = sig.butter(15,10,output='sos',fs = self.fs/self.ds_fact)
        sigs = np.array([sig.sosfilt(sos_lpf,raw_sigs[ii,:]) for ii in range(2)])
        
        model = ps.SINDy()
        model.fit(sigs.T,t=1/self.fs)
        model.print()
        t_test = np.arange(0,50,1/self.fs)
        sim = model.simulate(sigs[:,0],t_test)
        
        if plot:
            plt.figure()
            plt.subplot(121)
            plt.plot(sigs[0,:]);plt.plot(sigs[1,:])
            plt.subplot(122)
            plt.scatter(sigs[0,:],sigs[1,:],c=np.arange(0,sigs.shape[1]))
            plt.plot(sigs[0,:],sigs[1,:],alpha=0.2)
            plt.plot(sim[:,0],sim[:,1],linewidth=2,color='black',alpha=0.5)
            for ii in range(sim[:,0].shape[0])[::200]:
                plt.arrow(sim[ii,0],sim[ii,1],sim[ii+1,0]-sim[ii,0],sim[ii+1,1]-sim[ii,1],shape='left',lw=0,length_includes_head=True,head_width=0.2,color='black')
            plt.scatter(sim[0,0],sim[0,1],s=500,color='red')
            plt.xlim((-50,50))
            plt.ylim((-50,50))
        