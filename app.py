from flask import Flask, render_template, flash, url_for, request, make_response, jsonify, session,send_from_directory
from werkzeug.utils import secure_filename
import os, time
import io
import base64
import json
import datetime
import os, sys, glob
from flask import send_file
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from fnmatch import fnmatch
import time
import random
import pandas as pd
import flask
from db_dervices import DBO
from crypt_services import encrypt_sha256
import random
import string
from openpyxl import Workbook
from sheet_generation import Sheet_Generation


app = Flask(__name__)
app.secret_key = 'file_upload_key'
MYDIR = os.path.dirname(__file__)
print("MYDIR",MYDIR)
dbo = DBO()

app.config['UPLOAD_FOLDER_INPUTDATA'] = "static/inputData/"
equipmet_list = ['Dispensing Booth',
'Dispensing Scoop ( Small)','Dispensing Scoop (Large)',
'Spatula','Spatula' ,'Manufacturing Scoop',
'Blender Bin (350 liter)' ,'Blender Bin (25 liter)' ,
'Vibro Sifter II','sampling rod','sampling rod' 
]

sent_mail                     = False
server                        = 'smtp-mail.outlook.com'
port                          =  587
username                      = "pinpointengineers@hotmail.com"
password                      = "#############@12"
send_from                     = "pinpointengineers@hotmail.com"
send_to                       = "ashish@pinpointengineers.co.in"

def send_mail(subject,text,files,file_name,isTls=True):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if file_name!="":
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}.xlsx'.format(file_name))
            msg.attach(part)
            
        smtp = smtplib.SMTP(server, port)
        if isTls:
            smtp.starttls()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        
#################################### Start Login logout ######################################       
@app.route("/")
def render_default():
    session.pop('user', None)
    session.pop('selected_file', None)
    flash('Logout Successful')
    return make_response(render_template("LOGINPAGE/login.html",msg = True,err = False, warn = False,message='Logout Successful'),200)
    
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('selected_file', None)
    flash('Logout Successful')
    return make_response(render_template("LOGINPAGE/login.html",msg = True,err = False, warn = False,message='Logout Successful'),200)    
    
@app.route("/render_login", methods=["GET", "POST"])
def render_login(): 
    form_data    = request.form
    user_id      = form_data['login'].lower()
    password     = form_data['password']
    enc_pass     = encrypt_sha256(user_id+password)
    print(enc_pass)
    account      = dbo.get_cred(user_id)
    print(account)
    if(enc_pass == account["password"]):        
      session_var = {"user": user_id, "role": account["role"],"username": account["username"]}
      session['user'] = session_var
      return make_response(render_template('LOGINPAGE/homepage.html',msg = True, err = False, warn = False, role = session_var["role"]),200)
    else:
      flash('Invalid Credentials')
      return make_response(render_template("LOGINPAGE/login.html", msg = False, err = True, warn = False),403)   

#################################### End Login logout ###################################### 



############################### Start Admin Panel   #####################################################################   
@app.route("/add_user_page")
def add_user_page():
    if 'user' in session:
        session_var = session['user']
        return make_response(render_template('ADMIN/ADD_USER.html',role = session_var["role"]),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)
    
    

@app.route("/submit_add_user" )    
def submit_add_user():
    if 'user' in session:
        data            = request.args.get('params_data')
        data            = json.loads(data)    
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['Role','fname','lname','Password','email']]
        print(temp_df)  
        userlist =[]
        for row in temp_df.itertuples():        
            fname    = str(row[2]).strip()
            lname    = str(row[3]).strip()
            role     = row[1]
            password = row[4]
            email    = row[5]
            fname    = fname.lower()
            lname    = lname.lower()
            username = fname+lname[:2]+str(random.randint(10,99))
            dbo.create_user(username,fname,lname, role, encrypt_sha256(username+password),email)
            userlist.append(username)
            subject   = "NEW USER REGISTERED TYPE -{} ID: {} ".format(role,username)
            text      = """Hi PinPoint Team \n\n
                           {} {} has been reigistered into HVAC system with  {} role \n\n
                           Kindly note done Login ID for Reference - {}
                           Regards \n
                           Ajeet Shukla :) :) :)""".format(fname,lname,role,username)
            #send_mail(subject,text,"","") 
            d = {"error":"none","userID":userlist}   
            return json.dumps(d)
    return make_response(render_template('LOGINPAGE/login.html'),200)   

@app.route("/update_user_details_page")  
def update_user_details ():
    if 'user' in session:
        usernameList  = dbo.get_username()
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('ADMIN/UPDATE_USER_DETAILS.html',usernameList=usernameList,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)     
 

    
@app.route("/get_user_detail_by_userID_sheet")  
def get_user_detail_by_userID_sheet ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        user_detail   = dbo.get_user_detail_by_userID_sheet(basic_details['USERNAME']).to_dict('records') 
        d = {"error":"none","user_list":user_detail}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/delete_user")  
def delete_user ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        ret_msg       = dbo.delete_user(basic_details['USERNAME'])
        d = {"error":ret_msg}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/submit_update_user_details")  
def submit_update_user_details ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        dbo.update_user_details(basic_details) 
        d = {"error":"none"}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
    
@app.route("/update_self_profile_page")  
def update_self_profile_page ():
    if 'user' in session:
        usernameList  = dbo.get_username()
        session_var = session['user']
        role = session_var["role"]
        user_id = session_var["user"]
        user_detail   = dbo.get_user_detail_by_userID_sheet(user_id).to_dict('records') 
        print(user_id)
        print(user_detail)
        return make_response(render_template('ADMIN/SELF_PROFILE.html',user_detail = user_detail,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)        
############################### END Admin Panel   #####################################################################  

@app.route("/UpdateProductList")
def UpdateProductList():
    product_frame  = dbo.get_product_details()
    product_list   = product_frame.to_dict('records')
    return make_response(render_template('UpdateProductList.html',product_list  = product_list),200) 
    
@app.route("/submit_UpdateProductList")    
def submit_UpdateProductList():  
    session_var     = session['user']
    role            = session_var["role"]  
    userName        = session_var['username']
    data            = request.args.get('params_data')
    data            = json.loads(data)  
    observation     = data['observation']
    temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
    temp_df         = temp_df[['Product_Name','Generic_Name','Form', 'API_with_strength' ,'Minimum_Batch_size_NOS',
                       'Minimum_Batch_size_MG','MRDD','LRDD_MG','LRDD_NOS','PDE_VALUE','LD50','NOEL']]
    dbo.insert_product_details(temp_df,userName,userName)
    d = {"error":"none",}
    return json.dumps(d)
    
@app.route("/cleaning_room")
def cleaning_room():    
    product_frame  = dbo.get_product_details()
    product_list   = product_frame.Product_Name.unique().tolist()
    return make_response(render_template('cleaning_room.html',equipmet_list  = equipmet_list,product_list  = product_list),200) 
    
    

@app.route("/submit_cleaning_room_report")    
def submit_cleaning_room_report():
    session_var     = session['user']
    role            = session_var["role"]  
    userName        = session_var['username']
    data            = request.args.get('params_data')
    data            = json.loads(data)   
    temp_df         = pd.DataFrame(data)    

    product_frame  = dbo.get_product_details()
    file_name = "Cleaning_room_report_{}.xlsx".format(str(datetime.datetime.today().strftime('%d_%m_%Y')))    
    store_location = "static/inputData/"+file_name
    final_working_directory=MYDIR + "/" +store_location
    #final_working_directory=store_location
    
    product_frame['API_with_strength']      = product_frame['API_with_strength'].astype(float)
    product_frame['Minimum_Batch_size_NOS'] = product_frame['Minimum_Batch_size_NOS'].astype(float)
    product_frame['Minimum_Batch_size_MG']  = product_frame['Minimum_Batch_size_MG'].astype(float)    
    product_frame['MRDD']                   = product_frame['MRDD'].astype(float)
    product_frame['LRDD_MG']                = product_frame['LRDD_MG'].astype(float)
    product_frame['LRDD_NOS']               = product_frame['LRDD_NOS'].astype(float)
    product_frame['PDE_VALUE']              = product_frame['PDE_VALUE'].astype(float)
    product_frame['LD50']                   = product_frame['LD50'].astype(float)
    product_frame['NOEL']                   = product_frame['NOEL'].astype(float)
        
    wb = Workbook()
    ws = wb.active 
    wb = Sheet_Generation.create_equipment_sheet(wb,ws,temp_df)
    wb = Sheet_Generation.create_product_sheet(wb,ws,product_frame)
    wb = Sheet_Generation.create_pde_sheet(wb,ws,product_frame)
    wb = Sheet_Generation.create_toxicity_sheet(wb,ws,product_frame)
    wb = Sheet_Generation.create_dose_base_sheet(wb,ws,product_frame)
    wb.save(final_working_directory)
        
    dbo.insert_file(file_name,userName,final_working_directory)

    if sent_mail:
        send_mail(subject,text,final_working_directory,file_name) 
    d = {"error":"none","file_name":file_name,"file_path":store_location}
   
    return json.dumps(d)   

@app.route("/download_report")  
def download_report ():
    if 'user' in session:
        account = session["user"]
        usernameList = [account['user']]
        role         =  account['role']
        print(account)
        if role == "admin":
            usernameList  = dbo.get_username()           
        return make_response(render_template('DOWNLOAD_REPORT.html',usernameList=usernameList,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)  

@app.route("/view_reportlog")  
def view_reportlog():
    if 'user' in session:   
        data            = request.args.get('params_data')
        basic_details   = json.loads(data)    
        report_log      = dbo.get_report_log(basic_details).to_dict('records')
        d = {"error":"none","report_log":report_log}  
        return flask.jsonify(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 

@app.route("/render_elogbook")
def render_elogbook():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]       
        usernameList  = dbo.get_username()
        
        return make_response(render_template('ELOGBOOK.html', usernameList=usernameList,role = role),200) 
    return make_response(render_template('LOGINPAGE/login.html'),200)    
    
@app.route("/get_elogbook")  
def get_elogbook ():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)  
        elog_list     = dbo.get_filtered_elogbook(basic_details['user_id'],basic_details['STATUS'],
                                    basic_details['startdate'],basic_details['enddate']
                                ).to_dict('records')
     
        d = {"error":"none","elog_list":elog_list}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 
    
@app.route("/getProductData")
def getProductData():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)
        print(basic_details['version_number'])
        product_frame  = dbo.get_product_details_by_version(basic_details['version_number'])
        product_list   = product_frame.to_dict('records')
        d = {"error":"none","product_log":product_list}
        return json.dumps(d) 
    return make_response(render_template('LOGINPAGE/login.html'),200) 


if __name__ == '__main__':
    app.debug = True
    app.run()

