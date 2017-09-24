import os
import sys
import subprocess
import time
import numpy as np
from sklearn import datasets as ds
from sklearn import cluster as cs
import matplotlib.pyplot as plt

reduction_percentages = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
tda_libraries = ['GUDHI','PHAT','Dionysus']
files_to_run = []


def readData(filepath, delim=','):
    data = np.genfromtxt(filepath, delimiter=delim)
    return data

def outputData(data, label):
    np.savetxt(outDir+label+'.csv', data, delimiter=',')
    return

def outputDataDiagram(data,lbl):
    plt.scatter(data[:,0], data[:,1], c='b',label=lbl)
    plt.grid(True, which='both')
    plt.savefig(outDir + lbl + ".pdf")
    #plt.show()
    plt.clf()
    return

def getRValues(filename,tda_type):
    complex_size = ""
    tail_data = ""
    
    with open(filename,'r')as temp:
        temp = temp.readlines()
        if len(temp) > 0:
            tail_data = temp[-1]

            if tda_type == "GUDHI":
                complex_size = temp[0].split(' ')[-2]

            elif tda_type == "PHAT":
                complex_size = temp[0].split(' ')[-2]

            elif tda_type == "Dionysus":
                complex_size = temp[0].split(' ')[-2]
    os.remove(filename)
    return complex_size + "," + tail_data.rstrip() + "\n"





'''MAIN'''
if len(sys.argv) > 1:
    vectors = 100    

    print "Starting TDA!"
    for farg in sys.argv[1:]:
        files_to_run.append(farg)

    print "Files: " + str(files_to_run)

    

    for filename in files_to_run:
        data = []
        if filename == 'make_moons':
            data = ds.make_moons(vectors, noise=.025)
            data = data[0]
        elif filename == 'make_circles':
            data = ds.make_circles(vectors, noise=.025)
            data = data[0]
        elif filename == 'make_swiss':
            data = ds.make_swiss_roll(vectors, noise=.025)
            data = data[0]
        else:
            data = readData(filename)

        outDir = filename.split('.')[0] + "_output/"
        if not os.path.exists(outDir):
            os.makedirs(outDir)


        #Output Header
        outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
        outfile.write("Source File,Output Directory,Vectors,Dimensions,Reduction %,KMeans++ Time,R PH Library,Epsilon,Complex Size,PH Time,Bottleneck Distance[0],Wasserstein Distance[0],Bottleneck Distance[1],Wasserstein Distance[1],Bottleneck Distance[2...],Wasserstein Distance[2...],...,...\n")
        outfile.close() 


        for reduction in reduction_percentages:
            n_clust = int((1-reduction) * len(data))

            #KMeans++ Data Reduction
            kmeans_time = 0.0
            red_data = data
            if(n_clust != len(data)):
                start = time.time()
                red_data = cs.KMeans(n_clusters = n_clust, n_jobs=-1).fit(data)
                end = time.time()
                red_data = red_data.cluster_centers_
                kmeans_time = (end - start)

            #Output the data for R
            outputData(red_data, str(reduction) + "_Reduction")


            for tda_type in tda_libraries:
                #Output metaData
                outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
                outfile.write(filename + "," + outDir[:-1] + "," + str(len(red_data)) + "," + str(len(red_data[0])) + "," + str(reduction) + "," + str(kmeans_time) + "," + tda_type + ",")
                outfile.close() 


                #Call R for processing
                returnCode = subprocess.call(["Rscript",os.getcwd()+"/TDA_testRScript.r",".5","2",os.getcwd()+"/"+outDir,str(reduction) + "_Reduction",tda_type])

                #Extract PH Execution Time, complex size from temp output file
                outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
                outfile.write(getRValues(os.getcwd() + "/" + outDir +"r_temp.txt", tda_type))
                outfile.close() 
        

            outputDataDiagram(red_data,str(reduction) + "% reduction")

else:
    print "Requires filename or generation arguments to run. \n\n\tGeneration options: ['make_moons', 'make_circles'].\n"

