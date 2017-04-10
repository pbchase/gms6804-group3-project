library(XML)
theurl <- "https://my.pgp-hms.org/profile/hu43294F"
library(rvest)
# file<-read_html(theurl)
# tables<-html_nodes(file, "table")
# table1 <- html_table(tables[2], fill = TRUE)
# table_ex<-table1[[1]]

snp_set<-read.csv(file.choose())

snp_ID<-as.vector(snp_set$subject)
ziptotalf<-data.frame()
ziptotal<-data.frame()

for (i in 1:662){
  theurl <- paste0("https://my.pgp-hms.org/profile/",snp_ID[i])
  file<-read_html(theurl)
  tables<-html_nodes(file, "table")
  ano_table<-lapply(tables, function(x) html_table(x, fill=TRUE))
  ID<-snp_ID[i]
  #table1 <- html_table(tables[2], fill = TRUE)
  for (j in 1:length(ano_table)) {
    tab.0<-ano_table[[j]]
    tab.0[is.na(tab.0)] <- 0
    if(length(grep("Zip code:", tab.0)) > 0){
      ziptotal <-data.frame(ID,data.frame(t(tab.0$X2)))
    }else {
      print("no")
      }
  }
  #table_ex<-table1[[1]]
  # if(table_ex[1,1] == "State:"){
  #   ziptotal <-cbind(snp_ID[i],data.frame(t(table_ex$X2)))
  # } else {
  #   ziptotal <-cbind(snp_ID[i],"0","0")
  # }
  ziptotalf<-rbind(ziptotalf,ziptotal)
}
  

zip_final<-unique(ziptotalf)
write.csv(zip_final, file="C:/Users/waugh/Dropbox/Documents/GMS6804/Spatial_ids.csv", row.names = F)

