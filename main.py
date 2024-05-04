import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
from func import Explorer

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


exp = Explorer('data/ChicagoCrime2022.csv')
line_plot = exp.show_month_cnt()
pie_plot = exp.type_distribution()
map_ = exp.map_chi()

st.header("2022年芝加哥犯罪数据分析")
st.subheader("")
st.subheader("1.数据展示")
st.write(exp.data.head(10))
st.text(exp.info)
st.subheader("2.犯罪类型分析")
st.write(pie_plot)
st.subheader("3.犯罪数量月份数据")
st.pyplot(line_plot)
st.subheader("4.犯罪热度地图")
folium_static(map_)