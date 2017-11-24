#!/usr/local/bin/python3
import xml.etree.ElementTree as ET

content = ""
wordslist = []
indexlist = []
notindexlist = []
grouplist = []
cacllist = []

ufc_name = "ufc_cbankstageunitstock"
#ufc_index = "ufc_idx_cbankstageunitstock"
ufc_index = "ufc_idx_cbankstageunitstock_generatestage"

def get_indexs(filepath):
    if filepath.count('\\') > 0:
        ufc_name = filepath.split('\\')[-1].split('.')[0]
    else:
        ufc_name = filepath.split('.')[0]

    #tree = ET.parse(ufc_name + ".uftstructure")
    tree = ET.parse(filepath)
    root = tree.getroot()

    for child in root.findall("./indexs"):
        indexlist.append(child.get("name"))

    return indexlist

def get_words(filepath):
    if filepath.count('\\') > 0:
        ufc_name = filepath.split('\\')[-1].split('.')[0]
    else:
        ufc_name = filepath.split('.')[0]

    #tree = ET.parse(ufc_name + ".uftstructure")
    tree = ET.parse(filepath)
    root = tree.getroot()

    for child in root.findall("./properties"):
        wordslist.append(child.get("id"))

    return wordslist

if __name__ == "__main__":
    print("main begin")
    out_text = get_indexs("F:\\projects\\gene_sum\\ufc_cbankstageunitstock.uftstructure")
    out_text1 = get_words("F:\\projects\\gene_sum\\ufc_cbankstageunitstock.uftstructure")
    print(out_text)
    print(out_text1)