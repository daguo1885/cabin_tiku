# coding:utf-8
# create time:2024-11-07
__author__ = 'Daguo'

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import warnings
import os
import random
from io import BytesIO
from streamlit import cache_data
import streamlit.components.v1 as components
warnings.simplefilter("ignore")
CURRENT_PATH = os.path.dirname(__file__)
pic = os.path.join(CURRENT_PATH, r'static\icon2.png')


# 初始化设置：streamlit页面基本配置
def init_set(hide=False):
    st.set_page_config(
        page_title="陆海新通道乘务员技能竞赛理论题",
        page_icon=":rainbow:",
        layout="wide",
        initial_sidebar_state="auto"   # 侧边栏
    )
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
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
    else:
        st.session_state.first_visit = False

    if 'index' not in st.session_state:
        st.session_state.index = True

    if 'result' not in st.session_state:
        st.session_state.result = False


# 侧边栏：登陆前授权码提示等；根据授权码判定用户
def side_bar():
    st.sidebar.image(pic, width=200)
    st.sidebar.markdown("<BR/><font size=4 color=darkgreen>**试题数量选择**</font>", unsafe_allow_html=True)
    df = get_tiku().fillna('')
    dfa = df.loc[df['试题类型'] == '单选'].reset_index(drop=True)
    dfb = df.loc[df['试题类型'] == '判断'].reset_index(drop=True)
    dfc = df.loc[df['试题类型'] == '多选'].reset_index(drop=True)
    # with st.sidebar.form("试题选择"):
    dx = st.sidebar.slider('单选题数量', 0, 50, 10)
    pd = st.sidebar.slider('判断题数量', 0, 50, 10)
    mx = st.sidebar.slider('多选题数量', 0, 50, 10)
   # sd_btn = st.form_submit_button('生成试卷')
    sd_btn = st.sidebar.button('刷新试卷')

    if sd_btn:
        st.session_state['danxuan'] = random.sample(range(0, dfa.shape[0]), dx)
        st.session_state['panduan'] = random.sample(range(0, dfb.shape[0]), pd)
        st.session_state['duoxuan'] = random.sample(range(0, dfc.shape[0]), mx)
        st.session_state['index'] = False
        st.session_state['result'] = False
        # st.sidebar.write(st.session_state['danxuan'], dfa.shape[0])
        # st.sidebar.write(st.session_state['panduan'], dfa.shape[0])
        # st.sidebar.write(st.session_state['duoxuan'], dfa.shape[0])
    st.sidebar.divider()
    st.sidebar.caption(':copyright: 2024 ChongQingCabin by Daguo')


@cache_data
def get_tiku():
    df = pd.read_excel('data.xlsx')
    return df


def main_app():
    st.title('乘务员技能竞赛理论题')
    df = get_tiku().fillna('')
    dfa = df.loc[df['试题类型'] == '单选'].reset_index(drop=True)
    dfb = df.loc[df['试题类型'] == '判断'].reset_index(drop=True)
    dfc = df.loc[df['试题类型'] == '多选'].reset_index(drop=True)

    show_area = st.empty()
    with show_area.container():
        # 生成单选题
        st.subheader('单选题')
        dx_tbl = pd.DataFrame(None, columns=['题目', '你的选择', '正确答案'])
        for i, j in enumerate(st.session_state['danxuan']):
            _sel = []
            _sel_a = ''
            for z in ['A', 'B', 'C', 'D']:
                if dfa[z][j] !="":
                    _sel.append(z + '. ' +dfa[z][j])
                    _sel_a = _sel_a + '\n' + z + '. ' +dfa[z][j]

            _tigan = f"单选第{i+1}题：{dfa['试题题干'][j]}"
            xuz = st.radio(_tigan, _sel, None)
            if xuz is not None:
                xuz = xuz[0]
            df = pd.DataFrame([[_tigan + "\n" + _sel_a, xuz, dfa['答案'][j]]], columns=['题目', '你的选择', '正确答案'])
            dx_tbl = pd.concat([dx_tbl, df])

        # 生成判断题
        st.subheader('判断题')
        for i, j in enumerate(st.session_state['panduan']):
            _sel_1 = []
            _tigan_1 = f"判断第{i+1}题：{dfb['试题题干'][j]}"
            xuz_1 = st.radio(_tigan_1, ['正确', '错误'], None)
            df1 = pd.DataFrame([[_tigan_1, xuz_1, dfb['答案'][j]]], columns=['题目', '你的选择', '正确答案'])
            dx_tbl = pd.concat([dx_tbl, df1])

        # 生成多选题
        st.subheader('多选题')
        for i, j in enumerate(st.session_state['duoxuan']):
            _tigan_2 = f"多选第{i+1}题：{dfc['试题题干'][j]}"
            st.write(_tigan_2)
            _sel_2 = []
            _sel_2_a = ''
            xuz_2 = ''
            for z in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                if dfc[z][j] !="":
                    _sel_2.append(z + '. ' +dfc[z][j])
                    _sel_2_a = _sel_2_a + '\n' + z + '. ' +dfc[z][j]
                    ans_a = st.checkbox(z + '. ' + dfc[z][j])
                    if ans_a:
                        xuz_2 += z

            if xuz_2 is not None:
                xuz_2 = [''.join(n[0]) for n in xuz_2]
            df2 = pd.DataFrame([[_tigan_2 + "\n" + _sel_2_a, ''.join(xuz_2), dfc['答案'][j]]], columns=['题目', '你的选择', '正确答案'])
            dx_tbl = pd.concat([dx_tbl, df2])

        st.session_state['dx_tbl'] = dx_tbl

        ans_btn = st.button('提交')

    if ans_btn:
        show_area.empty()
        result_show()


def result_show():
    st.title('测试结果')
    timu_num = st.session_state['dx_tbl'].shape[0]
    ok_num = sum(st.session_state.dx_tbl['你的选择'] == st.session_state.dx_tbl['正确答案'])
    rat = ok_num / timu_num
    st.write(f"共{timu_num}道题，你正确了{ok_num}道，正确率为{rat}")
    df_wrong = st.session_state.dx_tbl.loc[st.session_state.dx_tbl['你的选择'] != st.session_state.dx_tbl['正确答案']]

    # 显示选择
    show_w = st.toggle('只显示答错题目', on_change=stat_change)
    save_excel(st.session_state['dx_tbl'], '练习题', label='下载全部试卷')
    save_excel(df_wrong, '错题单', label='下载答错题目')
    if show_w:
        show_table(df_wrong)
    else:
        show_table(st.session_state.dx_tbl)


def stat_change():
    st.session_state.result = True


def index_page():
    st.title('乘务技能竞赛训练')
    st.text('西部陆海新通道乘务员技能赛练习试题库')


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
    side_bar()          # 导航栏
    if st.session_state.index:
        index_page()
    elif st.session_state.result:
        result_show()
    else:
        main_app()
