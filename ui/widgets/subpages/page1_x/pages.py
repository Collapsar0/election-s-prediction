from model.gwtz import GWTZ
from model.gwtz_ty import GWTZ_TY
from model.jzz import JZZ
from model.lftz import LFTZ
from model.lftz_ty import LFTZ_TY
from model.lp import LP
from model.ls import LS
from model.lsjl import LSJL
from model.swtz import SWTZ
from model.swtz_ty import SWTZ_TY
from model.ts import TS
from model.tstg import TSTG
from model.zyrs import ZYRS
from ui.page_elements.search_page import SearchPage


class Pagelsjl(SearchPage):
    title = "来绍交流"
    model = LSJL
    summary = [
        '姓名',
        '性别',
        '出生日期',
        '常驻地址',
        '大陆手机号',
        '接待单位',
        '停留事由',
        '来访时间'
    ]


class Pagezstb(SearchPage):
    title = "在绍台胞"
    model = TSTG
    summary = [
        '姓名',
        '性别',
        '出生日期',
        '所在单位',
        '大陆联系方式'
    ]


class Pagezstb_tstg(Pagezstb):
    title = "在绍台胞-台商台干"
    default_conditions = {'type': '台商台干'}


class Pagezstb_jycy(Pagezstb):
    title = "在绍台胞-就业创业"
    default_conditions = {'type': '就业创业'}


class Pagezstb_qt(Pagezstb):
    title = "在绍台胞-其他"
    default_conditions = {'type': '其他'}


class Pagezyrs(SearchPage):
    title = "重要人士"
    model = ZYRS
    summary = [
        '姓名',
        '性别',
        '出生日期',
        '党派',
        '倾向',
        '联系方式',
        '单位职务',
        '来访时间'
    ]


class Pagelp(SearchPage):
    title = "陆配"
    model = LP
    summary = [
        '姓名',
        '性别',
        '地区',
        '活跃度',
        '大陆工作单位',
        '大陆联系电话',
        '配偶姓名',
        '配偶民族',
        '子女姓名',
        '子女性别',
        '子女出生年月',
        '子女工作单位/就读学校名称'
    ]


class Pagels(SearchPage):
    title = "陆生"
    model = LS
    summary = [
        '姓名',
        '地区',
        '是否在读',
        '届别',
        '活跃度',
        '联系方式'
    ]


class Pagets(SearchPage):
    title = "台属"
    model = TS
    summary = [
        '姓名',
        '地区',
        '出生年月',
        '单位职务',
        '联系电话',
        '活跃度',
        '在台亲属关系',
        '在台亲属姓名',
        '在台亲属单位职位',
        '在台亲属联系程度'
    ]


class Pagegwtz(SearchPage):
    title = "公务团组"
    model = GWTZ
    summary = [
        '年度',
        '团长',
        '人数',
        '联系人',
        '台湾邀请单位'
    ]
    member_page_name = 'gwtz_ty'


class Pagegwtz_ty(SearchPage):
    title = "公务团组团员"
    model = GWTZ_TY
    summary = [
        '姓名',
        '单位职务',
        '人物类型',
        '身份'
    ]


class Pageswtz(SearchPage):
    title = "商务团组"
    model = SWTZ
    summary = [
        '企业名称',
        '台方企业名称',
        '时间',
    ]
    member_page_name = 'swtz_ty'


class Pageswtz_ty(SearchPage):
    title = "商务团组团员"
    model = SWTZ_TY
    summary = [
        '姓名',
        '单位职务',
        '身份证号',
        '备注',
        '身份'
    ]


class Pagelftz(SearchPage):
    title = "来访台胞"
    model = LFTZ
    summary = [
        '时间',
        '团组名称',
        '人数',
        '天数',
        '团长',
        '考察内容',
        '备注'
    ]
    member_page_name = 'lftz_ty'


class Pagelftz_jc(Pagelftz):
    title = "来访台胞-基层"
    default_conditions = {'type': '基层'}


class Pagelftz_qn(Pagelftz):
    title = "来访台胞-青年"
    default_conditions = {'type': '青年'}


class Pagelftz_sj(Pagelftz):
    title = "来访台胞-商界"
    default_conditions = {'type': '商界'}


class Pagelftz_xj(Pagelftz):
    title = "来访台胞-学界"
    default_conditions = {'type': '学界'}


class Pagelftz_zj(Pagelftz):
    title = "来访台胞-政界"
    default_conditions = {'type': '政界'}


class Pagelftz_ty(SearchPage):
    title = "来访台胞团员"
    model = LFTZ_TY
    summary = [
        '姓名',
        '单位职务',
        '人物类型',
        '备注',
        '身份'
    ]


class Pageall_lftz_ty(SearchPage):
    title = "来访台胞人员汇总"
    model = LFTZ_TY
    summary = [
        '姓名',
        '团组名称',
        '单位职务',
        '人物类型',
        '身份'
    ]
    cant_add = True


class Pagejzz(SearchPage):
    title = "居住证人员"
    model = JZZ
    summary = [
        '姓名',
        '性别',
        '居住证号码',
        '通行证号码',
        '地址',
        '联系电话',
        '处理日期'
    ]
