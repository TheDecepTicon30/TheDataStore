from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import datetime
from flask import Flask, jsonify, request
from dateutil.relativedelta import *
import pandas as pd
import logging
from flask_pymongo import PyMongo
import pymongo
import secrets
import csv
import jwt
import calendar
from cryptography.fernet import Fernet

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.config['MONGO_DBNAME'] = 'Saber'
global uri
uri = "mongodb://24f9cd34-0ee0-4-231-b9ee:avd9uFDe9Vjcud890ovWifW9zVcv9D60P142TJvC1Ba8pc0qM1dPkt80MotOWdI5BNyfvnp5lSlHxzoGijKWyw==@24f9cd34-0ee0-4-231-b9ee.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
app.config['MONGO_URI'] = uri
mongo = PyMongo(app)
client = pymongo.MongoClient(uri)
db = client['Saber']
user = db['UserInfo']


def Get_val(request):
    username = request.user.username
    myquery = { "user_id":username }
    global credits
    for i in user.find(myquery):
        credits = i["Total_Credits"]


def home(request):
    Get_val(request)
    return render(request, 'home.html',{"Credits":credits})

def openDashboard(request):
    username = request.user.username
    usrinf,plantype,crdtconsumed,tspend,crdtrmn,searchinfo,searchvalues = '','','','','','',[]
    for q in user.find({"user_id":username}):
            usrinf = (q['Free_Plan'])
            plantype = (q['current_plan'])
            crdtconsumed = (q['RowsConsumed'])//10
            crdtrmn = (q['Total_Credits'])
            tspend = (q['TotalSpend'])
            searchinfo = (q['searchinfo'])
    crdtrmnprcnt = (int(crdtrmn)/500)*100
    i = searchinfo   
    for ca,ke,se,da,ta,so,to in zip(i['category'],i['keyword'],i['searchdate'],i['daterange'],i['tags'],i['source'],i['totalentries']):
        searchvalues.append({'category':ca,'keyword':ke,'searchdate':se,'daterange':da,'tags':ta,'source':so,'totalentries':to}) 
    searchvalues = searchvalues[:15]
    searchvalues.reverse()
    return render(request, 'dashboard.html',{"Credits":credits,"username":username,"plantype":plantype,"RowsConsumed":crdtconsumed,                     'total_credits':crdtrmn,'total_spend':tspend,'search_info':searchvalues,"crdtrmnprcnt":crdtrmnprcnt})

def openPaymentPage(request):
    return render(request, 'pay.html',{"Credits":credits})

def rough(request):
    return render(request, 'rough.html')

def invoice(request):
    return render(request, 'printInvoice.html',{'txnid':txnid, 'username':username, 'status':status, 'firstname':firstname, 'amount':amount
            , 'posted_hash':posted_hash, 'productinfo':productinfo, 'email':email, 'phone':phone})

def openHomePage(request):
    return render(request, 'home.html',{"Credits":credits})

def performPayment(request):
    return render(request, 'payment.html',{"Credits":credits})

def free_pln(request):
    if request.method == 'POST':
        username = request.user.username
        usrinf = ''
        credit_get = ''
        for q in user.find({"user_id":username}):
            usrinf = (q['Free_Plan'])
        if usrinf == "Not Activated":
            credit_get = "500 Credits has been added"
            user.update_one({"user_id":username},{ "$set":{"Free_Plan":"Activated","Total_Credits":"500","current_plan":"Free Plan"}})
        elif usrinf == "Activated":
            credit_get = "Free Plan has been used already"
        messages.info(request,credit_get)
        Get_val(request)
        global credits
        myquery = { "user_id":username }
        for i in user.find(myquery):
            credits = i["Total_Credits"]
        return render(request, 'pay.html', {'Credits_Get': credit_get,"Credits":credits})
        
def OpenApiPage(request):
        username = None
        username = request.user.username
        usrinf = []
        for q in user.find({"$and": [{"user_id" : {"$regex" : username,"$options":"i"}}]}):
            usrinf.append({'Date':q['gendate'],'ApiKey':q['api_key'],'expiryDate':q['expiryDate']})
        return render(request,'apikey.html',{'usr_inf':usrinf,"Credits":credits})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Your Account has been activated.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            client = pymongo.MongoClient(uri)
            db = client["Saber"]
            col = db["UserInfo"]
            usrname = str(user)
            col.insert_one({"user_id":usrname,"api_key":"","access_token":"","RowsConsumed":0,"TotalSpend":0,"gendate":"","Total_Credits":0,"Free_Plan":"Not Activated","current_plan":"","expiryDate":"","searchinfo":{'source':[],'daterange':[],'searhinfo':[],'category':[],'keyword':[],'tags':[],'searchdate':[],'totalentries':[]}})
            return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_active_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def generate_api(anything):
    key = (secrets.token_hex(16))

def add_one_month(orig_date):
    new_year = orig_date.year
    new_month = orig_date.month + 1
    if new_month > 12:
        new_year += 1
        new_month -= 12
    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)
    return orig_date.replace(year=new_year, month=new_month, day=new_day)

def ApiKeyGenerator(request):
    if request.method == 'POST':
        username = request.user.username
        for q in user.find({"user_id":username}):
            usrinf = (q['Free_Plan'])
        if usrinf == "Not Activated":
            credit_get = "Please,first select the Plan"
            messages.info(request,credit_get)
            return render(request, 'apikey.html')
        elif usrinf == "Activated":
        
            usrname = request.POST['usrname']
            ApiKey = secrets.token_urlsafe(16)
            date = datetime.now()
            expiryDate = add_one_month(date)
            date = date.strftime("%a, %d %B %Y %H:%M:%S")
            expiryDate = expiryDate.strftime("%a, %d %B %Y %H:%M:%S")
            user.update_one({"user_id":usrname},{"$set": {"api_key":ApiKey, "gendate":date, "expiryDate":expiryDate}}) 
            #return HttpResponse(ApiKey, content_type='text/plain')
            username = request.user.username
            usrinf = []
            for q in user.find({"$and": [{"user_id" : {"$regex" : username,"$options":"i"}}]}):
                usrinf.append({'Date':q['gendate'],'ApiKey':q['api_key'],'expiryDate':q['expiryDate']})
            return render(request, 'apikey.html', {'api_k':ApiKey,'usr_inf':usrinf,"Credits":credits})
    
    
def getSuccessfulTransactionData(request):
    global username, status, firstname, amount, txnid, posted_hash, productinfo, email, phone, myquery
    if request.method == 'POST':
        username = request.user.username
        status = request.POST["status"];
        firstname = request.POST["firstname"];
        amount = request.POST["amount"];
        txnid = request.POST["txnid"];
        posted_hash = request.POST["hash"];
        productinfo = request.POST["productinfo"];
        email = request.POST["email"];
        phone = request.POST["phone"];
        myquery = { "user_id":username }    
        for i in user.find(myquery): 
            credits3 = int(i["Total_Credits"])
        if amount == "1.00":
            credits3 = credits3 + 500
            user.update_one({"user_id":username},{"$set":{"Total_Credits":credits3, "current_plan":"Business"}})
        elif amount == "2.00":
            credits3 = credits3 + 1000
            user.update_one({"user_id":username},{"$set":{"Total_Credits":credits3, "current_plan":"Premium"}})
        credits = credits3
        return render(request, 'success.html', {'txnid':txnid, 'username':username, 'status':status, 'firstname':firstname, 'amount':amount
            , 'posted_hash':posted_hash, 'productinfo':productinfo, 'email':email, 'phone':phone})

def AccessTokenGenerator(request):
    username = request.user.username
    myquery = {"user_id" : username}
    global expiryDate
    username = request.user.username
    for i in user.find(myquery):
        expiryDate = i["expiryDate"]
    date = datetime.now()
    datestr = date.strftime('%a, %d %B %Y %H:%M:%S')
    date1 = datetime.strptime(datestr, "%a, %d %B %Y %H:%M:%S")


    expiryDate = datetime.strptime(expiryDate, '%a, %d %B %Y %H:%M:%S')

    if date1 >= expiryDate:
        messages.info(request, 'API Key Expired! Please generate another API Key to continue accessing our data!')
        return render(request, 'home.html')
    else:
        client = pymongo.MongoClient(uri)
       
        
        if request.method == 'POST':
            key = datetime.strftime(datetime.today() , '%d/%m/%Y')
            access_token = jwt.encode({'some':'payload'}, key, algorithm = 'HS256')
            import subprocess
            global gapikey, keyword, incat, intag, insrce, sdate, edate
            date = datetime.now().strftime("%a, %d %B %Y %H:%M:%S")
            gapikey = request.POST['ApiKey']
            keyword = request.POST['word']
            incat = request.POST['incat']
            intag = request.POST['intag']
            insrce = request.POST['insrce']
            sdate = request.POST['startdate']
            edate = request.POST['enddate']
            db = client["Saber"]
            col = db["UserInfo"]
            app.config['MONGO_DBNAME'] = 'Saber'
            app.config['MONGO_URI'] = uri
            
            mongo = PyMongo(app)
            
            global rfinds
            rfinds = []
            news = db["News"]
            
            if insrce == 'All Sources':
                insrce = ''
            elif insrce == 'Hindustan Times':
                insrce = 'HindustanTimes'
            elif insrce == 'India Today':
                insrce = 'IndiaToday'
            elif insrce == 'Economic Times':
                insrce = 'econominc-times'
            elif insrce == 'Livemint':
                insrce = 'livemint'
            elif insrce == 'Business Standard':
                insrce = 'businessStandard'
            elif insrce == 'Times of India':
                insrce = 'TimesofIndia'
            elif insrce == 'Bloomberg Quint':
                insrce = 'bloombergquint'
            elif insrce == 'Money Control':
                insrce = 'money-control'
                    
            if len(insrce) == 0 and len(incat) != 0 and len(intag) != 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newskct/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(intag) + "/" + str(incat) + "/" + str(gapikey))
            #tag ,cat,Source and keyword is missing
            elif len(insrce) == 0 and len(incat) == 0 and len(intag) == 0 and len(keyword) == 0:
                output = ("127.0.0.1:5000/News/" + str(sdate) + "/" + str(edate) + "/" + str(gapikey))
            #tag ,Source and keyword is missing
            elif len(insrce) == 0 and len(incat) != 0 and len(intag) == 0 and len(keyword) == 0:
                output = ("127.0.0.1:5000/Newsc/" + str(sdate) + "/" + str(edate) + "/" + str(incat) + "/" + str(gapikey))
            #tag ,cat and keyword is missing
            elif len(incat) == 0 and len(insrce) != 0 and len(intag) == 0 and len(keyword) == 0:
                output = ("127.0.0.1:5000/Newss/" + str(sdate) + "/" + str(edate) + "/" + str(insrce) + "/" + str(gapikey))
            #Source ,cat and keyword is missing
            elif len(incat) == 0 and len(insrce) == 0 and len(intag) != 0 and len(keyword) == 0:
                output = ("127.0.0.1:5000/Newst/" + str(sdate) + "/" + str(edate) + "/" + str(intag) + "/" + str(gapikey))
            #Source ,cat and tag is missing
            elif len(incat) == 0 and len(insrce) == 0 and len(intag) == 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newsk/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(gapikey))
            #Source and cat is missing
            elif len(incat) == 0 and len(insrce) == 0 and len(intag) != 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newskt/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(intag) + "/" + str(gapikey))
            #Source and tag is missing
            elif len(insrce) == 0 and len(intag) == 0 and len(incat) != 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newskc/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(incat) + "/" + str(gapikey))    
            #cat and tag is missing
            elif len(incat) == 0 and len(intag) == 0 and len(insrce) != 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newsks/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(insrce) + "/" + str(gapikey))
            #keyword and cat is missing
            elif len(keyword) == 0 and len(incat) == 0 and len(insrce) != 0 and len(intag) != 0:
                output = ("127.0.0.1:5000/Newsts/" + str(sdate) + "/" + str(edate) + "/" + str(intag) + "/" + str(insrce) + "/" + str(gapikey))
            #keyword and tag is missing
            elif len(keyword) == 0 and len(intag) == 0 and len(insrce) != 0 and len(incat) != 0:
                output = ("127.0.0.1:5000/Newscs/" + str(sdate) + "/" + str(edate) + "/" + str(incat) + "/" + str(insrce) + "/" + str(gapikey))
            #keyword and source is missing
            elif len(keyword) == 0 and len(insrce) == 0 and len(intag) != 0 and len(incat) != 0:
                output = ("127.0.0.1:5000/Newsct/" + str(sdate) + "/" + str(edate) + "/" + str(intag) + "/" + str(incat) + "/" + str(gapikey))
            #keyword is missing
            elif len(keyword) == 0 and len(intag) != 0 and len(insrce) != 0 and len(incat) != 0:
                output = ("127.0.0.1:5000/Newscts/" + str(sdate) + "/" + str(edate) + "/" + str(intag) + "/" + str(incat) + "/" + insrce + "/" + str(gapikey))    
            #cat is missing
            elif len(incat) == 0 and len(intag) != 0 and len(insrce) != 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newskcs/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(incat) + "/" + insrce + "/" + str(gapikey))
            # tag is missing
            elif len(intag) != 0 and len(incat) == 0 and len(insrce) != 0 and len(keyword) != 0:
                output = ("127.0.0.1:5000/Newskts/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/"  + insrce + "/" + str(gapikey))
            else:
                output = ("127.0.0.1:5000/NewsData/" + str(keyword) + "/" + str(sdate) + "/" + str(edate) + "/" + str(incat) + "/" + str(intag) + "/" + insrce + "/" + str(gapikey))
            col.update_one({"api_key":str(gapikey)},{"$set":{"access_token":str(access_token)}})
            #return HttpResponse(output, content_type='text/plain')
            
            for q in news.find({"$and": [{"Title" : {"$regex" : keyword,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{"Tags" : {"$regex" : intag,"$options":"i"}},{"Source" : {"$regex" : insrce,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
                rfinds.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
                
            username = request.user.username
            myquery = { "user_id":username }    
            global credits1, totalval
            for i in user.find(myquery): 
                credits1 = int(i["Total_Credits"])    
                
            rfindsc = 0
            if credits1 <= 500:
                rfindsc = rfinds[:1000] 
            totalval = len(rfindsc)
            tableval = rfinds[:40]
            
            user.update_one({"user_id":username},{"$push" : {"searchinfo.keyword":keyword,"searchinfo.category":incat,"searchinfo.tags":intag,
  "searchinfo.daterange":[sdate,edate],"searchinfo.source":insrce,"searchinfo.searchdate":date,"searchinfo.totalentries":totalval}})
            
            credits1 = credits1 - totalval//10
            if credits1 < 0:
                messages.info(request, "Doesn't have enough credits to consume this API!")  

            # Example API Link = 127.0.0.1:5000/Newss/2018-02-05/2018-02-09/Rueters/PrTnXu1mO8el8C7dCrtx8g
            # Example Encrypted Text = 127.0.0.1:5000/gAAAAABcQvB4Z1HUCVuenTlZ1Ex0eCLtnMPCKQwkaWjyydA5vIngu-ekK6E7iGpdjazoMogs27toCZfdRUp7DubBcrFppcfqS6gpuzpPvXLf_vRmbY2dXD2ZnUhVzfAx85htyvdBHtvbuIRqbrhcr8JkPKjj-7ebvg==/-kM9vNBuFurPhh06JATNezq-pWYL02TSkPsTegVBbUI=
            key = Fernet.generate_key() # Key
            output1 = output.split('/')
            encr = output1[1]
            for i in range(2, len(output1)):
                encr = encr + '/' + output1[i]

            cipher_suite = Fernet(key)
            encoded_text = cipher_suite.encrypt(encr.encode())
            output = output1[0] + '/' + encoded_text.decode('utf-8') + '/' + key.decode('utf-8')
            
            alert = '' 

            return render(request, 'home.html', {'r_finds':tableval,'acs_k':output,'totalval':totalval,'Credits':credits})
        

        
def File_Download(request):
    if request.method == 'POST':
        if credits1 < 0:
            messages.info(request, "Doesn't have enough credits to download csv!")
            return render(request, 'home.html',{'Credits':credits})
        else:
            username = request.user.username
            rowsconsumed = 0
            trowsconsumed = 0
            for q in user.find({"user_id":username}):
                rowsconsumed = (q['RowsConsumed'])
            trowsconsumed +=  rowsconsumed + totalval
            df = pd.DataFrame(rfinds)
            row = df.to_csv()
            username = request.user.username
            user.update_one({"user_id":username},{"$set":{"Total_Credits":credits1,"RowsConsumed":trowsconsumed}})
            response = HttpResponse(row,content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="NewsData.csv"'
            reload_page(request)
            return response
def reload_page(request):
        return render(request, 'home.html')
            