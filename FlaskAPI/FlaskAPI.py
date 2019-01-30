from flask import Flask, jsonify, request
from datetime import datetime
from flask_pymongo import PyMongo
import pymongo
import jwt
app = Flask(__name__)



app.config['MONGO_DBNAME'] = 'zash'
app.config['MONGO_URI'] = 'mongodb://adil:warsi3474@ds247191.mlab.com:47191/zash'


mongo = PyMongo(app)

"""@app.route('/framework',methods = ['GET'])
def get_all_framework():
    framework = mongo.db.News
    
    output = []
    
    for q in framework.find():
        output.append({'Title': q['Title'], 'Date': q['Date']})
        
    return jsonify({'result': output})
"""
def mongodbcrdntl():
    global news, keys
    news = mongo.db.News
    keys = mongo.db.UserInfo

def get_key():
    global key, encoded, vkey, pkey
    key = datetime.strftime(datetime.today() , '%d/%m/%Y')
    encoded = jwt.encode({'some':'payload'}, key, algorithm = 'HS256')
    vkey = str(jwt.encode({'some':'payload'}, key, algorithm = 'HS256'))
    pkey = "sabertooth_0007"
    
def authentication(api_key):
    global result
    fkey = 'notfound'
    for j in keys.find({'api_key':api_key}):
        fkey = j['access_token']
        
    if pkey == api_key or vkey == fkey:
        result = output
    else:
        result = 'Authentication failed'


@app.route('/News/<sdate>/<edate>/<api_key>', methods = ['GET'])
def News(sdate,edate,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})
@app.route('/Newss/<sdate>/<edate>/<source>/<api_key>', methods = ['GET'])
def Newss(sdate,edate,source,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Source" : {"$regex" : source,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        
@app.route('/Newsc/<sdate>/<edate>/<incat>/<api_key>', methods = ['GET'])
def Newsc(sdate,edate,incat,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Category" : {"$regex" : incat,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})
@app.route('/Newst/<sdate>/<edate>/<tag>/<api_key>', methods = ['GET'])
def Newst(sdate,edate,tag,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Tags" : {"$regex" : tag,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        

        
@app.route('/Newsk/<keyword>/<sdate>/<edate>/<api_key>', methods = ['GET'])
def Newsk(sdate,edate,keyword,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Title" : {"$regex" : keyword,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        
              
@app.route('/Newskt/<keyword>/<sdate>/<edate>/<intag>/<api_key>', methods = ['GET'])
def Newskt(sdate,edate,keyword,intag,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Tags" : {"$regex" : intag,"$options":"i"}},{"Title" : {"$regex" : keyword,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})
        
@app.route('/Newskc/<keyword>/<sdate>/<edate>/<incat>/<api_key>', methods = ['GET'])
def Newskc(sdate,edate,keyword,incat,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Category" : {"$regex" : incat,"$options":"i"}},{"Title" : {"$regex" : keyword,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})
        
@app.route('/Newsks/<keyword>/<sdate>/<edate>/<insrce>/<api_key>', methods = ['GET'])
def Newsks(sdate,edate,keyword,insrce,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Source" : {"$regex" : insrce,"$options":"i"}},{"Title" : {"$regex" : keyword,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        
        
@app.route('/Newsts/<sdate>/<edate>/<intag>/<insrce>/<api_key>', methods = ['GET'])
def Newsts(sdate,edate,intag,insrce,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Source" : {"$regex" : insrce,"$options":"i"}},{"Tags" : {"$regex" : intag,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        

@app.route('/Newscs/<sdate>/<edate>/<incat>/<insrce>/<api_key>', methods = ['GET'])
def Newscs(sdate,edate,insrce,incat,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Source" : {"$regex" : insrce,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})

@app.route('/Newsct/<sdate>/<edate>/<intag>/<incat>/<api_key>', methods = ['GET'])
def Newsct(sdate,edate,intag,incat,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Tags" : {"$regex" : intag,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})    
    
@app.route('/Newscts/<sdate>/<edate>/<intag>/<incat>/<insrce>/<api_key>', methods = ['GET'])
def Newscts(sdate,edate,intag,incat,insrce,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Tags" : {"$regex" : intag,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{"Source" : {"$regex" : insrce,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result}) 

@app.route('/Newskct/<keyword>/<sdate>/<edate>/<intag>/<incat>/<api_key>', methods = ['GET'])
def Newskct(keyword,sdate,edate,intag,incat,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Title" : {"$regex" : keyword,"$options":"i"}},{"Tags" : {"$regex" : intag,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{"Source" : {"$regex" : insrce,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        
    
    
@app.route('/Newskcs/<keyword>/<sdate>/<edate>/<incat>/<insrce>/<api_key>', methods = ['GET'])
def Newskcs(keyword,sdate,edate,incat,insrce,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Title" : {"$regex" : keyword,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{"Source" : {"$regex" : insrce,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})        
        
@app.route('/Newskts/<keyword>/<sdate>/<edate>/<intag>/<insrce>/<api_key>', methods = ['GET'])
def Newskts(keyword,sdate,edate,intag,insrce,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query 
    for q in news.find({"$and": [{"Title" : {"$regex" : keyword,"$options":"i"}},{"Tags" : {"$regex" : intag,"$options":"i"}},{"Source" : {"$regex" : insrce,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})
    
@app.route('/NewsData/<keyword>/<sdate>/<edate>/<incat>/<intag>/<insrce>/<api_key>', methods = ['GET'])
def NewsData(keyword,sdate,edate,incat,intag,insrce,api_key):
    
    mongodbcrdntl()
    get_key()
    
    global output
    output = []  
    #search query
    for q in news.find({"$and": [{"Title" : {"$regex" : keyword,"$options":"i"}},{"Category" : {"$regex" : incat,"$options":"i"}},{"Tags" : {"$regex" : intag,"$options":"i"}},{"Source" : {"$regex" : insrce,"$options":"i"}},{'Date': {'$gte': sdate, '$lt': edate}}]}).sort('Date',pymongo.ASCENDING):
        output.append({ 'Date':q['Date'],'Title':q['Title'],'Source':q['Source'],'Subtitle':q['Subtitle'],'Category':q['Category'],'Tags':q['Tags'],'Content':q['Content']})
    
    authentication(api_key)
    return jsonify({'result' :result})

    
if __name__ == '__main__':
    app.run()
