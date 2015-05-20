setwd("/Users/mkamdar/Desktop/MMRotation/stage_rdf_dump")

GetScore <- function (ontologyId) {
  return (dim(sortededges[sortededges$V1 == ontologyId,])[1])
}

GetIsScore <- function (ontologyId) {
  return (dim(sortededges[sortededges$V2 == ontologyId,])[1])
}

GetOutScore <- function (ontologyId) {
  return (dim(sortedxrefedges[sortedxrefedges$V1 == ontologyId,])[1])
}

GetInScore <- function (ontologyId) {
  return (dim(sortedxrefedges[sortedxrefedges$V2 == ontologyId,])[1])
}

GetTermCount <- function (ontologyId) {
  return (termcounts[termcounts$V1 == ontologyId,][2])
}

edges <- read.delim2("edgesAllaViews.tsv", sep="\t", header=FALSE)
sortededges <- edges[order(as.numeric(edges$V3), decreasing=TRUE),]
print(sortededges[sortededges$V1 == "CCONT",])

reuse.stats <- read.table("reuseStatsFileaViews.tsv", colClasses=c("character", "integer", "integer"), header=FALSE)
colnames(reuse.stats) <- c("Ontology", "ReusedCount", "TotalCount")
x <- reuse.stats$ReusedCount/reuse.stats$TotalCount
hist(x, breaks=50, col="blue")
reuse.stats <- cbind(reuse.stats, x)
sortedreuse <- cbind(reuse.stats, unlist(lapply(reuse.stats$Ontology, GetScore)))
sortedreuse <- sortedreuse[order(as.integer(sortedreuse[,5]), decreasing=TRUE),]
print(sortedreuse[1:10,])

isreuse.stats <- read.table("isReusedStatsFileaViews.tsv", colClasses=c("character", "integer", "integer"), header=FALSE)
colnames(isreuse.stats) <- c("Ontology", "ReusedCount", "TotalCount")
kx <- isreuse.stats$ReusedCount/isreuse.stats$TotalCount
hist(kx, breaks=100, col="blue")
isreuse.stats <- cbind(isreuse.stats, kx)
sortedisreuse <- cbind(isreuse.stats, unlist(lapply(isreuse.stats$Ontology, GetIsScore)))
sortedisreuse <- sortedisreuse[order(as.integer(sortedisreuse[,5]), decreasing=TRUE),]
print(sortedisreuse[1:10,])




terms <- read.table("termcounts.tsv", header=FALSE)
sortedterms <- terms[order(as.numeric(terms$V2), decreasing=TRUE),]
print(sortedterms[1:20,])


xrefedges <- read.delim2("pairFile.tsv", sep="\t", header=FALSE)
sortedxrefedges <- xrefedges[order(as.numeric(xrefedges$V3), decreasing=TRUE),]
print(sortedxrefedges[sortedxrefedges$V1 == "GO",])

incomingxrefs <- read.delim2("incomingXrefsWoViews.tsv", sep="\t", colClasses=c("character", "integer", "integer"), header=FALSE)
outgoingxrefs <- read.delim2("outgoingXrefsWoViews.tsv", sep="\t", colClasses=c("character", "integer", "integer"), header=FALSE)
inx <- incomingxrefs$V2/incomingxrefs$V3
outx <- outgoingxrefs$V2/outgoingxrefs$V3
incomingxrefs <- cbind(incomingxrefs, inx)
outgoingxrefs <- cbind(outgoingxrefs, outx)
sortedoutxrefs <- cbind(outgoingxrefs, unlist(lapply(outgoingxrefs$V1, GetOutScore)))
sortedoutxrefs <- sortedoutxrefs[order(as.integer(sortedoutxrefs[,5]), decreasing=TRUE),]
print(sortedoutxrefs[1:10,])

sortedinxrefs <- cbind(incomingxrefs, unlist(lapply(incomingxrefs$V1, GetInScore)))
sortedinxrefs <- sortedinxrefs[order(as.integer(sortedinxrefs[,5]), decreasing=TRUE),]
print(sortedinxrefs[1:10,])


termcounts <- read.delim2("termcounts.tsv", sep="\t", header=FALSE, colClasses=c("character", "integer"))
selectededges <- sortededges[sortededges$V2 %in% termcounts$V1,]
edgepairs <- cbind(selectededges, unlist(lapply(selectededges$V2, GetTermCount)))
colnames(edgepairs) <- c("source", "target", "strength", "targetsize")
xfrac <- edgepairs$strength/edgepairs$targetsize
edgeration <- cbind(edgepairs, xfrac)
edgeration <- edgeration[order(as.numeric(edgeration$xfrac), decreasing=TRUE),]
edgeration <- edgeration[edgeration$xfrac > 0.35, ]
aggregate <- table(edgeration$target)
aggregate[order(aggregate, decreasing=TRUE)]

ontoCompoFile<- read.delim2("../ontoCompo2.tsv", header=FALSE, sep="\t")
ontoCompoFile[order(as.integer(ontoCompoFile$V2), decreasing=TRUE),]

write.table(data.frame(sortedreuse), "SortedExplicitReuse.tsv", eol="\n", sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
write.table(data.frame(sortedisreuse), "SortedExplicitIsReuse.tsv", eol="\n", sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
write.table(data.frame(sortedinxrefs), "SortedIncomingXrefs.tsv", eol="\n", sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
write.table(data.frame(sortedoutxrefs), "SortedOutgoingXrefs.tsv", eol="\n", sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)