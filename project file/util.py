#shit=["dc_title","dc_identifier_uri","dspacetype","id","dc_format_mimetype","dc_language_iso","dc_type","dc_date_issued","dc_publisher","dc_source_uri","lrmi_learningresourcetype","dateaccessioned","dc_source","dc_subject","lrmi_educationalalignment_educationallevel","dc_contributor_other","lrmi_educationaluse","dc_contributor_author","dc_description","dc_type_degree","lrmi_timerequired","dc_contributor_advisor","dc_date_awarded","dc_creator_researcher","dc_date_copyright","dc_relation","dc_publisher_date" ,"dc_description_abstract" ,"dc_relation_requires","dc_identifier","dc_format","dc_identifier_other","dc_contributor" ,"dc_publisher_institution" ]
host='localhost'
pwd='dbuser'
db='kgp'
user='dbuser'
ip="localhost"

columnsq="select column_name from information_schema.columns where table_schema='public' AND table_name ='gen'"
dest="./switch2"
urd="/var/www/html/switch2/"
nspace1="{http://www.loc.gov/METS/}dmdSec"
nspace2="{http://www.loc.gov/mods/v3}dateAccessioned"
nspace3="{http://www.dspace.org/xmlns/dspace/dim}field"
nspace4="{http://www.loc.gov/METS/}structMap"
nspace5="{http://www.loc.gov/METS/}mptr"
nspace6="{http://www.w3.org/1999/xlink}href"
corename="collection1"



#query to delete all files on solr
#http://localhost:8983/solr/collection1/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E&commit=true


