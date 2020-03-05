############################################################################
# Back-pocket statistics for numerical Ebola data                          #
# E.M. Beasley      Data Lab Challenge #2     Spring 2020                  #
############################################################################

# Load req'd packages --------------------------------
library(tidyverse)

setwd("c:/users/beasley/documents/datalab2")

# Load data -----------------------------------------
inits <- read.table("smac/triggernaclean.csv", sep = ",", header = T, 
                    stringsAsFactors = F)

followup <- read.table("smac/followupclean.csv", sep = ",", header = T, 
                       stringsAsFactors = F)

# Select columns with disease data --------------------------------
inits %>%
  select(Trig_date, District, Chiefdom, Male_child:Total_female, ss_mc:cb_fa) %>%
  mutate(Total_all = Total_male+Total_female) %>%
  mutate(Sick_all = ss_mc+ss_fc+ss_ma+ss_fa) %>%
  mutate(Deaths_all = d_mc+d_fc+d_ma+d_fa) %>%
  select(Trig_date, District, Chiefdom, Total_all, Sick_all, Deaths_all) %>%
  group_by(District, Chiefdom) %>%
  summarise(smol.inits, Population = sum(Total_all), Sick = sum(Sick_all), 
            Deaths = sum(Deaths_all)) %>%
  {. ->> smol.inits}

