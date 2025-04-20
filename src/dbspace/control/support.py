
def support_analysis(
        self, support_struct, pt="POOL", condit="OnT", voltage="3", band="Alpha"
    ):
        # support_struct = pickle.load(open('/tmp/'+ pt + '_' + condit + '_' + voltage,'rb'))
        if band == "rP0":
            medians = self.dyn_L.swapaxes(
                0, 1
            )  # if we want to use the 0th component of the dyn_rPCA eigenvector
            band_i = 0
        else:
            medians = self.OBSmedian_response(pt=pt)[
                "OnT"
            ]  # if we want to use the standard median Alpha change
            band_i = dbo.feat_order.index(band)

        # medians = np.median(self.targ_response[pt][condit],axis=0)
        fig = plt.figure()
        # First, we'll plot what the medians actually are

        EEG_Viz.plot_3d_scalp(
            medians[:, band_i],
            fig,
            label="OnT Mean Response " + band,
            unwrap=True,
            scale=10,
        )
        plt.suptitle(pt)

        full_distr = medians[
            :, band_i
        ]  # - np.mean(medians[:,band_i]) #this zeros the means of the distribution

        primary_distr = full_distr[support_struct["primary"] == 1]
        # now we'll circle where the primary nodes are

        print(np.sum((support_struct["primary"] == 1).astype(np.int)))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        EEG_Viz.plot_3d_scalp(
            support_struct["primary"], ax, scale=10, alpha=0.5, unwrap=True
        )
        plt.title("Primary Channels")

        secondary_distr = full_distr[support_struct["secondary"] == 1]
        print(np.sum((support_struct["secondary"] == 1).astype(np.int)))
        fig = plt.figure()
        EEG_Viz.plot_3d_scalp(
            support_struct["secondary"], fig, scale=10, alpha=0.5, unwrap=True
        )
        plt.title("Secondary Channels")

        labels = []

        def add_label(violin, label):
            color = violin["bodies"][0].get_facecolor().flatten()
            labels.append((mpatches.Patch(color=color), label))

        plt.figure()
        bins = np.linspace(-2, 2, 20)
        # plt.hist(primary_distr,bins=bins,alpha=0.5,label='Primary')
        print("Primary mean: " + str(np.median(primary_distr)))
        add_label(plt.violinplot(primary_distr), "Primary Nodes")
        # pdb.set_trace()

        # plt.hist(secondary_distr,bins=bins,alpha=0.5,label='Secondary')
        print("Secondary mean: " + str(np.median(secondary_distr)))
        add_label(plt.violinplot(secondary_distr), "Secondary Nodes")
        plt.legend(*zip(*labels), loc=2)

        print(stats.ks_2samp(primary_distr, secondary_distr))

        # plt.hist(full_distr,bins=bins,alpha=0.5,label='FULL')
        # plt.legend(['Primary','','','Secondary'])
        plt.title(pt + " " + condit + " " + band)

    """I guess this is about developing a rPCA approach to *dynamic* response without oscillations?"""
