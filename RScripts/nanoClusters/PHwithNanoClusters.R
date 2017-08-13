require(TDA)

epsilon <- readline("Enter the scale parameter (epsilon) for the Rips complex: ")
epsilon <- as.numeric(epsilon)

maxDimension <- readline("Enter the maximum dimension of the homological features: ")
maxDimension <- as.numeric(maxDimension)

data <- read.csv("originalDataSet.csv", header = FALSE)
sink(file = "complexSizeRuntimeStability.txt", append = TRUE)
print(paste0("The scale parameter for the Rips complex is ", epsilon))
writeLines('\n\n')
print("Complex size and runtime (in seconds) for the Original Data")
print(system.time(Diag <- ripsDiag(X = data, maxDimension, epsilon,
                                   library = "GUDHI", printProgress = TRUE))["elapsed"])
writeLines('\n\n\n\n\n')
sink()
write.table(Diag[["diagram"]], file = "outputFromOriginalData.csv", quote = FALSE,
            sep = ",", row.names = FALSE)
pdf(file = "Plots.pdf", width = 11, height = 8.50)
plot(data, main = "Original Data")
plot(Diag[["diagram"]], main = "Persistence Diagram from Original Data")
plot(Diag[["diagram"]], barcode = TRUE, main = "Barcodes from Original Data")

reduction <- c(0.90, 0.75, 0.50, 0.25, 0.10)
for(i in reduction) {
  reducedNumPoints <- round(i*nrow(data))
  sink(file = "complexSizeRuntimeStability.txt", append = TRUE)
  print(paste0("Time (in seconds) to generate ", (1-i)*100, "% reduced data using k-means"))
  print(system.time(reducedData <- kmeans(data, reducedNumPoints, nstart = 25, iter.max = 10000)$centers)["elapsed"])
  sink()
  write.table(reducedData, file = paste0((1-i)*100, "%ReducedDataSet.csv"),
              quote = FALSE, sep = ",", row.names = FALSE)
  plot(reducedData, main = paste0("Data: ", (1-i)*100, "% Reduced"))
  sink(file = "complexSizeRuntimeStability.txt", append = TRUE)
  print(paste0("Complex size and runtime (in seconds) for ", (1-i)*100, "% Reduced Data"))
  print(system.time(reducedDiag <- ripsDiag(X = reducedData, maxDimension, epsilon,
                                     library = "GUDHI", printProgress = TRUE))["elapsed"])
  bottleneckDist <- vector()
  wassersteinDist <- vector()
  for(j in 0:maxDimension) {
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
  write.table(reducedDiag[["diagram"]], file = paste0("outputFrom", (1-i)*100, "%ReducedData.csv"),
              quote = FALSE, sep = ",", row.names = FALSE)
  plot(reducedDiag[["diagram"]], main = paste0("Persistence Diagram from ", (1-i)*100, "% Reduced Data"))
  plot(reducedDiag[["diagram"]], barcode = TRUE, main = paste0("Barcodes from ", (1-i)*100, "% Reduced Data"))
}
dev.off()
