# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:22:11 2022


Default users password : P@ssw0rd
"""
import pandas as pd
import datetime
import time
import os
import mysql.connector
from mysql.connector import errorcode
from dateutil.tz import gettz
import os 
import io
from crypt_services import encrypt_sha256
import base64
from base64 import b64encode
MYDIR        = os.path.dirname(__file__)

   
config = {
  'host':"pinpointserver.mysql.database.azure.com",
  'port':"3306",
  'user':"arissdb",
  'password':"ppedbpass@12",
  'db':'ROOMCLEANINGDB'
}



def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary=file.read()
    return binary

class DBO:
    def __init__(self):
        try:           
            pass                
        except Exception as e:
            pass
           
            
        
        
    def create_user(self, username,fname,lname, role, password,emailid):
        try:             
            query = """INSERT INTO ROOMCLEANINGDB.USERS ( USERNAME ,FNAME,LNAME ,ROLE, PASSWORD,EMAILID,STATUS,photo_blob)
                         VALUES ( '{}','{}','{}','{}','{}','{}','{}','')""".format(username,fname,lname,role,password,emailid,'ACTIVE')
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return 0
        except Exception as e:
            print(e)
            return e
        
    
    def delete_user(self, username):
        try:
            if username not in ('admin'):
                stmt = "DELETE from ROOMCLEANINGDB.USERS where USERNAME = '" + username + "'"  
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                cursor.execute(stmt)    
                conn.commit()
                return "User Deleted Successfully"
            else:
                return "Error : Cannot delete default users."
            
        except Exception as e:
            return e

        
    def get_cred(self, username):
        try:
            stmt = "SELECT ROLE, PASSWORD,FNAME,LNAME  from ROOMCLEANINGDB.USERS where status='ACTIVE' and USERNAME = '" + username + "'"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            ret_obj = {"role": "", "password": ""}
            for row in cursor:
                ret_obj["role"] = row[0]
                ret_obj["password"] = row[1]
                ret_obj["username"] = row[2]+" "+row[3]
                
                break
            return ret_obj
        except Exception as e:
            return e
        
    
    def update_user(self, username, role, password):
        try:
            query="UPDATE ROOMCLEANINGDB.USERS set PASSWORD = " + password + ", ROLE = " + role + " where USERNAME = '" + username + "'"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("[+] Password updated :", self.conn.total_changes)
            return 0
        except Exception as e:
            return e 
    def update_user_details(self,basic_details):
        try:
            username  = basic_details['USERNAME']            
            FirstNAME = basic_details['FirstNAME']
            LastNAME  = basic_details['LastNAME']
            emaild    = basic_details['emaild']
            PASSWORD  = basic_details['PASSWORD']
            
            if PASSWORD=="":
                role      = basic_details['ROLE']
                status    = basic_details['STATUS']
                query ="""UPDATE ROOMCLEANINGDB.USERS set 
                        ROLE = '{}' ,FNAME = '{}' ,LNAME = '{}' ,EMAILID = '{}' ,STATUS = '{}' 
                        where USERNAME = '{}'""".format(role,FirstNAME,LastNAME,emaild,status,username)
            else:
                temp_password = encrypt_sha256(username+PASSWORD)
                query ="""UPDATE ROOMCLEANINGDB.USERS set 
                        FNAME = '{}' ,LNAME = '{}' ,EMAILID = '{}' ,PASSWORD ='{}'
                        where USERNAME = '{}'""".format(FirstNAME,LastNAME,emaild,temp_password,username)   
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit() 
            return 0
        except Exception as e:
            return e 

    def get_username(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT userName from ROOMCLEANINGDB.USERS")
            username_list = []
            for row in cursor:
                username_list.append(row[0])
            return username_list
        except Exception as e:
            print(e)
            return e
      
    def get_user_detail_by_userID_sheet(self,userid):
            stmt = "SELECT * from ROOMCLEANINGDB.USERS where USERNAME='{}'".format(userid)
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(stmt)
            user_list = []
            for row in cursor:
                user_list.append(list(row))
            user_frame = pd.DataFrame(user_list,columns = ['USERNAME'  , 'FNAME' ,
                                            'LNAME' , 'ROLE' , 'PASSWORD' , 'EMAILID' ,
                                            'STATUS'  , 'photo_blob' ])
            return user_frame[['USERNAME','FNAME','LNAME','ROLE','PASSWORD','EMAILID','STATUS']]
###########################################################End of user query ##################################################################
    def insert_product_details(self,temp_Df,userID,userName):
        try:
            query = "SELECT max(version) from ROOMCLEANINGDB.product_Details"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            VERSION = 1
            for row in cursor:
                if row[0]==None:
                    VERSION=1
                else:
                    VERSION=int(row[0])+1
            print(VERSION)
            query = "update ROOMCLEANINGDB.product_Details set STATUS='INACTIVE'"
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit() 
            for row in temp_Df.itertuples():                             
                ts = time.time()
                update_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
                update_time = str(update_time.strftime('%d/%m/%Y %H:%M:%S')).split(".")[0]               
                query = """INSERT INTO ROOMCLEANINGDB.product_Details 
                       (Product_Name ,Generic_Name ,
                         Form ,API_with_strength , 
                         Minimum_Batch_size_NOS ,Minimum_Batch_size_MG ,
                         MRDD,LRDD_MG, 
                         LRDD_NOS,PDE_VALUE  , 
                         LD50 ,NOEL ,
                         VERSION ,STATUS,UPDATED_BY)
                         VALUES ('{}','{}',
                         '{}','{}',
                         '{}','{}',
                         '{}','{}',
                         '{}','{}',
                         '{}','{}',
                         '{}','{}','{}')""".format(row[1],row[2],
                         row[3],row[4],
                         row[5],row[6],
                         row[7],row[8],
                         row[8],row[10],
                         row[11],row[12],
                         VERSION,'ACTIVE',userID)                                            
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()                
                cursor.execute(query)
                conn.commit()            
        except Exception as e:
            print(e)
            return e   
            
    def get_product_details(self):
        stmt = """SELECT Product_Name ,Generic_Name ,
                         Form ,API_with_strength , 
                         Minimum_Batch_size_NOS ,Minimum_Batch_size_MG ,
                         MRDD,LRDD_MG, 
                         LRDD_NOS,PDE_VALUE  , 
                         LD50 ,NOEL from ROOMCLEANINGDB.product_Details where status='ACTIVE' """
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        product_list = []
        for row in cursor:
            product_list.append(list(row))
        product_frame = pd.DataFrame(product_list,columns = ['Product_Name' ,'Generic_Name' ,
                         'Form' ,'API_with_strength' ,'Minimum_Batch_size_NOS','Minimum_Batch_size_MG' ,
                         'MRDD','LRDD_MG','LRDD_NOS','PDE_VALUE','LD50' ,'NOEL'])
        return product_frame
        
    def get_product_details_by_version(self,version):
        stmt = """SELECT Product_Name ,Generic_Name ,
                         Form ,API_with_strength , 
                         Minimum_Batch_size_NOS ,Minimum_Batch_size_MG ,
                         MRDD,LRDD_MG, 
                         LRDD_NOS,PDE_VALUE  , 
                         LD50 ,NOEL from ROOMCLEANINGDB.product_Details where version='{}' """.format(version)
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        product_list = []
        for row in cursor:
            product_list.append(list(row))
        product_frame = pd.DataFrame(product_list,columns = ['Product_Name' ,'Generic_Name' ,
                         'Form' ,'API_with_strength' ,'Minimum_Batch_size_NOS','Minimum_Batch_size_MG' ,
                         'MRDD','LRDD_MG','LRDD_NOS','PDE_VALUE','LD50' ,'NOEL'])
        return product_frame
        
    def insert_file(self,report_name,prepared_by,file_path):
        try:   
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()            
            binary_file = convert_into_binary(file_path)            
            sql_insert_blob_query = """ INSERT INTO ROOMCLEANINGDB.file_repo (report_name,
                                         prepared_by,file_blob) VALUES (%s,%s,%s)"""
            insert_blob_tuple = (report_name,prepared_by,binary_file)  
            cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            conn.commit()
            print('File inserted successfully')
        except Exception as e:
            print(e)
            print("Failed to insert blob into the table")
            
            
    def get_report_log(self,basic_details):
        USERNAME     = basic_details['USERNAME']
        startDate    = basic_details['startdate']
        endDate      = basic_details['enddate']
        
       
        stmt = "SELECT report_name,prepared_by,file_blob from ROOMCLEANINGDB.file_repo"      
        if USERNAME!="ALL":
            stmt=stmt+"  where  prepared_by='{}'".format(USERNAME)
        #if startDate!="" :
         #   startDate    =  datetime.datetime.strptime(startDate, "%Y-%m-%d").strftime("%d/%m/%Y")
          #  stmt=stmt+" and date >='{}'".format(startDate)
        
        print(stmt)
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        report_list = []
        for row in cursor:
            temp_row=[]
            temp_row.append(row[0])
            temp_row.append(row[1])
            file_name ="{}.xlsx".format(row[0])
            temp_row.append(file_name)
            temp_row.append(base64.b64encode(row[2]).decode('ascii'))
            
                      
            report_list.append(temp_row)
        report_frame = pd.DataFrame(report_list,columns = ['report_number','prepared_by','file_name','data'])
        
         
        return report_frame  
        
    def get_filtered_elogbook(self,user_id,STATUS,startDate,endDate):
     
        startDate  =  datetime.datetime.strptime(startDate, "%Y-%m-%d").strftime("%d/%m/%Y")
        endDate    =  datetime.datetime.strptime(endDate, "%Y-%m-%d").strftime("%d/%m/%Y")
        
        
        
        stmt= """SELECT VERSION ,STATUS,UPDATED_BY from ROOMCLEANINGDB.product_Details  where STATUS is not null""".format(startDate,endDate)
        
        if user_id!="ALL":
            stmt=stmt+" and UPDATED_BY='{}'".format(user_id)    
            
       
        if STATUS!="ALL":
            stmt=stmt+" and STATUS='{}'".format(STATUS)
            
            
        stmt = stmt + " group by VERSION,STATUS,UPDATED_BY order by VERSION desc"
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(stmt)
        expense_list = []
        for row in cursor:
            expense_list.append(list(row))
        elog_frame = pd.DataFrame(expense_list,columns = ['VERSION' ,'STATUS','UPDATED_BY' ])
        return elog_frame
 
