import mne
import numpy as np


def get_eeg_positions(sfp_file=None):
    if sfp_file is None:
        sfp_file = "/home/virati/Dropbox/GSN-HydroCel-257.sfp"
    egipos = mne.channels.read_custom_montage(sfp_file).get_positions()["ch_pos"]
    etrodes = np.array([egipos[channel] for channel in egipos.keys()])

    return etrodes
