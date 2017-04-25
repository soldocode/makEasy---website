#!/usr/bin/env python
# coding: utf8
from gluon import *

def editNumber(label,fvalue,fname,fsize,**options):
    row_widget=TR(TH(label,_colspan="2",_id=fname),
                  TD(INPUT( _id=fname,
                            _name=fname,
                            _class='number value',
                            _type='number',
                            _value=fvalue,
                            _style='width:'+str(fsize)+'%',
                            **options)),
                  _id=fname)
    return row_widget



def writeEuro(label,fvalue,fname,fsize,fclass,**options):
    row_widget=TR(TH(label,_colspan="2", _id=fname),
                  TD(H4( fieldformat.euro(fvalue),
                         _id=fname,
                         _class='double '+fclass,
                         _type='text',
                         _value=fvalue,
                         _style='width:'+str(fsize)+'%; text-align:right;',
                         **options)))
    return row_widget



def editEuro(label,fvalue,fname,fsize,fclass,**options):
    if fvalue!=None:
        fvalue=str(fvalue)
        fvalue=fvalue.replace('.',',')
        split_field=fvalue.split(',')
        if int(split_field[1])==0: fvalue=split_field[0]+',00'
    row_widget=TR(TH(label,_colspan="2"),
                  TD(INPUT( _id=fname,
                            _name=fname,
                            _class='double value '+fclass,
                            _type='text',
                            _value=fvalue,
                            _style='width:'+str(fsize)+'%',
                            **options)))
    return row_widget



def editData(label,fvalue,fname,fsize):
    if fvalue is None: fvalue=datetime.datetime.now()
    fvalue=fvalue.strftime('%Y-%m-%d')
    row_widget=TR(TH(label,_colspan="2"),
                  TD(INPUT( _id=fname,
                             _name=fname,
                             _class='date value',
                             _type='date',
                             _value=fvalue,
                             _style='width:'+str(fsize)+'%')))
    return row_widget



def editDatetime(label,fvalue,fname,fsize):
    if fvalue is None: fvalue=datetime.datetime.now()
    fvalue=fvalue.strftime('%Y-%m-%dT%H:%M')
    row_widget=TR(TH(label,_colspan="2"),
                  TD(INPUT( _id=fname,
                             _name=fname,
                             _class='datetime value',
                             _type='datetime-local',
                             _value=fvalue,
                             _style='width:'+str(fsize)+'%')))
    return row_widget


def editString (label,fvalue,fname,fsize):
    row_widget=TR(TH(label,_colspan="2"),
                  TD(INPUT( _id=fname,
                             _name=fname,
                             _class='text value',
                             _type='text',
                             _value=fvalue,
                             _style='width:'+str(fsize)+'%')))
    return row_widget


def editList(label,fvalue,fname,foptions,fsize,**options):
    field_options=[]
    for opt in foptions: field_options.append(OPTION(opt['text'],_value=opt['value']))
    row_widget=TR(TH(label,_colspan="2"),
                  TD(SELECT(field_options,
                            value=fvalue,
                            width='inherit',
                            _name=fname,**options)))

    return row_widget


def editDBlist(label,fvalue,fname,list_rows,fformat):
    options=[dict(value=None,text='')]
    field_options=[]
    for lrow in list_rows:
        if type(fformat) is FunctionType: toption=fformat(lrow)
        else:                             toption=fformat % lrow
        field_options.append(OPTION(toption,_value=lrow['id']))
    row_widget=TR(TH(label,_colspan="2"),
                  TD(SELECT(field_options,
                            value=fvalue,
                            width='inherit',
                            _name=fname)))

    return row_widget
