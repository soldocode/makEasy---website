# coding: utf8

import json
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import sys, os
import jsonpickle
import g2
import requests

pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
sysfolder=pathname.split('web2py')[0]
prjfolder=sysfolder+"PyApp/makEasy/Projects/"
meFolder=sysfolder+"PyApp/makEasy/"
sys.path.append(meFolder)
import makEasy


def create():
    if request.vars.newproject:
        projectName=request.vars.newproject
        meprj=makEasy.projectLibrary[projectName]
        path_prj=meprj.Path

        # load form structure
        f = open(prjfolder+path_prj+'/form.json', 'r')
        PRJdata=json.load(f)
        f.close()
        form=SCRIPT('var PRJdata='+json.dumps(PRJdata))


        # load js functions
        f = open(prjfolder+path_prj+'/project.js', 'r')
        javascriptfunctions=f.read()
        f.close()
        scripts=SCRIPT(javascriptfunctions, _id='prjScript')

        # load project default data
        f = open(prjfolder+path_prj+'/data.json', 'r')
        pData=f.read()
        f.close()
        prj_data=json.dumps(pData)

    else:
        form=SCRIPT('var PRJdata={};')
        scripts=SCRIPT('')
        prj_data={}

    return dict(form=form,scripts=scripts,prj_data=prj_data)


def estimate():
    return dict(locals())


def sendOffer():
    # get parameters
    #item=json.loads(request.vars.item)
    prj_name=request.vars.prj_name
    json_prj_data=request.vars.prj_data
    prj_data=json.loads(json_prj_data)
    json_offer=request.vars.offer
    offer=json.loads(json_offer)

    #create items
    item=makEasy.newItemFromProject(prj_name,prj_data)

    #get project data
    prj=makEasy.projectLibrary[prj_name]
    prj_path=prj.Path

    f = open(prjfolder+prj_path+'/form.json', 'r')
    prj_form=json.load(f)
    f.close()

    html=''
    html+="<p>"
    html+="Buongiorno,<br>Vi inviamo offerta per la fornitura di:<br><br>"
    html+="Nr "+str(offer['data_form']['quantity'])+" "
    html+=item.Project.Title
    html+=" in "+item.ClassProperties['Material']
    html+=" sp " + str(item.ClassProperties['Thickness'])+"mm"
    html+=" con le seguenti dimensioni:<br>"
    for field in prj_form['form_data']:
        if 'label' in field:
            html+="> "+field['label']+": "+"<br>"
    #html+=json_prj_data
    #html+=json_offer
    html+="</p>"
    result=requests.post(
        "https://api.mailgun.net/v3/carpenteriasoldini.it/messages",
        auth=("api", "key-88b2ca18a8d06347d6f9fd35b7fe8a07"),
        data={"from": "SOLDINI snc - Offerte <info@carpenteriasoldini.it>",
              "to": "produzione@carpenteriasoldini.it",
              "subject": "Offerta",
              "html": html})

    re="Offerta inviata"
    return json.dumps(dict(msg=result.reason))




def exportDXF():
    dxf_result=''
    if request.vars.name:
        data=json.loads(request.vars.jsonstring)
        item=makEasy.newItemFromProject(request.vars.name,data['data_form'])
        wf=item.WorkFlow
        for ws in wf:
            if ws.Work.Class=='PlasmaCut':
                dxf_result=ws.getDXF()
    return json.dumps([dxf_result])


def new():
    projectName=''
    if request.vars.newproject:
        projectName=request.vars.newproject
        #print projectName
        meprj=makEasy.projectLibrary[projectName]
        path_prj=meprj.Path
        #print path_prj

        # load form structure
        f = open(prjfolder+path_prj+'/form.json', 'r')
        PRJdata=json.load(f)
        f.close()
        form=json.dumps(PRJdata["form_data"])

        # load js functions
        f = open(prjfolder+path_prj+'/project.js', 'r')
        javascriptfunctions=f.read()
        f.close()
        scripts=SCRIPT(javascriptfunctions, _id='prjScript')

        # load project default data
        f = open(prjfolder+path_prj+'/data.json', 'r')
        pData=f.read()
        f.close()
        prj_data=pData
        title=PRJdata["title"]

    else:
        form=[]
        scripts=SCRIPT()
        prj_data={}
        title="seleziona un progetto"

    print ('avviato nuovo progetto '+projectName)
    a={'projectname':projectName,
       'form':form,'scripts':str(scripts),
       'prj_data':prj_data,
       'prj_title':title}
    return json.dumps(a)


def createItem():
    meItem='{}'
    if request.vars.name:
        prj_data=json.loads(request.vars.jsonstring)
        item=makEasy.newItemFromProject(request.vars.name,prj_data)
        meItem=jsonpickle.encode(item)
    return meItem


def saveItem():
    meItem='{}'
    if request.vars.name:
        prj_data=json.loads(request.vars.jsonstring)
        print prj_data
        item=makEasy.newItemFromProject(request.vars.name,prj_data)
        meItem=jsonpickle.encode(item)
    return meItem


def getJson():
    path=meFolder+request.vars.jsonPath
    source={}
    #load json structure
    f = open(path, 'r')
    source=f.read()
    f.close()
    return  json.dumps(dict(source=source,path=path))


def view():
    return locals()
