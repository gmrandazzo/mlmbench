#!/usr/bin/env python3
import string
from pathlib import Path


def read_data_csv(csvtab):
    """
    Read a CSV table and save it into a dictionary where keys are the
    compound names. The header is instead saved into a list.
    """
    tab = {}
    header = None
    f = open(csvtab, "r")
    for line in f:
        v = str.split(line.strip(), ",")
        if "Molecule" in line:
            header = v[1:]
        else:
            tab[v[0]] = v[1:]
    f.close()
    return tab, header


def read_splits(fsplits):
    """
    Read the splits file. This is a specific file that needs
    to be engineered to be compatible with this method.
    The file is composed in lines which represent the model,
    groups splited by the "\t" character and every group represent
    the compound name and every name is splitted using "," character.
    i.e.
            train keys           test keys            validation keys
    line 1  mol1,mol2,mol3,.. \t mol200,mol201,... \t mol400,mol401,...
    line 2  ...
    line 3  ..
    """
    splits = []
    f = open(fsplits, "r")
    for line in f:
        v = str.split(line.strip(), ";")
        train_keys = v[0].split(",")
        test_keys = v[1].split(",")
        val_keys = v[2].split(",")
        splits.append({"train_keys": train_keys,
                       "test_keys": test_keys,
                       "val_keys": val_keys
                      })
    f.close()
    return splits


def read_smi(fsmi):
    """
    Read a smile list and save it into a dictionary where keys are the
    compound names
    """
    smi = {}
    f = open(fsmi, "r")
    for line in f:
        v = str.split(line.strip(), "\t")
        if len(v) == 2:
            smi[v[1]] = v[0]
        else:
            print("Problem with %s" % (line.strip()))
    f.close()
    return smi


def make_set(dataset, keys):
    """
    Giving a set of keys, from a dataset this method create
    a set of X, target, smiles data.
    """
    xdata = []
    target = []
    smi = []
    for key in keys:
        try:
            xdata_row = dataset["xdata"][key]
            target_row = dataset["target"][key]
            smi_row = dataset["smi"][key]
            xdata.append(xdata_row)
            target.append(target_row)
            smi.append(smi_row)
        except:
            continue
    return xdata, target, smi


class Datasets(object):
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
        return


    def load_datasets(self,):
        """
        Load the dataset availables into "data" folder
        """
        datadir = str(Path(__file__).parent.resolve())+"/../data"
        for item in Path(datadir).glob("*"):
            fxdata = str(item)+"/dataset.csv"
            ftarget = str(item)+"/target.csv"
            fsmi = str(item)+"/dataset.smi"
            fsplits = str(item)+"/cv.splits"
            if(Path(fxdata).exists() and
               Path(fsplits).exists() and
               Path(fsmi).exists() and
               Path(ftarget).exists()):
                self.dsets[item.stem] = {"fxdata": fxdata,
                                         "ftarget": ftarget,
                                         "fsplits": fsplits,
                                         "fsmi": fsmi,
                                         # data
                                         "xdata": None,
                                         "target": None,
                                         "smi": None,
                                         "splits": None}
            else:
                print("Problem with the dataset %s" % (item))
        return


    def get_available_datasets():
        """
        Get all available dataset names
        """
        return self.dsets.keys()


    def get_dataset(self, name):
        """
        Get a dataset by name and it return a dictionary which is an entire
        dataset itself in memory.
        """
        if name in self.dsets.keys():
            if self.dsets[name]["xdata"] is None:
                self.dsets[name]["xdata"] = read_data_csv(self.dsets[name]["fxdata"])

            if self.dsets[name]["target"] is None:
                self.dsets[name]["target"] = read_data_csv(self.dsets[name]["ftarget"])

            if self.dsets[name]["smi"] is None:
                self.dsets[name]["fsmi"] = read_smi(self.dsets[name]["fsmi"])

            if self.dsets[name]["splits"] is None:
                self.dsets[name]["splits"] = read_splits(self.dsets[name]["fsplits"])

            return {"xdata": self.dsets[name]["xdata"],
                    "target": self.dsets[name]["target"],
                    "smi": self.dsets[name]["smi"],
                    "splits": self.dsets[name]["splits"]}
        else:
            return None


if __name__ in "__main__":
    ds = Datasets()
    ds.get_dataset("esol")
