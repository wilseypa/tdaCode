import os
import sys
import subprocess
import time
import numpy as np
from math import sqrt
from sklearn import datasets as ds
from sklearn import cluster as cs
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

reduction_percentages = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
tda_libraries = ['GUDHI','SimBa','PHAT','Dionysus']
files_to_run = []
originalData = []
outdir = None


def readData(filepath, delim=','):
    data = np.genfromtxt(filepath, delimiter=delim)
    return data

def outputData(data, label):
    np.savetxt(outDir+label+'.csv', data, delimiter=',')
    a = file(outDir+label+'.csv', 'r')
    lines = a.readlines()
    a.close()
    out = file(outDir+label+'.mat', 'w')
    print len(data[0])
    out.write(str(len(data[0])) + "\n")
    out.writelines(lines)
    out.close()
    return

def outputDataDiagram(data,lbl, pp):
    plt.scatter(data[:,0], data[:,1],label=lbl, marker=".", s=3, color='r')
    plt.title("Point Cloud " + lbl)
    plt.grid(True, which='both')
    plt.savefig(pp, format='pdf')
    #plt.savefig(outDir + lbl + ".pdf")
    #plt.show()
    plt.clf()
    return

def outputOverlayDiagram(data,lbl,data_labels, pp):
    fig=plt.gcf()
    ax=fig.gca()
    ax.set(adjustable='box-forced', aspect='equal')

    
    plt.title("Point Cloud w/ centroids from kmeans++ " + lbl)
    plt.scatter(originalData[:,0], originalData[:,1], marker=".", s=1, color='lightgrey', label="Original")
    plt.scatter(data[:,0], data[:,1], marker=".", s=3,
                  color='r', label=lbl)
    plt.legend()
    plt.grid(True, which='both')
    #plt.axis('off')

    '''WIP: Cluster Avg/Max'''
    if data_labels != []:
        #For each Cluster
        for index in range(0,len(data)):
            #print index
            max_error = 0.0
            avg_error = 0.0
            count = 0.0
            center = [0.0,0.0,0.0,0.0]
            buff = []
            #For each label that matches the current cluster
            for lbl_index in range(0, len(data_labels)):
                if(data_labels[lbl_index] == index):
                    euc = 0
                    for z in range(0, len(originalData[lbl_index])):
                        loc = originalData[lbl_index][z]
                        #print loc, originalData[lbl_index][z], originalData[lbl_index]
                        center[z] += loc
                        euc += loc*loc
                    if euc > max_error:
                        max_error = euc
                    avg_error += sqrt(euc)
                    count += 1
            center[0] = center[0] / count
            center[1] = center[1] / count
            avg_error = avg_error / count
            #print center[0], center[1], avg_error, max_error, count
            #ax.add_artist(plt.Circle((center[0],center[1]), avg_error, color='lightgrey',alpha=0.25))
    plt.savefig(pp, format='pdf')
    #plt.savefig(outDir + lbl + "_overlay.pdf")
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
    vectors = 500    
    epsilon = 1
    print "Starting!"
    for farg in sys.argv[1:]:
        files_to_run.append(farg)

    print "\tFiles: " + str(files_to_run)

    for filename in files_to_run:
        
        data = []
        if filename == 'make_moons':
            data = ds.make_moons(vectors, noise=.01)
            data = data[0]
            epsilon = 1    #Testing this value
        elif filename == 'make_circles':
            data = ds.make_circles(vectors, noise=.01)
            data = data[0]
            epsilon = 0.5    #Testing this value
        elif filename == 'make_swiss':
            data = ds.make_swiss_roll(vectors, noise=.01)
            data = data[0]
            epsilon = 10    #Testing this value
        elif filename == 'make_s_curve':
            data = ds.make_s_curve(vectors, noise=.01)
            data = data[0]
            epsilon = 1    #Testing this value
        else:
            data = readData(filename)

        outDir = filename.split('.')[0] + "_output/"
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        pp = PdfPages(outDir + 'PythonPlots.pdf')
        originalData = data

        #Output Header
        outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
        outfile.write("Source File,Output Directory,Vectors,Dimensions,Reduction %,KMeans++ Time,R PH Library,Epsilon,Complex Size,PH Time,Bottleneck Distance[0],Wasserstein Distance[0],Bottleneck Distance[1],Wasserstein Distance[1],Bottleneck Distance[2...],Wasserstein Distance[2...],...,...\n")
        outfile.close() 


        for reduction in reduction_percentages:
            n_clust = int((1-reduction) * len(data))
            red_data_labels = []
            #KMeans++ Data Reduction
            kmeans_time = 0.0
            red_data = data
            try:
                if(n_clust != len(data)):
                    start = time.time()
                    red_data = cs.KMeans(n_clusters = n_clust, init='k-means++', n_jobs=-1).fit(data)
                    end = time.time()
                    red_data_labels = red_data.labels_
                    red_data = red_data.cluster_centers_
                    kmeans_time = (end - start)
            
                #Output the data for R
                outputData(red_data, str(reduction) + "_Reduction")

            except:
                print "Failed to run KMeans on data size\n\tExiting this run: " + str(reduction) + "% Reduction"

            for tda_type in tda_libraries:
                #Output metaData
                outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
                outfile.write(filename + "," + outDir[:-1] + "," + str(len(red_data)) + "," + str(len(red_data[0])) + "," + str(reduction) + "," + str(kmeans_time) + "," + tda_type + ",")
                outfile.close() 
                
                if(tda_type == "SimBa"):
                    if os.path.isfile("./SimBa"):
                        #Call SimBa for processing
                        returnCode = subprocess.call(["./SimBa","-i",os.getcwd()+"/"+outDir+"/"+str(reduction)+"_Reduction.mat","-o",os.getcwd()+"/"+outDir+"/"+str(reduction)+"_ReductionSimBa_Output.csv"])
                        #Call R for processing

                        '''WIP: Post-processing SimBa output b/d with R, extraction of complex size and runtime from output files'''    
                        #returnCode = subprocess.call(["Rscript",os.getcwd()+"/TDA_genPlots.r","2",os.getcwd()+"/"+outDir,str(reduction) + "_Reduction"])
                        
                    else:
                        print "Could not find SimBa, skipping."
                    #Extract PH Execution Time, complex size from temp output file
                    outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
                    outfile.write("\n")
                    outfile.close() 
                else:
                    #Call R for processing
                    returnCode = subprocess.call(["Rscript",os.getcwd()+"/TDA_testRScript.r",str(epsilon),"2",os.getcwd()+"/"+outDir,str(reduction) + "_Reduction",tda_type])

                    #Extract PH Execution Time, complex size from temp output file
                    outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
                    outfile.write(getRValues(os.getcwd() + "/" + outDir +"r_temp.txt", tda_type))
                    outfile.close() 
    
            outputDataDiagram(red_data,str(reduction) + "% reduction",pp)
            outputOverlayDiagram(red_data, str(reduction) + "% reduction", red_data_labels,pp)
        pp.close()
else:
    print "Requires filename or generation arguments to run. \n\n\tGeneration options: ['make_moons', 'make_circles'].\n\n\tpython TDA_testScript.py [Epsilon] <filenames*>"

