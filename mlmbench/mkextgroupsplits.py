#!/usr/bin/env python3
# mkextgroupsplits.py mlmbench
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
    if len(sys.argv) != 3:
        print("\nUsage: %s [manual group split] [splits output]" % (sys.argv[0]))
        print("\n The manual group splits should be a csv file with fist column")
        print(" the name of the molecule; second column the membership group.")
        print("\n")
        exit()

    f = open(sys.argv[1], "r")
    o = open(sys.argv[2], "w")
    groups = {}
    for line in f:
        if "Molecule" in line:
            continue
        else:
            v = line.split(",")
            if v[1] in groups.keys():
                groups[v[1]].append(v[0])
            else:
                groups[v[1]] = [v[0]]

    names = []
    for key in groups.keys():
        names.extend(groups[key])

    for key in groups.keys():
        val_keys = groups[key]
        subset = [n for n in names if n not in val_keys]
        train_keys, test_keys = train_test_split(subset,test_size=0.2)
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
