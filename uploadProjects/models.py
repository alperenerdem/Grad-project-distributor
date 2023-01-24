from django.db import models 
import os
import PyPDF2,sqlite3
from docx2pdf import convert
import random 
from fpdf import FPDF

noteDict = {"AA":4,"BA":3.5,"BB":3,"CB":2.5,"CC":2,"DC":1.5,"DD":1,"FF":0}
class Proffessor(models.Model):  
    password = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)  
    class Meta:  
        db_table = "proffessor"  

class TestList(models.Model):
    def __init__(self):
        self.students = []
        self.teachers = []
        self.projects = {}

    def createDumbStudents(self):
        while(len(self.students)<80):
            tempStudent = Student(str(len(self.students)),True)
            self.students.append(tempStudent)

    def createStudents(self):
        self.directories = os.listdir("uploadProjects/ogrenciler/")
        for x in self.directories:
            tempFiles = os.listdir("uploadProjects/ogrenciler/"+x)
            for y in tempFiles:
                if(y.endswith("Transkript.pdf")):
                    pdfFileObj = open("uploadProjects/ogrenciler/"+x+"/"+y, 'rb')
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)               
                    tempStudent = Student(pdfReader,False)
                    tercih = open("uploadProjects/ogrenciler/"+x+"/tercih.txt", 'r')
                    for line in tercih:
                        tempChoices = line.split('-')[:-1]
                        break
                    res = [eval(i)-1 for i in tempChoices]
                    
                    tempStudent.choiceList = res

                    self.students.append(tempStudent)
                    pdfFileObj.close()
                    break

    def createProjects(self):
        self.directories = os.listdir("uploadProjects/projeler/")
        for y in self.directories:
            if(y.endswith("docx")):
                convert("uploadProjects/projeler/"+y,"uploadProjects/projeler/"+y+".pdf")
                os.remove("uploadProjects/projeler/"+y)
        self.directories = os.listdir("uploadProjects/projeler/")
        for y in self.directories:
            pdfFileObj = open("uploadProjects/projeler/"+y, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj,strict=False)               
            tempProje = Teacher(pdfReader,y.split(".")[0])
            self.teachers.append(tempProje)
            pdfFileObj.close()
        count = 0
        for x in self.teachers:
            for y in x.projects:
                self.projects[str(count)] = y
                count = count +1

    def makeRandomChoicesFromProjects(self):
        for x in self.students:
            if(len(x.choiceList)<1 and x.dumbStudent):
                x.choiceList = (random.sample(range(0, len(self.projects)), random.randint(1, 10)))

    def matching(self):
        #print("hi")
        for x in self.students:
            if(x.choiceList[0]>-1):
                firstProject = str(x.choiceList[0])
                self.projects[firstProject].firstChosen.append(x)
                for index,y in enumerate(x.choiceList):
                    if(y>-1):
                        projectNumber = str(y)
                        if(index==1):
                            self.projects[projectNumber].secondChosen.append(x)
                        elif(index==2):
                            self.projects[projectNumber].thirdChosen.append(x)
                        elif(index==3):
                            self.projects[projectNumber].fourChosen.append(x)
                        elif(index==4):
                            self.projects[projectNumber].fiveChosen.append(x)
                        elif(index==5):
                            self.projects[projectNumber].sixChosen.append(x)
                        elif(index==6):
                            self.projects[projectNumber].sevenChosen.append(x)
                        elif(index==7):
                            self.projects[projectNumber].eightChosen.append(x)
                        elif(index==8):
                            self.projects[projectNumber].nineChosen.append(x)
                        elif(index==9):
                            self.projects[projectNumber].tenChosen.append(x)
                        self.projects[projectNumber].otherChosens.append([x,index])
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Projects")
        allProjects = cur.fetchall()
        cur.execute("SELECT * FROM Professors")
        allProfs = cur.fetchall()
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]
            if(len(project.firstChosen)==1):
                project.taken=True
                project.chosen = project.firstChosen[0]
                project.firstChosen[0].takenProject = project
            elif(len(project.firstChosen)>1):
                project.firstChosen.sort(key=lambda a:returnGrade(a,sortKey))
                project.taken=True
                project.chosen = project.firstChosen[0]
                project.firstChosen[0].takenProject = project

        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]        
            if(len(project.secondChosen)==1):
                project.taken=True
                if(project.secondChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.secondChosen[0]
                    project.secondChosen[0].takenProject = project
            elif(len(project.secondChosen)>1):
                project.secondChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.secondChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break

        
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]

            if(len(project.thirdChosen)==1):
                
                if(project.thirdChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.thirdChosen[0]
                    project.thirdChosen[0].takenProject = project
            elif(len(project.thirdChosen)>1):
                project.thirdChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.thirdChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
            
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.fourChosen)==1):
          
                if(project.fourChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.fourChosen[0]
                    project.fourChosen[0].takenProject = project
            elif(len(project.fourChosen)>1):
                project.fourChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.fourChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
            
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.fiveChosen)==1):
                project.taken=True
                if(project.fiveChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.fiveChosen[0]
                    project.fiveChosen[0].takenProject = project
            elif(len(project.fiveChosen)>1):
                project.fiveChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.fiveChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
            
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.sixChosen)==1):

                if(project.sixChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.sixChosen[0]
                    project.sixChosen[0].takenProject = project
            elif(len(project.sixChosen)>1):
                project.sixChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.sixChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
        
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.sevenChosen)==1):
                project.taken=True
                if(project.sevenChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.sevenChosen[0]
                    project.sevenChosen[0].takenProject = project
            elif(len(project.sevenChosen)>1):
                project.sevenChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.sevenChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
        
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.eightChosen)==1):

                if(project.eightChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.eightChosen[0]
                    project.eightChosen[0].takenProject = project
            elif(len(project.eightChosen)>1):
                project.eightChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.eightChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
            
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.nineChosen)==1):
                if(project.nineChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.nineChosen[0]
                    project.nineChosen[0].takenProject = project
            elif(len(project.nineChosen)>1):
                project.nineChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.nineChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
        
        for x in self.projects:
            project = self.projects[x]
            sortKey="1"
            for prof in allProfs:
                if(allProjects[int(x)][1]==prof[1]):
                    if(prof[4]!="1"):
                        sortKey = prof[4]    
            if(len(project.tenChosen)==1):
                if(project.tenChosen[0].takenProject == "none"):
                    project.taken=True
                    project.chosen = project.tenChosen[0]
                    project.tenChosen[0].takenProject = project
            elif(len(project.tenChosen)>1):
                project.tenChosen.sort(key=lambda a:returnGrade(a,sortKey))
                for student in project.tenChosen:
                    if(student.takenProject == "none"):
                        project.taken=True
                        project.chosen = student
                        student.takenProject = project
                        break
                
            for x in self.students:
                if(x.takenProject == "none"):
                    x.takenProject = "----"
        
                    con.commit()
        con.close()        


        


    def report(self):
        studentsProjects  = []
        random.shuffle(self.students)
        for x in self.students:
            if(x.takenProject != "----"):
                studentsProjects.append([x.name +" "+x.surname+ "-" +x.number,x.takenProject.name])
            else:
                studentsProjects.append([x.name +" "+x.surname+ "-" +x.number," PLEASE CONTACT COURSE ASISTANT."])
               

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(fname='uploadProjects/DejaVuSans.ttf')
        pdf.set_font("DejaVuSans", size=7)
        line_height = pdf.font_size * 2.5
        col_width = pdf.epw / 2  # distribute content evenly
        for row in studentsProjects:
            for datum in row:
                pdf.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
            pdf.ln(line_height)
        pdf.output('listOfMatches.pdf')

    def printStudents(self):
        for x in self.students:
            x.printStudentInfos()

def returnGrade(student,key):
        newKey = key.replace("CSE","BİL")
        if(key!="1"):
            if(key in student.courses):
                if((student.courses[key]) in noteDict):
                    point = noteDict[student.courses[key]]
                    point = 4*point
                    return -1*(point+float(student.avgGrade))
            elif(newKey in student.courses):
                if((student.courses[newKey]) in noteDict):
                    point = noteDict[student.courses[newKey]]
                    return -1*(point+float(student.avgGrade))
            
        return -1*float(student.avgGrade)


courseExt = ["BIL","BİL","CSE","MAT","ENG","FİZ","PHY"]
class Student(models.Model):
    def __init__(self,infos,dumbStudent):
        self.dumbStudent = dumbStudent
        self.name = "none"
        self.surname = "none"
        self.avgGrade = "none"
        self.identityNumber = "none"
        self.number = "none"
        self.bornDate = "none"
        self.courses = {}
        if(dumbStudent):
            self.createDumbStudent(infos)
        else:
            self.createTests(infos)
        self.choiceList = []
        self.takenProject = "none"

    def createDumbStudent(self,infos):
        self.name = "Student" + infos
        self.surname = "WillGraduate" + infos
        self.avgGrade = str(round(random.uniform(1.7, 3.1),2))
        self.identityNumber = infos + "1234567"
        self.number = infos
        self.bornDate = "notRealPerson"

    def createTests(self,infos):

        for x in range(infos.numPages):
            pageObj = infos.getPage(x)
            text = pageObj.extractText().splitlines()
            
            for index,y in enumerate(text):
                if(":Genel Not Ortalaması" in y and "GNO" not in y):
                    self.avgGrade = y.split(":")[0]
                elif any(y.startswith(ext) for ext in courseExt):
                    self.courses[(y.split(" "))[0]] = (text[index+1].split(" "))[-3]
                elif (y.startswith("Doğum Tarihi")):
                    self.number = y[12:]
                    self.identityNumber = text[index+1]
                    self.name = text[index+2]
                    self.bornDate = text[index+3][:-1]
                elif ("Soyadı" in y):
                    self.surname = y.split(" ")[-1]



    def printStudentInfos(self):
        print("Öğrencinin adı soyadı" + self.name + " " + self.surname)
        print("Öğrencinin numarası " + self.number)
        print("Öğrencinin doğum tarihi " + self.bornDate)
        print("Öğrencinin kimlik numarası " + self.identityNumber)
        print("Öğrencinin not ortalaması " + self.avgGrade)
        for x in self.courses:
            print(x + " - " + self.courses[x] )


projectStarts = ["1","2","3","4","5","6","7","8","9","•"]



class Teacher(models.Model):
    def __init__(self,infos,filename):
        self.projects = []
        self.createTests(infos,filename)
        
        
    def createTests(self,infos,filename):

        flag = True
        seperator = "."
        for x in range(infos.numPages):
            pageObj = infos.getPage(x)
            text = pageObj.extractText().splitlines()
            
            for index,y in enumerate(text):
                if any(y.startswith(ext) for ext in projectStarts):
                    if(flag):
                        seperator = y[1:2]
                        flag=False
                    if(self.checkIfItsProject(y.split(seperator)[0]) and len(y)>5):
                        tempProject = Project(y[y.index(seperator)+1:],filename)
                        self.projects.append(tempProject)
    
    def checkIfItsProject(self,string):
        if(string.isnumeric() or string in projectStarts):
            return True
        return False

class Project(models.Model):
    def __init__(self,name,teacherName):
        self.teacherName = teacherName
        self.name = name
        self.taken = False
        self.firstChosen = []
        self.secondChosen = []
        self.thirdChosen = []
        self.fourChosen = []
        self.fiveChosen = []
        self.sixChosen = []
        self.sevenChosen = []
        self.eightChosen = []
        self.nineChosen = []
        self.tenChosen = []
        self.otherChosens = []
        self.chosen = "none"