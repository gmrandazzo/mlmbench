# MLMBench - MachineLearning Molecular Benchmarch
MLMBench collects datasets and splits to do FAIR ML benchmarks.
MLMBench can be used with different ML algorithms and data representations
for molecular property/activity predictions.

The scope of this code is to keep a simple API representation
without the need for external libraries and keep the
dataset representation in a widely supported format such as CSV (RFC 4180 standard).


Splits are made using well known rational approaches such as:

- random split
- meaningful split for model target extrapolation
- meaningful split for chemical diversity extrapolation

The datasets are stored into the "data" directory in subfolders.
Every subfloder needs the following files with the following names:

- Readme.txt: explain some dataset info (provenience, type of data, descriptors version and so on)
- cv.splits: the split required to do a fair trainin,test,validation in any ml algorithm
- dataset.csv: the matrix of features 
- target.csv: the matrix of target/targets
- dataset.smi: the smiles list


How to use
----------

```
#!/usr/bin/env python3

from mlmbench.data import Datasets

ds = Datasets()
print(ds.get_available_datasets())

for train_data, test_data, val_data in ds.ttv_generator("esol-random"):
    print("train ", train_data["xdata"].shape, train_data["target"].shape, len(train_data["smi"]))
    print("test ", test_data["xdata"].shape, test_data["target"].shape, len(test_data["smi"]))
    print("val ", val_data["xdata"].shape, val_data["target"].shape, len(val_data["smi"]))
    
    # Do ml training/test validation, collect the results and store it in your 
    # appropriate format to do your analysis.

    print("-"*40)


```

