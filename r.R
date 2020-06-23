def <- read.csv("dataset.csv", sep=";");

str(def);
library(jtools)
library(lme4)
library(visreg)

lmer <- lmer(Duration ~ TURNTYPE + (1|dyadid), data=def);
