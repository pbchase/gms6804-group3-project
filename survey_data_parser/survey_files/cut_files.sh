for entry in survery_files/*
do
  name=${entry##*/}
  echo $name
  cut -d ',' -f1,4-30 $name > cut_files/$name

  sed -i 's/"//g' cut_files/$name
done


