library(TDA)

# Generate a data set of two circles having 50,000 points.
Circle1 <- circleUnif(16667)
Circle2 <- circleUnif(33333, r = 2) + 3
originalData <- rbind(Circle1, Circle2)
totalNumPoints <- nrow(originalData)

# Randomly suffle the points in the original data set.
# Source: https://stackoverflow.com/questions/6422273/how-to-randomize-or-permute-a-dataframe-rowwise-and-columnwise
shuffledData <- originalData[sample(totalNumPoints),]

# Specify the batch size and create batches of 500 points from the original data set.
batchSize <- 500
numBatches <- totalNumPoints/batchSize
batch <- list()
for(i in 1:numBatches)
  batch[[i]] <- shuffledData[((i-1)*500+1) : (i*500), ]

# Reduce the incoming batches of points to keep the number of points on which PH is to
# be computed at 500.
existingData <- batch[[1]]
for(i in 2:50) {
  reducedNumPoints <- round(((1/i)*batchSize) + 15)
  reducedBatch <- kmeans(batch[[i]], reducedNumPoints, nstart = 25, iter.max = 10000)$centers
  reducedNumExistingPoints <- round(((1 - (1/i))*batchSize) - 15)
  reducedExistingData <- kmeans(existingData, reducedNumExistingPoints, nstart = 25, iter.max = 10000)$centers
  existingData <- rbind(reducedExistingData, reducedBatch)
}

# Compute PH at the end of the fileStream
maxscale <- 5
maxdimension <- 1
Diag <- ripsDiag(X = existingData, maxdimension, maxscale,
                 library = "GUDHI", printProgress = TRUE)

pdf(file = "C:/Users/moitra.a/Desktop/Plots.pdf", width = 11, height = 8.50)
plot(existingData, pch = 20, main = "Retained Data at the End of the FileStream")
plot(Diag[["diagram"]], main = "Persistence Diagram at the End of the FileStream")
dev.off()
