# coding: utf8
# prova qualcosa come
import json
import os,sys

pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
sysfolder=pathname.split('web2py')[0]
workFolder=sysfolder+"PyApp/makEasy/Works/"
sys.path.append(sysfolder+"PyApp/makEasy")
import makEasy


def nesting():
    form=SCRIPT('var PRJdata={};')
    return locals()


def new():
    workName=''

    if request.vars.newWork:

        workName=request.vars.newWork
        meWork=makEasy.WORKSET[workName]
        path=meWork.Path

        #load form structure
        f = open(workFolder+path+'/form.json', 'r')
        data=json.load(f)
        f.close()
        form=json.dumps(data["form_data"])

        # load js functions
        f = open(workFolder+path+'/work.js', 'r')
        javascriptfunctions=f.read()
        f.close()
        scripts=SCRIPT(javascriptfunctions, _id='workScript')
    else:
        form=str([])
        scripts=SCRIPT('',_id='workScript')

    print 'start work '+workName
    a={'name':workName,'form':form,'scripts':str(scripts)}
    return json.dumps(a)
