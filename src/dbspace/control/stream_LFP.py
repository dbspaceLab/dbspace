import numpy as np
import dbspace as dbo
from collections import defaultdict
from dbspace import nestdict

BASE_LFP_DIRECTORY = "/home/virati/Data/phd_vrt_2013/neural/lfp/"
Targeting = defaultdict(dict)

Targeting["All"] = {
    "901": {
        "OnT": {
            "fname": "/home/extend/MDD_Data/hdEEG/Continuous/ALLMATS/DBS901_E52_On_Target_20151030_015625.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "901/Session_2014_05_16_Friday/DBS901_2014_05_16_17_10_31__MR_0.txt",
            "epochs": {"Bilat": (600, 630), "PreBilat": (500, 530)},
        },
        "OffT": {
            "fname": "/home/extend/MDD_Data/hdEEG/Continuous/ALLMATS/DBS901_E52_Off_Target_20151030_022924.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "901/Session_2014_05_16_Friday/DBS901_2014_05_16_16_25_07__MR_0.txt",
            "epochs": {"Bilat": (600, 630), "PreBilat": (480, 510)},
            "Volt": {},
        },
    },
    "903": {
        "OnT": {
            "fname": "",
            "lfp": BASE_LFP_DIRECTORY
            + "903/Session_2014_09_03_Wednesday/DBS903_2014_09_03_14_16_57__MR_0.txt",
            "epochs": {"Bilat": (550, 580), "PreBilat": (501, 531)},
        },
        "OffT": {
            "fname": "",
            "lfp": BASE_LFP_DIRECTORY
            + "903/Session_2014_09_04_Thursday/DBS903_2014_09_04_12_53_09__MR_0.txt",
            "epochs": {"Bilat": (550, 580), "PreBilat": (501, 531)},
            "Volt": {},
        },
    },
    "905": {
        "OnT": {
            "fname": "/home/extend/MDD_Data/hdEEG/Continuous/ALLMATS/DBS905_TurnOn_Day1_onTARGET_20150928_015403.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "905/Session_2015_09_28_Monday/Dbs905_2015_09_28_13_51_42__MR_0.txt",
            "epochs": {"Bilat": (610, 640), "PreBilat": (561, 591)},
        },
        "OffT": {
            "fname": "/home/extend/MDD_Data/hdEEG/Continuous/ALLMATS/DBS905_TurnOn_OffTargetStims_20150929_123449.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "905/Session_2015_09_29_Tuesday/Dbs905_2015_09_29_12_32_47__MR_0.txt",
            "epochs": {"Bilat": (610, 640), "PreBilat": (561, 591)},
        },
        "Volt": {},
    },
    "906": {
        "OnT": {
            #'fname':'/home/virati/MDD_Data/hdEEG/Continuous/DS500/DBS906_TurnOn_Day1_Sess1_20150827_024013_tds.mat'
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/Targeting/B04/DBS906/DBS906_TurnOn_Day1_Sess1_20150827_024013_OnTarget.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "906/Session_2015_08_27_Thursday/DBS906_2015_08_27_15_10_44__MR_0.txt",
            "epochs": {"Bilat": (610, 640), "PreBilat": (561, 591)},
        },
        "OffT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/Targeting/B04/DBS906/DBS906_TurnOn_Day1_Sess2_20150827_041726_OffTarget.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "906/Session_2015_08_27_Thursday/DBS906_2015_08_27_16_20_23__MR_0.txt",
            "epochs": {"Bilat": (610, 640), "PreBilat": (561, 591)},
        },
        "Volt": {
            #
            #'fname':'/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS906_TurnOn_Day2_Sess3_Sess4_20150828_043231_VoltageAndFreq.mat'
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS906_TurnOn_Day2_Sess2_20150828_032515_CurrentSweep.mat",
            "lfp": "",
        },
    },
    "907": {
        "OnT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS907_TurnOn_Day1_onTARGET_20151216_105913.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "907/Session_2015_12_16_Wednesday/DBS907_2015_12_16_12_09_04__MR_0.txt",
            "epochs": {"Bilat": (640, 670), "PreBilat": (590, 620)},
        },
        "OffT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS907_TurnOn_Day2_offTARGET_20151217_094245.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "907/Session_2015_12_17_Thursday/DBS907_2015_12_17_10_53_08__MR_0.txt",
            "epochs": {"Bilat": (625, 655), "PreBilat": (560, 590)},
        },
        "Volt": {
            #'fname':'/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS907_TurnOn_Day2_Voltage_20151217_102952.mat'
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS907_TurnOn_Day3_Current_20151218_092443.mat",
            "lfp": "",
        },
    },
    "908": {
        "OnT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/Targeting/B04/DBS908/DBS908_TurnOn_Day1_onTARGET_20160210_125231.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "908/Session_2016_02_10_Wednesday/DBS908_2016_02_10_13_03_10__MR_0.txt",
            "epochs": {"Bilat": (611, 641), "PreBilat": (551, 581)},
        },
        "OffT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/Targeting/B04/DBS908/DBS908_TurnOn_Day2_offTARGET_20160211_123540.mat",
            "lfp": BASE_LFP_DIRECTORY
            + "908/Session_2016_02_11_Thursday/DBS908_2016_02_11_12_34_21__MR_0.txt",
            "epochs": {"Bilat": (611, 641), "PreBilat": (551, 581)},
        },
        "Volt": {"fname": "", "lfp": ""},
    },
    "910": {
        "OnT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS910_TurnOn_OnTarget_20180530_022545.mat",
            "lfp": "",
        },
        "OffT": {
            "fname": "/home/virati/MDD_Data/hdEEG/Continuous/ALLMATS/DBS910_TurnOn_OffTarget_TO_20180530_014051.mat",
            "lfp": "",
        },
        "Volt": {},
    },
}


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
            calcpsds = {chann: psds[chann][:, seg] for chann in ["Left", "Right"]}

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
            pass
        return ret_vect

    def plot_tf(self, epoch_name="All"):
        TF_dict = self.tf_transform(epoch_name)

        dbo.plot_TF(TF_dict)

    def plot_f(self, epoch_name="All"):
        TF_dict = self.tf_transform(epoch_name)

        dbo.plot_F_fromTF(TF_dict)
