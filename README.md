Add Quickcharts to datasets
===========================

Copy a Quick Charts config from a single model dataset to multiple other datasets.

Usage:

    $ cp config.py.TEMPLATE config.py
    $ vi config.py # set values as needed
    $ pip3 install -r requirements.txt
    $ python3 add-quick-charts.py <model> <org> <pattern>
    
<model> - the HDX dataset identifier of the model dataset to use for Quick Charts
<org> - the HDX org identifier for the datasets being processed
<pattern> - a regular expression matching the identifiers of the datasets to be updated (the model will be skipped)


