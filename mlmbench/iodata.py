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

import csv
import sys


csv.field_size_limit(sys.maxsize)

class CSVTable():
    """
    Data structure CSV Table
    """
    def __init__(self):
        self.data = {}
        self.header = []

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__

def read_data_csv(csvtab):
    """
    Read a CSV table and save it into a dictionary where keys are the
    compound names. The header is instead saved into a list.
    """
    tab = CSVTable()
    with open(csvtab, "r", encoding="utf-8") as _f:
        reader = csv.reader(_f, delimiter=',', quotechar='"')
        for row in reader:
            try:
                if row[0] == "Molecule" or row[0] == "Objects":
                    tab.header = row[1:]
                else:
                    tab.data[row[0]] = [float(item) for item in row[1:]]
            except:
                print(f'Check your input file {csvtab}')
                raise
    return tab


def read_splits(fsplits):
    """
    Read the splits file.
    This is a specific file that needs to be compatible with the following
    standard. The file is composed in lines which represent the model,
    groups splited by the ";" character and every group represent
    the compound name and every name is splitted using "," character.
    i.e.
            train keys           test keys            validation keys
    line 1  mol1,mol2,mol3,.. ; mol200,mol201,... ; mol400,mol401,...
    line 2  ...
    line 3  ..
    """
    splits = []
    with open(fsplits, "r", encoding="utf-8") as _f:
        reader = csv.reader(_f, delimiter=';')
        for row in reader:
            splits.append({"train_keys": row[0].split(","),
                           "test_keys": row[1].split(","),
                           "val_keys": row[2].split(",")})
    return splits


def read_smi(fsmi):
    """
    Read a smile list and save it into a dictionary where keys are the
    compound names
    """
    smi = {}
    with open(fsmi, "r", encoding="utf-8") as _f:
        reader = csv.reader(_f, delimiter='\t')
        for row in reader:
            if len(row) == 2:
                smi[row[1]] = row[0]
            else:
                print(f'Problem with {row}')
    return smi
