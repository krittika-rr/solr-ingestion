import os
import util

os.system('sudo apt-get install python-psycopg2')
os.system('sudo apt-get update')
os.system('sudo apt-get install postgresql postgresql-contrib')
import psycopg2
os.system("sudo -u postgres psql")
#con= psycopg2.connect ("localhost"
os.system("alter user  \"postgres \" with password '12345';")

conn = psycopg2.connect(host=util.host, user=util.user ,password=util.pwd,dbname=util.db)
cur=conn.cursor()
sql="CREATE TABLE public.gen(  dc_title character varying(800),  dc_identifier_uri character varying(800),  dspacetype character varying(200),  id character varying(50) NOT NULL,  dc_format_mimetype character varying(800),  dc_language_iso character varying(200),  dc_type character varying(800),  dc_date_issued character varying(200),  dc_publisher character varying(800),  dc_source_uri character varying(800),  lrmi_learningresourcetype character varying(200),  dateaccessioned character varying(200),  dc_source character varying(800),  dc_subject character varying(800),  lrmi_educationalalignment_educationallevel character varying(200),  dc_contributor_other character varying(800), lrmi_educationaluse character varying(800),  dc_contributor_author character varying(800),  dc_description character varying(20000),  dc_type_degree character varying(200),  lrmi_timerequired character varying(200),  dc_contributor_advisor character varying(800),  dc_date_awarded character varying(200),  dc_creator_researcher character varying(800),  dc_date_accessioned character varying(800),  dc_date_available character varying(800),  dc_description_provenance character varying(20000),  dc_subject_ddc character varying(800),  dc_title_alternative character varying(800),  lrmi_typicalagerange character varying(800),  lrmi_interactivitytype character varying(800),  lrmi_educationalrole character varying(800),  lrmi_educationalalignment_pedagogicobjective character varying(800),  lrmi_educationalalignment_educationalframework character varying(800),  lrmi_educationalalignment_difficultylevel character varying(800),  dc_identifier character varying(800),  dc_relation character varying(800),  dc_relation_requires character varying(800),  dc_format character varying(800),  dc_identifier_other character varying(800),  dc_publisher_institution character varying(800),  dc_contributor character varying(800),  dc_date_copyright character varying(800),  dc_description_abstract character varying(20000),  dc_publisher_date character varying(800),  dc_creator character varying(800),  dc_date_created character varying(800),  dc_description_extent character varying(20000),  CONSTRAINT gen_pkey PRIMARY KEY (id))WITH (  OIDS=FALSE);ALTER TABLE public.gen  OWNER TO postgres;"+util.user+";"

#cur.execute(sql)
conn.commit()
conn.close()
#CREATE ROLE krittika LOGIN  SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION;

