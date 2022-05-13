#!/usr/bin/env python3
# mkrndsplits.py mlmbench
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
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split

def write_to_file(f, lst):
    f.write("%s" % (lst[0]))
    for i in range(1, len(lst)):
        f.write(",%s" % (lst[i]))
    return

def main():
    if len(sys.argv) != 5:
        print("\nUsage: %s [name list] [splits output] [n splits] [n repeats]" % (sys.argv[0]))
        exit()

    f = open(sys.argv[1], "r")
    o = open(sys.argv[2], "w")
    n_splits = int(sys.argv[3])
    n_repeats = int(sys.argv[4])
    lst = []
    for line in f:
        lst.append(line.strip())
    f.close()
    lst = np.array(lst)
    for rep in range(n_repeats):
        kf = KFold(n_splits=n_splits, random_state=None, shuffle=True)
        for subset_index, val_index in kf.split(lst):
            train_keys, test_keys = train_test_split(lst[subset_index],test_size=0.2)
            # write train
            write_to_file(o, train_keys)
            o.write(";")
            # write test
            write_to_file(o, test_keys)
            o.write(";")
            # write validation
            write_to_file(o, lst[val_index])
            o.write("\n")
    o.close()

if __name__ in "__main__":
    main()
