# Script to summarize benchmark trials
# Run with: python benchmarksummary.py inputdirs.txt > outputfile

import natsort
import os
import sys
import numpy as np
import string
import fileinput
import csv

origdir = os.getcwd()
alltestdata = list()

for line in fileinput.input():

        currentdir = line.rstrip('\n')
        os.chdir(currentdir)

        #Store all file names in directory
        allfiles = os.listdir(".")

        #Store the files with "clock" in the file name
        timefiles = [s for s in allfiles if "clock" in s]

        #Prepare to remove all non-digits in file name for sorting
        all=string.maketrans('','')
        nodigs=all.translate(all, string.digits)

        digtimefiles = list()

        #Remove all non-digits from file names
        for i in xrange(0,len(timefiles)):
               digtime=timefiles[i].translate(all, nodigs)
               digtimefiles.append(digtime)

        #Use natsort module to create an index for the sorted digit-only files
        sortindex = natsort.index_natsorted(digtimefiles)

        #Apply the new index to the file list
        timefiles = [timefiles[int(i)] for i in sortindex]

        #List containing the wall times for test
        testtimes = list()

        #Loop through each file name
        for tfile in timefiles:
                with open(tfile) as f:
                        #Loop through each line in file to find string "real" and store the corresponding time value 
                        for line in f:
                                if "real" in line:
                                        walltime = line.split(" ")[1]
                                        testtimes.append(walltime)
        #Convert test time strings to float
        numtesttimes = [float(x.strip(' "')) for x in testtimes]
        alltestdata.append(numtesttimes)

        #Return to original directory
        os.chdir(origdir)

arraytestdata = np.array(alltestdata)
#Summary stats

meantestdata = np.mean(arraytestdata, axis=0)
mediantestdata = np.median(arraytestdata, axis=0)
stdtestdata = np.std(arraytestdata, axis=0)
vartestdata = np.var(arraytestdata, axis=0)

sarraytestdata = np.vstack((meantestdata,mediantestdata,stdtestdata,vartestdata))
summaryarray = np.vstack((arraytestdata, sarraytestdata))

summaryarray = np.transpose(summaryarray)

triallist = ['Trial ' + str(i) for i in xrange(1,len(arraytestdata)+1)]
headerlist = triallist + (['Mean', 'Median', 'Std', 'Var'])

#Write summary array data to text file
with open('benchmark_summary.csv', 'wb') as f:
        f.write(bytes(headerlist))
        f.write(b'\n')
        np.savetxt(f, summaryarray, delimiter=',', fmt='%10.3f')
 
