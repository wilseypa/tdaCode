print(Sys.time())
require("RANN")
require("TDA")

# Circle1 <- circleUnif(60)
# Circle2 <- circleUnif(60, r = 2) + 3
# data <- as.data.frame(rbind(Circle1, Circle2))

# on peter
data <- read.csv("/work/moitraaa/tomatoDatasets/toyExample.csv", header = FALSE, sep = "")
data <- as.data.frame(data)
png(filename = "/work/moitraaa/toyExampleData.png", width = 1366, height = 716)
plot(data, main = "Data")
dev.off()

maxDimension <- 1
percentList <- c(1, 0.9, 0.8, 0.7)
for(p in percentList) {
  k <- round((nrow(data)-1)*p)
  meanDistFromPoint <- vector()
  for(i in 1:nrow(data)) {
    kNN <- nn2(data, query = data[i,], k)
    distances <- as.vector(kNN$nn.dists)
    meanDistFromPoint[i] <- mean(distances[2]:distances[length(distances)])
  }
  epsilon <- mean(meanDistFromPoint)
  print(epsilon)
  maxScale <- epsilon
  Diag <- ripsDiag(X = data, maxDimension, maxScale, library = "GUDHI", printProgress = FALSE)
  png(filename = paste("/work/moitraaa/outputToyExample", p, ".png", sep = ""), width = 1366, height = 716)
  # png(filename = paste("/home/anindya/output", p, ".png", sep = ""), width = 1366, height = 716)
  par(mfrow = c(1, 2), mai=c(0.8, 0.8, 0.3, 0.3))
  plot(Diag[["diagram"]], main = paste("Persistence Diagram with epsilon =", round(epsilon, digits = 3)))
  plot(Diag[["diagram"]], barcode = TRUE, main = paste("Barcodes with epsilon =", round(epsilon, digits = 3)))
  dev.off()
}
print(Sys.time())
