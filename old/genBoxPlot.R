setwd("/Users/mkamdar/Desktop/MMRotation/stage_rdf_dump")
ontoterm.matrix <- read.table("decomposedOntoTermMatrix.tsv", colClasses="numeric", header=FALSE)
term.cluster <- read.table("clusters.tsv", header=FALSE)


data.cluster <- as.data.frame(cbind(ontoterm.matrix,term.cluster))
colnames(data.cluster) <- c("q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "c")

use.cluster <- data.cluster[data.cluster$c < 20,]
jpeg('q10.jpg')
boxplot(q10~c, use.cluster)
dev.off()
print("Box Plot generated in the working directory")



