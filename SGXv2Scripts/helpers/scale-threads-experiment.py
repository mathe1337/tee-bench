#!/usr/bin/python3
import getopt
import sys

import yaml

import commons
import re
import statistics
import subprocess
import csv
import matplotlib.pyplot as plt

filename1 = "../data/scale-r-sgx-output.csv"
filename2 = "../data/scale-r-sgx-output.csv"
mb_of_data = 131072


def run_join(prog, alg, size_r, size_s, threads, reps, mode):
    f = open("../data/scale-threads-" + m + "-output.csv", "a")
    results = []
    for i in range(0, reps):
        stdout = subprocess.check_output(prog + " -a " + alg + " -x " + str(size_r) + " -y " + str(size_s) +
                                         " -n " + str(threads), cwd="../../", shell=True) \
            .decode('utf-8')
        for line in stdout.splitlines():
            if "Throughput" in line:
                throughput = re.findall("\d+\.\d+", line)[1]
                results.append(float(throughput))
                print("Throughput = " + str(throughput))
    if len(results) == 0:
        results = [-1]
    res = statistics.mean(results)
    s = (mode + "," + alg + "," + str(threads) + "," + str(round(size_r, 2)) +
         "," + str(round(size_s)) + "," + str(round(res, 2)))
    print("AVG : " + s)
    f.write(s + "\n")
    f.close()


if __name__ == '__main__':
    timer = commons.start_timer()
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv, 'r:', ['reps='])
        except getopt.GetoptError:
            print('Unknown argument')
            sys.exit(1)
        for opt, arg in opts:
            if opt in ('-r', '--reps'):
                config['reps'] = int(arg)

    for m in ['sgx', 'native']:
        filename = "../data/scale-threads-" + m + "-output.csv"
        if config['experiment']:
            commons.compile_app(m, enclave_config_file='Enclave/Enclave16GB.config.xml')  # , flags=["SGX_COUNTERS"])
            commons.remove_file(filename)
            commons.init_file(filename, "mode,alg,threads,sizeR,sizeS,throughput\n")

            for t in [2 ** x for x in range(0, 6)]:
                for alg in commons.get_all_algorithms_extended():
                    run_join(commons.PROG, alg, 512, 2500, t, 5, m)
