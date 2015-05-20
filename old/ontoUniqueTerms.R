setwd("/Users/mkamdar/Desktop/MMRotation/stage_rdf_dump/")
uniqueTerms <- read.delim2("ontoUniqueTerms.tsv", header=FALSE, sep="\t", col.names=c("term","source","count","other"), 
                           colClasses=c("character","character", "integer", "character"))
sortedTerms <- uniqueTerms[order(as.integer(uniqueTerms$count), decreasing=TRUE),]
sortedTerms[1:1000,1:3]