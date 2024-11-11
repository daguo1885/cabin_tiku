# coding:utf-8
# create time:2024-11-07
__author__ = 'Daguo'

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import warnings
import os
import random
from streamlit import cache_data

warnings.simplefilter("ignore")
CURRENT_PATH = os.path.dirname(__file__)
pic = r'.\static\icon2.png'


# 初始化设置：streamlit页面基本配置
def init_set(hide=False):
    st.set_page_config(
        page_title="技能竞赛理论题测试系统",
        page_icon=":100:",
        layout="centered",  # wide, centered
        initial_sidebar_state="expanded"   # 侧边栏 auto
    )

    st.logo(pic, size='large')
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

    if 're_run_index' not in st.session_state:
        st.session_state.re_run_index = True

    if 'result' not in st.session_state:
        st.session_state.result = False


@cache_data
def get_tiku():
    df = pd.read_excel('data.xlsx')
    return df


def main_page(bar):
    st.subheader(':rainbow[题库复习]', divider='rainbow')

    if st.button(label='返回首页', icon='🏠'):
        st.session_state.sel_menu = '系统介绍'
    if st.button(label='前往测试', icon='✅'):
        st.session_state.sel_menu = '在线测试'

    bar.empty()
    bar_ct = bar.container()
    with bar_ct:
        st.markdown("<BR/><font size=4 color=darkblue>**学习方式选择**</font>", unsafe_allow_html=True)
        sel_way = st.radio(':blue[选择学习方式]', ['顺序复习', '随机复习', '批量浏览'], label_visibility="hidden")

        st.markdown('</br>', unsafe_allow_html=True)
    st.markdown('</br>', unsafe_allow_html=True)

    def order_b():
        st.session_state.re_run_index = True

    df = get_tiku()
    df = df.fillna('')
    if sel_way == '随机复习':
        num_id = random.sample(range(0, df.shape[0]), 1)[0]
    elif sel_way == '顺序复习':
        start_num = bar_ct.slider('请选择开始题号', 1, 1842, 1, on_change=order_b)
        if st.session_state.re_run_index:
            st.session_state.numstep = 0
            st.session_state.re_run_index = False
        num_id = start_num + st.session_state.numstep
    elif sel_way == '批量浏览':
        start_num = bar_ct.slider('请选择开始题号', 1, 1842, 1, on_change=order_b)
        cnt = bar_ct.number_input('请选择题目数量', value=50)
        num_id = [start_num + i for i in range(0, cnt)]

    if type(num_id) == int:
        j = df.loc[df['序号'] == num_id].index[0]
        _sel_2 = df['试题题干'][j]
        st.markdown(f'<font size=3 color=darkblue><b>{df['试题类型'][j]}题</b></font>'
                    f'<font size=3 color=gray>【题库序号{num_id}】</font>', unsafe_allow_html=True)
        for z in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            if df[z][j] != "":
                _sel_2 = _sel_2 + '\n' + z + '. ' + str(df[z][j])
        st.text(_sel_2)
        st.markdown('</br>', unsafe_allow_html=True)
        st.caption(f'正确答案：{df['答案'][j]}')
        st.divider()
    else:
        for i in num_id:
            j = df.loc[df['序号'] == i].index[0]
            _sel_2 = df['试题题干'][j]
            st.markdown(f'<font size=3 color=darkblue><b>{df['试题类型'][j]}题</b></font>'
                        f'<font size=3 color=gray>【题库序号{i}】</font>', unsafe_allow_html=True)
            for z in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                if df[z][j] != "":
                    _sel_2 = _sel_2 + '\n' + z + '. ' + str(df[z][j])
            st.text(_sel_2)
            st.markdown('</br>', unsafe_allow_html=True)
            st.caption(f'正确答案：{df['答案'][j]}')
            st.divider()

    if st.button('下一题', icon='⤵️'):
        st.session_state.numstep += 1
        st.rerun()


    st.markdown('</br>', unsafe_allow_html=True)
    st.markdown('</br>', unsafe_allow_html=True)


if __name__ == '__main__':
    # init_set(hide=True)     # 初始化设置
    main_page(st)
