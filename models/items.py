# coding: utf8

db.define_table('material')

db.define_table('item_class')

db.define_table('item', Field('cod','string'),
                        Field('iclass',db.item_class),
                        Field('title','string'),
                        Field('description','string'),
                        Field('weight','double'),
                        Field('material_id',db.material),
                        Field('weight','double'),
                        Field('prj_parameters','string'),
                        Field('project','string'),
                        Field('prices','string'))
