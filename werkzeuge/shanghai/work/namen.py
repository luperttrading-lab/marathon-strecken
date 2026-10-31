# Straßen- und Ortsnamen in Pinyin ohne Töne, in der Schreibweise der Reiseführer (Nanjing Dong Lu, Huaihai Zhong Lu): Grundname
# zusammen, Richtung und „Lu“ (Straße) getrennt, Dong/Xi/Nan/Bei/Zhong = Ost/West/Süd/Nord/Mitte, Yi/Er = 1./2. Abschnitt, Dadao =
# Allee. Auf den Schildern in Shanghai steht der Name in Zeichen und darunter die Umschrift, meist als „Nanjing Rd. (E)“; der
# Streckenplan des Veranstalters schreibt „East Nanjing Rd.“. Zeichen stehen in strassen.json und in der Übergabe. Gegengelesen mit
# name:en in OSM und dem Plan (OSM schreibt „Zhizhaoju Road“, der Plan „Zhizaoju Rd.“; 制造局 = zhizaoju).
STRASSEN = {
    "中山东一路": "Zhongshan Dong Yi Lu", "中山东二路": "Zhongshan Dong Er Lu", "新开河路": "Xinkaihe Lu", "人民路": "Renmin Lu",
    "河南南路": "Henan Nan Lu", "河南中路": "Henan Zhong Lu", "南京路步行街": "Nanjing Dong Lu", "南京东路": "Nanjing Dong Lu",
    "湖北路": "Hubei Lu", "九江路": "Jiujiang Lu", "南京西路": "Nanjing Xi Lu", "华山路": "Huashan Lu", "常熟路": "Changshu Lu",
    "淮海中路": "Huaihai Zhong Lu", "马当路": "Madang Lu", "兴业路": "Xingye Lu", "黄陂南路": "Huangpi Nan Lu", "湖滨路": "Hubin Lu",
    "济南路": "Jinan Lu", "自忠路": "Zizhong Lu", "西藏南路": "Xizang Nan Lu", "高雄路": "Gaoxiong Lu", "制造局路": "Zhizaoju Lu",
    "龙华东路": "Longhua Dong Lu", "半淞园路": "Bansongyuan Lu", "望达路": "Wangda Lu", "苗江路": "Miaojiang Lu", "外马路": "Waima Lu",
    "陆家浜路": "Lujiabang Lu", "富润路": "Furun Lu", "江滨路": "Jiangbin Lu", "瑞宁路": "Ruining Lu", "龙腾大道": "Longteng Dadao",
    "瑞江路": "Ruijiang Lu", "龙恒东路": "Longheng Dong Lu", "云锦路": "Yunjin Lu", "宛平南路": "Wanping Nan Lu", "龙华路": "Longhua Lu",
    "华容路": "Huarong Lu", "龙华西路": "Longhua Xi Lu", "中山南二路": "Zhongshan Nan Er Lu",
}
# Straßenviertel (Jiedao, OSM admin_level 8) und Bezirke (Qu, admin_level 6)
ORTE = {
    "外滩街道": "Waitan", "小东门街道": "Xiaodongmen", "豫园街道": "Yuyuan", "南京东路街道": "Nanjing Dong Lu", "南京西路街道": "Nanjing Xi Lu",
    "石门二路街道": "Shimen Er Lu", "静安寺街道": "Jing'ansi", "湖南路街道": "Hunan Lu", "瑞金二路街道": "Ruijin Er Lu",
    "淮海中路街道": "Huaihai Zhong Lu", "老西门街道": "Laoximen", "半淞园路街道": "Bansongyuan Lu", "五里桥街道": "Wuliqiao",
    "斜土路街道": "Xietu Lu", "龙华街道": "Longhua", "长桥街道": "Changqiao", "枫林路街道": "Fenglin Lu", "漕河泾街道": "Caohejing",
    "徐家汇街道": "Xujiahui", "天平路街道": "Tianping Lu",
    "黄浦区": "Huangpu", "静安区": "Jing'an", "徐汇区": "Xuhui", "长宁区": "Changning", "浦东新区": "Pudong",
}
def name(n, prefix=""):
    n = (n or "").strip()
    if n and n not in STRASSEN: raise KeyError(f"Straße ohne Umschrift: {n}")
    return STRASSEN.get(n, "")
def ort(n):
    n = (n or "").strip()
    if n and n not in ORTE: raise KeyError(f"Ort ohne Umschrift: {n}")
    return ORTE.get(n, "")
# Viele Straßenviertel heißen nach einer Straße (南京东路街道, 半淞园路街道 …); „Xizang Nan Lu · Bansongyuan Lu“ läse sich wie zwei Straßen.
# Für sie steht deshalb der Bezirk (Huangpu, Jing'an, Xuhui), für die übrigen der Name des Viertels (Waitan, Jing'ansi, Longhua …).
def viertel(jiedao, bezirk):
    j = (jiedao or "").strip()
    if j.endswith("路街道") or not j: return ort(bezirk)
    return ort(j)
