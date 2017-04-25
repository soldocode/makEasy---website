#!/usr/bin/env python
# coding: utf8
from gluon import *

class Coord:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y


class PlasmaCutPlan:
    def __init__(self,
                 id_pgm=1,
                 breakthrough_time = 200,
                 margin = 10,
                 cutspeed = 2000
                 ):

        self.id_pgm = id_pgm
        self.last_N_program=0
        self.filename = str(id_pgm)+'.PGM'
        self.breakthrough_time = breakthrough_time
        self.margin = margin
        self.cutspeed = cutspeed
        self.cutseq=[]

    def __str__(self):
        text = 'Plasma Cut: ' + str(id_pgm) + '\n'
        for seq in self.cutseq:
            text = text + str(seq) + '\n'
        return text

    def run(self):

        prg= ['%' + str(self.id_pgm)+'\r\n',
              'N5G292 \r\n',
              'N10G64 \r\n',
              '?%ETK[0]=' + str(self.breakthrough_time)+'\r\n',
              'N15G54 \r\n']
        first_seq = self.cutseq[0]
        start_coord = first_seq.start_pos
        if first_seq.direction == 'cw':
            last_x=start_coord.x  + first_seq.onset
            last_y=start_coord.y
        else:
            last_x=start_coord.x - first_seq.onset * 0.707
            last_y=start_coord.y - first_seq.onset * 0.707

        prg.append('N20G0G90G40X' +str(last_x) +'Y' + str(last_y)+'\r\n')
        prg.append('')
        prg.append('N25G231'+'\r\n')
        prg.append('N30M2'+'\r\n')
        prg.append('N35G91'+'\r\n')

        set_speed=True
        prg_line=40

        for seq in self.cutseq:
            start_coord = seq.start_pos
            if seq.direction == 'cw':
                x_start=start_coord.x  + seq.onset
                y_start=start_coord.y
                print 'x_start:',x_start
            else:
                x_start=start_coord.x - seq.onset * 0.707
                y_start=start_coord.y - seq.onset * 0.707

            move_x = x_start - last_x
            move_y = y_start - last_y

            prg.append('N'+str(prg_line)+'G54'+'\r\n')

            if set_speed:
                prg_line=prg_line+5
                prg.append('N'+str(prg_line)+'F' +str(self.cutspeed)+'\r\n')
                set_speed=False


            prg.append('N'+str(prg_line+5)+'SYN'+'\r\n')
            prg.append('N'+str(prg_line+10)+'G41D1'+'\r\n')
            #if seq.direction=='cw':
            #    prg.append('N'+str(prg_line+10)+'G41D1')
            #else:
            #    prg.append('N'+str(prg_line+10)+'G41D2')

            prg.append('N'+str(prg_line+15)+'G0X'+str(move_x)+'Y'+str(move_y)+'\r\n')
            prg.append('N'+str(prg_line+20)+'M17'+'\r\n')

            if seq.direction=='cw':
                prg.append('N'+str(prg_line+25)+'G1X-' +str(seq.onset) + 'Y0'+'\r\n')
                if seq.__class__==CutRect:
                    prg.append('N'+str(prg_line+30)+'G1X-' + str(seq.width) + 'Y0'+'\r\n')
                    prg.append('N'+str(prg_line+35)+'G1X0Y' + str(seq.height) +'\r\n')
                    prg.append('N'+str(prg_line+40)+'G1X' + str(seq.width) + 'Y0'+'\r\n')
                    prg.append('N'+str(prg_line+45)+'G1X0Y-' + str(seq.height)+'\r\n')
                    prg_line=prg_line+50
                elif seq.__class__==CutRound:
                    prg.append('N'
                               + str(prg_line+30)
                               + 'G2X0Y0I-'
                               + str(seq.diameter/2*0.707)
                               + 'J'
                               + str(seq.diameter/2*0.707)
                               +'\r\n')
                    prg_line=prg_line+35
                prg.append('N'+str(prg_line)+'G40G1X0Y-' +str(seq.outset)+'\r\n')
                print 'CW'
                print start_coord.x
                print start_coord.y
                last_x=start_coord.x
                last_y=start_coord.y - seq.outset
            else: #direction ='ccw'
                prg.append('N'
                           +str(prg_line+25)
                           +'G1X'
                           +str(seq.onset*0.707)
                           +'Y'
                           +str(seq.onset*0.707)
                           +'\r\n')
                if seq.__class__==CutRect:
                    prg.append('N'+str(prg_line+30)+'G1X0Y' + str(seq.height/2)+'\r\n')
                    prg.append('N'+str(prg_line+35)+'G1X-' + str(seq.width) + 'Y0'+'\r\n')
                    prg.append('N'+str(prg_line+40)+'G1X0Y-' + str(seq.height)+'\r\n')
                    prg.append('N'+str(prg_line+45)+'G1X' + str(seq.width) + 'Y0'+'\r\n')
                    prg.append('N'+str(prg_line+50)+'G1X0Y' + str(seq.height/2)+'\r\n')
                    prg_line=prg_line+55
                elif seq.__class__==CutRound:
                    prg.append('N'
                               + str(prg_line+30)
                               + 'G3X0Y0I-'
                               + str(seq.diameter/2)
                               + 'J0'
                               +'\r\n')
                    prg_line=prg_line+35
                prg.append('N'
                           +str(prg_line)
                           +'G40G1X-'
                           +str(seq.outset * 0.707)
                           +'Y'
                           +str(seq.outset * 0.707)
                           +'\r\n')
                print 'CCW'
                print start_coord.x
                print start_coord.y
                last_x=start_coord.x - seq.outset * 0.707
                last_y=start_coord.y + seq.outset * 0.707

            prg.append('N'+str(prg_line+5)+'M20'+'\r\n')
            prg.append('N'+str(prg_line+10)+'G4F1.5'+'\r\n')
            prg.append('N'+str(prg_line+15)+'G40'+'\r\n')
            prg_line=prg_line+20

        prg.append('N'+str(prg_line)+'G90'+'\r\n')
        prg.append('END'+'\r\n')
        prg[6]=('RPT 35, '+str(prg_line)+', 1'+'\r\n')

        for line in prg: print line

        #out_file = open(self.filename, 'w')
        #for line in prg: out_file.write(line+'\n')
        #out_file.close()
        return prg




class CutSequence:
    def __init__(self,
                 id,
                 onset=8,
                 outset=6,
                 start_pos=Coord(),
                 direction='cw'):

        self.id=id
        self.onset=onset
        self.outset=outset
        self.start_pos=start_pos
        self.direction=direction

    def __str__(self):
        text = '  onset: ' + str(self.onset) + '\n'
        text = text + '  outset: '+ str(self.outset) + '\n'
        text = text + '  start_pos: '+ str(self.start_pos.x) +', ' \
                                     + str(self.start_pos.y) + '\n'
        text = text + '  direction: '+ str(self.direction) + '\n'
        return text



class CutRect(CutSequence):
    def __init__(self, id, width, height, start_x, start_y, direction):
        CutSequence.__init__(self,
                             id,
                             start_pos=Coord(start_x,start_y),
                             direction=direction)
        self.width=width
        self.height=height

    def __str__(self):
        text = str(self.id)+ ' CutRect: ' + str(self.width) + ',' + str(self.height) +'\n'
        text = text + str(CutSequence.__str__(self))
        return text


class CutRound(CutSequence):
    def __init__(self, id, diameter, start_x, start_y, direction):
        CutSequence.__init__(self,
                             id,
                             start_pos=Coord(start_x,start_y),
                             direction=direction)
        self.diameter=diameter

    def __str__(self):
        text = str(self.id)+' CutRound: ' + str(self.diameter) + '\n'
        text = text + str(CutSequence.__str__(self))
        return text


#print '****** ROUND CUT *******'


#id_pgm = input('ID PROGRAMMA: ')
#prg=PlasmaCutPlan(id_pgm)
#prg.cutseq.append(CutRound(1,100,300,250,'ccw'))
#prg.cutseq.append(CutRound(2, 500, 426.75, 73.25,'cw'))


#print prg



#prova = prg.save()
