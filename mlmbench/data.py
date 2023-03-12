"""
mlmbench - iodata.py

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

from pathlib import Path
import numpy as np
from iodata import read_smi
from iodata import read_splits
from iodata import read_data_csv


class Datasets():
    """
    Datasets class defition.
    This class will read all the datasets present into "data"
    and will load it into memory. So the user from this will be
    able to read training, test and validation sets and to
    ml model comparisson with high reproducibility.
    """
    def __init__(self,):
        self.dsets = {}
        self.load_datasets()


    def load_datasets(self,):
        """
        Load the dataset availables into "data" folder
        """
        datadir = str(Path(__file__).parent.resolve())+"/data"
        for item in Path(datadir).glob("*"):
            if Path(f'{str(item)}/dataset.csv').exists():
                fxdata = Path(f'{str(item)}/dataset.csv').absolute()
            else:
                fxdata = None

            if Path(f'{str(item)}/target.csv').exists():
                ftarget = Path(f'{str(item)}/target.csv').absolute()
            else:
                ftarget = None

            if Path(f'{str(item)}/dataset.smi').exists():
                fsmi = Path(f'{str(item)}/dataset.smi').absolute()
            else:
                fsmi = None

            if Path(f'{str(item)}/cv.splits').exists():
                fsplits = Path(f'{str(item)}/cv.splits').absolute()
            else:
                fsplits = None
            self.dsets[item.stem] = {"fxdata": fxdata,
                                     "ftarget": ftarget,
                                     "fsplits": fsplits,
                                     "fsmi": fsmi,
                                     # data
                                     "xdata": None,
                                     "target": None,
                                     "smi": None,
                                     "splits": None}

    def get_available_datasets(self,):
        """
        Get all available dataset names
        """
        return self.dsets.keys()

    def get_target_type(self, name):
        y = np.array(list(self.dsets[name]["target"].data.values()),
                     dtype=float)
        if np.equal(y, y.astype(int)).all():
            if y.shape[1] > 1:
                if y[0].sum() > 1:
                    return "multi-label classification"
                else:
                    return "multi-class classification"
            else:
                return "single-class classification"
        else:
            if y.shape[1] > 1:
                return "multi-task regression"
            else:
                return "single-task regression"

    def get_info(self, name):
        """
        Get info regarding the dataset
        """
        if name in self.dsets.keys():
            if self.dsets[name]["xdata"] is None:
                self.get_dataset(name)
            nobjects = len(self.dsets[name]["xdata"].data.keys())
            nfeatures = len(self.dsets[name]["xdata"].header)
            ntargets = len(self.dsets[name]["target"].header)
            dataset_type = self.get_target_type(name)
            return nobjects, nfeatures, ntargets, dataset_type
        else:
            return None, None, None

    def get_dataset(self, name):
        """
        Get a dataset by name and it return a dictionary which is an entire
        dataset itself in memory.
        """
        if name in self.dsets.keys():
            if self.dsets[name]["fxdata"] is not None:
                if self.dsets[name]["xdata"] is None:
                    self.dsets[name]["xdata"] = read_data_csv(self.dsets[name]["fxdata"])
            else:
                self.dsets[name]["xdata"] = None

            if self.dsets[name]["ftarget"] is not None:
                if self.dsets[name]["target"] is None:
                    self.dsets[name]["target"] = read_data_csv(self.dsets[name]["ftarget"])
            else:
                self.dsets[name]["target"] = None

            if self.dsets[name]["fsmi"] is not None:
                if self.dsets[name]["smi"] is None:
                    self.dsets[name]["smi"] = read_smi(self.dsets[name]["fsmi"])
            else:
                self.dsets[name]["smi"] = None

            if self.dsets[name]["fsplits"] is not None:
                if self.dsets[name]["splits"] is None:
                    self.dsets[name]["splits"] = read_splits(self.dsets[name]["fsplits"])
            else:
                self.dsets[name]["splits"] = None

            return {"xdata": self.dsets[name]["xdata"],
                    "target": self.dsets[name]["target"],
                    "smi": self.dsets[name]["smi"],
                    "splits": self.dsets[name]["splits"]}
        else:
            return None

    def get_data(self, data, key):
        """
        Check if a data exists and contain a key
        """
        if data is not None and isinstance(data, dict):
            if key in data.keys():
                return data[key]
            else:
                return None
        else:
            return None

    def make_set(self, dataset, keys):
        """
        Giving a set of keys, from a dataset this method create
        a set of X, target, smiles data.
        """
        xdata = []
        target = []
        smi = []
        for key in keys:
            xdata_row = self.get_data(dataset["xdata"].data, key)
            target_row = self.get_data(dataset["target"].data, key)
            smi_row = self.get_data(dataset["smi"], key)
            if xdata_row != None and target_row != None:
                xdata.append(xdata_row)
                target.append(target_row)
                smi.append(smi_row)
            else:
                continue

        return {"xdata": np.array(xdata, dtype=float),
                "target": np.array(target, dtype=float),
                "smi": smi}

    def ttv_generator(self, name):
        """
        Generate a train,test and validation by name
        """
        dataset = self.get_dataset(name)
        for split in dataset["splits"]:
            train_data = self.make_set(dataset, split["train_keys"])
            test_data = self.make_set(dataset, split["test_keys"])
            val_data = self.make_set(dataset, split["val_keys"])
            yield [train_data,
                   test_data,
                   val_data,
                   split["train_keys"],
                   split["test_keys"],
                   split["val_keys"]]

if __name__ in "__main__":
    ds = Datasets()
    print("Test ESOL")
    print(ds.get_info("NIR_Gasoline-random"))
    for train_data, test_data, val_data, _, _, _ in ds.ttv_generator("NIR_Gasoline-random"):
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
