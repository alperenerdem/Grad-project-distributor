from django.shortcuts import render,redirect 
from django.http import HttpResponse,FileResponse
import os
from uploadProjects.functions import handle_uploaded_file,handleRequestInstructor,handleRequestStudent
from uploadProjects.form import StudentForm,InstructorForm,ChooseForm,ReportForm 
import sqlite3

def reports(request):
    if request.method == 'POST':
        infos = request.POST
        if(infos.__contains__('key')):
            print(infos)
            password = infos["key"]
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute("SELECT Name FROM Professors WHERE Key is '" + password + "';")
            if(cur.fetchone()==None):
                con.commit()
                con.close()
                return HttpResponse("Şifre Yanlış")
            else:
                report = ReportForm(key = password)
                return render(request,"reports.html",{'form':report})
        else:
            if(infos.__contains__('rapor')):
                file = infos["reportCheck"]
                return FileResponse(open("uploadProjects/raporlar/"+file, 'rb'), content_type='application/pdf')
            else:
                for x in infos:
                    if(x.endswith(".pdf")):

                        path="uploadProjects/raporlar/"+x

                        if(infos[x]=="True"):
                            os.remove(path)
                        elif(infos[x]=="False"):
                            print("selam")
                            projectNumber = x[:-4].split('_')[0]
                            number = x[:-4].split('_')[1]
                            tercihFile = open("uploadProjects/ogrenciler/"+number+"/tercih.txt","r+")
                            for x in tercihFile:
                                x=x.replace('-'+projectNumber+'-',"-0-")
                                tercihFile = open("uploadProjects/ogrenciler/"+number+"/tercih.txt","w+")
                                tercihFile.write(x)
                            os.remove(path)
                return HttpResponse("Seçimler Kaydedildi")
            
    else:
        student = InstructorForm()  
        return render(request,"password.html",{'form':student})  

def uploadProjects(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():  
            return handle_uploaded_file(request.POST,request.FILES['file'])   
    else:
        print("hi")
        student = StudentForm()  
        return render(request,"index.html",{'form':student})  

def home(request):
    if request.method == 'POST':  
        infos = request.POST
        if(infos.__contains__('student')):
 
            return redirect(student)
        elif(infos.__contains__('prof')):

            return redirect(uploadProjects)
        elif(infos.__contains__('asistant')):
  
            return redirect(instructor)

        elif(infos.__contains__('degerlendirme')):
  
            return redirect(reports)

        
    else:
        return render(request,'home.html')



def instructor(request):  
    if request.method == 'POST':  
        return handleRequestInstructor(request.POST)
        
    else:

        student = InstructorForm()  
        return render(request,"instructor.html",{'form':student})  

def student(request):  
    if request.method == 'POST':  
        return handleRequestStudent(request.POST,request.FILES)
        
    else:
        print("hi")
        student = ChooseForm()  
        return render(request,"student.html",{'form':student})  