#!/usr/bin/env python3

class CSVTable(object):
    def __init__(self):
        self.data = {}
        self.header = []
        return


def read_data_csv(csvtab):
    """
    Read a CSV table and save it into a dictionary where keys are the
    compound names. The header is instead saved into a list.
    """
    tab = CSVTable()

    f = open(csvtab, "r")
    for line in f:
        v = str.split(line.strip(), ",")
        if "Molecule" in line:
            tab.header = v[1:]
        else:
            tab.data[v[0]] = v[1:]
    f.close()
    return tab


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
