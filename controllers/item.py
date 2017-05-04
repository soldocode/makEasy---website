# coding: utf8

import json
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import sys, os
import jsonpickle


pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
sysfolder=pathname.split('web2py')[0]
prjfolder=sysfolder+"PyApp/makEasy/Projects/"
sys.path.append(sysfolder+"PyApp/makEasy/")


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
    else:
        form=SCRIPT('var PRJdata={};')
        scripts=SCRIPT('')

    return locals()


def exportDXF():

    dxf_result=''
    if request.vars.name:
        data=json.loads(request.vars.jsonstring)
        item=makEasy.newItemFromProject(request.vars.name,data['data_form'])
        dxf_result=item.ExportDXF()


    return json.dumps(dxf_result)


def new():
    projectName=''
    if request.vars.newproject:
        projectName=request.vars.newproject
        meprj=makEasy.projectLibrary[projectName]
        path_prj=meprj.Path

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
    else:
        form=[]
        scripts=SCRIPT()

    print 'avviato nuovo progetto '+projectName
    a={'projectname':projectName,'form':str(form),'scripts':str(scripts)}
    return json.dumps(a)

def createItem():
    meItem='{}'
    if request.vars.name:
        data=json.loads(request.vars.jsonstring)
        item=makEasy.newItemFromProject(request.vars.name,data['data_form'])
        meItem=jsonpickle.encode(item)

    return meItem

def saveItem():
    meItem='{}'
    if request.vars.name:
        data=json.loads(request.vars.jsonstring)
        item=makEasy.newItemFromProject(request.vars.name,data['data_form'])
        meItem=jsonpickle.encode(item)

    return meItem


def view():
    return locals()
