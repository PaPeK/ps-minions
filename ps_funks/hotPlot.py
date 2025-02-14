import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib.cm as mplcm
from cycler import cycler
import numpy as np
import ps_funks.juteUtils as jut
from pathlib import Path
import seaborn as sns


def shareXlimits(axs):
    """
    chooses automatically the maximal
    INPUT:
        axs list or 1d-np.ndarray
    """
    xlim = list(axs[0].get_xlim())
    for ax in axs[1:]:
        xlim += list(ax.get_xlim())
    minne = np.min(xlim)
    maxxe = np.max(xlim)
    for ax in axs:
        ax.set_xlim([minne, maxxe])


def shareYlimits(axs):
    """
    INPUT:
        axs list or 1d-np.ndarray
    """
    ylim = list(axs[0].get_ylim())
    for ax in axs[1:]:
        ylim += list(ax.get_ylim())
    minne = np.min(ylim)
    maxxe = np.max(ylim)
    for ax in axs:
        ax.set_ylim([minne, maxxe])


def no_spines(axs):
    for k in axs.spines.keys():
        axs.spines[k].set_visible(False)


def get_twinx(ax, color="C0"):
    axtwin = ax.twinx()
    no_spines(axtwin)
    axtwin.spines["right"].set_visible(True)
    axtwin.spines["right"].set_color(color)
    axtwin.tick_params(axis="y", labelcolor=color, color=color)
    axtwin.yaxis.label.set_color(color)
    return axtwin


def setRcParams(cycleLinestyles=False, cycleColors=True, spinesRight=False):
    if cycleColors:
        matplotlib.rcParams["axes.prop_cycle"] = cycler("color", cssCblind)
    if cycleLinestyles:
        # color AND linestyle cycle for lines
        # However, cycler + cycler of different length shortens the longer one
        matplotlib.rcParams["axes.prop_cycle"] += cycler("linestyle", lss)
    # make that only left and bottom spines are shown
    matplotlib.rcParams["axes.spines.top"] = False
    matplotlib.rcParams["axes.spines.right"] = spinesRight
    matplotlib.rcParams["font.family"] = "sans-serif"
    # top and bottom spine
    # facecolors
    matplotlib.rcParams["axes.facecolor"] = "white"
    matplotlib.rcParams["savefig.facecolor"] = "white"


def reduce_color_cycle(N):
    matplotlib.rcParams["axes.prop_cycle"] = cycler("color", cssCblind[:N])


def reset_color_cycle():
    matplotlib.rcParams["axes.prop_cycle"] = cycler("color", cssCblind)


def set_color_cycle(clrs):
    matplotlib.rcParams["axes.prop_cycle"] = cycler("color", clrs)


def savefig_multiformat(dir, f_name, f, formats=["png", "pdf", "svg"], **kwgs):
    """
    THE IDEA at the start of notebook partialize the function by:
        savefig_multi = partial(savefig_multiformat, dir=dir)

    INPUT:
        dir Path
            directory to save the figure
        f_name str
            name of the figure
        f matplotlib.figure.Figure
            figure to save
        formats list
            list of formats to save the figure
    """
    dir = Path(dir)
    dir.mkdir(exist_ok=True)
    default_paras = dict(dpi=300, bbox_inches="tight", pad_inches=0)
    default_paras.update(kwgs)
    for fmt in formats:
        dir_ = dir / fmt
        dir_.mkdir(exist_ok=True)
        f.tight_layout()
        f.savefig(dir_ / (f_name + "." + fmt), **default_paras)


def axesGrid(N, **kwgs):
    return subplots(N, **kwgs)
def subplots(N, size=0.8, aspect=1, flatten=True, n_col=None, n_row=None, axes_offset=5, **kwgs):
    """
    returns
    INPUT:
        aspect float
            changes the aspect of each axis
            e.g.: 0.5: |__
                  2: |
                     |_
        flatten bool
            Default=True
            True: returns axs.flatten()[:N]
            False: returns axs-array
    """
    m, n = rows_and_cols(N, n_row, n_col)
    f, axs = plt.subplots(m, n, figsize=m * size * plt.figaspect(m / n * aspect), **kwgs)
    if m * n > N:
        axs = axs.flatten()
        _ = [ax.remove() for ax in axs[N:]]
        axs = axs.reshape(m, n)
    if flatten and N > 1:
        axs = axs.flatten()[:N]
    # set position of axis outwards (no crossing)
    offset = axes_offset
    if N == 1:
        axs = [axs]
    for ax in axs:
        ax.spines['bottom'].set_position(('outward', offset))
        ax.spines['left'].set_position(('outward', offset))
    if N == 1:
        axs = axs[0]
    return f, axs


def rows_and_cols(N, n_row, n_col):
    if n_row is not None:
        m = n_row
        n = int((t := N / m)) + int(np.mod(t, 1) > 0)
    elif n_col is not None:
        n = n_col
        m = int((t := N / n)) + int(np.mod(t, 1) > 0)
    else:
        m = int(np.sqrt(N))
        n = m + int((m - np.sqrt(N)) < 0)
        m += int((n * m - N) < 0)
    return m, n


def abc_plotLabels(
    coord,
    axs,
    lower_case=False,
    fontsize=22,
    Nskip=0,
    abc=None,
    facecolors=None,
    edgecolors=None,
    **kwgs,
):
    """
    INPUT:
        coord.shape (2)
            coordinates relative to borders of plot
        axs [matplotlib.subplotobject, ....]
            list of subplots which needs label
    """
    abc = jut.setDefault(abc, get_ABC(len(axs), Nskip=Nskip, lower_case=lower_case))
    for i, ax in enumerate(axs):
        dic = {}
        if facecolors is not None:
            dic["facecolor"] = facecolors[i]
        if edgecolors is not None:
            dic["edgecolor"] = edgecolors[i]
        if edgecolors is None and facecolors is None:
            dic = None
        ax.text(
            coord[0],
            coord[1],
            abc[i],
            fontsize=fontsize,
            transform=ax.transAxes,
            bbox=dic,
            **kwgs,
        )


def get_ABC(N, Nskip=None, lower_case=False):
    Nskip = jut.setDefault(Nskip, 0)
    # fmt: off
    abc = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    ]
    ABC = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    ]
    # fmt: on
    if not lower_case:
        abc = ABC
    return abc[Nskip : Nskip + N]


def rotate_xticklabels(ax, deg):
    for tick in ax.get_xticklabels():
        tick.set_rotation(deg)


def rotate_yticklabels(ax, deg):
    for tick in ax.get_yticklabels():
        tick.set_rotation(deg)


def hist_logx(ax, x, bins, **kwargs):
    hist, bins = np.histogram(x, bins=bins)
    logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
    logbins[-1] += logbins[0] / 100  # to include the last datapoint
    ax.hist(x, bins=logbins, **kwargs)
    ax.set(xscale="log")


def nice_dates(ax, y=False, monthstep=2, month_offset=1, rotation_major=0, rotation_minor=None):
    assert isinstance(monthstep, int), "monthstep must be integer"
    assert isinstance(month_offset, int), "month_offset must be integer"
    axis = ax.yaxis if y else ax.xaxis
    axis.set_minor_locator(matplotlib.dates.MonthLocator(np.arange(1, 13)))
    axis.set_minor_formatter(DateFormatter_withEmptyStrings("%b", monthstep))
    axis.set_major_locator(matplotlib.dates.YearLocator())
    axis.set_major_formatter(matplotlib.dates.DateFormatter("%b\n%Y"))
    if rotation_major is not None:
        for t in axis.get_majorticklabels():
            t.set_rotation(rotation_major)
            t.set_horizontalalignment("center")
    if rotation_minor is not None:
        for t in axis.get_minorticklabels():
            t.set_rotation(rotation_minor)


class DateFormatter_withEmptyStrings(matplotlib.dates.DateFormatter):
    # def __init__(self, fmt, month_step, **kwargs):
    def __init__(self, fmt, month_step, tz=None):
        super().__init__(fmt, tz=tz, usetex=False)
        self._month_step = month_step

    def __call__(self, x, pos=0):
        out = super().__call__(x, pos)
        if self._month_step > 1:
            months_short = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            keep = list(
                set(months_short[:: self._month_step])
                - set(months_short[(-self._month_step + 1) :])
            )
            out = out if out in keep else ""
        return out


def text_only_plot(ax, txt, **kwgs):
    # in order to have well-aligned text on top, the code should start there
    ax.text(0, 1, txt, va="top", **kwgs)
    ax.axis("off")
    ax.set(title="")


def text_input_output_plot(txt_input, txt_output, wspace=None, from_file=True, max_length=None):
    """
    INPUT:
        txt_input str OR txt-file
        txt_output str OR txt-file
        wspace float
            horizontal (width) space between the subplots
            should be set to larger values if text txt_input is long

    NOTE:
        remember to save with option "bbox_inches='tight'"
            f, axs = text_input_output_plot(in, out, wspace=1)
            f.savefig('test.pdf', bbox_inches='thight')
    """
    if from_file:
        txt_input = Path(txt_input).open("r").read()
        txt_output = Path(txt_output).open("r").read()
    if max_length is not None:
        txt_input = jut.text_addLineBreaks(txt_input, max_length)
        txt_input = jut.text_addLineBreaks(txt_input, max_length, breaker="-")
        txt_input = jut.text_addLineBreaks(txt_input, max_length, breaker=".")
        txt_output = jut.text_addLineBreaks(txt_output, max_length)
        txt_output = jut.text_addLineBreaks(txt_output, max_length, breaker="-")
        txt_output = jut.text_addLineBreaks(txt_output, max_length, breaker=".")
    gridspec_kw = {}
    if wspace is not None:
        gridspec_kw["wspace"] = wspace
    f, axs = axesGrid(2, gridspec_kw=gridspec_kw)
    _ = [text_only_plot(ax, txt) for ax, txt in zip(axs, [txt_input, txt_output])]
    _ = [ax.set_title(ti, fontsize=12, weight="bold") for ax, ti in zip(axs, ["input:", "output:"])]
    return f, axs


def swarmplot_single(ax, df, col, orient="h", **kwgs):
    """
    In order for sns.swarmplot to use "hue" coloring, an y-value must be given
        * create a dummy y value
    """

    df[""] = ""
    if orient == "h":
        x, y = col, ""
    else:
        y, x = col, ""
    sns.swarmplot(data=df, x=x, y=y, ax=ax, orient=orient, **kwgs)
    undo_seaborn_xaxis(ax)
    if orient == "h":
        yAxisOff(ax)
    else:
        xAxisOff(ax)
    df.drop(columns=[""], inplace=True)


def yAxisOff(axs):
    axs.get_yaxis().set_visible(False)  # no ticks
    axs.spines["left"].set_visible(False)  # no spine
    axs.spines["right"].set_visible(False)  # no spine


def yAxisAlmostOff(axs):
    '''everything is off but the y-label can be still set'''
    axs.get_yaxis().ticks([])  # no ticks
    axs.spines["left"].set_visible(False)  # no spine
    axs.spines["right"].set_visible(False)  # no spine


def xAxisOff(axs):
    axs.get_xaxis().set_visible(False)  # no ticks
    axs.spines["bottom"].set_visible(False)  # no spine


def xAxisAlmostOff(axs):
    axs.get_xaxis().set_ticks([])  # no ticks
    axs.spines["bottom"].set_visible(False)  # no spine
    axs.spines["top"].set_visible(False)  # no spine


def undo_seaborn_xaxis(ax):
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color("k")
    ax.tick_params(axis="x", which="both", reset=True, top=False)


def legend_sorted(ax, reverse=False, **kwgs):
    return sorted_legend(ax, reverse=reverse, **kwgs)


def sorted_legend(ax, reverse=False, **kwgs):
    handles, labels = ax.get_legend_handles_labels()
    # sort both labels and handles by labels
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    if reverse:
        labels, handles = labels[::-1], handles[::-1]
    return ax.legend(handles, labels, **kwgs)


def legend_handle_same_size(legend, size=30):
    for handle in legend.legendHandles:
        if hasattr(handle, "set_sizes"):
            handle.set_sizes([size])
        elif hasattr(handle, "set_linewidth"):
            handle.set_linewidth(size)
        else:
            print("legend handle is neither marker nor line")
            print(f"its: {type(handle)}")


def undo_seaborn_params():
    matplotlib.rcParams["xtick.bottom"] = True
    matplotlib.rcParams["ytick.left"] = True
    matplotlib.rcParams["axes.grid"] = False
    matplotlib.rcParams["axes.spines.top"] = False
    matplotlib.rcParams["axes.spines.right"] = False
    matplotlib.rcParams["axes.spines.bottom"] = True
    matplotlib.rcParams["axes.spines.left"] = True
    matplotlib.rcParams["axes.edgecolor"] = "k"


def color_to_rgb(c):
    return mplc.to_rgb(c)


# extended list of linestyles, linestyletuples are created via (offset,(xpt line, xpt space, line, space, ...))
lss = [
    "-",
    ":",
    "--",
    "-.",
    (0, (1, 1, 1, 4)),  # = .. .. (double dots)
    (0, (5, 1, 1, 1, 1, 1)),  # = -..-.. (dash double dots)
    (0, (7, 2)),  # = -- -- (long dashes)
    (0, (1, 1, 1, 1, 1, 4)),  # = ... ... (triple dots)
    (0, (1, 1, 1, 1, 1, 1, 6, 1)),
]  # = ...-...- (triple dots dash)

# colorpalette optimized for colorblind people: https://www.nature.com/articles/nmeth.1618
# * other noce websites:
#       * https://davidmathlogic.com/colorblind/#%23D81B60-%231E88E5-%23FFC107-%23004D40
#       * https://gka.github.io/palettes/#/9%7Cd%7C0033a6,0098ce,ecf8fa%7Cffb5a1,ff5659,b40000%7C1%7C1
cssCblind_A = [
    (0, 0, 0),
    (230, 159, 0),
    (86, 180, 233),
    (0, 158, 115),
    (240, 228, 66),
    (0, 114, 178),
    (213, 94, 0),
    (204, 121, 167),
]
cssCblind = [(t[0] / 255, t[1] / 255, t[2] / 255) for t in cssCblind_A]


def histProb(dat, axs=None, **kwgs):
    '''
    as plt.hist but the bins sum to 1
    which is different to plt.hist(dat, density=True)
    where the integral (area) sums to 1
    '''
    if axs is None:
        f, axs = plt.subplots(1)
    weights = np.ones(len(dat), dtype=float)/len(dat)
    out = axs.hist(dat, weights=weights, **kwgs)
    return out

def df_scatter_and_lines(
    ax,
    df,
    x_c,
    y_c,
    bins=50,
    c_q="C1",
    c_a="C2",
    show_scatter=True,
    show_xy=True,
    show_med=True,
    show_iqr=False,
    show_avg=False,
    scatter_kwgs=None,
    med_kwgs=None,
    rasterized=True,
):
    """
    plots the scatter and different information of the
    equi-data-x-bins (created via qcut, i.e. quartiles)
    INPUT:
        ax matplotlib.axes
        df pd.DataFrame
        x_c string
            column of df that defines the x-axis
        y_c string
            column of df that defines the y-axis
        bins int
            number of x-bins
        c_q str
            color used for quantile lines
        c_a str
            color used for average line
    """
    scatter_kwgs = dict(alpha=0.2, s=5) if scatter_kwgs is None else scatter_kwgs
    med_kwgs = (
        dict(
            marker="o",
            markersize=3,
        )
        if med_kwgs is None
        else med_kwgs
    )
    x = df[x_c]
    if show_scatter:  # scatter
        ax.scatter(x, df[y_c], rasterized=rasterized, **scatter_kwgs)
    df_q = jut.df_xbin_yquantile(df, x_c, y_c, bins=bins)
    if show_med:  # median
        ax.plot(df_q["x_mean"], df_q[0.5], color=c_q, label="median", **med_kwgs)
    if show_iqr:  # Inter Quartile Range
        ax.fill_between(
            df_q.x_mean,
            df_q[0.25],  # y1
            df_q[0.75],  # y2
            color=c_q,
            alpha=0.2,
            label="IQR",
        )
    if show_avg:  # average
        ax.plot(
            df_q["x_mean"],
            df_q["y_mean"],
            marker="o",
            markersize=3,
            color=c_a,
            label="mean",
        )
    ax.set(xlabel=x_c, ylabel=y_c)
    if show_xy:  # line with y=x
        if not show_scatter:
            x = df_q.x_mean
        plot_xy(ax, x, color="grey", label="_nolegend")
        # ax.plot((xl:=np.linspace(0, x.max(), 100)), xl, color='grey', label='_nolegend')


def plot_xy(ax, x, **kwgs):
    """
    line with y = x
    """
    x = np.linspace(np.nanmin(x), np.nanmax(x), 3)
    ax.plot(x, x, **kwgs)


def scatter3d_3angles(x, y, z, fc='k', angles=None, elev=10, equal_aspect=False, min_aspect=0.2, **kwgs):
    """creates a 3d scatter plot with 3 different angles
    it uses the subplot_mosaic layout (plt.subplots not possible with 3d plots)

    Args:
        x (N): array of x-values
        y (N): arrray of y-values
        z (N): array of z-values
        fc (str, optional): facecolor of the plot. Defaults to 'k'.
        angles (list of angles, optional): list of angles. Defaults to None.

    Returns:
        f, axs: figure and axs-list
    """
    angles = [-145, -90, -35] if angles is None else angles
    layout = [list(range(len(angles)))]
    f, axs = plt.subplot_mosaic(layout, subplot_kw={'projection': '3d', 'fc':fc}, figsize=(12, 4), facecolor=fc)
    ca = 'w' if fc == 'k' else 'k'
    if equal_aspect:
        aspect = np.array([np.ptp(x), np.ptp(y), np.ptp(z)])
        aspect /= aspect.max()
        if min_aspect is not None:
            print(f'attention: aspect ratio is set to at least {min_aspect}, if undesired set min_aspect=None')
            aspect[aspect<min_aspect] = min_aspect
    for i, id in enumerate(layout[0]):
        ax = axs[id]
        ax.scatter(x, y, z, **kwgs)
        ax.set_xlabel("x", color=ca)
        ax.set_ylabel("y", color=ca)
        ax.set_zlabel("", color=ca)
        ax.view_init(elev=elev, azim=angles[i])
        if equal_aspect:
            ax.set_box_aspect(aspect)
        if fc == 'k':
            ax.tick_params(axis='x', colors='w')
            ax.tick_params(axis='y', colors='w')
            ax.tick_params(axis='z', colors='w')
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
    axs[1].set_zlabel("z", color=ca)
    f.tight_layout()
    return f, axs

def cmap_zerowhite(mat, cmap=None, redsandblues=True, maxval=None):
    """creates a cmap with reds for negative, white=0 and blur for positive values
    """
    mini = np.nanmin(mat)
    maxi = np.nanmax(mat)
    maxse = np.max([np.abs(mini), maxi])
    maxval = jut.setDefault(maxval, maxse)
    br = mplcm.bwr # alternative BluesReds()
    cmap = jut.setDefault(cmap, br)
    if mini * maxi < 0:
        cmap = cmap
        vmin, vmax = -maxval, maxval
    elif mini >= 0:
        cmap = truncate_colormap(cmap, minval=0.5, maxval=1.0, n=500)
        vmin, vmax = mini, maxval
        if redsandblues:
            cmap = mplcm.Reds
            vmin, vmax = mini, maxi
    elif maxi <= 0:
        cmap = truncate_colormap(cmap, minval=0, maxval=0.5, n=500)
        vmin, vmax = -maxval, maxi
        if redsandblues:
            cmap = mplcm.Blues_r
            vmin, vmax = mini, maxi
    else:
        cmap = mplcm.Greys
        vmin, vmax = mini, maxi
    return cmap, vmin, vmax


def truncate_colormap(cmap, minval=None, maxval=None, n=None):
    """
    to truncate an existing colormap
    source:
    https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """
    minval = jut.setDefault(minval, 0.0)
    maxval = jut.setDefault(maxval, 1.0)
    n = jut.setDefault(n, 100)
    new_cmap = mplc.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


def BluesReds(unwhite=0):
    """returns a colormap with Blue_r for negative values and Red for positive
    INPUT:
        unwhite (float): value between [0, 1], if 0: the middle is white
                         MOTIVATION: Sometimes it is important to know
                            if it is neg. or pos. and you
                            but not if it is 0 --> use unwhite=0.1 for example
    """
    # colors in total
    colors1 = mplcm.Blues_r(np.linspace(0, 1-unwhite, 200))
    colors2 = mplcm.Reds(np.linspace(unwhite, 1, 200))
    # combine them and build a new colormap
    clrs = np.vstack((colors1, colors2))
    mymap = mplc.LinearSegmentedColormap.from_list("my_colormap", clrs)
    return mymap
