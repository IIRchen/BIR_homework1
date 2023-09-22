# %%
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys
import re
import nltk
import string
from nltk.tokenize import sent_tokenize, word_tokenize
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
def dick(hi):
    return hi

#
def xml_parser(xml_file_path):
    try :
    # 解析XML文件
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # 查找PMID元素，如果找不到就設置為"default"
        PMID_element = root.find(".//PMID")
        PMID_text = PMID_element.text.strip() if PMID_element is not None else "default"

        # 查找ArticleTitle元素，如果找不到就設置為"default"
        article_title_element = root.find(".//ArticleTitle")
        article_title = article_title_element.text.strip() if article_title_element is not None else "default"

        # 查找DateRevised元素，如果找不到就設置為"default"
        date_revised_element = root.find(".//MedlineCitation/DateRevised/Year")
        date_revised_year = date_revised_element.text.strip() if date_revised_element is not None else "default"

        date_revised_element = root.find(".//MedlineCitation/DateRevised/Month")
        date_revised_month = date_revised_element.text.strip() if date_revised_element is not None else "default"

        date_revised_element = root.find(".//MedlineCitation/DateRevised/Day")
        date_revised_day = date_revised_element.text.strip() if date_revised_element is not None else "default"

        # 如果找不到DateRevised元素，設置date_revised為"default"
        if date_revised_year == "default" or date_revised_month == "default" or date_revised_day == "default":
            date_revised = "default"
        else:
            date_revised = f"{date_revised_year}/{date_revised_month}/{date_revised_day}"

        # 查找Abstract元素，如果找不到就設置為"default"
        abstract_text_element = root.find(".//Abstract")
        if abstract_text_element is not None:
            abstract_text = ET.tostring(abstract_text_element, encoding='utf-8', method='xml').decode('utf-8')
            abstract_text = re.sub(r'<CopyrightInformation>.*?</CopyrightInformation>', '', abstract_text)
            abstract_text = re.sub(r'<.*?>', ' ', abstract_text)
        else:
            abstract_text = "default"

        authors = []
        author_elements = root.findall(".//Author")
        for author_element in author_elements:
            last_name_element = author_element.find(".//LastName")
            first_name_element = author_element.find(".//ForeName")
            last_name = last_name_element.text.strip() if last_name_element is not None else 'None'
            first_name = first_name_element.text.strip() if first_name_element is not None else ''
            authors.append(f"{last_name}, {first_name}")

        pubmed_data = {
            'PMID' : PMID_text,
            'ArticleTitle': article_title,
            'DateRevised': date_revised,
            'AbstractText': abstract_text,
            'Authors': authors
        }
        return pubmed_data
    
    except Exception as e:
        print(f"提取信息时出现错误：{str(e)}")
        pubmed_data = {
            'PMID' : "error",
            'ArticleTitle': "error",
            'DateRevised': "error",
            'AbstractText': "error",
            'Authors': ["error"]
        }
        return pubmed_data
#  %%
#根據xml　檔案進行解析
def extract_pubmed_info(xml_file_path):
    xml_pickle_path = 'xml_pickle/'
    pubmed_data = xml_parser(xml_file_path)
    another = text_statistics(pubmed_data["AbstractText"])
    pubmed_data = {**pubmed_data, **another}
    with open(xml_pickle_path+'X'+str(pubmed_data["PMID"])+".pkl",'wb') as file :
            pickle.dump(pubmed_data,file)
    return pubmed_data

def  extract_twitter_info(twitter_file_path):
    with open(twitter_file_path, 'r') as json_file:
        # 使用json.load加载JSON数据
        data = json.load(json_file)

    twitter_data = {
            'ID': data[0]['ID'],
            'Date': data[0]['date'],
            'Text': data[0]['Text'],
            'Authors_id': str(data[0]['Author ID'])
        }
    another = text_statistics(twitter_data["Text"])
    twitter_data = {**twitter_data, **another}
    return twitter_data



# %%

# %%

#nltk.download('punkt')
def text_statistics(text):
    ##確認NLTK是否安裝
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        # 如果出現 LookupError，表示 'punkt' 尚未下載
        print("punkt 資源未安裝，正在安裝...")
        nltk.download('punkt')
        print("punkt 資源安裝完成")
    else:
        # 如果沒有出現 LookupError，表示 'punkt' 已經安裝
        pass
    # 1. 計算字元數
    
    if nltk.data.find('tokenizers/punkt') is  None :
        nltk.download('punkt')
    char_count = len(text)

    # 2. 計算不含空白的字元數
    temp = text
    char_count_no_spaces = len(temp.replace(" ", ""))

    # 3. 計算詞數
    text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text_without_punctuation)
    word_count = len(words)

    # 4. 計算句數
    sentences = sent_tokenize(text)
    sentence_count = len(sentences)
    print(sentences)

    return {
        "char": char_count,
        "char(no_space)": char_count_no_spaces,
        "words": word_count,
        "sen": sentence_count
    }

# 測試函數


# %%
def find_dicts_containing_string(search_string):
    # 用來存儲包含搜索字符串的字典的列表

    # parse 所有的pickle檔出來
    list_of_dicts = []
    temp = os.listdir("xml_pickle")
    xml_path = ["xml_pickle/" + element for element in temp]
    for file_name in xml_path:
        with open(file_name,'rb') as file :
            temp_dict = pickle.load(file)
            list_of_dicts.append(temp_dict)

    matching_dicts = []
    # 遍歷列表中的每個字典，檢查是否包含搜索字符串
    for dictionary in list_of_dicts:
        if dictionary is not None :
            for key in ["ArticleTitle",'DateRevised','AbstractText','Authors','PMID'] :
                if search_string in dictionary.get(key, ""):
                    matching_dicts.append(dictionary)
                    break
    
    for dictionary in matching_dicts:
        count = 0
        for key in ["ArticleTitle",'DateRevised','AbstractText','Authors','PMID']  :
            count += dictionary[key].count(search_string)
        dictionary["matching_num"] = count
        
    return matching_dicts

def find_dicts_containing_string_twitter(list_of_dicts, search_string):
    # 用來存儲包含搜索字符串的字典的列表
    matching_dicts = []

    # 遍歷列表中的每個字典，檢查是否包含搜索字符串
    for dictionary in list_of_dicts:
        if dictionary is not None :
            for key in ["ID",'Date','Text','Authors_id'] :
                if search_string in dictionary.get(key, ""):
                    matching_dicts.append(dictionary)
                    break
            
    return matching_dicts
# %%
def find_dicts_containing_string_num(list_of_dicts, search_string):
    
    return_dict = list(list_of_dicts)
    

    return return_dict
def find_dicts_containing_string_num_twitter(list_of_dicts, search_string):

    return_dict = list(list_of_dicts)
    for dictionary in return_dict:
        count = 0
        for key in ["ID",'Date','Text','Authors_id']  :
            count += dictionary[key].count(search_string)
        dictionary["matching_num"] = count

    return return_dict

# %%
def sort_by_num(dictionary):
    return dictionary["matching_num"]


# %%



def parsing_all(match_string):
    

    matching_dicts = find_dicts_containing_string(match_string)
    sorted_list = sorted(matching_dicts, key=sort_by_num , reverse= True)

    return  sorted_list

def parsing_all_twitter(match_string):
    temp = os.listdir("json")
    json_path = ["json/" + element for element in temp]
    Article_list = []
    for file_name in json_path:
        article = extract_twitter_info(file_name)
        Article_list.append(article)

    matching_dicts = find_dicts_containing_string_twitter(Article_list,match_string)
    matching_dicts_and_num = find_dicts_containing_string_num_twitter(matching_dicts,match_string)
    sorted_list = sorted(matching_dicts_and_num, key=sort_by_num , reverse= True)
    return  sorted_list

def getting_matching_value_print(list_of_dicts):
    temp_list = []
    for k in list_of_dicts:
        temp_list.append(k["matching_num"])

    plt.bar(range(len(temp_list)), temp_list)
    plt.xticks([])  # 移除X轴的刻度
    plt.xlabel('File_rank')
    plt.ylabel('Frequency')
    plt.savefig('bar_chart.png')

    return



