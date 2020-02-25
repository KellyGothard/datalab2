############################################################
# R Script for data lab ebola project                      #
# Feb-March 2020                                           #
############################################################

# Load packages and set directory
library(phonics)

setwd("c:/users/beasley/documents/datalab2")

# Load quantitative data
quant.trigger <- read.table('smac/trigger_na.csv', sep = ',', header = T, 
                            stringsAsFactors = F)

