"""chroma-spec."""
import json
import logging
import pathlib

import imageio
import matplotlib.pyplot as plt
from colour.plotting import plot_planckian_locus_in_chromaticity_diagram_CIE1931, render

from . import utils


def stat_chroma_spec(x, y):
    """Compute a chromatic properties.

    Args:
        x (float): CIE 1931 chromacity coordinate x
        y (float): CIE 1931 chromacity coordinate x

    Returns:
        tuple (cct, duv): cct and duv numerical values

    Example:
        >>> from chroma_spec import spec
        >>> spec.stat_chroma_spec(0.3604, 0.3339)
        (4330.655950072925, -0.015143925038518163)
    """
    cct = utils.xy_to_CCT(x, y)
    duv = utils.xy_to_DUV(x, y)

    cct_str = "%4.0f" % cct
    duv_str = "%.4f" % duv
    logging.info(
        "[" + str(x) + "; " + str(y) + "] --> CCT: " + cct_str + "K - DUV: " + duv_str,
    )
    return cct, duv


def plot_chroma_spec(x, y, fl, outdir, zoom=False):
    """Generate a chromatic graph.

    Args:
        x (float): CIE 1931 chromacity coordinate x
        y (float): CIE 1931 chromacity coordinate x
        fl (string): Measure description
        outdir (string): Output directory where the graph will be saved
        zoom (bool): Flag to enable zoom

    Example:
        >>> from chroma_spec import spec
        >>> spec.plot_chroma_spec(0.3604, 0.3339, "PL47MU", "/tmp")
    """
    xy = [x, y]

    cct, duv = stat_chroma_spec(x, y)

    cct_str = "%4.0f" % cct
    duv_str = "%.4f" % duv

    label = (
        fl
        + " ["
        + str(x)
        + "; "
        + str(y)
        + "]\nCCT: "
        + cct_str
        + "K\nDUV: "
        + duv_str
        + "\n"
    )

    if zoom is True:
        bbox = [x - 0.08, x + 0.08, y - 0.08, y + 0.08]
    else:
        bbox = [0.3, 0.75, 0.25, 0.65]

    fig = plt.figure(figsize=(1280 / 100, 1000 / 100), dpi=100)

    figure, axes = plot_planckian_locus_in_chromaticity_diagram_CIE1931(
        {fl: xy},
        spectral_locus_labels=[],
        standalone=False,
        axes=fig.gca(),
    )

    render(
        axes=axes,
        bounding_box=bbox,
        filename=pathlib.Path(outdir, fl + ".svg"),
        title=label,
    )


def chroma_spec_single(x, y, fl, outdir, zoom=False):
    """Chromatic graph for a given measure.

    Args:
        x (float): CIE 1931 chromacity coordinate x
        y (float): CIE 1931 chromacity coordinate x
        fl (string): Measure description
        outdir (string): Output directory where the graph will be saved
        zoom (bool): Flag to enable zoom

    Example:
        >>> from chroma_spec import spec
        >>> spec.chroma_spec_single(0.3604, 0.3339, "PL47MU", "/tmp")
    """
    plot_chroma_spec(x, y, fl, outdir, zoom=zoom)


def chroma_spec_batch(indb, outdir):
    """Chromatic graphs of all measures from a database.

    Args:
        indb (string): Input database file
        outdir (string): Output directory

    Example:
        >>> from chroma_spec import spec
        >>> spec.chroma_spec_batch("data/sotc.json", "/tmp")
    """
    with open(indb) as i:
        fldb = json.load(i)

    for fl in fldb["flashlights"]:
        fl_path = pathlib.Path(outdir, fl["model"])
        pathlib.Path.mkdir(fl_path, exist_ok=True)

        for rec in fl["measures"]:
            rec_fname = fl["model"] + "_" + rec["mod"] + "_" + rec["level"]
            plot_chroma_spec(rec["ciex"], rec["ciey"], rec_fname, fl_path)


def chroma_spec_evol(indb, outdir):
    """Chromatic graph for a given model evolution.

    Args:
        indb (string): Input database file
        outdir (string): Output directory

    Example:
        >>> from chroma_spec import spec
        >>> spec.chroma_spec_evol("data/sotc.json", "/tmp")
    """
    with open(indb) as i:
        fldb = json.load(i)

    for fl in fldb["flashlights"]:
        fl_path = pathlib.Path(outdir, fl["model"])
        pathlib.Path.mkdir(fl_path, exist_ok=True)
        fl_dict = dict()
        for rec in fl["measures"]:
            rec_xy = [rec["ciex"], rec["ciey"]]
            rec_fl = rec["mod"] + " " + rec["level"]
            fl_dict[rec_fl] = rec_xy

        figure, axes = plot_planckian_locus_in_chromaticity_diagram_CIE1931(
            fl_dict,
            standalone=False,
        )
        render(
            axes=axes,
            bounding_box=[0.32, 0.42, 0.32, 0.42],
            filename=pathlib.Path(fl_path, fl["model"] + ".svg"),
            title=fl["model"],
        )


def chroma_spec_gifs(indb, outdir):
    """Chromatic graphs gifs of all multi-measure entries from a database.

    Args:
        indb (string): Input database file
        outdir (string): Output directory

    Example:
        >>> from chroma_spec import spec
        >>> spec.chroma_spec_gifs("data/sotc.json", "/tmp")
    """
    with open(indb) as i:
        fldb = json.load(i)

    for fl in fldb["flashlights"]:
        fl_path = pathlib.Path(outdir, fl["model"])
        pathlib.Path.mkdir(fl_path, exist_ok=True)
        if len(fl["measures"]) >= 2:
            frames = []
            for rec in fl["measures"]:
                rec_fname = rec["mod"] + "_" + rec["level"]
                figure, axes = plot_planckian_locus_in_chromaticity_diagram_CIE1931(
                    {rec_fname: [rec["ciex"], rec["ciey"]]},
                    standalone=False,
                )
                render(
                    axes=axes,
                    bounding_box=[0.3, 0.4, 0.3, 0.4],
                    filename=pathlib.Path(fl_path, rec_fname + ".png"),
                    title=fl["model"],
                )
                frames.append(imageio.imread(pathlib.Path(fl_path, rec_fname + ".png")))
            imageio.mimsave(
                pathlib.Path(fl_path, fl["model"] + ".gif"),
                frames,
                format="GIF",
                duration=1000,
                loop=3,
            )


# kang2002 = colour.xy_to_CCT((x, y),'Kang 2002')
# print(kang2002)
# hernandez1999 = colour.xy_to_CCT((x, y), 'Hernandez 1999')
# print(hernandez1999)
# mccamy1992 = colour.xy_to_CCT((x, y), 'McCamy 1992')
# print(mccamy1992)
