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


def run_join(prog, algo, size_r, size_s, threads, reps, m):
    f = open("../data/wait_time_mutex_spinlock" + m + "-output.csv", "a")
    for i in range(0, reps):
        stdout = subprocess.check_output(prog + " -a " + algo + " -x " + str(size_r) + " -y " + str(size_s) +
                                         " -n " + str(threads), cwd="../../", shell=True) \
            .decode('utf-8')
        throughput = -1
        time_mutex = -1
        total_time = -1
        for line in stdout.splitlines():
            if "throughput =" in line:
                throughput = re.findall("\d+\.\d+", line)[1]
            elif "Time waited on mutex avg:" in line:
                time_mutex = re.findall("\d+\.\d+", line)[1]
            elif "Total join runtime:" in line:
                total_time = re.findall("\d+\.\d+", line)[1]
        s = (m + "," + algo + "," + str(threads) + "," + str(round(size_r, 2)) +
             "," + str(round(size_s, 2)) + "," + str(round(float(throughput), 2)) + "," + str(
                    round(float(time_mutex), 4)) + "," + str(round(float(total_time), 4)))
        print("Run " + str(i) + ": " + s)
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

    for mode in ['sgx']:
        filename = "../data/wait_time_mutex_spinlock" + mode + "-output.csv"
        if config['experiment']:
            commons.compile_app(mode, enclave_config_file='Enclave/Enclave8GB.config.xml',
                                flags=["TIME_MUTEX", "SPIN_LOCK"])
            commons.remove_file(filename)
            commons.init_file(filename, "mode,alg,threads,sizeR,sizeS,throughput,waitTimeMutex,totalTime\n")
            for t in range(1, 16, 1):
                for alg in ["RHO"]:
                    run_join(commons.PROG, alg, 512,1000, t, 20, mode)

        # plot(filename,l)
        # plot_with_ewb()
        commons.stop_timer(timer)
