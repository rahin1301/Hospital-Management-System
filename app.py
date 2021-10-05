from flask import Flask,render_template, json, request,session,redirect
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
mysql=MySQL()
# mysql.init_app(app)
# from waitress import serve 
app = Flask(__name__)
app.secret_key = 'my name is abhinav'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Abhinav@1211'
app.config['MYSQL_DATABASE_DB'] = 'hospital_manage'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


# app.config['MYSQL_DATABASE_USER'] = 'sql12350891'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'gcKJTwhbZX'
# app.config['MYSQL_DATABASE_DB'] = 'sql12350891'
# app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'


mysql.init_app(app)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/showSignIn")
def showSignIn():
    return render_template("signin.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route("/userHome")
def userHome():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from receptionist;")
        data = cursor.fetchall()
        return render_template('userHome.html',value=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect("/")




@app.route("/check_appointments")
def check_appointments():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from appointments;")
        data = cursor.fetchall()
        # print(data)

        new_data=[]
        # i=1
        k="select * from doctor where Doctor_ID=%s"
        for row in data:
            # print(row)
            temp=[]

            temp.append(row[1])
            cursor = con.cursor()
            cursor.execute("select Name from doctor where Doctor_ID="+str(row[1]))
            doc_name=cursor.fetchall()
            temp.append(doc_name[0][0])
            temp.append(row[2])
            cursor.execute("select Name from patient where patient_id="+str(row[2]))
            p_name=cursor.fetchall()
            print()
            print()
            print(p_name)
            print()
            print()
            temp.append(p_name[0][0])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            temp.append(row[0])
            # temp.append(i)
            # i+=1
            new_data.append(temp)

        print(new_data)


        return render_template('check_appointments.html',value=new_data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')






@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from appointments where appointment_no="+str(id))
        data = cursor.fetchall()
        
        new_data=[]
        # i=1
        k="select * from doctor where Doctor_ID=%s"
        for row in data:
            # print(row)
            temp=[]

            temp.append(row[1])
            cursor = con.cursor()
            cursor.execute("select Name from doctor where Doctor_ID="+str(row[1]))
            doc_name=cursor.fetchall()
            temp.append(doc_name[0][0])
            temp.append(row[2])
            cursor.execute("select Name from patient where patient_id="+str(row[2]))
            p_name=cursor.fetchall()
            temp.append(p_name[0][0])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            temp.append(row[0])
            # temp.append(i)
            # i+=1
            new_data.append(temp)

        return render_template('edit.html',value=new_data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

        # cur.execute("""
        #        UPDATE students
        #        SET name=%s, email=%s, phone=%s
        #        WHERE id=%s
        #     """, (name, email, phone, id_data))
        # # flash("Data Updated Successfully")
        # mysql.connection.commit()


@app.route("/edit",methods=['POST'])
def edit():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            ano = request.form["ano"]
            did = request.form["did"]
            pid = request.form["pid"]
            doa = request.form["doa"]
            toa = request.form["toa"]
            stat = request.form["stat"]


            s="update appointments set date=%s, time=%s,status=%s where appointment_no=%s"
            cursor.execute(s,(doa,toa,stat,ano))
            conn.commit()
            cursor.execute("select * from appointments;")
            data = cursor.fetchall()
            print(data)

            print()
            print()
            print("appointent updated")
            print()
            print()

            return redirect('/check_appointments')


        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

            
    else:
        return render_template('error.html',error = 'Unauthorized Access')

        



@app.route('/pres/<int:id>',methods=['POST','GET'])
def pres(id):
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from appointments where appointment_no="+str(id))
        data = cursor.fetchall()
        
        new_data=[]
        # i=1
        k="select * from doctor where Doctor_ID=%s"
        for row in data:
            # print(row)
            temp=[]

            temp.append(row[1])
            cursor = con.cursor()
            cursor.execute("select Name from doctor where Doctor_ID="+str(row[1]))
            doc_name=cursor.fetchall()
            temp.append(doc_name[0][0])
            temp.append(row[2])
            cursor.execute("select Name from patient where patient_id="+str(row[2]))
            p_name=cursor.fetchall()
            temp.append(p_name[0][0])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            temp.append(row[0])
            # temp.append(i)
            # i+=1
            new_data.append(temp)

        return render_template('pres.html',value=new_data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')




@app.route('/pres1',methods=['POST','GET'])
def pres1():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            ano = request.form["ano"]
            qty = request.form["qty"]
            me1 = request.form["med"+str(0+1)]
            q1 = request.form["qt"+str(0+1)]
            med=[]
            qt=[]
            print(type(qty))
            for ip in range(int(qty)):
                print(ip)
                k = request.form["med"+str(ip+1)]
                l = request.form["qt"+str(ip+1)]
                print(k,l)
                med.append(int(k))
                qt.append(int(l))
            print(med,qt)

            s="insert into prescription values(%s,%s,%s)"

            for i in range(int(qty)):
                cursor.execute(s,(ano,med[i],qt[i]))
                conn.commit()

            cursor.execute("select * from prescription;")
            data = cursor.fetchall()
            print(data)

            print()
            print()
            print("prescription added")
            print()
            print()

            # data.append(ano)
            # data.append(did)
            # data.append(pname)
            # data.append(dname)
            # data.append(qty)

            s="update appointments set status='completed' where appointment_no=%s"
            cursor.execute(s,(ano))
            conn.commit()
            
            return redirect('/check_appointments')
        
        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

            
    else:
        return render_template('error.html',error = 'Unauthorized Access')


            # stat = request.form["stat"]




@app.route('/f_pres/<int:id>',methods=['POST','GET'])
def f_pres(id):
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from appointments where appointment_no="+str(id))
        data = cursor.fetchall()
        
        medi=[]
        # i=1
        # k="select * from doctor where Doctor_ID=%s"
        temp=[]
        for row in data:
            # print(row)
            

            # temp.append(row[1])
            temp.append(row[0]) # ano    0
            cursor = con.cursor()
            cursor.execute("select Name from doctor where Doctor_ID="+str(row[1]))
            doc_name=cursor.fetchall()
            temp.append(doc_name[0][0]) # dname    1
            # temp.append(row[2])
            cursor.execute("select Name from patient where patient_id="+str(row[2]))
            p_name=cursor.fetchall()
            temp.append(p_name[0][0])   #pname    2
            temp.append(row[3]) # date     3
            temp.append(row[4]) # time     4
            # temp.append(row[5])

            cursor.execute("select med_id,quantity from prescription where app_no="+str(id))
            data1 = cursor.fetchall()
            print(data1)
            po = len(data1)
            temp.append(po) # number of medicines    5

            
            # temp.append(i)
            # i+=1
            k = "select price,medicine_name from medicine where medicine_id=%s"
            
            tot=0
            for row1 in data1:
                tol=[]
                cursor.execute(k,(int(row1[0])))
                data2 = cursor.fetchall()
                tol.append(data2[0][1]) #med_name    5
                tol.append(data2[0][0]) # med_price    6
                tol.append(row1[1]) # quantity    7
                tot += int(row1[1])*int(data2[0][0])
                tol.append(row1[1]*data2[0][0]) # tot medicine amount   8
                medi.append(tol)
                
            temp.append(tot) # final toatal    6

            # new_data.append(temp)

        return render_template('f_pres.html',medicine=medi,value=temp)
    else:
        return render_template('error.html',error = 'Unauthorized Access')









@app.route('/erase/<int:id>',methods=['POST','GET'])
def erase(id):
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from appointments where appointment_no="+str(id))
        data = cursor.fetchall()
        
        new_data=[]
        # i=1
        k="select * from doctor where Doctor_ID=%s"
        for row in data:
            # print(row)
            temp=[]

            temp.append(row[1])
            cursor = con.cursor()
            cursor.execute("select Name from doctor where Doctor_ID="+str(row[1]))
            doc_name=cursor.fetchall()
            temp.append(doc_name[0][0])
            temp.append(row[2])
            cursor.execute("select Name from patient where patient_id="+str(row[2]))
            p_name=cursor.fetchall()
            temp.append(p_name[0][0])
            temp.append(row[3])
            temp.append(row[4])
            temp.append(row[5])
            temp.append(row[0])
            # temp.append(i)
            # i+=1
            new_data.append(temp)

        return render_template('delete.html',value=new_data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')



@app.route("/delete",methods=['POST'])
def delete():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            ano = request.form["ano"]
            did = request.form["did"]
            pid = request.form["pid"]
            doa = request.form["doa"]
            toa = request.form["toa"]
            stat = request.form["stat"]


            s="delete from appointments where appointment_no=%s"
            cursor.execute(s,(ano))
            conn.commit()
            cursor.execute("select * from appointments;")
            data = cursor.fetchall()
            print(data)

            print()
            print()
            print("Appointment deleted")
            print()
            print()

            return redirect('/check_appointments')


        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

            
    else:
        return render_template('error.html',error = 'Unauthorized Access')





@app.route("/fix_appointments")
def fix_appointments():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from doctor;")
        data = cursor.fetchall()
        return render_template('fix_appointments.html',value=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route("/app_fix",methods=['POST'])
def app_fix():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            ano = request.form["ano"]
            did = request.form["did"]
            pid = request.form["pid"]
            doa = request.form["doa"]
            toa = request.form["toa"]
            stat = request.form["stat"]


            s="insert into appointments values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(s,(ano,did,pid,doa,toa,stat))
            conn.commit()
            cursor.execute("select * from appointments;")
            data = cursor.fetchall()
            print(data)

            print()
            print()
            print("appointent fixed")
            print()
            print()

            return redirect('/check_appointments')


        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

            
    else:
        return render_template('error.html',error = 'Unauthorized Access')





@app.route('/medicine',methods=['POST','GET'])
def medicine():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from medicine;")
        data = cursor.fetchall()
        return render_template('medicine.html',value=data)

    else:
        return render_template('error.html',error = 'Unauthorized Access')







@app.route("/new_patient")
def new_patient():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from receptionist;")
        data = cursor.fetchall()
        return render_template('new_patient.html',value=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route("/p_add",methods=['POST'])
def p_add():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            p_id = request.form["p_id"]
            p_name = request.form["p_name"]
            p_age = request.form["p_age"]
            p_gender = request.form["p_gender"]
            dr = request.form["dr"]
            p_cno = request.form["p_cno"]
            p_address = request.form["p_address"]

            s="insert into patient values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(s,(p_address,p_gender,p_name,p_id,dr,p_age,p_cno))
            conn.commit()
            cursor.execute("select * from patient;")
            data = cursor.fetchall()
            print(data)

            print()
            print()
            print("New Patient added")
            print()
            print()

            return redirect('/userHome')


        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

            
    else:
        return render_template('error.html',error = 'Unauthorized Access')




@app.route("/doc")
def doc():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from doctor;")
        data = cursor.fetchall()

        new_data=[]
        for row in data:
            temp=[]
            temp.append(row[4]) #id
            temp.append(row[1]) #name
            cursor.execute("select name from hospital where Hospital_id="+str(row[6]))
            hos = cursor.fetchall()
            temp.append(hos[0][0])  #hos name
            temp.append(row[2]) # sp
            temp.append(row[3]) #type
            temp.append(row[5]) #cno
            new_data.append(temp)
        return render_template('doctor.html',value=new_data)
    
    else:
        return render_template('error.html',error = 'Unauthorized Access')



@app.route("/patient")
def patient():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from patient;")
        data = cursor.fetchall()

        new_data=[]
        for row in data:
            temp=[]
            temp.append(row[3]) #id
            temp.append(row[2]) #name
            temp.append(row[1])  #gender
            temp.append(row[5]) # age
            temp.append(row[4]) #dreg
            temp.append(row[6]) #cno
            temp.append(row[0]) #address
            new_data.append(temp)
        
        return render_template('patient.html',value=new_data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')







@app.route("/new_doc")
def new_doc():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from hospital;")
        data = cursor.fetchall()
        return render_template('new_doc.html',value=data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')



@app.route("/d_add",methods=['POST'])
def d_add():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            d_id = request.form["d_id"]
            d_name = request.form["d_name"]
            d_sp = request.form["d_sp"]
            d_type = request.form["d_type"]
            hs = request.form["hs"]
            d_cno = request.form["d_cno"]
            d_address = request.form["d_address"]

            s="insert into doctor values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(s,(d_address,d_name,d_sp,d_type,d_id,d_cno,hs))
            conn.commit()
            cursor.execute("select * from doctor;")
            data = cursor.fetchall()
            print(data)

            print()
            print()
            print("New Doctor added")
            print()
            print()

            return redirect('/userHome')


        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()

            
    else:
        return render_template('error.html',error = 'Unauthorized Access')









@app.route("/co_worker")
def co_worker():
    if session.get('user'):
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("select * from staff;")
        data = cursor.fetchall()

        new_data=[]
        s="select name from hospital where Hospital_id=%s"
        for row in data:
            temp=[]
            temp.append(row[1]) #eid
            temp.append(row[3]) #name
            temp.append(row[0]) #gender
            cursor.execute(s,(row[4]))
            data1 = cursor.fetchall()
            temp.append(data1[0][0]) # hname
            temp.append(row[5]) #mob
            temp.append(row[2]) #address
            new_data.append(temp)

            
        return render_template('co_worker.html',value=new_data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')





@app.route("/validateLogin",methods=['POST'])
def validateLogin():
    try:
        _id = request.form["id"]
        _password = request.form["in_password"]
        print(_id,_password)
        con = mysql.connect()
        cursor = con.cursor()

        cursor.execute("select * from receptionist;")
        data = cursor.fetchall()
        print()
        print()
        print(data)
        print()
        print()

        flag=0
        for i in data:
            if(i[0]==_id and (str(i[1])==_password)):
                flag=1
                break
        if flag==1:
            print("login successful")
            session['user'] = data[0][0]
            return redirect('/userHome')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
        
        # data = cursor.fetchall()
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/signup',methods=['POST'])
def signup():
    # print("hello")
    try:
        _id = request.form['id']
        _password = request.form['in_password']
        if _id and _password:

            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            print(_id,_hashed_password,_password)
            # cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            cursor.execute("select * from receptionist;")
            data = cursor.fetchall()
            print()
            print()
            print(data)
            print()
            print()
            flag=0
            for i in data:
                if(i[0]==_id):
                    flag=1
                    break
            if(flag==1):
                print("id already exist")
                return render_template('error.html',error = 'Wrong Email address or Password.')
                print("hello")
            else:
                s="insert into receptionist values(%s,%s)"
                cursor.execute(s,(_id,_hashed_password))
                conn.commit()
                cursor.execute("select * from receptionist;")
                data = cursor.fetchall()
                print(data)
                print("signup successful")
                session['user'] = data[0][0]
                return redirect('/userHome')

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

            
app.run()

# serve(app,host = "0.0.0.0",port = 8080)