"""Test cases for the __main__ module."""
import json

import jsonschema
import pytest
from click.testing import CliRunner

from chroma_spec import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_single(runner: CliRunner, tmp_path) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        __main__.main,
        [
            "single",
            "--CIEx",
            "0.3604",
            "--CIEy",
            "0.3339",
            "--model",
            "PL47MU_sw45kd220",
            "--outdir",
            tmp_path,
        ],
    )
    assert result.exit_code == 0


def test_batch(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        __main__.main,
        [
            "batch",
            "--indb",
            "data/sotc.json",
            "--outdir",
            "data/SOTC",
        ],
    )
    assert result.exit_code == 0


def test_evol(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        __main__.main,
        [
            "evol",
            "--indb",
            "data/sotc.json",
            "--outdir",
            "data/SOTC",
        ],
    )
    assert result.exit_code == 0


def test_gifs(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        __main__.main,
        [
            "gifs",
            "--indb",
            "data/sotc.json",
            "--outdir",
            "data/SOTC",
        ],
    )
    assert result.exit_code == 0


def test_db_schema():
    """Validate sotc.json with schema."""
    with open("data/sotc.json") as i:
        db = json.load(i)

    with open("data/sotc.schema") as j:
        schema = json.load(j)

    jsonschema.validate(instance=db, schema=schema)


def test_db_schema_2fail():
    """Validate faulty dummy json with schema."""
    db = {
        "version": "0.0.1",
        "flashlights": [
            {
                "id": "002",
                "model": "TS10",
                "status": "stolen",
                "configuration": "stock",
                "measures": [
                    {
                        "date": "2022-07-21",
                        "mod": "og",
                        "level": "1-150",
                        "ciex": 0.3418,
                        "ciey": 0.3518,
                    }
                ],
            }
        ],
    }

    with open("data/sotc.schema") as j:
        schema = json.load(j)

    with pytest.raises(jsonschema.exceptions.ValidationError) as exc:
        jsonschema.validate(instance=db, schema=schema)

    assert exc.type == jsonschema.exceptions.ValidationError
