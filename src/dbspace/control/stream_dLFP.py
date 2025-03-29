import dbspace as dbo
from dbspace import nestdict
from dbspace.control import Targeting
import numpy as np


class streamLFP:
    def __init__(self, pt="908", condit="OnT", ds_fact=1, spotcheck=False):
        self.donfft = 2**10

        self.pt = pt
        self.condit = condit

        container = dbo.load_BR_dict(Targeting["All"][pt][condit]["lfp"], sec_offset=0)
        fs = 422

        rec_length = container["Left"].shape

        self.tvect = np.linspace(0, rec_length[0] * 1 / fs, rec_length[0])
        self.data_dict = container
        self.Fs = fs
        self.gen_epochs()

    def gen_epochs(self):
        print("Generating Epochs...")
        # Go in and generate the epochs associated with this recording
        self.epochs = Targeting["All"][self.pt][self.condit]["epochs"]
        self.epochs["ALL"] = (0, -1)

    """
    This should return the timeseries associated with a particular segment
    """

    def time_series(self, epoch_name="All", full_stim=False):
        # Find the indices we need
        # Do adjustments here if you want LARGER or SMALLER epochs
        if full_stim:
            rec_idxs = np.where(
                np.logical_and(
                    self.tvect < self.epochs[epoch_name][1] + 140,
                    self.tvect > self.epochs[epoch_name][0] - 5,
                )
            )
        else:
            rec_idxs = np.where(
                np.logical_and(
                    self.tvect < self.epochs[epoch_name][1],
                    self.tvect > self.epochs[epoch_name][0],
                )
            )

        return {key: self.data_dict[key][rec_idxs] for key in self.data_dict}

    def tf_transform(self, epoch_name):
        ts_dict = self.time_series(epoch_name)

        SG = dbo.gen_SG(ts_dict, Fs=422, overlap=False)

        return SG

    """
    Plots and transforms below
    """

    def osc_plot(self, epoch_name="All"):
        Osc_state = self.osc_transform(epoch_name)

    def osc_transform(self, epoch_name):
        # psds = dbo.gen_psd()
        firstpsds = dbo.gen_SG(
            self.time_series(epoch_name=epoch_name),
            Fs=self.Fs,
            nfft=self.donfft,
            overlap=False,
        )
        fvect = np.linspace(0, self.Fs / 2, firstpsds["Left"]["F"].shape[0])
        psds = {chann: firstpsds[chann]["SG"] for chann in firstpsds.keys()}

        out_vect = nestdict()
        # need to manually go into segments
        for seg in range(psds["Left"].shape[1]):
            try:
                calcpsds = {chann: psds[chann][:, seg] for chann in ["Left", "Right"]}
            except:
                pdb.set_trace()
            out_vect[seg] = dbo.calc_feats(
                calcpsds,
                fvect,
                dofeats=["Delta", "Theta", "Alpha", "Beta*", "Gamma1"],
                modality="lfp",
            )
        try:
            ret_vect = {
                chann: np.array(
                    [out_vect[seg][0][:, cc] for seg in range(psds[chann].shape[1])]
                )
                for cc, chann in enumerate(["Left", "Right"])
            }
        except:
            pdb.set_trace()
        return ret_vect

    def plot_tf(self, epoch_name="All"):
        TF_dict = self.tf_transform(epoch_name)

        dbo.plot_TF(TF_dict)

    def plot_f(self, epoch_name="All"):
        TF_dict = self.tf_transform(epoch_name)

        dbo.plot_F_fromTF(TF_dict)
