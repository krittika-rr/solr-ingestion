#from pythonds.basic.stack import Stack
import sys
import os
import psycopg2
import util
import zipfile
import urllib
import xml.etree.ElementTree as ET
import zipfile
def function(interm):

 try:conn = psycopg2.connect(host=util.host, user=util.user ,password=util.pwd,dbname=util.db)
 except:print "connection to database failed"

#constants in a util.py 
 flag =0

 f= zipfile.ZipFile(interm, 'r').namelist()[0]

 #unzipping the main aip file
 os.system("unzip "+ interm+ " -d .")
 SRCBASE=f

 count=0

 shit=list()
 cur= conn.cursor()
 cur.execute(util.columnsq)
 it= cur.fetchall()
 for i in it:
   shit.append(i[0])

 DEST=util.dest
 BASEURL="http://"+util.ip+"/switch2/"
 #make directory to inflate the component zip files
 try:os.system("mkdir "+ DEST)
 except:print "failed to make directory"


 URD=util.urd+f
 #make directory for local server access
 os.system("mkdir "+ URD)
 #unzipping component files
 for i in os.listdir(SRCBASE):     
    os.system("unzip "+ SRCBASE+"/"+i +" -d "+DEST+"/"+i)

 count=0
 s=list()


 for i in os.listdir(DEST):
    
    
    if i.find("COMMUNITY")<0 and i.find("COLLECTION")<0 and i.find("ITEM")<0:
    #In a queue appending the master file      
          
          s.append([i,""])
 num=len(os.listdir(DEST))
 
 while count<=num :
       #getting the first item from the queue to process it
       if len(s)==0 :break
       maha=s.pop()
             
       i=maha[0]
       par=maha[1]

       
       #parsing the mets file to get all the metadata       
       tree = ET.parse(DEST+"/"+ i +"/mets.xml")
       root = tree.getroot()
       
       l= dict()
        
       l["id"] = root.attrib.get("OBJID")[5:]
       n= root.findall(util.nspace1)
       for child in n[0].iter(util.nspace2):
               l["dateAccessioned"]=child.text
       if i.find("COMMUNITY")>=0 and par!="":
          l["dspacetype"]="COMMUNITY"
          
          for child in n[1].iter(util.nspace3):
             if child.text is not None and child.text.find("hdl.handle")<0:l[child.attrib.get("mdschema")+"_"+child.attrib.get("element")]=child.text
          del l["dc_identifier"]
          
          tit=l["dc_title"].replace("/", "_")
          tit=tit.replace(" ", "_")
          relp=URD+par+tit
          if not os.path.exists(relp):
             os.mkdir(relp)


       elif i.find("COLLECTION")>=0 and par!="": 
          
          l["dspacetype"]="COLLECTION"
          
          for child in n[1].iter(util.nspace3):
             if child.text is not None  and child.text.find("hdl.handle")<0 :l[child.attrib.get("mdschema")+"_"+child.attrib.get("element")]=child.text
          del l["dc_identifier"]
          tit=l["dc_title"].replace("/", "_") 
          tit=tit.replace(" ", "_")        
          relp=URD+par+tit
          if not os.path.exists(relp):           os.mkdir(relp)

       
       elif i.find("ITEM")>=0 and par!="":
          l["dspacetype"]="ITEM"
          
          
          for child in n[1].iter(util.nspace3):
              if  child.text.find("hdl.handle")>=0:continue
               
              elif child.attrib.get("qualifier") is not None : 
                     key=(child.attrib.get("mdschema")+"_"+child.attrib.get("element")+"_"+child.attrib.get("qualifier")).lower()
                     if key not in shit: 
                             #if column is not in the database table, add column
                             shit.append(key)
                             if key.find("description")>0:cur.execute("ALTER TABLE GEN ADD COLUMN "+key+" VARCHAR(20000);")
                             else:cur.execute("ALTER TABLE GEN ADD COLUMN "+key+" VARCHAR(800);")
                             
                             conn.commit()
                             
                     l[key]=l.get(key,"")+child.text+";"

                              
                         
              else: 
                     key=child.attrib.get("mdschema")+"_"+child.attrib.get("element").lower()
                     
                     if key not in shit: 
                             #if column is not in the database table, add column
                             shit.append(key)
                             cur.execute("ALTER TABLE GEN ADD COLUMN "+key+" VARCHAR(800);")
                             
                             conn.commit()
                             

                     l[key]=l.get(key,"")+child.text+";"
          tit=l["id"].replace("/", "_")
          relp=URD+par+tit
          
          if not os.path.exists(relp):
             os.mkdir(relp)
             
            
          for j in os.listdir(DEST+"/"+i):
             #if the aip file has content. Storing it on local system and generating url and pushing data to  solr.Note that it uploads only one file. If this has to be executed for multiple files- everything after this condition has to be executed for each file
             if j.find(".txt")<0 and j.find(".")>0 and j!="mets.xml":
                 flag=1
             
               
                 fil= DEST+"/"+i+"/"+j
                 #extracting content from the content file by calling java class ParserExtraction and storing content in buffer.txt.
                 os.system('java -cp ".:./jarfiles/*" ParserExtraction '+fil)
          
                 os.system("cp "+fil+" "+relp+"/")
                 #generating url
                 l['dc_identifier_uri']=BASEURL+relp[22:]
                 b=list()
                 for key, val in l.items():
                   if val!=None:
                     #encoding the metadata first to utf-8 and then to url encoding
                     z=urllib.quote_plus(val.encode('utf-8'))
                     b.append("&literal."+key+"_t=\""+z+"\"") 
                 st="".join(b)
                 #query to upload data to solr
                 query='curl "http://'+util.ip+':8983/solr/'+util.corename+'/update/extract?commit=true&literal.id='+l["id"]+st+'&captureAttr=true&defaultField=text&capture=div&fmap.div=foo_t&boost.foo_t=3" -F "myfile=@buffer.txt"'

                 try:os.system(query)
                 except:print query
          
                     
          
          

       else:
          par=""
          l["dspacetype"]="MASTER"
          
          for child in n[1].iter(util.nspace3):
               if child.text is not None :     l[child.attrib.get("mdschema")+"_"+child.attrib.get("element")]=child.text
          #for child in  root.iter("{http://www.loc.gov/mods/v3}identifier"):
                #l["dc_identifier_uri"]=child.text

          del l["dc_identifier"]
          tit=l["dc_title"].replace("/", "_")
          tit=tit.replace(" ", "_")
          relp=URD+par+tit
          if not  os.path.exists(relp):
           os.mkdir(relp)
       for child in root.iter(util.nspace4):
           for c in child.iter(util.nspace5):
             if c.attrib.get("LOCTYPE")=='URL':
              s.insert(0,[ c.attrib.get(util.nspace6),par+tit+"/"])

        
       m=",".join(l.keys()).upper() 
       
       z=l.values()
       num=")s, %(".join(l.keys())
       
       #query to make an entry into the database
       sql="""INSERT INTO GEN ("""+ m +""") VALUES(%("""+num+""")s);"""
       try:
         
         cur.execute(sql,l)
         count= count+1
       except:       print i, par
      
          
         
 
       conn.commit()
           
   


 conn.close()
 #delete component zip files 
 os.system("rm -r "+ DEST)
 os.system("rm -rf ~/.local/share/Trash/files/"+DEST)
 #delete unzipped aip file
 os.system("rm -r "+ SRCBASE)
 os.system("rm -rf ~/.local/share/Trash/files/"+SRCBASE)

 if flag==0:
    #if  no content was present , delete directory made for local server access
    os.system("rm -r "+ URD)
    os.system("rm -rf ~/.local/share/Trash/files/"+URD)
 return count

