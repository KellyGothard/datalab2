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
quant.trigger$District <- gsub(c("\\W"), "", quant.trigger$District)
quant.trigger$District <- gsub(c("\\d"), "", quant.trigger$District)

quant.trigger$Chiefdom <- gsub("\\W", "", quant.trigger$Chiefdom)
quant.trigger$Chiefdom <- gsub("\\d", "", quant.trigger$Chiefdom)

# Soundex, revisited --------------------------------
dist.soundex <- phonics(quant.trigger$District, method = "soundex", clean = T)
chief.soundex <- phonics(quant.trigger$Chiefdom, method = "soundex", clean = T)

qt.soundex <- cbind(dist.soundex, chief.soundex)
colnames(qt.soundex) <- c("dist.word", "dist.soundex", "chief.word", "chief.soundex")

# Treat district/chiefdom as key/value pairs to fill missing data ---------------
# Look for missing soundex values
unique(qt.soundex[,c(2,4)])

# See if we can do a simple replacement
qt.soundex$dist.soundex[which(qt.soundex$chief.soundex==C100),]
#Replace missing district value
qt.soundex$dist.soundex[which(qt.soundex$chief.soundex=='C100')] <- "B530"

# Merge soundex columns with the main dataset -----------------------------
quant.trigger$dist.soundex <- qt.soundex$dist.soundex
quant.trigger$chief.soundex <- qt.soundex$chief.soundex

# Save cleaned .csv ---------------------------------------
write.csv(quant.trigger, file = "trigger_na_phonicsclean.csv")
