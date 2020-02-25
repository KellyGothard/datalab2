############################################################
# R Script for data lab ebola project                      #
# Feb-March 2020                                           #
############################################################

# Load packages and set directory
library(phonics)
library(tidyverse)

setwd("c:/users/beasley/documents/datalab2")

# Load quantitative data
quant.trigger <- read.table('smac/trigger_na.csv', sep = ',', header = T, 
                            stringsAsFactors = F)

# Test the phonics function --------------------------------
head(phonics(quant.trigger$District, method = "soundex.refined", clean = T))

# Seems to be working? Count how many we have; does it match known districts?
district.soundex <- phonics(quant.trigger$District, method = "soundex.refined", 
                            clean = T)
unique(district.soundex)
unique(quant.trigger$District)

# Soundex hates spaces, apparently

# Remove spaces from district and chiefdom names --------------------------
quant.trigger$District <- gsub("\\s", "", quant.trigger$District)
quant.trigger$Chiefdom <- gsub("\\s", "", quant.trigger$Chiefdom)

# Soundex, revisited --------------------------------
dist.soundex <- phonics(quant.trigger$District, method = "soundex.refined", clean = T)
chief.soundex <- phonics(quant.trigger$Chiefdom, method = "soundex.refined", clean = T)

qt.soundex <- cbind(dist.soundex, chief.soundex)
colnames(qt.soundex) <- c("dist.word", "dist.soundex", "chief.word", "chief.soundex")
