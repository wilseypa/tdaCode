import os
import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt

## Argument Parsing

fname = "outputFrom"
fpath = "."
minLength = 0.05
outfile = 'BarCodeResults.pdf'

parser = argparse.ArgumentParser(description='Process and output plots for files matching argument filename')
parser.add_argument('--fname', '-f', help='A string for matching the filename on')
parser.add_argument('--fpath', '-p', help='The filepath of the output files')
parser.add_argument('--minlength', '-m', help='Minimum interval (length) to filter output data on')
parser.add_argument('--outfile', '-o', help='File path for graph output')
args = parser.parse_args()

if(args.fname):
	fname = args.fname
if(args.fpath):
	fpath = args.fpath
if(args.minlength):
	minlength = args.minlength



## File reading, aggregating, and labeling
outputFile = "AggregatedOutput.csv"
oF = open(outputFile, "w+")
oF.write("FileName, Dimension, Birth, Death, Length\n")
maxTime = 0.0;

lof = os.listdir(fpath)
for f in lof:
	if f.find(fname) >= 0:
		with open(f) as csvFile:
			readCSV = csv.reader(csvFile,delimiter=',')
			for row in readCSV:
				if row[0] != "dimension" and (float(row[2]) - float(row[1])) >= minLength:
					oF.write(f + "," + str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(float(row[2])-float(row[1])) + '\n')
				if row[0] != "dimension" and (float(row[2])) > maxTime:
					maxTime = float(row[2])
		
oF.close()



## Plot the resultant data (AggregatedOutput.csv)
a = np.genfromtxt('AggregatedOutput.csv', unpack=True, names=True, delimiter=',', dtype=None)
ind = 0;
lind = [0,0]
labellist = []
d0 = plt.subplot(212)
d1 = plt.subplot(211)
for i in xrange(len(a)):
	curplot = d0		
	lind[a[i][1]] = lind[a[i][1]] + 1
	if a[i][0].find("10") >= 0:
		c = 'red'
	if a[i][0].find("25") >= 0:
		c = 'blue'
	if a[i][0].find("50") >= 0:
		c = 'green'
	if a[i][0].find("75") >= 0:
		c = 'orange'
	if a[i][0].find("Orig") >= 0:
		c = 'gray'
	
	if a[i][1] == 1:
		curplot = d1
	

	if a[i][0] not in labellist and a[i][1] == 1:
		curplot.hlines(lind[a[i][1]],a[i][2],a[i][3], colors=c, label=a[i][0].replace("outputFrom", "").replace(".csv",""))

		labellist.append(a[i][0])
	else:
		curplot.hlines(lind[a[i][1]], a[i][2], a[i][3], colors=c)

d0.set_title('0D Bar Codes')
d1.set_title('1D Bar Codes')
d0.set_xlim(0,maxTime)
d1.set_xlim(0,maxTime)
d0.set_ylim(0,lind[0] + 1)
d1.set_ylim(0,lind[1] + 1)
d0.set_xlabel('Time')
d1.set_xlabel('Time')
d0.set_ylabel('Index')
d1.set_ylabel('Index')

d0.legend(fontsize=8)
d1.legend(fontsize=8)	
plt.subplots_adjust(hspace=.5)
plt.savefig(outfile)
#plt.show()

