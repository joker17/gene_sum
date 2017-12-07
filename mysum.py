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

def generate_sum(filepath, cacllist, index_name = ''):
    print('in param')
    print(cacllist)
    ufc_index = "ufc_idx_cbankstageunitstock_generatestage"

    if filepath.count('\\') > 0:
        ufc_name = filepath.split('\\')[-1].split('.')[0]
    elif filepath.count('//') > 0:
        ufc_name = filepath.split('//')[-1].split('.')[0]
    elif filepath.count('/') > 0:
        ufc_name = filepath.split('/')[-1].split('.')[0]
    else:
        ufc_name = filepath.split('.')[0]
    if len(index_name) > 0:
        ufc_index = index_name

    #tree = ET.parse(ufc_name + ".uftstructure")
    tree = ET.parse(filepath)
    root = tree.getroot()

    for child in root.findall("./properties"):
        wordslist.append(child.get("id"))

    for child in root.findall("./indexs"):
        if child.get("name") == ufc_index:
            for tmpnode in child.find("./childIndexs"):
                indexlist.append(tmpnode.get("attrname"))
            for tmpnode in child.find("./childIndexs[2]"):
                grouplist.append(tmpnode.get("attrname"))

    def formexp(inlist, exp, del_endstr = "", return_num = 1):
        tmp_indexlist = inlist
        indexstr=""
        count = exp.count("%")
        i = 0
        for tmpword in tmp_indexlist:
            i += 1
            if count == 1:
                indexstr += (exp % (tmpword) )
            elif count == 2:
                indexstr += (exp % (tmpword, tmpword) )
            elif count == 3:
                indexstr += (exp % (tmpword, tmpword, tmpword) )
            if i % return_num == 0:
                indexstr += "\n"
        if len(del_endstr) > 0:
           pos = indexstr.rfind(del_endstr)
           indexstr = indexstr[:pos]
           indexstr += "\n"
        return indexstr


    for aword in wordslist:
        if aword not in indexlist:
            notindexlist.append(aword)

    #cacllist = ["current_amount", "original_cost", "carryover_cost", "original_real_cost", "@carryover_real_cost",
    #            "original_interest_cost", "carryover_interest_cost"]

    content = (
    "[并发遍历记录开始][ufc_cfundmarket." + ufc_name + "(" + ufc_index + ")][\n" 
    "   " + formexp(indexlist, "%s = @%s, ", ",") +
    "][" + formexp(notindexlist, "%s = @%s, ", ",") + "]\n"
    "{\n"
    "\\\\过滤不汇总的数据\n"
    "\\\\to add\n\n"
    "@v_flag = CONST_FLAG_YES;"
    + formexp(notindexlist, "@v1_%s = @%s; ") +
    "\n\n"
    "@v_num +=1;\n"
    "if ("
    + formexp(grouplist, "@v_%s == @%s && ", "&&", 3) +
    ")\n"
    "{\n"
    + formexp(cacllist, "@%s = @%s + @v_%s; ") +
    "}\n"
    "if ( @v_num != 1 \n"
    " && (" + formexp(grouplist, "@v_%s != @%s || ", "||", 3) + ") )"
    "{\n[插入记录][" + ufc_name + "][\n"
    + formexp(wordslist, "@%s = @v_%s, ", ",") +
    "]\n"
    "@v_num = 1;\n"
    + formexp(wordslist, "@%s = @v1_%s;") +
    "}\n\n\n"
    + formexp(wordslist, "@v_%s = @%s;") +
    "\n"
    "}\n"
    "[并发遍历记录结束]\n\n\n"
    "if (@v_num > 0 && @v_flag == CONST_FLAG_YES)"
    "{\n"
    "[插入记录][" + ufc_name + "][\n"
    + formexp(wordslist, "@%s = @v_%s, ", ",") +
    "]\n"
    "}\n"
    )
    return content

if __name__ == "__main__":
    print("main begin")
    out_text = generate_sum("F:\\projects\\gene_sum\\ufc_cbankstageunitstock.uftstructure", "ufc_idx_cbankstageunitstock")
    print(out_text)