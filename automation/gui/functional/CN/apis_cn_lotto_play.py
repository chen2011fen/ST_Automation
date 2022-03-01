import json
from os import path


class ReadPlay:
    def _read_file(self, filename):
        apis = list()
        if path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                apis += data
        else:
            print(f'無搜尋到檔案 {filename}')
            return None
        return apis

    def process_k3_official(self):
        apis = self._read_file('./CN/api_k3_official_playcode.txt')

        # 官方模式第一級玩法的玩法名稱
        k3_official = list()
        # 陣列名稱是用第一層的玩法名稱取的(playcode)
        sum_k3 = list()
        same_3_k3 = list()
        different_3_k3 = list()
        even_3_k3 = list()
        same_2_k3 = list()
        different_2_k3 = list()
        fun_k3 = list()
        any_code_k3 = list()
        span_k3 = list()
        show_hand_k3 = list()

        # 抓Lott的api資料，覆蓋到apis
        for api in apis:
            if api['prizeModeId'] == 1:
                apis = api['playMenuGroups']
            else:
                continue

        for api in apis:
            play_menus = list()

            # 把第一層玩法名稱(playCode)加入到list
            play_code = api['playCode']
            k3_official.append(play_code)

            # 抓每筆裡的playMenus
            play_menus += api['playMenus']

            for menu in play_menus:
                if play_code == 'Sum_K3':
                    sum_k3.append(menu['playCode'].lower())
                elif play_code == 'Same_3_K3':
                    same_3_k3.append(menu['playCode'].lower())
                elif play_code == 'Different_3_K3':
                    different_3_k3.append(menu['playCode'].lower())
                elif play_code == 'Even_3_K3':
                    even_3_k3.append(menu['playCode'].lower())
                elif play_code == 'Same_2_K3':
                    same_2_k3.append(menu['playCode'].lower())
                elif play_code == 'Different_2_K3':
                    different_2_k3.append(menu['playCode'].lower())
                elif play_code == 'Fun_K3':
                    fun_k3.append(menu['playCode'].lower())
                elif play_code == 'Any_Code_K3':
                    any_code_k3.append(menu['playCode'].lower())
                elif play_code == 'Span_K3':
                    span_k3.append(menu['playCode'].lower())
                elif play_code == 'Show_Hand_K3':
                    show_hand_k3.append(menu['playCode'].lower())

        return k3_official, sum_k3, same_3_k3, different_3_k3, even_3_k3, same_2_k3, different_2_k3, fun_k3, any_code_k3, span_k3, show_hand_k3
