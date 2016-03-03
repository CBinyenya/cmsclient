import datetime
from docx import *
self_today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
today = datetime.date.today()
date = today.strftime("%d, %b %Y")
relationships = relationshiplist()
contenttypes = contenttypes()
websettings = websettings()
wordrelationships = wordrelationships(relationships)
def creator(letter_type,addr,other=[]):            
    docname = "sample/"+letter_type
    document = opendocx(docname)
    body = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
    ldate = date
    lname = addr[0]
    laddress= addr[1]
    ltown = addr[2]
    body = replace(body,'date',ldate)    
    body = replace(body,'name',lname)
    body = replace(body,'address',laddress)    
    body = replace(body,'town',ltown)
    body = replace(body,'country',"KENYA")
    if letter_type == "balance_let.docx":
        body = replace(body,'CANTIDAD',str(addr[3]))
    elif letter_type == "renewal_let.docx":
        print "replacing renewals",addr[3],addr[4]
        body = replace(body,'POLITICA',addr[3])        
        body = replace(body,'FECHA',addr[4].strftime("%d %b,%Y"))
    elif letter_type == "newinvoice_let.docx":
        print "replacing invoices",addr[3],addr[4]
        body = replace(body,'POLITICA',addr[3])
        body = replace(body,'CANTIDAD',str(addr[4]))
    try:
        body = replace(body,'Company',other[0])
        body = replace(body,'backto',other[1])
    except:
        pass
    title    = 'Envelopes'
    subject  = 'Create envelopes/letters'
    creator  = 'Caleb Binyenya'
    keywords = ['python', 'Office Open XML', 'Word']    
    coreprops = coreproperties(title=title, subject=subject, creator=creator,
                               keywords=keywords)
    appprops = appproperties()
    if len(other) == 0:
        file_name = laddress+" %s"%str(time.time())        
        filename = 'letters/'+file_name+".docx"       
    elif len(other) > 0:
        file_name = laddress+" %s"%str(time.time())        
        filename = 'envelopes/'+file_name+".docx"        
    savedocx(document, coreprops, appprops, contenttypes, websettings,
             wordrelationships, filename)

    


    return True 

        




