import streamlit as st
from fun import *
from streamlit_option_menu import option_menu
from Parsing_pubmed import *
import pandas as pd

def download_pubmed_online():
    st.title("Pubmed searching(From Internet)")
    # 添加文本輸入欄位
    text_input = st.text_input("Query：")

    # 添加數字輸入欄位
    number_input = st.number_input("Maximum_num：", step=1, format="%d")

    submit_button = st.button("submit")
    if submit_button :
        # 檢查是否有輸入
        if text_input and number_input:
            Download(text_input,number_input)

        else:
            st.warning("請填寫兩個欄位以提交。")
    

def light_yellow(input,match_string):
    temp = input 
    temp2 = temp.replace(match_string, f"<span style='background-color: yellow'>{match_string}</span>")
    st.markdown(temp2,unsafe_allow_html=True)


def meta_data(input,case):
    st.markdown("#### **Metadata**")
    if case == 1:
            metadata_text = (
            "<div style='display: inline-block; white-space: nowrap; font-weight: bold;'>char           : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>char(no_space) : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>words          : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>sen            : </div>{}"
        ).format(input["char"], input["char(no_space)"], input["words"], input["sen"])

    else :
        metadata_text = (
            "<div style='display: inline-block; white-space: nowrap; font-weight: bold;'>char           : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>char(no_space) : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>words          : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>sen            : </div>{}"
            "<div style='display: inline-block; white-space: nowrap; margin-left: 1em; font-weight: bold;'>matching num            : </div>{}"
        ).format(input["char"], input["char(no_space)"], input["words"], input["sen"],input["matching_num"])

    st.markdown(metadata_text, unsafe_allow_html=True)

def show_article(article,input_string=''):
    st.markdown("## **PMID**")
    light_yellow(article["PMID"],input_string)
    st.markdown("## **Title**")
    light_yellow(article["ArticleTitle"],input_string)
    st.markdown("## **Date**")
    light_yellow(article["DateRevised"],input_string)
    st.markdown("## **Authors**")
    temp = " | ".join(article["Authors"])
    light_yellow(temp,input_string)
    st.markdown("## **Abstract**")
    light_yellow(article['AbstractText'],input_string)
    temp = article['AbstractText']
    if input_string == '' :
        meta_data(article,1)
    else: 
        meta_data(article,0)
    st.markdown("---")
    return

def analysis_pubmed_module() :
    st.title("Pubmed searching")
    input_string = st.text_area("")
    if st.button("Analysis"):
        if input_string:
            result = parsing_all(input_string)
            if len(result) == 0 :
                st.write("## **No result**")
            else :
                getting_matching_value_print(result)
                st.image("bar_chart.png", caption='統計圖表', use_column_width=True)
                df = pd.DataFrame(result)
                selected_columns = ['PMID', 'char', 'char(no_space)', 'words', 'matching_num']
                selected_df = df[selected_columns]
                # 重新设置行索引从1开始
                selected_df.index = range(1, len(df) + 1)

                # 将行索引列名更改为"Rank"

                # 使用Markdown来显示DataFrame
                st.markdown(selected_df.style.set_table_styles([{
                    'selector': 'table',
                    'props': [('text-align', 'center')]
                }]).render(), unsafe_allow_html=True)
            for article in result :
                show_article(article,input_string)
        else:
            st.warning("请输入文本以进行分析")

def analysis_twitter_module():
    st.title("Twitter searching")
    input_string = st.text_area("")
    if st.button("Analysis"):
        if input_string:
            result = parsing_all_twitter(input_string)
            if len(result) == 0 :
                st.write("## **No result**")
            else :
                getting_matching_value_print(result)
                st.image("bar_chart.png", caption='統計圖表', use_column_width=True)
            for article in result :
                st.markdown("## **ID**")
                light_yellow(article["ID"],input_string)
                st.markdown("## **Date**")
                light_yellow(article["Date"],input_string)
                st.markdown("## **Authors**")
                light_yellow(article["Authors_id"],input_string)
                st.markdown("## **Text**")
                light_yellow(article['Text'],input_string)
                meta_data(article)
                st.markdown("---")
        else:
            st.warning("请输入文本以进行分析")

def uploading_module(file_path):
    st.title("Upload")
    uploaded_file = None
    if file_path == 'xml/' :
        uploaded_file = st.file_uploader("上传文件", type=[".xml"])
    else :
        uploaded_file = st.file_uploader("上传文件", type=[".json"])
    if uploaded_file is not None:
        # 处理上传的文件
        data = uploaded_file.read()
        file_name = file_path + 'X'+uploaded_file.name
        with open(file_name, "wb") as xml_file:
            xml_file.write(data)
        uploaded_file.close()
        extract_pubmed_info(file_name)
    st.markdown("---")


def deleting_module(file_path) : 
    ##處理刪除的文件    
    file_list = os.listdir(file_path) 
    st.title("File list")
    user_input = st.number_input("PMID", step=1)
    file_name = "X" + str(user_input) + '.xml'
    if st.button("Display Content"):
        if file_name in file_list:
            selected_file_name = file_name
            temp = selected_file_name.split(".")
            temp1 = temp[0] + '.pkl'
            # 读取和显示选定的文件内容
            with open(os.path.join("xml_pickle", temp1), "rb") as selected_file:
                file_contents = pickle.load(selected_file)
                show_article(file_contents)
            # 添加一个按钮以删除选定的文章
        else:
            st.error("該PMID不存在")


with st.sidebar:
    selected = option_menu("", ["Pubmed_searching", 'Pubmed_file' ,"Twitter_searching", "Twitter_file","Download_pubmed"], 
        icons=['house', 'upload' , 'house' , 'upload' ,'upload'], menu_icon="cast", default_index=1,
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "Blue"},
    })


if selected == "Pubmed_searching" :
    analysis_pubmed_module()
elif selected == "Pubmed_file":
    uploading_module("xml/")
    deleting_module("xml/")
elif selected == "Twitter_file":
    uploading_module("json/")
    deleting_module("json/")
elif selected == "Twitter_searching" :
    analysis_twitter_module()
elif selected == "Download_pubmed":
    download_pubmed_online()

    

# 4. Manual Item Selection
if st.session_state.get('switch_button'):
    print("In")
    st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None





    

# Streamlit UI