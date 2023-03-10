#!/usr/bin/env python3
# mktgtextrapsplits.py mlmbench
#
# Copyright (C) <2022>  Giuseppe Marco Randazzo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sys
import numpy as np
from iodata import read_data_csv
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split

def write_to_file(f, lst):
    f.write("%s" % (lst[0]))
    for i in range(1, len(lst)):
        f.write(",%s" % (lst[i]))
    return

def main():
    if len(sys.argv) != 4:
        print("\nUsage: %s [target csv] [splits output] [n splits]" % (sys.argv[0]))
        print("\nThe number of repetitions depends on the number of target to consider")
        exit()

    tgt = read_data_csv(sys.argv[1])

    o = open(sys.argv[2], "w")
    n_splits = int(sys.argv[3])
    """
    Algorithm:
    1) For each target we create a matrix of name,value and we order this
       matrix from the min to the max value.
    2) we split this ordered matrix into n_splits part
    3) For each split, consider this split as validation part and the rest as
       subset to be divided into training/test using a random selection approach
    4) Continue until the number of splits ends for any target.
    """

    for tgtid in range(len(tgt.header)):
        lst = []
        for key in tgt.data.keys():
            lst.append([key, tgt.data[key][tgtid]])

        lst = sorted(lst,key=lambda x: x[1])

        splits = np.array_split(lst, n_splits)
        for i in range(len(splits)):
            subset_keys = []
            val_keys = None
            for j in range(len(splits)):
                if i == j:
                    val_keys = [row[0] for row in splits[j]]
                else:
                    subset_keys.extend([row[0] for row in splits[j]])

            train_keys, test_keys = train_test_split(subset_keys,test_size=0.2)
            # write train
            write_to_file(o, train_keys)
            o.write(";")
            # write test
            write_to_file(o, test_keys)
            o.write(";")
            # write validation
            write_to_file(o, val_keys)
            o.write("\n")
    o.close()

if __name__ in "__main__":
    main()
