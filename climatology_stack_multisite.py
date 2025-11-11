'''
Example for creating classic study site climatology stack plots (temperature,
precipitation d2H, precipitation amount) seen in many presentations and
publications in the UB Paleoclimate Dynamics research group.

Python code for producing this figure with multiple study sites.

Author: Kurt R. Lindberg
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Use these parameters for easier editing in Inkscape/Illustrator
plt.rcParams['svg.fonttype'] = 'none'   # makes text recognized as editable text
# plt.rcParams['font.size'] = 12    # changes all figure fonts
plt.rcParams['font.family'] = "Liberation Sans"     # changes all figure text


## Reformat Climate Reanalyzer ERA5 .csv files for climatology plots
# there's definitely a better way to do this... but oh well
def climplot_format(df, data_type, site_name, start_year, end_year):
    '''
    Function arguments:
        df: input pandas DataFrame
        data_type: string name of the data type being formatted
        (e.g., "temp", "precip")
        site_name: string name of the climatology data location
        (e.g., "QPT", "RedPond")

    Returns:
        df_plot: output pandas DataFrame formatted to correctly produce the
        plot in the figure script below
    '''

    # Filter data within user-specified year range
    df_range = df[(df['Year'] > (start_year-1)) & (df['Year'] <= end_year)]

    # Rearrange data into single column
    df_plot = pd.concat(
        [
            df_range.Jan,
            df_range.Feb,
            df_range.Mar,
            df_range.Apr,
            df_range.May,
            df_range.Jun,
            df_range.Jul,
            df_range.Aug,
            df_range.Sep,
            df_range.Oct,
            df_range.Nov,
            df_range.Dec
        ]
    ).to_frame(name=data_type).reset_index(drop=True)

    # Add new column labeling data by month
    df_plot.insert(
        loc=1,
        column="month",
        value=(
            ['Jan']*len(df_range.Jan) +
            ['Feb']*len(df_range.Feb) +
            ['Mar']*len(df_range.Mar) +
            ['Apr']*len(df_range.Apr) +
            ['May']*len(df_range.May) +
            ['Jun']*len(df_range.Jun) +
            ['Jul']*len(df_range.Jul) +
            ['Aug']*len(df_range.Aug) +
            ['Sep']*len(df_range.Sep) +
            ['Oct']*len(df_range.Oct) +
            ['Nov']*len(df_range.Nov) +
            ['Dec']*len(df_range.Dec)
        )
    )

    # Add new column labeling data by location (for plotting multiple sites)
    df_plot.insert(
        loc=2,
        column="site_name",
        value=([str(site_name)]*len(df_plot.month)
        )
    )

    return df_plot

'''
##### Climate Data Download Instructions #####

ERA5 Temperature and preicpitation amount .csv files were downloaded from the
Climate Reanalyzer website:
https://climatereanalyzer.org/research_tools/monthly_tseries/

"Variable" selected are "2m Temperature" and "Total Precipitation".

Select the "Region" dropdown menu and choose "Specify Point" to provide
the latitude and longitude of your study site.

Click "Plot" to apply changes, then to go the "Export Chart"  and select
"Download CSV data" to get the .csv file format used in this Python file.
'''


# Import .csv files downloaded from Climate Reanalyser
temp_afr = pd.read_csv("AFR_temp.csv", header=8)
temp_cf8 = pd.read_csv("CF8_temp.csv", header=8)
temp_qpt = pd.read_csv("QPT_temp.csv", header=8)

precip_afr = pd.read_csv("AFR_precip.csv", header=8)
precip_cf8 = pd.read_csv("CF8_precip.csv", header=8)
precip_qpt = pd.read_csv("QPT_precip.csv", header=8)

# Import .csv with data from the Online Isotopes in Precipitation Calculator
# https://wateriso.utah.edu/waterisotopes/pages/data_access/oipc.html
# Also includes columns for plotting individual water samples
oipc_eca = pd.read_csv("ECA_oipc.csv")

# Format imported data using climplot_format()
temp_afr_plot = climplot_format(
    temp_afr, data_type="temp", site_name="AFR", start_year=1991, end_year=2020
)
temp_cf8_plot = climplot_format(
    temp_cf8, data_type="temp", site_name="CF8", start_year=1991, end_year=2020
)
temp_qpt_plot = climplot_format(
    temp_qpt, data_type="temp", site_name="QPT", start_year=1991, end_year=2020
)

precip_afr_plot = climplot_format(
    precip_afr, data_type="precip", site_name="AFR", start_year=1991, end_year=2020
)
precip_cf8_plot = climplot_format(
    precip_cf8, data_type="precip", site_name="CF8", start_year=1991, end_year=2020
)
precip_qpt_plot = climplot_format(
    precip_qpt, data_type="precip", site_name="QPT", start_year=1991, end_year=2020
)

# Combine all precipitation amount DataFrames
precip_all_plot = pd.concat(
    [
        precip_afr_plot,
        precip_cf8_plot,
        precip_qpt_plot
    ]
).reset_index()


##### Figure plotting script #####
fig, axs = plt.subplots(3,1)
# fig, axs = plt.subplots(3,2)  # thinner plot

site_colors = [
    "#2c7bb6",
    "#fdae61",
    "#d7191c"
]

# Temperature panel
ax = axs[0]
# ax = axs[0,0]  # thinner plot
ax.hlines(
    xmin=0, xmax=11, y=0,
    linestyles='--', color='black', alpha=0.5, zorder=5
)  # horizontal dashed line at 0 degC
sns.pointplot(
    ax=ax, x=temp_afr_plot.month, y=temp_afr_plot.temp,
    color=site_colors[0], marker=None, linewidth=1.5, zorder=20
)
sns.pointplot(
    ax=ax, x=temp_cf8_plot.month, y=temp_cf8_plot.temp,
    color=site_colors[1], marker=None, linewidth=1.5, zorder=15
)
sns.pointplot(
    ax=ax, x=temp_qpt_plot.month, y=temp_qpt_plot.temp,
    color=site_colors[2], marker=None, linewidth=1.5, zorder=10
)
ax.set_xticklabels('')
ax.set_xlabel('')
ax.set_ylabel("Temp. (C)")
# ax.set_yticks(ticks=[-30,-20,-10,0,10])
# ax.set_ylim([-35,10])
ax.spines['bottom'].set_visible(False)  # removes panel borders

# OIPC panel
ax = axs[1]
# ax = axs[1,0]  # thinner plot
sns.pointplot(
    ax=ax, x=oipc_eca.month, y=oipc_eca.d2h, hue=oipc_eca.site,
    legend=False, linewidth=1.5, palette=site_colors, markers="", zorder=10
)
sns.scatterplot(
    ax=ax, x=oipc_eca.sample_month, y=oipc_eca.sample_d2h, hue=oipc_eca.sample_site,
    legend=False, palette=site_colors, marker='d', s=50, edgecolors="black", zorder=15
)  # plots individual water samples
ax.yaxis.set_label_position("right")
ax.yaxis.set_ticks_position("right")
ax.set_xticklabels('')
ax.set_xlabel('')
ax.set_ylabel("OIPC d2H (permil)")
# ax.set_ylim([-300,-50])
# ax.set_yticks(ticks=[-300,-250,-200,-150,-100])
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Precipitation amount panel
ax = axs[2]
# ax = axs[2,0]  # thinner plot
sns.boxplot(
    ax=ax, x=precip_all_plot.month, y=(precip_all_plot.precip)*1000, hue=precip_all_plot.site_name,
    palette=site_colors, fliersize=3
)  # precipitation amount data in the .csv is provided in meters
ax.set_xticklabels('')
ax.set_xlabel("Month")
ax.set_ylabel("Precip. (mm)")
ax.set_xticks(
    ticks=np.arange(0,12),
    labels=["J","F","M","A","M","J","J","A","S","O","N","D"]
)
# ax.set_yticks(ticks=[0,50,100,150,200])
# ax.set_ylim([0,200])
# ax.legend(loc='center left', bbox_to_anchor=(1,0.5))
ax.spines['top'].set_visible(False)

# Thinner plot: uncomment following 3 lines
# fig.delaxes(axs[0,1])
# fig.delaxes(axs[1,1])
# fig.delaxes(axs[2,1])

plt.subplots_adjust(wspace=0, hspace=0)  # removes whitespace between panels
climatology_figure = plt.gcf()
climatology_figure.savefig("climatetology_stack_multisite.svg", dpi=300)
# Can change saved figure to .png or other image file formats
