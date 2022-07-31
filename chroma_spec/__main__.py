"""Command-line interface."""
import click

from . import spec


@click.group(name="main")
@click.version_option()
def main():
    """chroma-spec main cli."""
    pass


@main.command(name="single")
@click.option("--CIEx", type=float, required=True, help="CIE 1931 x coordinate.")
@click.option("--CIEy", type=float, required=True, help="CIE 1931 y coordinate.")
@click.option("--model", type=str, required=True, help="Measure description.")
@click.option(
    "--outdir", type=click.Path(exists=True), default="data", help="Output directory."
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.version_option()
def single(ciex, ciey, model, outdir, verbose):
    """chroma-spec plots a given chromatic measure."""
    spec.chroma_spec_single(ciex, ciey, model, outdir)


@main.command(name="batch")
@click.option(
    "--indb",
    type=click.Path(exists=True),
    default="data/sotc.json",
    help="Input database file.",
)
@click.option(
    "--outdir",
    type=click.Path(exists=True),
    default="data/SOTC",
    help="Output directory.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.version_option()
def batch(indb, outdir, verbose):
    """chroma-spec batch plot chromatic measures."""
    spec.chroma_spec_batch(indb, outdir)


@main.command(name="evol")
@click.option(
    "--indb",
    type=click.Path(exists=True),
    default="data/sotc.json",
    help="Input database file.",
)
@click.option(
    "--outdir",
    type=click.Path(exists=True),
    default="data/SOTC",
    help="Output directory.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.version_option()
def evol(indb, outdir, verbose):
    """chroma-spec evol plot chromatic evolutions."""
    spec.chroma_spec_evol(indb, outdir)


@main.command(name="gifs")
@click.option(
    "--indb",
    type=click.Path(exists=True),
    default="data/sotc.json",
    help="Input database file.",
)
@click.option(
    "--outdir",
    type=click.Path(exists=True),
    default="data/SOTC",
    help="Output directory.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.version_option()
def gifs(indb, outdir, verbose):
    """chroma-spec gifs plot animated chromatic evolutions."""
    spec.chroma_spec_gifs(indb, outdir)


if __name__ == "__main__":
    main(prog_name="chroma-spec")  # pragma: no cover
