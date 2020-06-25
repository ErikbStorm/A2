def <- read.csv("dataset.csv", sep=";");

str(def);
library(jtools)
library(lme4)
library(visreg)

df <- data.frame(c("WYSIWYG", "TBT"), c(6.9, 7.3))
str(df)

counts <- table(df)
counts

#time
barplot(c(130, 527), main="Average gametime per interface", ylab='Average time of a game in seconds', names.arg = c("WYSIWYG", "TBT"), col = c("darkblue", "lightblue"), ylim = c(0,550))

#messages per turn
barplot(c(1.02, 1.232), main="Average m/t per interface", ylab='Average messages per turn', names.arg = c("WYSIWYG", "TBT"), col = c("darkblue", "lightblue"), ylim = c(0,1.5))

#overlap
barplot(c(8.68, 19.86), main="Overlap of words per interface", ylab='Percentage of Word overlap between turns.', names.arg = c("WYSIWYG", "TBT"), col = c("darkblue", "lightblue"), ylim = c(0,20))

#Data usage
barplot(c(6.9, 7.3), main="Dmata Usage of Interfaces", ylab='average chars per line', names.arg = c("WYSIWYG", "TBT"), col = c("darkblue", "lightblue"), ylim = c(0,10))

#Happiness
barplot(c(0.016, 0.032), main="Happiness per Interface", ylab='Happiness per line?', names.arg = c("WYSIWYG", "TBT"), col = c("darkblue", "lightblue"), ylim = c(0,0.04))

#Emotional change per line
barplot(c(0.04, 0.0765), main="Emotional Change per Interface", ylab='Emotional change per line', names.arg = c("WYSIWYG", "TBT"), col = c("darkblue", "lightblue"), ylim = c(0,0.1))


data <- read.csv("lengths.csv", sep=";")
str(data)

plot(data$gameid, data$game_length)

wt <- data[data$experiment_type == 'TBTWYSIWYG' & data$game_length < 500000 & data$Interface_used == "WYSIWYG", ]
head(wt)

data <- data[data$game_length < 500000, ]

nice <- aggregate(data$game_length, by=list(data$Interface_used, data$experiment_type), FUN=mean)
nice

nice2 <- aggregate(data$game_length, by=list(data$Interface_used), FUN=mean)
nice2
barplot(nice2$x, main="Average gametime per interface", names.arg = nice2$Group.1, ylab="Average time per game in milliseconds" ,col = c("lightblue", "darkblue"), ylim=c(0, 250000))

barplot(nice$x, main="Average gametimes", names.arg = nice$Group.1, ylab="Average time per game in milliseconds" ,col = c("lightblue", "lightblue", "darkblue", "darkblue"), ylim=c(0, 250000))
legend("topleft", inset = c(0.05, 0), c("TBTWYSIWYG", "WYSIWYGTBT"), fill=c("lightblue","darkblue"))

