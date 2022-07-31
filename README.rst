chroma-spec
===========

.. readme-only-start
.. image:: data/SOTC/E14_III/E14_III.svg
.. readme-only-end

This package is aimed at generating reliable and standardised chromatic graphs for flashligth enthousiasts.

Features
--------

* TODO

Requirements
------------

* TODO

The State Of The Collection(SOTC) database
------------------------------------------

A sample entry in the database:

.. code-block:: json

    {
        "version": "0.0.1",
        "flashlights": [
            {
                "id": "001",
                "model": "TS10",
                "status": "owned",
                "configuration": "stock",
                "measures": [
                    {
                        "date": "2022-07-21",
                        "mod": "og",
                        "level": "1-150",
                        "ciex": 0.3418,
                        "ciey": 0.3518
                    }
                ]
            }
        ]
    }


An associated schema is provided to insure json validity.
