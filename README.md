# MLMBench - MachineLearning Molecular Benchmarch

![Page views](https://visitor-badge.glitch.me/badge?page_id=gmrandazzo.mlmbench)
[![Licence: GPL v3](https://img.shields.io/github/license/gmrandazzo/mlmbench)](https://github.com/gmrandazzo/mlmbench/blob/master/LICENSE)

MLMBench collects datasets and splits them to do FAIR ML benchmarks.
MLMBench can be used with different ML algorithms and data representations
for molecular property/activity predictions and more.

The scope of this code is:
- keep a simple API representation
- no need of other libraries
- keep the dataset offline and represented as CSV file (RFC 4180 standard) or SMILES string list.


Splits are made using well-known rational approaches such as:

- random split
- meaningful split for model target extrapolation
- meaningful split for chemical diversity extrapolation
- literature published split

The datasets are stored in the "data" directory in subfolders.
Every subfolder needs the following files with the following names:

- Readme.txt: explain some dataset info (provenience, type of data, descriptors version, and so on)
- cv.splits: the split required to do a fair trainin, test, validation in any ml algorithm
- dataset.csv: the matrix of features 
- target.csv: the matrix of target/targets
- dataset.smi: the smiles list

Install
-------

```

pip3 install mlmbench

```

Split types per dataset
-----------------------
mlmbench includes for every dataset two different splits:
- random split using "mkrndsplits.py" starting from a list of names
- target extrapolation using "mktgtextrapsplits.py" starting from the target file.
  In this case, the algorithm will first import the target file, and then for every column,
  rank from min to max the queue and split the ordered target
  into "N" splits selected by the user. This split aims to check for "extrapolation."
- literature split (if available). In this case, we try to preserve particular splits published by users.

Available datasets
------------------

- BACE-moleculenet
- BACE-random
- BACE-tgt_extrapolation
- FU-random
- FU-tgt_extrapolation
- HLMCLint-random
- HLMCLint-tgt_extrapolation
- MeltingPoint-random
- MeltingPoint-tgt_extrapolation
- NIR_Gasoline-random
- NIR_Gasoline-tgt_extrapolation
- SteroidsLSS-isomers
- SteroidsLSS-random
- SteroidsLSS-tgt_extrapolation
- esol-chemdiversity
- esol-random
- esol-tgt_extrapolation
- logDpH7.4-random
- logDpH7.4-tgt_extrapolation

How to use
----------

```
#!/usr/bin/env python3

from mlmbench.data import Datasets

ds = Datasets()
print(ds.get_available_datasets())
print(f'Dataset info: {ds.get_info("esol-random")}')
for train_data, test_data, val_data in ds.ttv_generator("esol-random"):
    print("train ", train_data["xdata"].shape, train_data["target"].shape, len(train_data["smi"]))
    print("test ", test_data["xdata"].shape, test_data["target"].shape, len(test_data["smi"]))
    print("val ", val_data["xdata"].shape, val_data["target"].shape, len(val_data["smi"]))
    
    # Do ml training/test validation, collect the results and store it in your 
    # appropriate format to do your analysis.

    print("-"*40)

```

Submit new dataset
__________________

1) Fork the project!
2) Clone the forked project
3) Add the dataset in this form:
    dataset.csv: tabular data for any kind of descriptors
    target.csv: tabular data for one or multiple targets
    dataset.smi: smiles of the molecule in its appropriate format "c1ccccc1 benzene"
    cv.split: The split you like. This specific file needs to be compatible with the following
    	      standard. The file comprises lines representing the model,
    	      groups split by the ";" character, and every group representing
    	      the compound name, and every name is split using the "," character.
    i.e.
           train keys           test keys            validation keys
    line 1  mol1,mol2,mol3,.. ; mol200,mol201,... ; mol400,mol401,...
    line 2  ...
    line 3  ..

    Readme.md: Info regarding the dataset(i.e. source and so on)
4) Create a pull request and 99.9% will be merged

