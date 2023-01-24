from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
import os
import sqlite3

def funct():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Courses")
    rows = cur.fetchall()
    returnList = ()
    con.commit()
    con.close()
    return tuple(rows)

def projectfunct():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Projects")
    rows = cur.fetchall()
    con.commit()
    con.close()
    newList=[]
    y=1
    newList.append((0,"Bir Proje Seçiniz"))
    for x in rows:
        newList.append((y,x[1]+"-"+x[0]))
        y=y+1
    #print(tuple(rows))
    return tuple(newList)

CHOICES =(
    ("1", "Genel Ortalama"),
    ('Dersten Alınan Not', funct()
    )
)
UPLOADCHOICES =(
    ("1", "Genel Ortalama"),
    ('Dersten Alınan Not', funct()
    )
)

BooleanChoices = (
    (None, "Sonra değerlendireceğim"),
    (True, "Geçerli"),
    (False, "Geçersiz")
) 

class StudentForm(forms.Form):  
    key       = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}),label= "Şifre", max_length=50)  
    file      = forms.FileField(label= "Proje listesi") # for creating file input  
    rapor     = forms.BooleanField(label="Rapor gerekli mi?",required=False)
    dagitmaSekli = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="Neye göre dağıltsın?",choices=CHOICES)

class InstructorForm(forms.Form):  
    key       = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__group'}),label= "Şifre", max_length=50,)  

class ReportForm(forms.Form):
    def __init__(self, key = None, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        if(key):
            for x in self.fields:
                print(x)
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM Projects")
            projects = cur.fetchall()
            cur.execute("SELECT Name FROM Professors WHERE Key is '" + key + "';")
            name = cur.fetchone()[0]
            print(name)
            path = './uploadProjects/raporlar'
            ourList = []
            for x in os.listdir(path):
                no = int(x.split('_')[0])
                if(projects[no-1][1]==name):
                    number = x.split('_')[-1][:-4]
                    ourList.append((x,(number+"-"+projects[no-1][0])))
            self.fields["reportCheck"]= forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="Bakmak istediğiniz raporu seçin",choices=tuple(ourList))
            for x in os.listdir(path):
                no = int(x.split('_')[0])
                if(projects[no-1][1]==name):
                    self.fields[x]=forms.ChoiceField(label="Rapor geçerli mi? " + number+"-"+projects[no-1][0],widget=forms.RadioSelect(),choices = BooleanChoices)


            con.commit()
            con.close()

        


class ChooseForm(forms.Form):
    Tercih1 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="1.Tercih",choices=projectfunct())
    file1 = forms.FileField(label= "1.Rapor",required=False)
    Tercih2 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="2.Tercih",choices=projectfunct())
    file2 = forms.FileField(label= "2.Rapor",required=False)
    Tercih3 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="3.Tercih",choices=projectfunct())
    file3 = forms.FileField(label= "3.Rapor",required=False)
    Tercih4 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="4.Tercih",choices=projectfunct())
    file4 = forms.FileField(label= "4.Rapor",required=False)
    Tercih5 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="5.Tercih",choices=projectfunct())
    file5 = forms.FileField(label= "5.Rapor",required=False)
    Tercih6 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="6.Tercih",choices=projectfunct())
    file6 = forms.FileField(label= "6.Rapor",required=False)  
    Tercih7 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="7.Tercih",choices=projectfunct())
    file7 = forms.FileField(label= "7.Rapor",required=False) 
    Tercih8 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="8.Tercih",choices=projectfunct())
    file8 = forms.FileField(label= "8.Rapor",required=False)  
    Tercih9 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="9.Tercih",choices=projectfunct())
    file9 = forms.FileField(label= "9.Rapor",required=False)  
    Tercih10 = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}),label="10.Tercih",choices=projectfunct())
    file10 = forms.FileField(label= "10.Rapor",required=False)  
 
    transkript = forms.FileField(label= "Transkript") # for creating file input  
    