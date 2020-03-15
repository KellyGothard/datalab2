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
  select(Trig_date, District, Chiefdom, Name_of_community, Male_child:Total_female,
         ss_mc:cb_fa) %>%
  mutate(Total_all = Total_male+Total_female) %>%
  mutate(Sick_all = ss_mc+ss_fc+ss_ma+ss_fa) %>%
  mutate(Deaths_all = d_mc+d_fc+d_ma+d_fa) %>%
  select(Trig_date, District, Chiefdom, Name_of_community, Total_all, Sick_all,
         Deaths_all) %>%
  group_by(District, Chiefdom, Name_of_community) %>%
  summarise(Population = sum(Total_all), Sick = sum(Sick_all), 
            Deaths = sum(Deaths_all)) %>%
  na.omit() %>%
  mutate(PercSick = Sick/Population, PercDead = Deaths/Population) %>%
  add_column(Visit = "Trigger") %>%
  {. ->> smol.inits}

followup %>%
  select(Date_of_visit, District, Name_of_community, Chiefdom, Male_Child:Total_female,
         ss_mc:cb_fa) %>%
  mutate(Total_all = Total_male+Total_female) %>%
  mutate(Sick_all = ss_mc+ss_fc+ss_ma+ss_fa) %>%
  mutate(Deaths_all = d_mc+d_fc+d_ma+d_fa) %>%
  select(Date_of_visit, District, Chiefdom, Name_of_community, Total_all, Sick_all,
         Deaths_all) %>%
  group_by(District, Chiefdom, Name_of_community) %>%
  mutate(Date_of_visit = as.Date(Date_of_visit, '%Y-%m-%d')) %>%
  distinct(District, Chiefdom, Name_of_community, .keep_all = T) %>%
  summarise(Population = sum(Total_all), Sick = sum(Sick_all), 
            Deaths = sum(Deaths_all))%>%
  na.omit() %>%
  mutate(PercSick = Sick/Population, PercDead = Deaths/Population) %>%
  add_column(Visit = "1stFollowup") %>%
  {. ->> smol.followup}

# Remove followup data that doesn't exist in the inits
smol.followup <- match_df(smol.followup, smol.inits, on = c('District', 'Chiefdom',
                                                            'Name_of_community'))

# Combine dataframes
smol <- rbind(smol.inits, smol.followup)

# Factor visit column for neater plots
smol$Visit <- factor(smol$Visit, levels = c("Trigger", "1stFollowup"))

# Make a few quick plots --------------------------------------------
qplot(data = smol.inits, x = District, geom = "bar")
# Sampling effort varies a lot

qplot(data = smol.inits, x = District, y = PercSick, geom = "jitter")

qplot(data = smol.inits, x = District, y = PercDead, geom = "jitter")

# Clean up interesting plots -------------------------------
ggplot(data = smol, aes(x = District, fill = Visit))+
  geom_bar(position = position_dodge(preserve = "single"))+
  scale_fill_manual(values = c("black", "limegreen"))+
  scale_y_continuous(expand = c(0,0))+
  labs(y = "Observations")+
  theme_bw(base_size = 18)+
  theme(panel.grid = element_blank())

ggsave("obsbydist.jpeg", width = 10, height = 5, units = "in")
