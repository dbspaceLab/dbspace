#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 11:37:00 2018

@author: virati
Main file to co-register the TVB coordinates and the tractography information
"""

import pickle
import numpy as np
import dbspace.control.DTI as DTI
import dbspace as dbo
from dbspace.utils.structures import nestdict
import nilearn
from nilearn import plotting, image, datasets
import json

import scipy.signal as sig

niimg = datasets.load_mni152_template()

from dbspace.viz.MM import EEG_Viz


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import mayavi.mlab as mlab
from mayavi.mlab import *

import pdb

#%%


class head_model:
    def __init__(self):
        self.electrode_map = DTI.Etrode_map
        self.parcel_coords = []
        self.dti_coords = []
        self.eeg_coords = []

    def import_parcellation(self):
        self.parcel_coords = 0.8 * np.load("/home/virati/Dropbox/TVB_192_coord.npy")

    def import_dti(self):
        data = nestdict()
        dti_file = nestdict()
        for ss, side in enumerate(["L", "R"]):
            cntct = self.electrode_map[condit][pt][ss] + 1
            dti_file[side] = (
                "/home/virati/Dropbox/projects/Research/MDD-DBS/Data/Anatomy/DTI/MDT_DBS_2_7V_Tractography/DBS"
                + str(pt)
                + "."
                + side
                + str(cntct)
                + "."
                + str(voltage)
                + "V.bin.nii.gz"
            )

            data[side] = image.smooth_img(dti_file[side], fwhm=1)

        # Combine the images
        combined = image.math_img("img1+img2", img1=data["L"], img2=data["R"])
        # plotting.plot_glass_brain(combined,black_bg=True,title=pt + ' ' + condit)

        #%% DTI STUFF
        # manual, numpy way
        voxels = np.array(combined.dataobj)
        vox_loc = np.array(np.where(voxels > 0)).T

        mni_vox = []
        for vv in vox_loc:
            mni_vox.append(
                np.array(image.coord_transform(vv[0], vv[1], vv[2], niimg.affine))
            )

        mni_vox = sig.detrend(np.array(mni_vox), axis=0, type="constant")

        #%% CALCULATE TRACT->PARCEL
        # now that we're coregistered, we go to each parcellation and find the minimum distance from it to the tractography

        vox_loc = mni_vox / 3

        display_vox_loc = (
            vox_loc[np.random.randint(vox_loc.shape[0], size=(1000,)), :] / 3
        )
        display_vox_loc += np.random.normal(0, 1, size=display_vox_loc.shape)
        z_translate = np.zeros_like(display_vox_loc)
        z_translate[:, 2] = 1
        y_translate = np.zeros_like(display_vox_loc)
        y_translate[:, 1] = 1
        tract_offset = 15
        self.dti_coords += brain_offset * z_translate + tract_offset * y_translate

    def import_coords(self):
        pass

    def primary_nodes(self):
        pass

    def secondary_nodes(self):
        pass

    def viz_head(self):

        mlab.figure(bgcolor=(1.0, 1.0, 1.0))
        ## NEED TO PRETTY THIS UP with plot_3d_scalp updates that give much prettier OnT/OffT pictures
        # First, we plot the tracts from the DTI
        EEG_Viz.plot_tracts(
            self.dti_coords,
            active_mask=[True] * self.dti_coords.shape[0],
            color=(1.0, 0.0, 0.0),
        )
        EEG_Viz.plot_coords(
            self.dti_coords,
            active_mask=[True] * self.dti_coords.shape[0],
            color=(1.0, 0.0, 0.0),
        )

        # Next, we plot the parcellation nodes from TVB
        EEG_Viz.plot_coords(
            self.parcel_coords, active_mask=prior_locs, color=(0.0, 1.0, 0.0)
        )
        EEG_Viz.plot_coords(
            self.parcel_coords, active_mask=second_locs, color=(0.0, 0.0, 1.0)
        )

        # Finally, we plot the EEG channels with their primary and secondary masks
        EEG_Viz.plot_maya_scalp(
            chann_mask, ax, color=(1.0, 0.0, 0.0), scale=10, alpha=0.5, unwrap=False
        )
        EEG_Viz.plot_maya_scalp(
            second_chann_mask,
            ax,
            color=(0.0, 0.0, 1.0),
            scale=10,
            alpha=0.3,
            unwrap=False,
        )

    def plot_mechanism(self):
        #%% Here we plot for the primary and secondary channels
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        EEG_Viz.plot_3d_scalp(second_chann_mask, ax, scale=10, alpha=0.2, unwrap=False)
        plt.title("Secondary Channels")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        EEG_Viz.plot_3d_scalp(chann_mask, ax, scale=10, alpha=0.5, unwrap=True)
        plt.title("Primary Channels")

        fig = plt.figure()
        ax = fig.add_subplot(111)
        EEG_Viz.plot_3d_scalp(second_chann_mask, ax, scale=12, alpha=0.5, unwrap=True)
        plt.title("Secondary Channels")

    def head_model_set(self):
        self.parcel_coords = 0.84 * np.load("/home/virati/Dropbox/TVB_192_coord.npy")
        # Load in the DTI coordinates
        self.brain_offset = 25
        self.tract_offset = -50  # this gives us forward/backward offset?
        self.dti_scale_factor = 0.35

    def build_model(pt, voltage, dti_parcel_thresh=70, eeg_thresh=70, condit="OnT"):
        Etrode_map = DTI.Etrode_map

        self.import_dti()

        dist_to_closest_tract = [None] * parcel_coords.shape[0]
        for ii in range(parcel_coords.shape[0]):
            tract_dist = []
            for jj in range(display_vox_loc.shape[0]):
                tract_dist.append(
                    np.linalg.norm(parcel_coords[ii, :] - display_vox_loc[jj, :])
                )

            dist_to_closest_tract[ii] = np.min(np.array(tract_dist))

        dist_to_closest_tract = np.array(dist_to_closest_tract)

        #%% Threshold tract -> parcellations
        # This is our FIRST threshold

        # plt.hist(dist_to_closest_tract)
        prior_locs = dist_to_closest_tract < dti_parcel_thresh
        plt.figure()
        plt.hist(dist_to_closest_tract)
        plt.title("Tract->Parcel histogram")
        #%%
        # So, above, we've just found the prior parcellations that we expect changes in
        # No we're going to find the 2nd order nodes
        first_order = prior_locs.astype(np.float)

        f_laplacian = np.load("/home/virati/Dropbox/TVB_192_conn.npy")
        second_order = np.dot(f_laplacian, first_order)
        third_order = np.dot(f_laplacian, second_order)

        def plot_first_scnd(first_order, second_order, fl):
            plt.figure()
            plt.subplot(221)
            plt.plot(first_order)
            plt.subplot(222)
            plt.plot(second_order)
            plt.subplot(2, 1, 2)
            plt.imshow(fl)

        # plot_first_scnd(first_order,second_order,f_laplacian)
        # This value is chosen semi-randomly to achieve a reasonable secondary-EEG density

        # plt.figure();plt.hist(second_order)https://schmidtsciencefellows.org/
        # plt.title('Histogram of Second Order Laplacian Magnitudes')
        second_locs = second_order > 10
        #%%
        #
        eeg_scale = 10
        EEG_coords = EEG_Viz.get_coords(scale=eeg_scale)
        # maybe scale things here..

        # Find First order EEG channels
        dist_to_closest_parcel = [None] * EEG_coords.shape[0]
        for cc in range(EEG_coords.shape[0]):
            parcel_dist = []
            for jj in parcel_coords[prior_locs]:
                parcel_dist.append(np.linalg.norm(EEG_coords[cc, :] - jj))

            dist_to_closest_parcel[cc] = np.min(np.array(parcel_dist))

        # pdb.set_trace()
        # Find second order EEG channels
        dist_to_closest_second = [None] * EEG_coords.shape[0]
        for cc in range(EEG_coords.shape[0]):
            parcel_dist = []
            for jj in parcel_coords[second_locs]:
                parcel_dist.append(np.linalg.norm(EEG_coords[cc, :] - jj))

            dist_to_closest_second[cc] = np.min(np.array(parcel_dist))

        #%%

        # This is our SECOND threshold
        prior_channs = np.array(dist_to_closest_parcel) < eeg_thresh

        # plt.figure()
        # plt.hist(dist_to_closest_parcel)

        second_channs = np.array(dist_to_closest_second) < eeg_thresh

        chann_mask = np.zeros((257,))
        chann_mask[prior_channs] = 1

        second_chann_mask = np.zeros((257,))
        second_chann_mask[second_channs] = 1

        second_chann_mask = np.logical_and(
            second_chann_mask == 1, ~(chann_mask == 1)
        ).astype(np.int)

        # pdb.set_trace()
        #%%
        # Channel mask writing

        EEG_support = {
            "primary": chann_mask,
            "secondary": second_chann_mask,
            "parcel_coords": parcel_coords,
            "prior_locs": prior_locs,
            "eeg_scale": eeg_scale,
            "second_locs": second_locs,
            "dti_scale_factor": dti_scale_factor,
            "brain_offset": brain_offset,
            "tract_offset": tract_offset,
        }
        # pickle.dump(EEG_support,open('/tmp/' + pt + '_' + condit + '_' + voltage,'wb'))
        return EEG_support

    def plot_model(self):
        mlab.figure(bgcolor=(1.0, 1.0, 1.0))

        EEG_Viz.plot_coords(
            display_vox_loc,
            active_mask=[True] * display_vox_loc.shape[0],
            color=(1.0, 0.0, 0.0),
        )  # First, we plot the tracts from the DTI

        # Next, we plot the parcellation nodes from TVB
        EEG_Viz.plot_coords(
            parcel_coords, active_mask=prior_locs, color=(0.0, 1.0, 0.0)
        )
        EEG_Viz.plot_coords(
            parcel_coords, active_mask=second_locs, color=(0.0, 0.0, 1.0)
        )

        # Finally, we plot the EEG channels with their primary and secondary masks
        EEG_Viz.plot_maya_scalp(
            chann_mask, color=(1.0, 0.0, 0.0), scale=10, alpha=0.5, unwrap=False
        )
        EEG_Viz.plot_maya_scalp(
            second_chann_mask, color=(0.0, 0.0, 1.0), scale=10, alpha=0.3, unwrap=False
        )


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def DTI_support_model(
    pt,
    voltage,
    dti_parcel_thresh=70,
    eeg_thresh=70,
    condit="OnT",
    electrode_map_file=None,
):
    if electrode_map_file is None:
        raise ValueError(
            "Need to pass in a map of electrodes used for OnTarget and OffTarget Stimulation..."
        )

    with open(electrode_map_file, "r") as electrode_map:
        Etrode_map = json.load(electrode_map)

    # Load in the coordinates for the parcellation
    parcel_coords = np.load(
        "/home/virati/Dropbox/TVB_192_coord.npy"
    )  # usually 0.84 factor
    # Load in the DTI coordinates
    brain_offset = 5  # 25 normally #higher = further up
    tract_offset = 20  # 40 normally; this gives us forward/backward offset? #higher = further forward
    # horizontal scaling for tractography
    tract_horiz = 1.4
    dti_scale_factor = 1.5  # 1 normally
    parcel_scale_factor = 0.9
    eeg_scale = 10

    data = nestdict()
    dti_file = nestdict()
    for ss, side in enumerate(["L", "R"]):
        cntct = Etrode_map[condit][pt][ss] + 1
        dti_file[side] = (
            "/home/virati/Dropbox/projects/Research/MDD-DBS/Data/Anatomy/DTI/MDT_DBS_2_7V_Tractography/DBS"
            + str(pt)
            + "."
            + side
            + str(cntct)
            + "."
            + str(voltage)
            + "V.bin.nii.gz"
        )

        data[side] = image.smooth_img(dti_file[side], fwhm=1)

    # Combine the images
    combined = image.math_img("img1+img2", img1=data["L"], img2=data["R"])
    # plotting.plot_glass_brain(combined,black_bg=True,title=pt + ' ' + condit)

    #%%
    # Move now to the DTI stuff directly
    # manual, numpy way
    voxels = np.array(combined.dataobj)
    vox_loc = np.array(np.where(voxels > 0)).T

    mni_vox = []
    for vv in vox_loc:
        mni_vox.append(
            np.array(image.coord_transform(vv[0], vv[1], vv[2], niimg.affine))
        )

    mni_vox = sig.detrend(np.array(mni_vox), axis=0, type="constant")
    vox_loc = (
        mni_vox * dti_scale_factor
    )  # This scale factor is for the tractography. We want to make sure the tracts, especially the dorsal aspect of the cingulum, makes sense wrt the location of the rest of it
    vox_loc[:, 0] = tract_horiz * vox_loc[:, 0]
    #%%
    # now that we're coregistered, we go to each parcellation and find the minimum distance from it to the tractography
    display_vox_loc = vox_loc[np.random.randint(vox_loc.shape[0], size=(1000,)), :] / 3
    display_vox_loc += np.random.normal(0, 1, size=display_vox_loc.shape)
    z_translate = np.zeros_like(display_vox_loc)
    z_translate[:, 2] = 1
    y_translate = np.zeros_like(display_vox_loc)
    y_translate[:, 1] = 1
    display_vox_loc += (
        brain_offset * z_translate + tract_offset * y_translate
    )  # DISPLAYED

    # Translate and scale parcellations
    z_translate_parcel = np.zeros_like(parcel_coords)
    z_translate_parcel[:, 2] = 1
    parcel_coords = (
        parcel_coords * parcel_scale_factor * [1, 1.5, 1]
        + brain_offset * z_translate_parcel
    )  # DISPLAYED

    #%%
    # scale both display vox and parcel coords in the vertical direction
    # display_vox_loc[:,2] = 1.4 * display_vox_loc[:,2]
    # parcel_coords[:,2] = 1.4 * parcel_coords[:,2]

    # display_vox_loc[:,1] = 1.4 * display_vox_loc[:,1]
    # parcel_coords[:,1] = 1.4 * parcel_coords[:,1]

    #%%
    # EEG Scaling stuff
    EEG_coords = EEG_Viz.get_coords(scale=eeg_scale)
    # maybe scale things here..

    #%%

    ## ALL TRANSFORMATIONS SHOULD BE ABOVE HERE
    dist_to_closest_tract = [None] * parcel_coords.shape[0]
    for ii in range(parcel_coords.shape[0]):
        tract_dist = []
        for jj in range(display_vox_loc.shape[0]):
            tract_dist.append(
                np.linalg.norm(parcel_coords[ii, :] - display_vox_loc[jj, :])
            )

        dist_to_closest_tract[ii] = np.min(np.array(tract_dist))

    # The distance from each parcel to the closest tract
    dist_to_closest_tract = np.array(dist_to_closest_tract)
    primary_locs = dist_to_closest_tract < dti_parcel_thresh

    #%%
    # VISUALIZATION SANITY CHECK PASSES!!!! SO WTF STUPID SHIT IS HAPPENING TO SCREW UP PRIMARY LOCS?
    if 0:
        EEG_Viz.plot_coords(
            display_vox_loc,
            active_mask=[True] * display_vox_loc.shape[0],
            color=(1.0, 0.0, 0.0),
            plot_overlay=False,
            alpha=0.1,
        )  # this plots the tracts
        EEG_Viz.plot_coords(
            parcel_coords,
            active_mask=[],
            color=(0.0, 0.0, 0.0),
            plot_overlay=False,
            alpha=0.8,
        )
        EEG_Viz.plot_coords(
            parcel_coords,
            active_mask=primary_locs,
            color=(0.0, 1.0, 0.0),
            plot_overlay=False,
            alpha=0.8,
        )
    #%%

    # So, above, we've just found the prior parcellations that we expect changes in
    f_laplacian = np.load("/home/virati/Dropbox/TVB_192_conn.npy")
    # No we're going to find the 2nd order nodes
    first_order = primary_locs.astype(np.float)
    second_order = np.dot(f_laplacian, first_order)
    third_order = np.dot(f_laplacian, second_order)

    second_locs = second_order > 0.5 * np.sum(first_order)  # used to be 10

    # prune out 'primary' locs from the second_locs
    # second_locs = np.logical_and(second_locs==True,primary_locs==False) #THIS IS WHERE WE CAN DO MORE ADVANCED MODELING, like checking to see if a 'primary' effect would be larger than a very convergent 'secondary' effect from multiply primary upstream regions; in which case you prioritize the brain region as a 'secondary' node and not a 'primary' node

    #%%
    # alt thresholding
    second_locs = np.logical_and(second_order > first_order, second_order > 20)
    second_normed = second_order / np.max(np.abs(second_order))

    plt.figure()
    # plt.hist(first_order,bins=20)
    plt.hist(second_normed, bins=20)
    primary_locs = np.logical_and(
        primary_locs, second_normed < 0.2
    )  # this worked for 906
    #%%
    # Find First order EEG channels
    prim_EEG_to_parcel = [None] * EEG_coords.shape[0]
    for cc in range(EEG_coords.shape[0]):
        parcel_dist = []
        for jj in parcel_coords[primary_locs]:
            parcel_dist.append(np.linalg.norm(EEG_coords[cc, :] - jj))

        prim_EEG_to_parcel[cc] = np.min(np.array(parcel_dist))

    # Find second order EEG channels
    sec_EEG_to_parcel = [None] * EEG_coords.shape[0]
    for cc in range(EEG_coords.shape[0]):
        parcel_dist = []
        for jj in parcel_coords[second_locs]:
            parcel_dist.append(np.linalg.norm(EEG_coords[cc, :] - jj))

        sec_EEG_to_parcel[cc] = np.min(np.array(parcel_dist))

    #%%

    # This is our SECOND threshold
    primary_channs = np.array(prim_EEG_to_parcel) < eeg_thresh

    # plt.figure()
    # plt.hist(dist_to_closest_parcel)

    second_channs = np.array(sec_EEG_to_parcel) < eeg_thresh

    primary_chann_mask = np.zeros((257,))
    primary_chann_mask[primary_channs] = 1

    second_chann_mask = np.zeros((257,))
    second_chann_mask[second_channs] = 1

    second_chann_mask = np.logical_and(
        second_chann_mask == 1, ~(primary_chann_mask == 1)
    ).astype(np.int)

    # pdb.set_trace()
    #%%
    # Channel mask writing
    EEG_support = {
        "primary": primary_chann_mask,
        "secondary": second_chann_mask,
        "parcel_coords": parcel_coords,
        "primary_locs": primary_locs,
        "eeg_scale": eeg_scale,
        "EEG_coords": EEG_coords,
        "second_locs": second_locs,
        "dti_scale_factor": dti_scale_factor,
        "brain_offset": brain_offset,
        "tract_offset": tract_offset,
        "display_vox_loc": display_vox_loc,
    }
    # pickle.dump(EEG_support,open('/tmp/' + pt + '_' + condit + '_' + voltage,'wb'))
    return EEG_support

    #%%
    # Do Mayavi Plotting
    # EEG_Viz.plot_maya_scalp(chann_mask,scale=10,alpha=0.5,unwrap=False)
    # EEG_Viz.plot_maya_scalp(np.ones((257,)),ax,scale=eeg_scale,animate=False)
    # EEG_Viz.plot_maya_scalp(chann_mask,ax,scale=10,alpha=0.5,unwrap=False)


#%%
# The main support model code
def plot_EEG_masks(EEG_support):

    primary_chann_mask = EEG_support["primary"]
    second_chann_mask = EEG_support["secondary"]
    #%%
    # We clugy ourselves an EEG display for the primary and secondary channels
    EEG_Viz.maya_band_display(1 * primary_chann_mask - second_chann_mask)

    #%EEG_Viz.maya_band_display(-1*second_chann_mask)


def plot_support_model(
    EEG_support,
    pt,
    voltage=3,
    condit="OnT",
    layers=[1, 1, 1],
    electrode_map_file=None,
):
    if electrode_map_file is None:
        raise ValueError(
            "Need to pass in a map of electrodes used for OnTarget and OffTarget Stimulation..."
        )

    with open(electrode_map_file, "r") as electrode_map:
        Etrode_map = json.load(electrode_map)

    # brain_offset = EEG_support['brain_offset']
    # dti_scale_factor = EEG_support['dti_scale_factor']
    # tract_offset = EEG_support['tract_offset']
    display_vox_loc = EEG_support["display_vox_loc"]
    #%%
    # Load in the coordinates for the parcellation
    parcel_coords = EEG_support["parcel_coords"]
    primary_locs = EEG_support["primary_locs"]
    second_locs = EEG_support["second_locs"]
    # eeg_scale = EEG_support['eeg_scale']
    EEG_coords = EEG_support["EEG_coords"]

    primary_chann_mask = EEG_support["primary"]
    second_chann_mask = EEG_support["secondary"]
    # EEG_Viz.plot_3d_scalp(chann_mask,ax,scale=eeg_scale,alpha=0.5,unwrap=False)

    #%% FINAL PLOTTING
    # This figure is for the
    mlab.figure(bgcolor=(1.0, 1.0, 1.0))
    ## NEED TO PRETTY THIS UP with plot_3d_scalp updates that give much prettier OnT/OffT pictures
    # First, we plot the tracts from the DTI
    # EEG_Viz.plot_tracts(display_vox_loc,active_mask=[True]*display_vox_loc.shape[0],color=(1.,0.,0.))
    if layers[0]:
        EEG_Viz.plot_coords(
            display_vox_loc,
            active_mask=[True] * display_vox_loc.shape[0],
            color=(1.0, 0.0, 0.0),
            plot_overlay=False,
            alpha=0.1,
        )  # this plots the tracts

    # Next, we plot the parcellation nodes from TVB
    if layers[1]:
        EEG_Viz.plot_coords(
            parcel_coords,
            active_mask=[],
            color=(0.0, 0.0, 0.0),
            plot_overlay=False,
            alpha=0.2,
        )

        EEG_Viz.plot_coords(
            parcel_coords,
            active_mask=primary_locs,
            color=(0.0, 1.0, 0.0),
            alpha=0.8,
            plot_overlay=False,
        )
        EEG_Viz.plot_coords(
            parcel_coords,
            active_mask=second_locs,
            color=(0.0, 0.0, 1.0),
            alpha=0.8,
            plot_overlay=False,
        )

    # Finally, we plot the EEG channels with their primary and secondary masks
    if layers[2]:
        EEG_Viz.plot_maya_scalp(
            primary_chann_mask, color=(1.0, 0.0, 0.0), scale=10, alpha=0.6, unwrap=False
        )
        EEG_Viz.plot_maya_scalp(
            second_chann_mask, color=(0.0, 0.0, 1.0), scale=10, alpha=0.6, unwrap=False
        )


if __name__ == "__main__":
    for pt in ["906"]:
        for voltage in [4]:
            supp_model = DTI_support_model(
                pt, str(voltage), dti_parcel_thresh=15, eeg_thresh=60
            )
            plot_support_model(supp_model, pt=pt)
