import function
import os
import sys
 
n= sys.argv[1]
if n.find(".zip")>0:print str(function.function(n)) +" number of items have been stored into the database"

 
else:
  count =0
  for i in os.listdir(n):
    count =count+   function.function(n+"/"+i)
  print str(count)+" number of items have been stored into the database"
