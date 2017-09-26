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
import palettable

colors = palettable.colorbrewer.qualitative.Dark2_7.mpl_colors

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

def outputBarcodeDiagram(filename,lbl,pp):
	delim = ','
	if(filename.find('SimBa') >= 0):
		delim= ' '	

	if(not os.path.isfile(filename)):
		return
	plt.clf()
	data = np.loadtxt(filename, dtype=np.float, delimiter = delim, skiprows=1)

	if(len(data.shape) <2):
		return

	plt.title("Bar Codes " + lbl)
	plt.grid(True, which='both')

	maxDeath = np.ceil(np.max(data[:,2]))

	c = [0,0,0]
	bc = np.bincount(data[:,0].astype(int))
	print bc
	if(len(bc) > 1):
		c[1] = bc[0]+5
		c[2] = bc[1]+ bc[0]+5

	for i in xrange(len(data)):

		print data[i,0],data[i,1],data[i,2]

		if data[i,0] == 0:
			color = 'black'
		elif data[i,0] == 1:
			color = 'red'
		elif data[i,0] == 2:
			color = 'blue'
		else:
			print "Barcode > 2 not displayed"
		
		plt.hlines(int(c[int(data[i,0])]),data[i,1],data[i,2])

		c[int(data[i,0])] += 1

	
	plt.xlim(0,maxDeath)
	#d0.set_ylim(0,lind[0] + 1)
	#d1.set_ylim(0,lind[1] + 1)
	#d2.set_ylim(0,lind[1] + 1)
	plt.xlabel('Time')
		

	plt.savefig(pp, format='pdf')
	plt.clf()
	return

def outputDataDiagram(data,lbl, pp):
    plt.clf()
    plt.scatter(data[:,0], data[:,1],label=lbl, marker=".", s=5, color='r')
    plt.title("Point Cloud " + lbl)
    plt.grid(True, which='both')
    plt.savefig(pp, format='pdf')
    #plt.savefig(outDir + lbl + ".pdf")
    #plt.show()
    plt.clf()
    return

def outputPersistenceDiagram(filename,lbl,pp):
	delim = ','
	if(filename.find('SimBa') >= 0):
		delim= ' '

	if(not os.path.isfile(filename)):
		return
	plt.clf()
	data = np.loadtxt(filename, dtype=np.float, delimiter = delim, skiprows=1)
	#print data[:, [1, 2]][data[:, 0] == 1]
	#print data[:, [2]][data[:, 0] == 1]
	print len(data.shape)
	if(len(data.shape) >1):
		maxDeath = np.ceil(np.max(data[:,2]))
		maxBetti = np.ceil(np.max(data[:,0]))
		if maxDeath > 5:
			maxDeath = 5

		plotSize=5.0
		plt.figure(figsize=(plotSize, plotSize))

		birthBetti0 = data[:, [1]][data[:, 0] == 0]
		deathBetti0 = data[:, [2]][data[:, 0] == 0]
		birthBetti1 = data[:, [1]][data[:, 0] == 1]
		deathBetti1 = data[:, [2]][data[:, 0] == 1]

		if maxBetti > 1 :
			birthBetti2 = data[:, [1]][data[:, 0] == 2]
			deathBetti2 = data[:, [2]][data[:, 0] == 2]
			birthBetti3 = data[:, [1]][data[:, 0] == 3]
			deathBetti3 = data[:, [2]][data[:, 0] == 3]
			plt.figure(figsize=(2*plotSize, plotSize))

		axisOffset=.1
		markerSize = 7

		plt.title("Persistence Diagram\n" + lbl)

		#plt.axes(frameon=False)
		#plt.axis('off')
		plt.grid(True)

		plt.xticks(np.arange(0, maxDeath+1, 1.0))
		plt.yticks(np.arange(0, maxDeath+1,1.0))
		plt.xlim(-.05, maxDeath+0.05)
		plt.ylim(-.05, maxDeath+0.05)

		# plot black diagonal line
		plt.plot(np.arange(maxDeath+1), color='black', linewidth=.2)

		plt.scatter(deathBetti0,birthBetti0, color=colors[0], marker='o', s=markerSize)
		plt.text(0.5*maxDeath,(0.5*maxDeath)-axisOffset, "0-Cell\n(x,y)=(death, birth)", color=colors[0], ha='left', va='top')
		plt.scatter(birthBetti1,deathBetti1, color=colors[1], marker='^', s=markerSize)
		plt.text(0.75*maxDeath,(0.75*maxDeath)+axisOffset, "1-Cell\n(x,y)=(birth, death)", color=colors[1], ha='right', va='bottom')

		if maxBetti > 1 :
			plt.axvline(0, color='black', linewidth=.2)
			plt.plot(np.negative(np.arange(maxDeath+1)), np.arange(maxDeath+1), color='black', linewidth=.2)
			plt.scatter(np.negative(birthBetti2),deathBetti2, color=colors[2], marker='*', s=markerSize)
			plt.text(-(0.75*maxDeath),(0.75*maxDeath)+axisOffset, "2-Cell\n(x,y)=(birth, death)", color=colors[2], ha='left', va='bottom')
			plt.scatter(np.negative(deathBetti3),birthBetti3, color=colors[3], marker='x', s=markerSize)
			plt.text(-(0.5*maxDeath),(0.5*maxDeath)-axisOffset, "3-Cell\n(x,y)=(death, birth)", color=colors[3], ha='right', va='top')
			plt.xlim(-(maxDeath+0.25), maxDeath+0.25)
			plt.xticks(np.arange(-(maxDeath), maxDeath+1, 1.0))

		plt.savefig(pp, format='pdf')
	
		plt.figure(figsize=(plotSize, plotSize))
	plt.clf()
	
	

def calculateClusterStatistics(data, data_labels):
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
			#print avg_error = avg_error / count
			#print center[0], center[1], avg_error, max_error, count
			#ax.add_artist(plt.Circle((center[0],center[1]), avg_error, color='lightgrey',alpha=0.25))



def outputOverlayDiagram(data,lbl,data_labels, pp):
    plt.clf()
    fig=plt.gcf()
    ax=fig.gca()
    ax.set(adjustable='box-forced', aspect='equal')

    
    plt.title("Point Cloud " + lbl)
    plt.scatter(originalData[:,0], originalData[:,1], marker=".", s=3, color='lightgrey', label="Original")
    plt.scatter(data[:,0], data[:,1], marker=".", s=5,
                  color='r', label=lbl)
    plt.legend()
    plt.grid(True, which='both')
    #plt.axis('off')

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
    vectors = 400    
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
                        returnCode = subprocess.call(["./SimBa","-i",os.getcwd()+"/"+outDir+"/"+str(reduction)+"_Reduction.mat","-c","1.001","-o",os.getcwd()+"/"+outDir+"/"+str(reduction)+"_ReductionSimBa_Output.csv"])
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
                    returnCode = subprocess.call(["Rscript",os.getcwd()+"/TDA_testRScript.r",str(epsilon),"2",os.getcwd()+"/"+outDir,str(reduction) + "_Reduction",str(reduction*100) + "% Reduction", tda_type])

                    #Extract PH Execution Time, complex size from temp output file
                    outfile = file(os.getcwd() + "/" + outDir + "/agg_results.csv", 'a')
                    outfile.write(getRValues(os.getcwd() + "/" + outDir +"r_temp.txt", tda_type))
                    outfile.close()
                outputPersistenceDiagram(os.getcwd() + "/" + outDir + "/" + str(reduction)+"_Reduction"+tda_type+"_Output.csv", str(reduction*100) + "% Reduction " + tda_type, pp)
                outputBarcodeDiagram(os.getcwd() + "/" + outDir + "/" + str(reduction)+"_Reduction"+tda_type+"_Output.csv", str(reduction*100) + "% Reduction " + tda_type, pp)



            outputDataDiagram(red_data,str(reduction*100) + "% Reduction",pp)
            outputOverlayDiagram(red_data, str(reduction*100) + "% Reduction", red_data_labels,pp)
        pp.close()
else:
    print "Requires filename or generation arguments to run. \n\n\tGeneration options: ['make_moons', 'make_circles'].\n\n\tpython TDA_testScript.py [Epsilon] <filenames*>"

