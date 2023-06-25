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
    f = open("../data/scale-" + mode + "-output_correct.csv", "a")
    results = []
    ewbs = []
    for i in range(0, reps):
        stdout = subprocess.check_output(prog + " -a " + alg + " -r " + str(size_r) + " -s " + str(size_s) +
                                         " -n " + str(threads) , cwd="../../", shell=True) \
            .decode('utf-8')
        for line in stdout.splitlines():
            if "Throughput" in line:
                throughput = re.findall("\d+\.\d+", line)[1]
                results.append(float(throughput))
                print("Throughput = " + str(throughput))
            elif "EWB :" in line:
                ewb = int(re.findall(r'\d+', line)[-2])
                print("EWB = " + str(ewb))
                ewbs.append(ewb)
    if len(results) == 0:
        results = [-1]
    if len(ewbs) == 0:
        ewbs = [-1]
    res = statistics.mean(results)
    ewb = int(statistics.mean(ewbs))
    s = (mode + "," + alg + "," + str(threads) + "," + str(round(size_r / mb_of_data, 2)) +
         "," + str(round(size_s / mb_of_data, 2)) + "," + str(round(res, 2)) + "," + str(ewb))
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

    max_r_size_mb = 2500
    s_sizes = [1 * mb_of_data,  # 1MB
               16 * mb_of_data,  # 16 MB
               28 * mb_of_data,  # 28 MB
               512 * mb_of_data]  # 512 MB
    for mode in ['sgx','native']:
        filename = "../data/scale-" + mode + "-output_correct.csv"
        if config['experiment']:
            commons.compile_app(mode, enclave_config_file='Enclave/Enclave11GB.config.xml')  # , flags=["SGX_COUNTERS"])
            commons.remove_file(filename)
            commons.init_file(filename, "mode,alg,threads,sizeR,sizeS,throughput,ewb\n")

            for s_size in s_sizes:
                for alg in ['INL']:
                    for i in range(500, max_r_size_mb + 1, 500):  # range(50, max_r_size_mb + 1, 50):
                        run_join(commons.PROG, alg,  i * mb_of_data,s_size, config['threads'], config['reps'], mode)

        commons.stop_timer(timer)
