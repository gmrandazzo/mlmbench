"""
mlmbench - test.py

Copyright (C) <2022>  Giuseppe Marco Randazzo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from mlmbench.data import Datasets


def print_ds(dataset):
    """
    Print the dataset
    """
    for train_data, test_data, val_data, _, _, _ in dataset:
        print("train ",
              train_data["xdata"].shape,
              train_data["target"].shape,
              len(train_data["smi"]))
        print("test ",
              test_data["xdata"].shape,
              test_data["target"].shape,
              len(test_data["smi"]))
        print("val ",
              val_data["xdata"].shape,
              val_data["target"].shape,
              len(val_data["smi"]))
        print("-"*40)

ds = Datasets()
print(ds.get_available_datasets())

for name in ds.get_available_datasets():
    print(name)
    print_ds(ds.ttv_generator(name))
