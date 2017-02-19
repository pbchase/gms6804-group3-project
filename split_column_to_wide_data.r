# Build a data frame of subjects and fruit preferences based on a random
# sampling of a random amount of fruit from a vector of possible fruit
subjects <- seq(1,10,1)
all_fruit <- c("apple","banana","cantalope","drurian","date","lychee","carambola","kumquat","loquat","grape","orange","mango")

sample_a_vector <- function(x) {
  paste(sample(x,floor(runif(1,0,length(x)/4))),  collapse=",")
}

df <- data.frame(subjects)
df$favorite_fruit <- replicate(length(subjects), sample_a_vector(all_fruit))
df

# Make a new data frame of one column per fruit listed in favorite_fruit column
# For this exercise assume we do not know the list of all_fruit.
# We must derive our list of fruit from our sample of fruit in the favorite_fruit column
library(dplyr)
library(tidyr)
df.tall <- df %>% mutate(favorite_fruit = strsplit(favorite_fruit, ",")) %>% unnest(favorite_fruit)
df.tall$likes_fruit <- rep(1,nrow(df.tall))
df.wide <- spread(df.tall, favorite_fruit,likes_fruit)
df.wide.combined <- merge(df,df.wide, by="subjects", all.x=TRUE)
df.wide.combined

# If you hate NAs in the fruit columns...
df.wide.combined[is.na(df.wide.combined)] <- 0
df.wide.combined
