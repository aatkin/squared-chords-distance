# -*- coding: utf-8 -*-

import sys
import os
import math
import csv
import json

import numpy as np

from error_codes import Error

# credits: http://stackoverflow.com/questions/5574702/ddg#14981125
def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def err_to_json(type, obj):


def read_data(data):
    try:
        read_data = np.genfromtxt(
            data, dtype=None, delimiter=';', skip_header=1)
        return read_data
    except Exception as e:
        print_err(str(e) + '\n')
        print_err('Could not read data from ' + data + '\n'
              'Check data validity and/or fix it, and try again.\n'
              '\nExiting program with error')
        sys.exit(Error.BAD_FILE)


def check_training_data(data):
    features_len = len(data[0])
    for row in data:
        if len(row) != features_len:
            print_err('error: inconsistent amount of features in training data')
            sys.exit(Error.INCONSISTENT_DATA_TRAINING)
    return True


def check_test_data(data1, data2):
    # ensure all features exist
    features_len = len(data1[0])
    for row in data1:
        if len(row) != features_len:
            print_err('error: inconsistent amount of features in training data')
            sys.exit(Error.INCONSISTENT_DATA_TRAINING)
    for row in data2:
        if len(row) != features_len:
            print_err('error: inconsistent amount of features in test data')
            sys.exit(Error.INCONSISTENT_DATA_TEST)
    return True


# squared chord distance is defined as sum pow(sqrt(x_i) - sqrt(y_i), 2)
# aka euclidean squared distance
def squared_chord_distance(vec1, vec2):
    result = 0
    for a, b in zip(vec1, vec2):
        val = math.pow(math.sqrt(a) - math.sqrt(b), 2)
        result += val
    return result


def calculate_training_sqcds(data, lakes):
    result = []
    result.append([None] + lakes)
    for index, lake in enumerate(lakes):
        lake_distances = []
        lake_distances.append(lakes[index])
        for feature in data:
            lake_distances.append(squared_chord_distance(
                list(data[index])[1:], list(feature)[1:]))
        result.append(lake_distances)
    return result


def calculate_test_sqcds(test_data, training_data, test_lakes, training_lakes):
    result = []
    result.append([None] + training_lakes)
    for test_index, test_lake in enumerate(test_lakes):
        lake_distances = []
        lake_distances.append(test_lake)
        for training_index, training_lake in enumerate(training_lakes):
            lake_distances.append(squared_chord_distance(
                list(test_data[test_index])[1:],
                list(training_data[training_index])[1:]))
        result.append(lake_distances)
    return result


def write_to_csv(data, filename):
    with open(filename, 'wb') as fp:
        writer = csv.writer(fp, delimiter=';')
        writer.writerows(data)


def extract_lakes(data):
    lakes = []
    for row in list(data):
        lakes.append(row[0])
    return lakes

def training_sqcd(filename, output_path):
    data = read_data(filename)
    if check_training_data(data):
        lakes = extract_lakes(data)
        result_data = calculate_training_sqcds(data, lakes)
        write_to_csv(result_data, output_path)

def test_sqcd(training_filename, test_filename, output_path):
    training_data = read_data(training_filename)
    test_data = read_data(test_filename)
    if check_test_data(training_data, test_data):
        training_lakes = extract_lakes(training_data)
        test_lakes = extract_lakes(test_data)
        result_data = calculate_test_sqcds(
            test_data, training_data, test_lakes, training_lakes)
        write_to_csv(result_data, output_path)

def sqcd(training, test):
    tr_data = read_data(training)
    test_data = read_data(test)
    data = { "training": len(tr_data[0]), "test": len(test_data[0]) }
    print(json.dumps(data))
