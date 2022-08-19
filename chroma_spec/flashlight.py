"""chroma-spec flashlight."""

import matplotlib.pyplot as plt
from colour.plotting import plot_planckian_locus_in_chromaticity_diagram_CIE1931, render

from . import utils


class Flashlight:
    """Docstring for Flashlight."""

    def __init__(self, properties):
        """Docstring for __init__."""
        super(Flashlight, self).__init__()
        self._model = properties["model"]
        self._status = properties["status"]
        self._configuration = properties["configuration"]
        self._measures = properties["measures"]

    @property
    def model(self):
        """Docstring for model."""
        return self._model

    @property
    def status(self):
        """Docstring for status."""
        return self._status

    @property
    def configuration(self):
        """Docstring for configuration."""
        return self._configuration

    @property
    def measures(self):
        """Docstring for measures."""
        return self._measures

    def get_cct(self, measure_id):
        """Docstring for get_cct."""
        return utils.xy_to_CCT(
            self.measures[measure_id]["ciex"],
            self.measures[measure_id]["ciey"],
        )

    def get_duv(self, measure_id):
        """Docstring for get_duv."""
        return utils.xy_to_DUV(
            self.measures[measure_id]["ciex"],
            self.measures[measure_id]["ciey"],
        )

    def get_plot(self, measure_id):
        """Docstring for get_plot."""
        cct_str = "%4.0f" % self.get_cct(measure_id)
        duv_str = "%.4f" % self.get_duv(measure_id)
        x = self.measures[measure_id]["ciex"]
        y = self.measures[measure_id]["ciey"]
        xy = [x, y]

        label = (
            self.model
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

        bbox = [0.3, 0.75, 0.25, 0.65]

        fig = plt.figure(figsize=(1280 / 100, 1000 / 100), dpi=100)

        figure, axes = plot_planckian_locus_in_chromaticity_diagram_CIE1931(
            {self.model: xy},
            spectral_locus_labels=[],
            standalone=False,
            axes=fig.gca(),
        )
        render(
            axes=axes,
            bounding_box=bbox,
            # filename=pathlib.Path(outdir, fl + ".svg"),
            title=label,
        )
