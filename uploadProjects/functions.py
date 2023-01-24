from django.http import HttpResponse,FileResponse
from reportlab.pdfgen import canvas  
from .models import TestList
import sqlite3
import os,shutil
import PyPDF2
projectStarts = ["1","2","3","4","5","6","7","8","9","•"]
courseExt = ["BIL","BİL","CSE","MAT","ENG","FİZ","PHY"]





def esletirmeBaslat():
    tests = TestList()
    tests.createStudents()
    tests.createDumbStudents()
    tests.createProjects()
    tests.makeRandomChoicesFromProjects()
    tests.matching()
    #tests.report()

    tests.printStudents()
##For grad student

def handleRequestStudent(infos,files):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT stat FROM status WHERE name is 'choosing'")
    sonuc = cur.fetchone()
    if(sonuc=="off"):
        con.commit()
        con.close()
        return HttpResponse("Tercihler Aktif Değil, başlamadı veya bitti")

    #sonra Transkript kontrolü yapıyoruz
    number = checkIfItsTranscript((files['transkript']))
    if(number.startswith("Hata")):
        return HttpResponse(number)
    
    tercihList=[]
    for x in infos:
        if("Tercih" in x):
            if(int(infos[x])>0):
                tercihList.append(int(infos[x]))
    cur.execute("SELECT * FROM Projects")
    path = 'uploadProjects/ogrenciler/'+number+"/tercih.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+') as destination:  
        for x in tercihList:
            destination.write(str(x)+"-")
    projects=cur.fetchall()
    #print(projects)
    for y in files:
        if("file" in y):
            order = y[4:]
            print(order)
            projectNumber = int(infos['Tercih'+order])
            print(projectNumber)
            file = files[y]
            print(projectNumber)
            print(projects[projectNumber-1][2])
            if(projectNumber>0 and projects[projectNumber-1][2] == "1"):
                path = 'uploadProjects/raporlar/'
                print(path)
                path = path + (str(projectNumber)+"_"+number) + ".pdf"
                print(path)
                with open(path, 'wb+') as destination:  
                    for chunk in file.chunks():  
                        destination.write(chunk)

    con.commit()
    con.close()
    return HttpResponse("Tercihini yaptın")
    #sonra Transkript kontrolü yapıyoruz
    





def checkIfItsTranscript(pdfFile):
    pdfReader = PyPDF2.PdfFileReader(pdfFile,strict=False)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText().splitlines()
    if(text[0].startswith('Öğrenci No')):
        return transcriptDevlet(pdfFile)
    elif(text[0].startswith('Öğrenci Müfredat Durum Formu')):
        return "Hatalı Transkript, EDevletteki transkripti yükleyiniz."
        #return transcriptMufredat(pdfFile)
    else:
        return "Hatalı Transkript, EDevletteki transkripti yükleyiniz."
        #return transcriptGtu(pdfFile)
        

    return True

def transcriptDevlet(infos):
    pdfReader = PyPDF2.PdfFileReader(infos,strict=False)
    for x in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(x)
        text = pageObj.extractText().splitlines()
            
        for index,y in enumerate(text):
            if(":Genel Not Ortalaması" in y and "GNO" not in y):
                avgGrade = y.split(":")[0]
            elif (y.startswith("Doğum Tarihi")):
                number = y[12:]
                print(number)
                path = 'uploadProjects/ogrenciler/'+number+"/devletTranskript.pdf"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb+') as destination:  
                    for chunk in infos.chunks():  
                        destination.write(chunk)
                return number
    return "Hatalı Transkript"
                

def transcriptGtu(infos):
    pdfReader = PyPDF2.PdfFileReader(infos,strict=False)
    for x in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(x)
        text = pageObj.extractText().splitlines()
            
        for index,y in enumerate(text):
            if(":Genel Not Ortalaması" in y and "GNO" not in y):
                avgGrade = y.split(":")[0]
            elif (y.startswith("Ayrılış")):
                number = text[index-3].split()[1]
                path = 'uploadProjects/ogrenciler/'+number+"/ogrencisleriTranskript.pdf"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb+') as destination:  
                    for chunk in infos.chunks():  
                        destination.write(chunk)
                return number
                
    return "Hatalı Transkript"

def transcriptMufredat(infos):   
    pdfReader = PyPDF2.PdfFileReader(infos,strict=False)
    for x in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(x)
        text = pageObj.extractText().splitlines()
            
        for index,y in enumerate(text):
            print(y)
            if(":Genel Not Ortalaması" in y and "GNO" not in y):
                avgGrade = y.split(":")[0]
            elif (y.startswith("Gebze Teknik Üniversitesi")):
                number = text[index+2][2:]
                print(number)
                path = 'uploadProjects/ogrenciler/'+number+"/müfredatTranskript.pdf"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb+') as destination:  
                    for chunk in infos.chunks():  
                        destination.write(chunk)
                return number
    return "Hatalı Transkript"

##For grad instructor
def handleRequestInstructor(infos):
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute("SELECT name FROM status WHERE stat is '" + infos['key'] + "';")
    if(cur.fetchone()==None):
        con.commit()
        con.close()
        return HttpResponse("Şifre Yanlış")
    
    if(infos.__contains__('baslat')):
        cur.execute("UPDATE status SET stat = 'off' WHERE name is 'uploadProjects'")
        cur.execute("UPDATE status SET stat = 'on' WHERE name is 'choosing'")
        cur.execute("DELETE from Projects")
        con.commit()
        con.close()
        addProjects()
        return HttpResponse("Tercihler Başladı")
    if(infos.__contains__('bitir')):
        cur.execute("UPDATE status SET stat = 'on' WHERE name is 'uploadProjects'")
        cur.execute("UPDATE status SET stat = 'off' WHERE name is 'choosing'")
        con.commit()
        con.close()
        return HttpResponse("Tercihler Bitti")
    if(infos.__contains__('resetle')):
        cur.execute("UPDATE status SET stat = 'on' WHERE name is 'uploadProjects'")
        cur.execute("UPDATE status SET stat = 'off' WHERE name is 'choosing'")
        cur.execute("DELETE from Projects")
        con.commit()
        con.close()
        ogrenciler = 'uploadProjects/ogrenciler'
        projeler = 'uploadProjects/projeler'
        for x in os.listdir(projeler):
            os.remove(projeler+"/"+x)
        for x in os.listdir(ogrenciler):
            for y in os.listdir(ogrenciler+"/"+x):
                os.remove(ogrenciler+"/"+x+"/"+y)
            os.rmdir(ogrenciler+"/"+x)
        addProjects()
        return HttpResponse("Projeler,tercihler ve transkriptler resetlendi")
    if(infos.__contains__('eslestir')):
        esletirmeBaslat()
        source = 'uploadProjects/static/upload/projects'
        dest = 'uploadProjects/projeler'
        for x in os.listdir(dest):
            os.remove(dest+"/"+x)
        shutil.copytree(source, dest,dirs_exist_ok=True)
        return FileResponse(open('listOfMatches.pdf', 'rb'), content_type='application/pdf')
  

def addProjects():
    directories = os.listdir("uploadProjects/static/upload/projects/")
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    for x in directories:
        cur.execute("SELECT * FROM Professors WHERE Key is '" + x[:-4] + "';")
        rows = cur.fetchone()
        rapor =rows[2]
        name = rows[1]
        pdfFileObj = open('uploadProjects/static/upload/projects/'+x, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj,strict=False)
        flag = True
        seperator = "."
        for x in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(x)
            text = pageObj.extractText().splitlines() 
            for index,y in enumerate(text):
                if any(y.startswith(ext) for ext in projectStarts):
                    if(flag):
                        seperator = y[1:2]
                        flag=False
                    
                    if(checkIfItsProject(y.split(seperator)[0]) and len(y)>5):
                        cur.execute("INSERT INTO Projects VALUES (\"" + str(y) + "\",'" + name + "','"+ str(rapor) + "')")
                                
    con.commit()
    con.close()
                        





##For Teachers
def handle_uploaded_file(infos,f):
    result,name = checkKey(infos)
    if(result==1):  
        with open('uploadProjects/static/upload/projects/'+infos["key"]+".pdf", 'wb+') as destination:  
            for chunk in f.chunks():  
                destination.write(chunk)
        return HttpResponse(name + " Proje Listesi Eklendi <br>" + checkProjects(infos["key"]))
    elif(result==2):
        with open('uploadProjects/static/upload/projects/'+infos["key"]+".pdf", 'wb+') as destination:  
            for chunk in f.chunks():  
                destination.write(chunk)
            checkProjects(infos["key"])
        return HttpResponse(name + " Proje Listesi Güncellendi <br>" + checkProjects(infos["key"]))
    elif(result==0):
        return HttpResponse("Şifre yanlış")

def checkProjects(fileName):
    pdfFileObj = open('uploadProjects/static/upload/projects/'+fileName+".pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj,strict=False)
    flag = True
    seperator = "."
    projectCount = 0
    projects = ""
    for x in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(x)
        text = pageObj.extractText().splitlines() 
        for index,y in enumerate(text):
            if any(y.startswith(ext) for ext in projectStarts):
                if(flag):
                    seperator = y[1:2]
                    flag=False
                
                if(checkIfItsProject(y.split(seperator)[0]) and len(y)>5):
                    projects = projects + (y[y.index(seperator)+1:]) +"<br>"
                    projectCount = projectCount+1
    returnStr = " Toplam proje sayısı = " + str(projectCount) + "<br><br>" + projects
    return returnStr


def checkIfItsProject(string):
    if(string.isnumeric() or string in projectStarts):
        return True
    return False

def checkKey(infos):
    key = infos["key"]
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT Name FROM Professors WHERE Key is '" + key + "';")
    if(cur.fetchone()==None):
        con.commit()
        con.close()
        return 0,""
    if(infos.__contains__('rapor')):
        cur.execute("UPDATE Professors SET Rapor = '"+ str(1) +"' WHERE Key is '" + key + "';")
    else:
        cur.execute("UPDATE Professors SET Rapor = '"+ str(0) +"' WHERE Key is '" + key + "';")

    cur.execute("UPDATE Professors SET Dagitma = '"+ infos["dagitmaSekli"] +"' WHERE Key is '" + key + "';")

    cur.execute("SELECT Name FROM Professors WHERE Key is '" + key + "';")
    name=cur.fetchone()[0]
    cur.execute("SELECT Yükledi FROM Professors WHERE Key is '" + key + "';")
    yukledi = cur.fetchone()[0]
    if(yukledi==1):
        con.commit()
        con.close()
        return 2,name


  
  
    cur.execute("UPDATE Professors SET Yükledi = '"+ str(1) +"' WHERE Key is '" + key + "';")
    con.commit()
    con.close()
    return 1,name