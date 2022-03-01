from os import path
from re import search


# 讀取檔案，把每條api資料依序存入apis清單
def read_file():
    apis = list()
    filename = './VN/api_gi8.txt'
    if path.isfile(filename):
        with open(filename, "r", encoding='utf-8') as f:
            for line in f:
                string = line.strip().replace('\ufeff', '').split('},{')
                apis += string
        return apis
    else:
        print('無搜尋到', filename)
        return None


# 依序將彩種名稱、gamecode存入對應彩種分類的dict
def pattern_name(apis):
    vnc = dict()
    lao = dict()
    mas = dict()
    thai = dict()
    dial = dict()
    stock = dict()
    other = dict()

    # 截取gamecode、彩種名稱
    pattern_id = '"gameId":\d+'
    pattern_code = '"gameCode":".*","remark"'
    pattern_lotto = '"remark":".*","numero"'

    for api in apis:
        match_id = search(pattern_id, api)
        match_code = search(pattern_code, api)
        match_lotto = search(pattern_lotto, api)

        id = match_id.group(0)
        id = id.replace(id[:9], '')
        id = int(id)

        gamecode = match_code.group(0)
        gamecode = gamecode.replace(gamecode[:12], '')
        gamecode = gamecode.replace(gamecode[-10:], '')
        gamecode = gamecode.swapcase()

        lotto_name = match_lotto.group(0)
        lotto_name = lotto_name.replace(lotto_name[:10], '')
        lotto_name = lotto_name.replace(lotto_name[-10:], '')

        if 'VNC' in api:
            vnc[lotto_name] = id
            vnc[id] = gamecode
        elif 'LAO' in api:
            lao[lotto_name] = id
            lao[id] = gamecode
        elif 'MAS' in api:
            mas[lotto_name] = id
            mas[id] = gamecode.replace(gamecode[-1:], '')
        elif 'THAI' in api:
            thai[lotto_name] = id
            thai[id] = gamecode
        elif '"gameGroupCode":"STOCK"' in api:
            stock[lotto_name] = id
            stock[id] = gamecode
        elif 'SGC' in api:
            other[lotto_name] = id
            gamecode = gamecode.replace(gamecode[:1], '')
            other[id] = gamecode.replace(gamecode[-1:], '')
        elif 'TWC' in api:
            other[lotto_name] = id
            gamecode = gamecode.replace(gamecode[:1], '')
            other[id] = gamecode.replace(gamecode[-1:], '')
        elif 'PK10' or 'K3' in api:
            dial[lotto_name] = id
            dial[id] = gamecode

    return vnc, lao, mas, thai, dial, stock, other


# 放進彩種分類、彩種名稱，回傳出相對應的gamecode
def lotto_to_gamecode(lotto_type, lotto_name):
    # 取出所有彩種分類的dict
    vnc, lao, mas, thai, dial, stock, other = pattern_name(read_file())
    switcher = dict()

    # 判斷選擇的彩種分類，比對對應的dict
    if lotto_type == '越南彩':
        switcher = vnc
    elif lotto_type == '老挝彩':
        switcher = lao
    elif lotto_type == '外國彩':
        switcher = mas
    elif lotto_type == '大泰彩':
        switcher = thai
    elif lotto_type == '快彩':
        switcher = dial
    elif lotto_type == '股票彩':
        switcher = stock
    elif lotto_type == '其它':
        switcher = other

    # 放進彩種名稱，會顯示出對應的gameid，用id去尋找gamename，執行對應的function
    id = switcher.get(lotto_name, lambda: "Invalid lotto name")
    func = switcher.get(id, lambda: "Invalid lotto id")
    return eval('gi8.'+func+'()')
    # print(eval('gi8.'+func+'()'))
