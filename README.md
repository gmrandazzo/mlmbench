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


