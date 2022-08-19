"""chroma-spec utils."""
import logging
import math
import sys


def xy_to_CCT(x, y):
    """CIE 1931 to CCT (McCamy's approximation).

    Args:
        x (float): CIE 1931 chromacity coordinate x
        y (float): CIE 1931 chromacity coordinate x

    Returns:
        float: Correlated Colour Temperature (CCT)

    Example:
        >>> from chroma_spec import utils
        >>> utils.xy_to_CCT(0.3604, 0.3339)
        4330.655950072925
    """
    n = (x - 0.3320) / (0.1858 - y)

    return 437 * math.pow(n, 3) + 3601 * math.pow(n, 2) + 6861 * n + 5517


def xy_to_uv(x, y):
    """CIE 1931 to uvp chromaticity coordinates.

    Args:
        x (float): CIE 1931 chromacity coordinate x
        y (float): CIE 1931 chromacity coordinate x

    Returns:
        tuple: (u, v) uvp chromaticity coordinates

    Example:
        >>> from chroma_spec import utils
        >>> utils.xy_to_uv(0.3604, 0.3339)
        (0.22933503022589885, 0.3187082405345212)
    """
    u = (4 * x) / (-2 * x + 12 * y + 3)
    v = (6 * y) / (-2 * x + 12 * y + 3)

    return u, v


def xy_to_DUV(x, y):
    """CIE 1931 to DUV.

    Args:
        x (float): CIE 1931 chromacity coordinate x
        y (float): CIE 1931 chromacity coordinate x

    Returns:
        float: Delta uv (DUV)

    Example:
        >>> from chroma_spec import utils
        >>> utils.xy_to_DUV(0.3604, 0.3339)
        -0.015143925038518163
    """
    k6 = -0.00616793
    k5 = 0.0893944
    k4 = -0.5179722
    k3 = 1.5317403
    k2 = -2.4243787
    k1 = 1.925865
    k0 = -0.471106
    u, v = xy_to_uv(x, y)
    lfp = math.sqrt(math.pow((u - 0.292), 2) + math.pow((v - 0.24), 2))
    a = math.acos((u - 0.292) / lfp)
    lbb = (
        k6 * math.pow(a, 6)
        + k5 * math.pow(a, 5)
        + k4 * math.pow(a, 4)
        + k3 * math.pow(a, 3)
        + k2 * math.pow(a, 2)
        + k1 * a
        + k0
    )

    return lfp - lbb


def setup_logger(verbose=False):
    """Setup logger.

    Args:
        verbose (bool, optional): Flag to enable/disable verbose. Defaults to False.

    Example:
        >>> from chroma_spec import utils
        >>> utils.setup_logger()
        >>> import logging
        >>> logging.info("Logger using custom format.")
    """
    logging_format = (
        "%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
    )

    if verbose is True:
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.DEBUG,
            format=logging_format,
        )
    else:
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format=logging_format,
        )
