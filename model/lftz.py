from sqlalchemy import Column, String, Text

from model.base import Base
from model.lftz_ty import LFTZ_TY


class LFTZ(Base):
    __tablename__ = 'lftz'

    class_name = '来访团组'
    ty = LFTZ_TY

    field = [
        'id', 'datetime', 'name', 'number_of_people', 'number_of_day', 'stroke', 'group_organization',
        'head',
        'type', 'area', 'content', 'remark'
    ]
    read_field = ['head']
    date_field = ['datetime']

    combo_field = {
        'type': {
            'exclude': False,
            'items': ['基层', '青年', '商界', '学界', '政界', '其他']
        }
    }

    template_start_row = 3

    datetime = Column(String(100), comment='时间')
    name = Column(String(100), comment='团组名称')
    number_of_people = Column(String(100), comment='人数')
    number_of_day = Column(String(100), comment='天数')
    stroke = Column(String(100), comment='行程')
    group_organization = Column(String(100), comment='组团单位')
    assisting_unit = Column(String(100), comment='协助单位')
    remark = Column(Text, comment='备注')
    type_ = Column('type', String(100), comment='身份')
    area = Column(String(100), comment='地区')
    content = Column(Text, comment='考察内容')
    head_ = Column('head', String(100), comment='团长')

    @property
    def head(self):
        if self.id is None:
            return None
        from model.lftz_ty import LFTZ_TY
        try:
            tmp = LFTZ_TY.search(lftz_id=self.id)['data'][0].nickname
            if self.head_ == None and tmp != None:
                self.modify(head_=tmp)
            return tmp
        except IndexError:
            return None

    @property
    def type(self):
        if self.type_ is None:
            return []
        return self.type_.split(' ')

    @type.setter
    def type(self, val):
        if isinstance(val, list):
            while '' in val:
                val.remove('')
            self.type_ = ' '.join(val)
        else:
            self.type_ = val
