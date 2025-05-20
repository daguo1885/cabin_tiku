# coding:utf-8
# create time:2024-11-07
__author__ = 'Daguo'

from operator import index

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import warnings
import os
import random
from io import BytesIO
from streamlit import cache_data
import streamlit.components.v1 as components
import sqlite3
warnings.simplefilter("ignore")
CURRENT_PATH = os.path.dirname(__file__)
pic = r'icon2.png'


# 初始化设置：streamlit页面基本配置
def init_set(hide=False):
    st.set_page_config(
        page_title="应急救护竞赛理论题测试系统",
        page_icon=":100:",
        layout="wide",  # wide, centered
        initial_sidebar_state="expanded"   # 侧边栏 auto
    )

    # st.logo(pic, size='large')
    # 隐藏右边的菜单以及页脚
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid=stVerticalBlock]{gap: 0.6rem}
        </style>
        """
    if hide:
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 调整主页面位置
    st.markdown("""
        <style>
            html {
            font-size: 14px;}
            .st-emotion-cache-1mi2ry5{
            padding: 1rem 1rem 1rem; height: 0;}
            .st-emotion-cache-12fmjuu{
            height: 1rem}
            .st-emotion-cache-1jicfl2{
            padding-left: 1rem; padding-right: 1rem; padding-top: 1rem;}                                    
        </style>""", unsafe_allow_html=True)
    # 全局变量设置
    if 'role' not in st.session_state:
        st.session_state.role = ""

    if 'index' not in st.session_state:
        st.session_state.index = True

    if 'result' not in st.session_state:
        st.session_state.result = False

    if 're_run_index' not in st.session_state:
        st.session_state.re_run_index = True


# 侧边栏：登陆前授权码提示等；根据授权码判定用户
def side_bar(bar):
    bar.empty()
    with bar.container():
        if st.session_state.role != '':
            st.write(f':blue[**{st.session_state.role}**]，欢迎你！')

        st.markdown("<BR/><font size=4 color=darkblue>**试题数量选择**</font>", unsafe_allow_html=True)
        df = get_tiku().fillna('')
        dfa = df.loc[df['试题类型'] == '单选'].reset_index(drop=True)
        dfb = df.loc[df['试题类型'] == '判断'].reset_index(drop=True)
        dfc = df.loc[df['试题类型'] == '多选'].reset_index(drop=True)
        # with st.sidebar.form("试题选择"):
        dx = st.slider('单选题数量', 0, 50, 10)
        pd = st.slider('判断题数量', 0, 50, 10)
        # mx = st.slider('多选题数量', 0, 50, 10)
        mx = 0
       # sd_btn = st.form_submit_button('生成试卷')
        sd_btn = st.button('刷新试卷')

    if sd_btn:
        st.session_state['danxuan'] = random.sample(range(0, dfa.shape[0]), dx)
        st.session_state['panduan'] = random.sample(range(0, dfb.shape[0]), pd)
        st.session_state['duoxuan'] = random.sample(range(0, dfc.shape[0]), mx)
        st.session_state['index'] = False
        st.session_state['result'] = False
        # st.sidebar.write(st.session_state['danxuan'], dfa.shape[0])
        # st.sidebar.write(st.session_state['panduan'], dfa.shape[0])
        # st.sidebar.write(st.session_state['duoxuan'], dfa.shape[0])


def menu_bar():
    st.sidebar.image(pic, width=200)
    st.sidebar.markdown("<br/>", unsafe_allow_html=True)

    if st.sidebar.button('系统介绍', icon='🏠'):
        st.session_state.sel_menu = '系统介绍'

    if st.sidebar.button('在线学习', icon='📝'):
        st.session_state.sel_menu = '在线学习'

    if st.sidebar.button('在线测试', icon='✅'):
        st.session_state.sel_menu = '在线测试'

    st.session_state.sid = st.sidebar.empty()

    if st.session_state.role == "":
        with st.session_state.sid:
            st.session_state.role = st.text_input('请输入员工号记录你的成绩')
    else:
        with st.session_state.sid:
            st.write(f':blue[**{st.session_state.role}**]欢迎你！')

    st.sidebar.divider()
    st.sidebar.caption(':copyright: 2024 ChongQingCabin by Daguo')


@cache_data
def get_tiku():
    # cox = sqlite3.connect('data.db')
    df = pd.read_excel('data.xlsx').fillna('')
    # df.to_sql('data', cox, if_exists='replace')
    # df = pd.read_sql("select * from data", cox)
    return df


def main_app():
    st.subheader(':rainbow[乘务员技能竞赛理论题]', divider='rainbow')

    df = get_tiku().fillna('')
    dfa = df.loc[df['试题类型'] == '单选'].reset_index(drop=True)
    dfb = df.loc[df['试题类型'] == '判断'].reset_index(drop=True)
    dfc = df.loc[df['试题类型'] == '多选'].reset_index(drop=True)

    show_area = st.empty()
    with show_area.container():
        # 生成单选题
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<font size=4 color=darkblue>**一. 单项选择题**</font>', unsafe_allow_html=True)
        dx_tbl = pd.DataFrame(None, columns=['序号','题目', '你的选择', '正确答案'])
        for i, j in enumerate(st.session_state['danxuan']):
            _sel = []
            _sel_a = ''
            for z in ['A', 'B', 'C', 'D']:
                if dfa[z][j] !="":
                    _sel.append(z + '. ' + str(dfa[z][j]))
                    _sel_a = _sel_a + '\n' + z + '. ' + str(dfa[z][j])
            _tigan = f"[单选第{i+1}题]  {dfa['试题题干'][j]}"
            st.markdown("<br/>", unsafe_allow_html=True)
            xuz = st.radio(":blue" + _tigan, _sel, None, horizontal=True)
            if xuz is not None:
                xuz = xuz[0]
            df = pd.DataFrame([[dfa['序号'][j], _tigan + "\n" + _sel_a, xuz, dfa['答案'][j]]], columns=['序号', '题目', '你的选择', '正确答案'])
            dx_tbl = pd.concat([dx_tbl, df])

        # 生成判断题
        st.markdown('<font size=4 color=darkblue>**二. 判断题**</font>', unsafe_allow_html=True)
        for i, j in enumerate(st.session_state['panduan']):
            st.markdown("<br/>", unsafe_allow_html=True)
            _sel_1 = []
            _tigan_1 = f"[判断第{i+1}题]  {dfb['试题题干'][j]}"
            xuz_1 = st.radio(":blue" + _tigan_1, ['正确', '错误'], None, horizontal=True)
            df1 = pd.DataFrame([[dfb['序号'][j], _tigan_1, xuz_1, dfb['答案'][j]]], columns=['序号', '题目', '你的选择', '正确答案'])
            dx_tbl = pd.concat([dx_tbl, df1])

        # 生成多选题
        if len(st.session_state['duoxuan']) > 0:
            st.markdown('<font size=4 color=darkblue>**三. 多项选择题**</font>', unsafe_allow_html=True)
            for i, j in enumerate(st.session_state['duoxuan']):
                st.markdown("<br/>", unsafe_allow_html=True)
                _tigan_2 = f"[多选第{i+1}题]  {dfc['试题题干'][j]}"
                st.write(":blue" + _tigan_2)
                _sel_2 = []
                _sel_2_a = ''
                xuz_2 = ''
                for z in ['A', 'B', 'C', 'D', 'E']:
                    if dfc[z][j] !="":
                        _sel_2.append(z + '. ' + str(dfc[z][j]))
                        _sel_2_a = _sel_2_a + '\n' + z + '. ' + str(dfc[z][j])
                        ans_a = st.checkbox(z + '. ' + str(dfc[z][j]))
                        if ans_a:
                            xuz_2 += z

                if xuz_2 is not None:
                    xuz_2 = [''.join(n[0]) for n in xuz_2]
                df2 = pd.DataFrame([[dfc['序号'][j], _tigan_2 + "\n" + _sel_2_a, ''.join(xuz_2), dfc['答案'][j]]], columns=['序号', '题目', '你的选择', '正确答案'])
                dx_tbl = pd.concat([dx_tbl, df2])

        st.session_state['dx_tbl'] = dx_tbl

        ans_btn = st.button('提交')

    if ans_btn:
        show_area.empty()
        result_show()


def result_show():
    st.markdown(f'<font size=4 color=darkblue>**{st.session_state.role}练习测试结果**</font>', unsafe_allow_html=True)
    timu_num = st.session_state['dx_tbl'].shape[0]
    ok_num = sum(st.session_state.dx_tbl['你的选择'] == st.session_state.dx_tbl['正确答案'])
    rat = ok_num / timu_num
    if rat == 1:
        st.balloons()
        st.toast('太厉害了！恭喜你100%正确！加油！')
    elif rat >= 0.9:
        st.toast('非常优秀！加油！你还可以做的更好！')
    elif rat >= 0.8:
        st.toast('不错！继续努力！')
    else:
        st.toast('加油！多练练一定可以的！')
    st.write(f"共{timu_num}道题，你正确了{ok_num}道，正确率为{rat*100:0.2f}%")
    df_wrong = st.session_state.dx_tbl.loc[st.session_state.dx_tbl['你的选择'] != st.session_state.dx_tbl['正确答案']]

    # 显示选择
    show_w = st.toggle('只显示答错题目', on_change=stat_change)
    save_excel(st.session_state['dx_tbl'], '练习题', label='下载全部试卷')
    save_excel(df_wrong, '错题单', label='下载答错题目')
    # 此处保存答题数据
    dfa = st.session_state['dx_tbl']
    dfa['用户'] = st.session_state.role
    dfa['时间'] = datetime.now()
    cox = sqlite3.connect('data.db')
    dfa.to_sql('测试记录', cox, if_exists='replace')
    # st.dataframe(dfa)
    if show_w:
        show_table(df_wrong[['题目', '你的选择', '正确答案']])
    else:
        show_table(st.session_state.dx_tbl[['题目', '你的选择', '正确答案']])


def stat_change():
    st.session_state.result = True


def index_page():
    st.subheader(':rainbow[应急救护竞赛理论题测试系统]', divider='rainbow')
    st.write('👈️**请在侧边菜单栏选择相应功能**')
    st.write('竞赛理论试题在线刷题工具，系统根据官方下发理论题库制作，集成题库学习和在线测试功能。')
    st.write('在线学习可以自主选择:blue[**顺序复习、随机复习、批量阅读**]的方式。')
    st.write('在线测试可以自定义生成试卷时各种题型的数量。')
    st.write(':blue[提示：]完成测试后下载错误试题为excel格式，可手工将题干列设置为自动换行并调整列宽，可获得较好的显示效果。')
    st.markdown('</br>', unsafe_allow_html=True)
    st.write(":green[以下方式可以展开或隐藏侧边栏菜单]")

    if st.session_state.role != '':
        st.session_state.sid.write(f':blue[**{st.session_state.role}**]，欢迎你！')

    cl = st.columns(4)
    with cl[0]:
        st.image("static/zhankai.jpg", width=200)
    with cl[1]:
        st.image("static/zhedie.jpg", width=200)


def show_table(df, **kwargs):
    """
    # 实现表格显示功能
    # 利用dataframe.to_html功能，编辑html表格边框显示
    # 存在的BUG：对于较多单元格存在换行的情况，表格高度控制无法自适应
    """
    line = df.shape[0]
    html = df.to_html(index=False, justify='left', border=0, float_format='%.3f')
    htm = html.replace('class', 'cellpadding=\"2\" cellspacing=\"1\" style=\"font-size:12px\" bgcolor=\"lightblue\" class')
    htm = htm.replace('tr', 'tr bgcolor=\"#ffffff\"')
    htm = htm.replace('tr', 'tr bgcolor=\"#f0f8ff\"', 1)
    htm = htm.replace('\\n', '<br>')
    try:
        height_num = kwargs['height']
        return components.html(htm, height=height_num, scrolling=True)
    except:
        height_num = 80*line
        return components.html(htm, height=height_num, scrolling=True)


def trans_record_data_to_io(data, **kwargs):
    try:
        idx = kwargs['index']
    except:
        idx = False
    file = BytesIO()
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    data.to_excel(writer, index=idx)
    # writer.save()  # 这个save不会落盘
    writer.close()
    return file.getvalue()


@st.fragment
def save_excel(df, file_name, *args, **kwargs):
    try:
        fn = f'{file_name}{args[0]}.xlsx'
    except:
        fn = f'{file_name}_{date.today().isoformat()}.xlsx'
    try:
        labels = kwargs['label']
    except:
        labels = '下载至excel'
    try:
        key_1 = kwargs['key']
    except:
        key_1 = None
    try:
        idx = kwargs['index']
    except:
        idx = False
    try:
        onclk = kwargs['onclick']
    except:
        onclk = None
    st.download_button(
        label=labels,
        key=key_1,
        data=trans_record_data_to_io(df, index=idx),
        file_name=fn,
        mime='text/csv',
        on_click=onclk)


if __name__ == '__main__':
    init_set(hide=True)     # 初始化设置
    menu_bar()

    if 'sel_menu' not in st.session_state:
        index_page()
    else:
        if st.session_state.sel_menu == '系统介绍':
            index_page()
        elif st.session_state.sel_menu == '在线测试':
            side_bar(st.session_state.sid)  # 导航栏
            if st.session_state.result:
                result_show()
            else:
                if 'danxuan' not in st.session_state:
                    st.subheader(':blue[请在左侧菜单刷新试卷]')
                    st.write(":blue[提示：]你可以选择测试各类型题目的数量后刷新试卷")
                else:
                    main_app()
        elif st.session_state.sel_menu == '在线学习':
            from online_review import main_page
            main_page(st.session_state.sid)
        else:
            index_page()
