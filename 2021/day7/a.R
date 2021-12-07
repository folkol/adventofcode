#!/usr/local/bin/Rscript

data <- scan("input.dat", sep=",")
M = median(data)
distances = lapply(data, {function(x) abs(x - M)})

print(sum(unlist(distances)))
