library(ggplot2)
library(gridExtra)
library(grid)
df<-read.csv(file.choose())



df$fraction = df$X.N.A_Race/ sum(df$X.N.A_Race)                                                                  # create fraction column 
df = df[order(df$fraction), ]                                                                                   # sort dataframe by fraction 
df$ymax = cumsum(df$fraction)                                                                                   # set end for each fraction              
df$ymin = c(0, head(df$ymax, n=-1))                                                                             # set start for each fraction 

######Create the circle plot one by one
######Terrible but it works
NA_Race<- ggplot(df, aes(fill=Row.Labels, ymax=ymax, ymin=ymin, xmax=4, xmin=3,size=2)) + 
  geom_rect(color="black",size=.2) + 
  coord_polar(theta="y") + 
  xlim(c(0, 4)) + 
  theme(panel.grid=element_blank()) +                                                            # remove grid from plot 
  theme(axis.ticks=element_blank(),axis.text=NULL)+theme_classic() +theme(axis.line=element_blank(),axis.text.x=element_blank(),
                                                                          axis.text.y=element_blank(),      axis.ticks=element_blank(),
                                                                          axis.title.x=element_blank(),
                                                                          axis.title.y=element_blank())+ggtitle("NA")+scale_fill_brewer(palette="Set1", guide_colorbar())+annotate("text", x=0, y=0, label= paste0("N=",sum(df$X.N.A_Race)),fontface=2,size=5)
NA_Race_1


get_legend<-function(myggplot){
  tmp <- ggplot_gtable(ggplot_build(myggplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)
}




legend <- get_legend(NA_Gender)

grid.draw(legend) 

grid.arrange(arrangeGrob(ncol=3,Male,Female,NA_Gender),
             arrangeGrob(ncol=2,White,Black,American_Indian,Asian,Hispanic,NA_Race,legend),nrow=4)




grid_arrange_shared_legend <- function(..., nrow = 1, ncol = length(list(...)), position = c("bottom", "right")) {
  
  plots <- list(...)
  position <- match.arg(position)
  g <- ggplotGrob(plots[[1]] + theme(legend.position = position))$grobs
  legend <- g[[which(sapply(g, function(x) x$name) == "guide-box")]]
  lheight <- sum(legend$height)
  lwidth <- sum(legend$width)
  gl <- lapply(plots, function(x) x + theme(legend.position = "none"))
  gl <- c(gl, nrow = nrow, ncol = ncol)
  
  combined <- switch(position,
                     "bottom" = arrangeGrob(do.call(arrangeGrob, gl),
                                            legend,
                                            ncol = 1,
                                            heights = unit.c(unit(1, "npc") - lheight, lheight)),
                     "right" = arrangeGrob(do.call(arrangeGrob, gl),
                                           legend,
                                           ncol = 2,
                                           widths = unit.c(unit(1, "npc") - lwidth, lwidth)))
  grid.newpage()
  grid.draw(combined)
  
}


grid_arrange_shared_legend(Male,Female,NA_Gender,nrow =1 , ncol = 3)

grid_arrange_shared_legend(White,Black,American_Indian,Asian,Hispanic,NA_Race,nrow = 2, ncol = 3)



