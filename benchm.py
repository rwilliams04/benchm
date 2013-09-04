#!/usr/bin/env python

import time
import sys
import subprocess

import numpy as np

'''
Format of BENCH-INPUT file is 

[number of trials] [command line]

3
sleep 1  (run "sleep 1" three times)
sleep 2  (run "sleep 2" three times)
'''

def main():

    tests = open('BENCH-INPUT','r').readlines()

    trials = int(tests[0])
    testresults = []
    for line in tests[1:]:
        test = line.split()
        exe = test[0]
        args = test[1:]
        trialtimes = runit(exe,args,trials)
        testresults.append(trialtimes)

    print_report(testresults)
    

def runit(exe,args,trials=3):

    trialtimes = []

    for i in xrange(0,trials):
        t = get_runtime(exe,args)
        trialtimes.append(t)

    return trialtimes

def get_runtime(exe,args):

    pass2call = [exe]
    [pass2call.append(a) for a in args]

    t1 = time.time()

    subprocess.call(pass2call)

    t2 = time.time()

    return t2-t1

def print_report(testresults):

    alloutput = []
    for trialtimes in testresults: 

        testoutput = []

        for trial in trialtimes:
            testoutput.append(",%f" % trial)

        testoutput.append("Trials,%i" % len(trialtimes))
        testoutput.append("Average,%f" % np.average(trialtimes))
        testoutput.append("Mean,%f" % np.mean(trialtimes))
        testoutput.append("Median,%f" % np.median(trialtimes))
        testoutput.append("StdDev,%f" % np.std(trialtimes))
        testoutput.append("Variance,%f" % np.var(trialtimes))
        
        alloutput.append(testoutput)

    for i in xrange(0,len(alloutput[0])):
        print ','.join(test[i].ljust(20) for test in alloutput)

        

if __name__ == '__main__':
    main()
