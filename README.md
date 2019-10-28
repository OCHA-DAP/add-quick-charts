Add Quickcharts to datasets
===========================

Copy a Quick Charts config from a single model dataset to multiple other datasets.

Usage:

    $ cp config.py.TEMPLATE config.py
    $ vi config.py # set values as needed
    $ pip3 install -r requirements.txt
    $ python3 add-quick-charts.py <model> <pattern> <org>
    
**model** - the HDX dataset identifier of the model dataset to use for Quick Charts

**pattern** - a regular expression matching the identifiers of the datasets to be updated (the model will be skipped)

**org** - the HDX org identifier for the datasets being processed


## Example

The _sample_ org has created datasets for every country, following the pattern _sample-data-<iso3>_. You manually create Quick Charts for one of those datasets, _sample-data-nld_, then use this command to copy the charts to all of the other datasets (using the regular expression "sample-data-..." to match any dataset):

```
$ python3 add-quick-charts.py sample-data-nld sample-data-... sample
```

## License

This code is released into the Public Domain, and comes with NO WARRANTY.