#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

prefix = args[1]

library(methods)
library(limma)
library(edgeR)

# Read in the count file as produced by featureCount program.
count_file = paste(prefix, 'counts', sep='.')
fc = read.table(count_file, skip=2, header=FALSE)
names(fc) = c('Geneid','Chr','Start','End','Strand','Length','Count')

# Get the rpkms (or fpkms in the case of paired data.
x <- DGEList(counts=fc[,'Count'], genes=fc[,c("Geneid","Length")])
x_rpkm = rpkm(x, x$genes$Length)

# Write the outputtable.
fpkm_file = paste(prefix, 'fpkm', sep='.')
write.table(data.frame(fc$Geneid, x_rpkm), file = fpkm_file, sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
