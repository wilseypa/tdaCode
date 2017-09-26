require(TDA)

args <- commandArgs(trailingOnly=TRUE)


# Input the scale parameter of the Rips filtration and the maximum dimension of homological features
# from the command line.
epsilon <- as.numeric(args[1])
maxDimension <- as.numeric(args[2])
path <- args[3]
fileName <- args[4]
label <- args[5]
tdaType <- args[6]
fullPath <- paste(path,fileName,".csv", sep="")
# Read the data set from the disk.
data <- read.csv(fullPath, header = FALSE)

# Create a text file in which the runtimes, complex sizes and stability measures will be written.
sink(file = paste(path,"agg_results.csv",sep=""), append = TRUE)
cat(epsilon)
cat(',')

sink()
sink(file = paste(path,"r_temp.txt",sep=""), append = FALSE)
cat(system.time(Diag <- ripsDiag(X = data, maxDimension, epsilon,
                                   library = tdaType, printProgress = TRUE))["elapsed"])
#cat(',')
sink()


# Write the output of persistent homology from the original data set to a csv file on disk.
write.table(Diag[["diagram"]], file = paste(path,fileName,tdaType,"_Output.csv",sep=""), quote = FALSE,
            sep = ",", row.names = FALSE)

# Plot the output of persistent homology from the original data set on a pdf file.
pdf(file = paste(path,"RPlot_",fileName,"_",tdaType,".pdf",sep=""), width = 11, height = 8.50)
plot(data, main = paste(label,tdaType))
plot(Diag[["diagram"]], main = paste("Persistence Diagram\n",label,tdaType))
plot(Diag[["diagram"]], barcode = TRUE, main = paste("Barcodes from\n",label,tdaType))


sink(file = paste(path,"r_temp.txt",sep=""), append = TRUE)

originalData <- read.csv(paste(path,"0.0_Reduction",tdaType,"_Output.csv",sep=""), header = TRUE) 
originalData <- as.matrix(originalData) 

bottleneckDist <- vector()
wassersteinDist <- vector()
for(j in 0:maxDimension) {
#Compute the stability measures for each dimension.
	bottleneckDist[j+1] <- bottleneck(originalData, Diag[["diagram"]], dimension = j)
	wassersteinDist[j+1] <- wasserstein(originalData, Diag[["diagram"]], p = 2, dimension = j)
	cat(',')
	cat(bottleneckDist[j+1])
	cat(',')
	cat(wassersteinDist[j+1])
}




sink()

dev.off()
