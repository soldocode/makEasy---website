# coding: utf8
# prova qualcosa come
import json
import Plasma
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import meForm


def index(): return dict(message="hello from platecut.py")


def taglia():
    print request.vars
    form_data=[]
    for var in request.vars:
        form_data.append(INPUT( _id=var, _name=var,_value=request.vars[var],_type='hidden'))
    shape_data=FORM(form_data, _id='shape_data' )
    sheet_margin_bottom=10
    sheet_margin_left=10
    sheet_width=float(request.vars['misure2:number'])+sheet_margin_left+10
    sheet_height=float(request.vars['misure3:number'])+sheet_margin_bottom+10
    return locals()


def vista():
    #### crea form ####
    formrows=[]
    #### crea tabella campi ###
    formtable=[]
    shape_options=[{'text':'Rettangolare','value':'1'},
              {'text':'Circolare','value':'2'}]
    formtable.append(meForm.editList('sagoma piastra','1','shape:number',shape_options,20,_onchange="view_form()"))
    formtable.append(meForm.editNumber('spessore',10,'misure1:number',30))
    formtable.append(meForm.editNumber('larghezza',500,'misure2:number',40))
    formtable.append(meForm.editNumber('altezza',500,'misure3:number',40))
    formtable.append(TR(TD(A('Aggiungi Foratura',_class="button",_onclick="add_holes()")+
                           INPUT(_name="id_hole",_type="hidden", _value=-1),
                           _style="padding-top:10px" )))

    cwidth=[COL(_width='50%'),
            COL(_width='5%'),
            COL(_width='45%')]

    formrows.append(TABLE(COLGROUP(*cwidth),*formtable,_id='dbmanage',_width='100%'))

    form=FORM(*formrows,
              _id="data_form",
              _action=URL('platecut','taglia'),
              _method='post',
              _enctype="multipart/form-data")

    return locals()


def item():
    ### Parametri ###
    ctitle=[TH('Lavorazione'),TH('Tempo(min)'),TH('Costo Orario')]
    cwidth=[COL(_width='50%'),COL(_width='25%'),COL(_width='25%')]
    rows=[{'include':True,'work':'Taglio Plasma','time':10,'hourly_cost':50},
          {'include':True,'work':'Smerigliatura','time':10,'hourly_cost':30},
          {'include':True,'work':'Foratura','time':5,'hourly_cost':30},
          {'include':True,'work':'Filettatura','time':5,'hourly_cost':30}]
    return locals()


def costi():
    ### Lavorazioni ###
    ctitle=[TH('Lavorazione'),TH('Tempo(min)'),TH('Costo Orario')]
    cwidth=[COL(_width='50%'),COL(_width='25%'),COL(_width='25%')]
    rows=[{'include':True,'work':'Taglio Plasma','time':10,'hourly_cost':50},
          {'include':True,'work':'Smerigliatura','time':10,'hourly_cost':30},
          {'include':True,'work':'Foratura','time':5,'hourly_cost':30},
          {'include':True,'work':'Filettatura','time':5,'hourly_cost':30}]

    #### Griglia Dati ####
    bodyrows=[]
    trclass="sol"
    trcount=0

    for row in rows:
        trcount=trcount+1
        bodycol=[]

        ### Crea campo include ###
        #bodycol.append(TD(INPUT(row['work'],_type="checkbox", _name="include")))

        #### Crea campo link ####
        #viewstack.append(dict(tname='fatture',tid=row['id']))
        bodycol.append(TD(INPUT(_value=row['work'],
                                _type="checkbox",
                                _checked="checked",
                                _name="include", 
                                _style="vertical-align:middle;"),
                          SPAN(' '),
                          A(B(row['work']),
                              _class='link',
                              _href=URL('edit',vars=dict(mode='edit')))))
        #viewstack.pop()

        #### Altri Campi ####
        bodycol.append(TD(row['time']))
        bodycol.append(TD(row['hourly_cost']))


        bodyrows.append(TR(*bodycol,_class=trclass, _id=trcount))
        if trclass=="sol":
            trclass="alt"
        else:
            trclass="sol"

    grid_lavorazioni=TABLE(COLGROUP(*cwidth),
                     THEAD(TR(*ctitle)),
                     TBODY(*bodyrows,_id='bodyview'), 
                     _id="dbmanage",
                     _width="100%")


    ### Materiali ###
    ctitle=[TH('Qualità'),TH('Materiale'),TH('Peso(kg)'),TH('Costo al kg')]
    cwidth=[COL(_width='20%'),COL(_width='40%'),COL(_width='20%'),COL(_width='20%')]
    rows=[{'material':'Lamiera sp.10mm','quality':'S235JR','weight':10,'cost':50}]

    #### Griglia Dati ####
    bodyrows=[]
    trclass="sol"
    trcount=0

    for row in rows:
        trcount=trcount+1
        bodycol=[]

        #### Crea campo link ####
        #viewstack.append(dict(tname='fatture',tid=row['id']))
        bodycol.append(TD(A(B(row['quality']),_class='link',_href=URL('edit',vars=dict(mode='edit')))))
        #viewstack.pop()

        #### Altri Campi ####
        bodycol.append(TD(row['material']))
        bodycol.append(TD(row['weight']))
        bodycol.append(TD(row['cost']))


        bodyrows.append(TR(*bodycol,_class=trclass, _id=trcount))
        if trclass=="sol":
            trclass="alt"
        else:
            trclass="sol"

    grid_materiali=TABLE(COLGROUP(*cwidth),
                     THEAD(TR(*ctitle)),
                     TBODY(*bodyrows,_id='bodyview'), 
                     _id="dbmanage",
                     _width="100%")

    return locals()


def make_pgm():
    strprg={}
    data=json.loads(request.vars.jsonstring)
    print json.dumps(data, sort_keys=True, indent=4)

    print '****** PLASMA CUT *******'
    id_pgm = 1234
    prgr=Plasma.PlasmaCutPlan(id_pgm)

    centerx=float(data['shape_data']['misure2'])/2+float(data['data_form']['sheet_margin_left'])
    centery=float(data['shape_data']['misure3'])/2+float(data['data_form']['sheet_margin_bottom'])
    cutid=1
    # percorso taglio dei fori #
    if 'holes' in data['shape_data'].keys():
        for holes in data['shape_data']['holes']:

            if holes['intfo']<>'':
                modulo=float(holes['intfo'])/2
            else:
                modulo=0
            print 'modulo:',modulo

            if holes['num']<>'':
                numfori=int(holes['num'])
            else:
                numfori=1
            print 'numfori:',numfori

            if holes['par']<>'':
                angpar=int(holes['par'])
            else:
                angpar=0
            print 'angpar:',angpar
            angpasso=360/numfori
            for i in range(0,numfori):
                cutid=cutid+1
                cx=centerx+modulo*math.cos(math.radians(angpar+angpasso*i))
                cy=centery+modulo*math.sin(math.radians(angpar+angpasso*i))
                prgr.cutseq.append(Plasma.CutRound(cutid,
                                                   float(holes['dia']),
                                                   cx+float(holes['dia'])/2,
                                                   cy,
                                                   'ccw'))
                print 'foro'+str(i)
                print 'x:',cx,' y:',cy


    # percorso taglio della piastra #
    if data['shape_data']['shape']==1:
        on_set=8
        out_set=6
        xstart=float(data['shape_data']['misure2'])+float(data['data_form']['sheet_margin_left'])
        ystart=float(data['data_form']['sheet_margin_bottom'])
        print xstart
        print ystart
        prgr.cutseq.append(Plasma.CutRect(1,
                                          float(data['shape_data']['misure2']),
                                          float(data['shape_data']['misure3']),
                                          xstart,
                                          ystart,
                                          'cw'))
    elif data['shape_data']['shape']==2:
        on_set=8
        out_set=6
        print 'allora!'
        diam=data['shape_data']['misure2']
        print 'diametro:',diam
        xstart=centerx + diam * 0.707
        ystart=centery - diam * 0.707
        prgr.cutseq.append(Plasma.CutRound(1,
                                           diam,
                                           xstart,
                                           ystart,
                                           'cw'))


    #prgr.cutseq.append(Plasma.CutRect(1,100,300,250,250,'ccw'))
    #prgr.cutseq.append(Plasma.CutRound(2, 500, 426.75, 73.25,'cw'))
    strprg=prgr.run()
    return json.dumps(strprg)


def esporta_dxf():
    output = cStringIO.StringIO()
    drawing = dxf.drawing('item.dxf')

    data=json.loads(request.vars.jsonstring)
    print json.dumps(data, sort_keys=True, indent=4)
    centerx=0
    centery=0
    cutid=1
    # disegna fori interni #
    if 'holes' in data['data_form'].keys():
        for holes in data['data_form']['holes']:
            if holes['intfo']<>'':
                modulo=holes['intfo']/2
            else:
                modulo=0
            print 'modulo:',modulo

            if holes['num']<>'':
                numfori=int(holes['num'])
            else:
                numfori=1
            print 'numfori:',numfori

            if holes['par']<>'':
                angpar=int(holes['par'])
            else:
                angpar=0
            print 'angpar:',angpar
            angpasso=360/numfori
            for i in range(0,numfori):
                cutid=cutid+1
                cx=centerx+modulo*math.cos(math.radians(angpar+angpasso*i))
                cy=centery+modulo*math.sin(math.radians(angpar+angpasso*i))
                drawing.add(dxf.circle(float(holes['dia']/2), (cx,cy)))

    # disegna sagoma piastra #
    if data['data_form']['shape']==1:
        xstart=-(data['data_form']['misure2']/2)
        ystart=-(data['data_form']['misure3']/2)


        drawing.add(dxf.line((xstart, ystart), 
                             (xstart, data['data_form']['misure3']/2)))
        drawing.add(dxf.line((xstart, data['data_form']['misure3']/2),
                             (data['data_form']['misure2']/2, data['data_form']['misure3']/2)))
        drawing.add(dxf.line((data['data_form']['misure2']/2, data['data_form']['misure3']/2),
                             (data['data_form']['misure2']/2, ystart)))
        drawing.add(dxf.line((data['data_form']['misure2']/2, ystart),
                             (xstart, ystart)))
    elif data['data_form']['shape']==2:
        drawing.add(dxf.circle(data['data_form']['misure2']/2, (centerx,centery)))


    drawing.save_to_fileobj(output)
    dxf_result=[output.getvalue()]
    return json.dumps(dxf_result)

def treD(): return dict(message="hello from platecut.py")
