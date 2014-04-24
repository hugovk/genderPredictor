#!/usr/bin/env python
# encoding: utf-8
"""
fi_loader.py
"""
import glob
import csv
import os
import pickle


def getNameList():
    if not os.path.exists('fi_names.pickle'):
        print('fi_names.pickle does not exist, generating')

        print('Extracting names from names.zip')
        namesDict = get_names_from_txts()

        maleNames = list()
        femaleNames = list()

        print('Sorting names')
        for name in namesDict:
            counts = namesDict[name]
            tuple = (name, counts[0], counts[1])
            if counts[0] > counts[1]:
                maleNames.append(tuple)
            elif counts[1] > counts[0]:
                femaleNames.append(tuple)

        names = (maleNames, femaleNames)

        print('Saving fi_names.pickle')
        fw = open('fi_names.pickle', 'wb')
        pickle.dump(names, fw, -1)
        fw.close()
        print('Saved fi_names.pickle')
    else:
        print('fi_names.pickle exists, loading data')
        f = open('fi_names.pickle', 'rb')
        names = pickle.load(f)
        print('fi_names.pickle loaded')

    print('%d male names loaded, %d female names loaded' % (len(names[0]), len(names[1])))
    return names


def get_names_from_txts():
    filenames = glob.glob('finnish_*male_given_names.txt')

    names = dict()

    for filename in filenames:
        file = open(filename, 'r')
        rows = csv.reader(file, delimiter=',')

        for row in rows:
            name = row[0].lower()
            if "_male_" in filename:
                gender = 0
            elif "_female_" in filename:
                gender = 1
            count = 1
            if name not in names:
                names[name] = [0, 0]
            names[name][gender] = names[name][gender]+count
        file.close()

        print('\tImported %s' % filename)
    return names

if __name__ == "__main__":
    getNameList()

# End of file
