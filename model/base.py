from sqlalchemy import Column, Integer, asc, create_engine, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from libs.exception import AppException
from config.secure import SQLALCHEMY_URL
from config.settings import DEFAULT_PAGE_SIZE
from libs.service import (download_file, read_excel, save_excel,
                          save_jg_detial, save_word)
import traceback
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename=r'info.log',
                    filemode='a')

engine = create_engine(SQLALCHEMY_URL)
DBSession = sessionmaker(bind=engine)
session = DBSession()

base_class = declarative_base()


def init_database():
    base_class.metadata.create_all(engine)


class Base(base_class):
    __abstract__ = True
    __tablename__ = ''
    __table_args__ = {"extend_existing": True}
    disable_mh = False

    class_name = ''
    pic = False
    ty = None
    foreign_key = ''
    export_docx = True
    field = []
    file_field = []
    read_field = []
    date_field = []
    export_handle_file = []
    combo_field = {}
    translations = {}

    template_start_row = 0

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def get_by_id(cls, id_):
        return session.query(cls).get(id_)
    
    #删除表单全部数据
    @classmethod
    def delete_all(cls):
        session.query(cls).delete()
        session.commit()

    @classmethod
    def create(cls, **kwargs):
        base = cls()
        for key, value in kwargs.items():
            if hasattr(cls, key) and key not in cls.read_field:
                try:
                    setattr(base, key, value)
                except:
                    pass
        try:
            session.add(base)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(e.__dict__['orig'])
            raise AppException(":" + error)
        else:
            return base

    def modify(self, **kwargs):
        for key, value in kwargs.items():
            try:
                if hasattr(self, key):
                    setattr(self, key, value)
            except BaseException as e:
                pass
        session.commit()

    def delete(self):
        if self.ty:
            for ty in self.ty.search(**{self.foreign_key: self.id}, page_size=-1)['data']:
                ty.delete()

        session.delete(self)
        session.commit()

    @classmethod
    def get_all_id(cls):
        return session.query(cls.id).all()

    @classmethod
    def search(cls, **kwargs):  # noqa: C901
        try:
            res = session.query(cls)
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        if isinstance(value, str):
                            if value.startswith(('>=', '==', '<=', '<', '>', '=')):
                                try:
                                    if value.startswith('=') and not value.startswith('=='):
                                        value = '=' + value
                                    try:
                                        cmd = 'res.filter(getattr(cls, key)' + value + ')'
                                        res = eval(cmd)
                                    except Exception:
                                        key = key + "_"
                                        cmd = 'res.filter(getattr(cls, key)' + value + ')'
                                        res = eval(cmd)
                                    continue
                                except Exception:
                                    pass
                            if cls.disable_mh:
                                try:
                                    res = res.filter(getattr(cls, key).like(value))
                                except Exception:
                                    key = key + "_"
                                    res = res.filter(getattr(cls, key).like(value))
                            else:
                                try:
                                    res = res.filter(getattr(cls, key).like("%" + value + "%"))
                                except Exception:
                                    key = key + "_"
                                    res = res.filter(getattr(cls, key).like("%" + value + "%"))
                        else:
                            res = res.filter(getattr(cls, key) == value)

            if kwargs.get('order'):
                for key, value in kwargs['order'].items():
                    if hasattr(cls, key):
                        if value == 'asc':
                            try:
                                res = res.order_by(asc(getattr(cls, key)))
                            except Exception:
                                res = res.order_by(asc(getattr(cls, key + '_')))
                        if value == 'desc':
                            try:
                                res = res.order_by(desc(getattr(cls, key)))
                            except Exception:
                                res = res.order_by(desc(getattr(cls, key + '_')))

            page = kwargs.get('page') if kwargs.get('page') else 1
            page_size = kwargs.get('page_size') if kwargs.get('page_size') else DEFAULT_PAGE_SIZE
            if page_size == -1:
                page_size = 100000000
            data = {
                'meta': {
                    'count': res.count(),
                    'page': page,
                    'page_size': page_size
                }
            }

            res = res.offset((page - 1) * page_size).limit(page_size)
            res = res.all()
            data['data'] = res
            return data
        except Exception as e:
            logging.info(traceback.format_exc())
            raise AppException("发生异常数据,请查看日志info.log或加载可用的备份数据")

    @classmethod
    def import_(cls, filename, **kwargs):
        try:
            res = read_excel(filename, cls.template_start_row, cls.class_name)
            for kk, i in enumerate(res):
                field = cls.field.copy()
                field.remove('id')
                for file in cls.file_field:
                    field.remove(file)
                for file in cls.read_field:
                    field.remove(file)
                data = {field[idx]: i[idx] for idx in range(len(field))}
                if cls.__tablename__ == 'swtz' or cls.__tablename__ == 'lftz':
                    time = data['datetime']
                    flag = 1
                    answer = ""
                    # 1 全数字 8位
                    # 2 有符号 无0
                    # 3 有符号 有0
                    # 4 无法判断
                    fh = []
                    for j in time:
                        if j > '9' or j < '0':
                            flag = 2
                            fh.append(j)
                    if flag == 1:
                        if len(time) < 8:
                            flag = 4
                        else:
                            answer = time[0:4] + "/" + time[4:6] + "/" + time[6:8]
                    else:
                        if len(fh) < 2:
                            flag = 4
                        else:
                            ele = []
                            ind = 1
                            for indx, j in enumerate(time):
                                if '9' >= j >= '0':
                                    if len(ele) < ind:
                                        ele.append(j)
                                    else:
                                        ele[ind - 1] += j
                                else:
                                    if indx == 0: continue
                                    if '9' >= time[indx - 1] >= '0':
                                        ind += 1
                            if len(ele) < 3:
                                flag = 4
                            else:
                                answer = ele[0].rjust(4, '0') + "/" + ele[1].rjust(2, '0') + '/' + ele[2].rjust(2, '0')
                    if flag == 4:
                        answer = time
                    data['datetime'] = answer
                    data.update(kwargs)
                if cls.__tablename__ != 'jg':
                    if cls.search(**data)['meta']['count'] == 0:
                        if 'type' in kwargs:
                            del data['type']
                        cls.create(**data, **kwargs)
                else:
                    for k in cls.import_handle_file:
                        if not data[k]:
                            peo = []
                        else:
                            peo = data[k].split(',')
                        data[k] = peo
                    if 'type' in data and 'type' in kwargs:
                        del data['type']
                    cls.create(**data, **kwargs)
        except AppException as e:
            logging.info(traceback.format_exc())
            raise AppException("发生不可预料的错误,请查看日志info.log")

    @classmethod
    def export(cls, filename, **kwargs):
        res = cls.search(page_size=-1, **kwargs)['data']
        field = cls.field.copy()
        for file in cls.file_field:
            field.remove(file)
        for file in cls.read_field:
            field.remove(file)
        data = [[getattr(i, key) for key in field] for i in res]
        save_excel('template/{}.xlsx'.format(cls.__tablename__), cls.template_start_row, data, filename)

    @classmethod
    def export_template(cls, filename):
        download_file('template/{}.xlsx'.format(cls.__tablename__), filename)

    @classmethod
    def export_document(cls, id_, filename):
        base = cls.get_by_id(id_)
        data = dict()
        field = cls.field.copy()
        field.remove("id")
        if cls.pic:
            field.insert(1, "photo")
        for file in cls.file_field:
            field.remove(file)
        for file in cls.read_field:
            field.remove(file)
        for ind, file in enumerate(field):
            if file in cls.export_handle_file:
                field[ind] = file + '_'

        for item in field:
            attr = getattr(cls, item)
            try:
                data[attr.comparator.comment] = getattr(base, item) if getattr(base, item) else ''
            except AttributeError:
                pass
        ty_data = []
        if cls.ty and cls.class_name != '在绍台企':
            ty_field = cls.ty.field.copy()
            ty_field.remove("id")
            for file in cls.ty.file_field:
                ty_field.remove(file)
            ty_list = cls.ty.search(**{cls.ty.foreign_key: id_}, page_size=-1)['data']
            for ty in ty_list:
                tmp = dict()
                for item in ty_field:
                    if item == 'identity' or item == 'type': item = item + '_'
                    attr = getattr(cls.ty, item)
                    tmp[attr.comparator.comment] = getattr(ty, item) if getattr(ty, item) else ''
                ty_data.append(tmp)

        if cls.class_name == '机构':
            save_jg_detial(filename, cls.class_name, data)
        else:
            save_word(filename, cls.class_name, data, cls.pic, ty_data)
