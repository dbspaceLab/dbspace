#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 17:32:26 2020

@author: virati
DBStim Classes
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

def idxer(x,c):
    return np.argmin(np.abs(x-c))

class harmonic_map:
    def __init__(self):
        self.w = np.linspace(-1000,1000,10000)
        #self.s = np.zeros_like(w)
        
    def setup_sigs(self):
        w = self.w
        
        s[idxer(w,130)] = 1
        #s[idxer(w,-130)] = 1
        s[idxer(w,105.5)] = 0.5
        s[idxer(w,-105.5)] = 0.5
        s[idxer(w,260)] = 1
        s[idxer(w,-260)] = 1
        #s[idxer(w,190)] = 1
        #s[idxer(w,202)] = 1
        #s[idxer(w,-190)] = 1
        #s[idxer(w,-202)] = 1
        
        for ii in [1,3,5,7,9]:
            s[idxer(w,130*ii)] = 1
            s[idxer(w,-130*ii)] = 1

        self.s = s

    def setup_samps(self):
        
        p = np.zeros_like(w)
        p[idxer(w,0)] = 1
        p[idxer(w,422)] = 1
        p[idxer(w,844)] = 1
        p[idxer(w,-422)] = 1
        p[idxer(w,-844)] = 1
        
        self.p = p
        
    def run_convolve(self):        
        #convolve
        res = sig.convolve(s,p,mode='same')
        w_ext = np.linspace(-1000,1000,10000)
        
        return w_ext,res
    
    def plot_harmonics(self):
        
        w_ext,res = self.run_convolve()
            
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(w,s)
        plt.plot(w,p)
        plt.subplot(2,1,2)
        plt.plot(w_ext,res)
        #plt.xlim((0,200))
