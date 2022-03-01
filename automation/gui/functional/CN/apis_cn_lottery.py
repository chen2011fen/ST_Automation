import json
from os import path


class ReadLottery:
    # 讀取檔案，把每條api資料依序存入apis清單
    def _read_file(self):
        apis = list()
        filename = './CN/api_tcgdemov3.txt'
        if path.isfile(filename):
            with open(filename, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                apis += data
        else:
            print(f'無搜尋到檔案 {filename}')
            return None
        return apis

    # 依序將彩種名稱、gamecode存入對應彩種分類的dict，Combobox標籤值也是用這個function回傳的參數。
    def process_cn_lottery(self):
        apis = self._read_file()

        ssc = list()
        lhc = list()
        pcb = list()
        eleven_5 = list()
        lf = list()
        pk10 = list()
        k3 = list()
        keno = list()

        for api in apis:
            group_code = api['gameGroupCode']
            lotto_name = api['remark']
            game_code = api['gameCode']

            if group_code == 'SSC':
                ssc.append(lotto_name + ' (' + game_code + ')')
            elif group_code == 'LHC':
                lhc.append(lotto_name + ' (' + game_code + ')')
            elif group_code == 'PCB':
                pcb.append(lotto_name + ' (' + game_code + ')')
            elif group_code == '11X5':
                eleven_5.append(lotto_name + ' (' + game_code + ')')
            elif group_code == 'LF':
                lf.append(lotto_name + ' (' + game_code + ')')
            elif group_code == 'PK10':
                pk10.append(lotto_name + ' (' + game_code + ')')
            elif group_code == 'K3':
                k3.append(lotto_name + ' (' + game_code + ')')
            elif group_code == 'KENO':
                keno.append(lotto_name + ' (' + game_code + ')')

        return ssc, lhc, pcb, eleven_5, lf, pk10, k3, keno
