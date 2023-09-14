import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np

class Pfahltabelle:
    
    def __init__(self, input_file):
        self.input_file = pd.read_csv(input_file, sep=';')

    def plot(self, relative_force, save_fig=False, annotate=False, ann_size=5, ann_min=None, markersize=5,
                        ann_max=None, ann_dist=0.3, add_hist=False, n_bins=None, save_xlsx=False, filename='Pfahlausnutzung'):
        df = self.input_file
        names = []
        for index, row in df.iterrows():
            names.append('C' + str(index+1))
        df['name'] = names
        df['force'] = df['Reaktionen'] / relative_force

        if add_hist:
            ncolums = 2
            width_ratios = [2, 1]
            fig = plt.figure(figsize=(15, 6))
        else:
            ncolums = 1
            width_ratios = [1]
            fig = plt.figure()

        gs = fig.add_gridspec(nrows=1, ncols=ncolums, width_ratios=width_ratios)

        # basic view
        ax1 = fig.add_subplot(gs[0,0])        
        scatter_plot = ax1.scatter(df['X'], df['Y'], s=markersize, c=df['force'], cmap='RdYlGn_r')
        anz_pfaehle = len(df)
        ax_1_title = 'Pfahlausnutzung($R_d$ = ' + str(relative_force) + ' kN), ' + '%.0f' % anz_pfaehle +  ' Pfähle: ' \
             + '%.2f' % df['force'].min() + '$\leq \\alpha_{eff} \leq$' + '%.2f' % df['force'].max()
        ax1.set_title(ax_1_title)
        ax1.set_aspect('equal')
        
        if add_hist:
            # histogramm
            ax2 = fig.add_subplot(gs[0,1])
            cm = plt.cm.get_cmap('RdYlGn_r')
            if n_bins != None:
                n, bins, patches = ax2.hist(df['force'], color='green', bins=n_bins)
            else:
                n, bins, patches = ax2.hist(df['force'], color='green')

            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            col = bin_centers - min(bin_centers)
            col /= max(col)
            for c, p in zip(col, patches):
                p.set_facecolor(cm(c))

            try:
                max_anz_Pfaehle = max(n)
                position = n.tolist().index(max_anz_Pfaehle)
                Ausnutzung_unten = bins[position-1]
                Ausnutzung_oben = bins[position+1]
                ax_2_title = '%.0f' % max_anz_Pfaehle + ' Pfähle: ' +'%.2f' % Ausnutzung_unten + '$\leq \\alpha_{eff} \leq$' + '%.2f' % Ausnutzung_oben
            except:
                ax_2_title 

            ax2.set_title('Verteilung, ' + ax_2_title)

        if annotate:
            if ann_min == None:
                ann_min = df['force'].min()
            if ann_max == None:
                ann_max = df['force'].max()
            for value in range(df.shape[0]):
                label = '%.2f' % df.iloc[value, 4]
                x = df.iloc[value, 1]
                y = df.iloc[value, 2]
                text_location = [x + ann_dist, y + ann_dist]
                text_color = scatter_plot.to_rgba(df.iloc[value, df.columns.get_loc('force')])  # Use 'scatter_plot.to_rgba()' to get the correct color
                if ann_min <= df.iloc[value, 4] <= ann_max:
                    ax1.annotate(text=label, xy=text_location, color=text_color, fontsize=ann_size)

        if add_hist:
            # Set aspect ratio to be equal for both subplots
            ax1.set_aspect('equal', adjustable='datalim')
            ax2.set_aspect('auto')
    
        if save_fig:
            plt.savefig(format='png', fname=filename + '.png', dpi=600)
            plt.savefig(format='pdf', fname=filename + '.pdf')
        plt.show()

        if save_xlsx:
            df.to_excel(excel_writer=filename + '.xlsx')


# Pt1 = Pfahltabelle(input_file='21159 Pfahltabelle.csv')
# Pt1.plot(relative_force=1250, save_fig=True, annotate=True, ann_size=5, ann_min=0.7,
#          ann_max=None, ann_dist=0.4, add_hist=True, save_xlsx=False, n_bins=20, filename='Pfaehlungsanalyse')