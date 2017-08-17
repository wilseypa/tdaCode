#############################################################################################

# This R script reduces the number of points in a data set. This is done by creating small
# groups of similar data points, which we call nano-clusters.  A nano-cluster is represented
# by its centroid.  The centroid is the mean of data points in a nano-cluster. Thus,
# a data set having a large number of points can be summarized by a smaller set of
# nano-clusters. The nano-clusters are created using Hartigan and Wong's k-means algorithm. 
# We call a data set whose number of points is reduced this way a reduced data set. The
# reduced data set is then used to create a Rips filtration which is the input to the
# standard algorithm of persistent homology.

#############################################################################################


require(TDA)

# Input the scale parameter of the Rips filtration and the maximum dimension of homological features
# from the command line.
epsilon <- readline("Enter the scale parameter (epsilon) for the Rips complex: ")
epsilon <- as.numeric(epsilon)

maxDimension <- readline("Enter the maximum dimension of the homological features: ")
maxDimension <- as.numeric(maxDimension)

# Read the data set from the disk.
data <- read.csv("originalDataSet.csv", header = FALSE)

# Create a text file in which the runtimes, complex sizes and stability measures will be written.
sink(file = "complexSizeRuntimeStability.txt", append = TRUE)
print(paste0("The scale parameter for the Rips complex is ", epsilon))
writeLines('\n\n')
print("Complex size and runtime (in seconds) for the Original Data")
print(system.time(Diag <- ripsDiag(X = data, maxDimension, epsilon,
                                   library = "GUDHI", printProgress = TRUE))["elapsed"])
writeLines('\n\n\n\n\n')
sink()

# Write the output of persistent homology from the original data set to a csv file on disk.
write.table(Diag[["diagram"]], file = "outputFromOriginalData.csv", quote = FALSE,
            sep = ",", row.names = FALSE)

# Plot the output of persistent homology from the original data set on a pdf file.
pdf(file = "Plots.pdf", width = 11, height = 8.50)
plot(data, main = "Original Data")
plot(Diag[["diagram"]], main = "Persistence Diagram from Original Data")
plot(Diag[["diagram"]], barcode = TRUE, main = "Barcodes from Original Data")

# Declare the sequece of % reductions of the number of points of the original data set.
reduction <- c(0.90, 0.75, 0.50, 0.25, 0.10)
for(i in reduction) {
  reducedNumPoints <- round(i*nrow(data))
  sink(file = "complexSizeRuntimeStability.txt", append = TRUE)
  print(paste0("Time (in seconds) to generate ", (1-i)*100, "% reduced data using k-means"))
  
  # Use k-means to generate the nano-clusters and note its runtime.
  print(system.time(reducedData <- kmeans(data, reducedNumPoints, nstart = 25, iter.max = 10000)$centers)["elapsed"])
  sink()
  
  # Write the reduced data set on disk.
  write.table(reducedData, file = paste0((1-i)*100, "%ReducedDataSet.csv"),
              quote = FALSE, sep = ",", row.names = FALSE)
  
  # Plot the reduced data set on the pdf file previously created.
  plot(reducedData, main = paste0("Data: ", (1-i)*100, "% Reduced"))
  
  # Write the runtime, complex size and stability measures for the reduced data set on the same
  # text file previously created.
  sink(file = "complexSizeRuntimeStability.txt", append = TRUE)
  print(paste0("Complex size and runtime (in seconds) for ", (1-i)*100, "% Reduced Data"))
  print(system.time(reducedDiag <- ripsDiag(X = reducedData, maxDimension, epsilon,
                                     library = "GUDHI", printProgress = TRUE))["elapsed"])
  bottleneckDist <- vector()
  wassersteinDist <- vector()
  for(j in 0:maxDimension) {
    # Compute the stability measures for each dimension.
    bottleneckDist[j+1] <- bottleneck(Diag[["diagram"]], reducedDiag[["diagram"]], dimension = j)
    wassersteinDist[j+1] <- wasserstein(Diag[["diagram"]], reducedDiag[["diagram"]], p = 2, dimension = j)
    writeLines('\n')
    print(paste0("The bottleneck distance between persistence diagrams of the original data and ",
                 (1-i)*100, "% reduced data for dimension ", j, " is ", bottleneckDist[j+1]))
    print(paste0("The 2nd Wasserstein distance between persistence diagrams of the original data and ",
                 (1-i)*100, "% reduced data for dimension ", j, " is ", wassersteinDist[j+1]))
  }
  writeLines('\n\n\n\n\n')
  sink()
  
  # Write the output of persistent homology from the reduced data set to a csv file on disk.
  write.table(reducedDiag[["diagram"]], file = paste0("outputFrom", (1-i)*100, "%ReducedData.csv"),
              quote = FALSE, sep = ",", row.names = FALSE)
  
  # Plot the output of persistent homology from the reduced data set on the pdf file created before.
  plot(reducedDiag[["diagram"]], main = paste0("Persistence Diagram from ", (1-i)*100, "% Reduced Data"))
  plot(reducedDiag[["diagram"]], barcode = TRUE, main = paste0("Barcodes from ", (1-i)*100, "% Reduced Data"))
}
dev.off()
