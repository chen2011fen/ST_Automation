from os import path
from os import system
from re import search
from datetime import date
from telebot import TeleBot
from win32api import GetSystemMetrics
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from automation.gui.functional.CN.apis_cn_lottery import ReadLottery
from automation.gui.functional.CN.apis_cn_lotto_play import ReadPlay
from automation.gui.functional.get_test_data import YamlUtil

today = date.today()

API_KEY = '1801571910:AAFyQRgFtIZ6VBawYJxhIYK4bpNMxqHeabk'
bot = TeleBot(API_KEY)

ssc, lhc, pcb, eleven_5, lf, pk10, k3, keno = ReadLottery().process_cn_lottery()
k3_official, sum_k3, same_3_k3, different_3_k3, even_3_k3, same_2_k3, different_2_k3, fun_k3, any_code_k3, span_k3, show_hand_k3 = ReadPlay().process_k3_official()


class Application(tk.Frame):
    def __init__(self, frame):
        # 繼承外框架
        super().__init__(frame)
        self.frame = frame
        self.create_tools()
        self.grid()
        self.combobox_vendor_selected(frame)
        # 路徑計數
        self.count = 1

    def create_tools(self):
        # 選擇測試彩票類型
        tk.Canvas(self, height=5, width=15).grid(column=0, row=0)   # 空白行，當間格
        label_vendor = tk.Label(self, text='測試彩票類型(區域) :')
        label_vendor.grid(column=0, row=1, padx=12, sticky=tk.W)
        self.combobox_vendor = ttk.Combobox(self, state='readonly')
        self.combobox_vendor['values'] = ['VN-gi8', 'CN-tcgdemov3', 'SEA-tcgdemov3']
        self.combobox_vendor.grid(column=0, row=2, padx=15)
        self.combobox_vendor.current(1)

        # 選擇裝置
        tk.Canvas(self, height=5, width=15).grid(column=0, row=3)  # 空白行，當間格
        label_device_type = tk.Label(self, text='裝置類型 :')
        label_device_type.grid(column=0, row=4, padx=12, sticky=tk.W)
        self.combobox_device_type = ttk.Combobox(self, state='readonly')
        self.combobox_device_type['values'] = ['UI', 'H5']
        self.combobox_device_type.grid(column=0, row=5, padx=15)
        self.combobox_device_type.current(0)

        # 選擇模版
        tk.Canvas(self, height=5, width=15).grid(column=0, row=6)  # 空白行，當間格
        label_template = tk.Label(self, text='模版 :')
        label_template.grid(column=0, row=7, padx=12, sticky=tk.W)
        self.combobox_template = ttk.Combobox(self, state='readonly')
        self.combobox_template.grid(column=0, row=8, padx=15)

        # 選擇彩種分類
        tk.Canvas(self, height=5, width=15).grid(column=0, row=9)  # 空白行，當間格
        label_lotto_type = tk.Label(self, text='彩票分類 :')
        label_lotto_type.grid(column=0, row=10, padx=12, sticky=tk.W)
        self.combobox_lotto_type = ttk.Combobox(self, state='readonly')
        self.combobox_lotto_type.grid(column=0, row=11, padx=15)

        # 選擇彩種(預設tcgdemov3)
        temp_lotto = list()
        tk.Canvas(self, height=5, width=15).grid(column=0, row=12)  # 空白行，當間格
        label_lotto = tk.Label(self, text='彩種 :')
        label_lotto.grid(column=0, row=13, padx=12, sticky=tk.W)
        self.combobox_lotto = ttk.Combobox(self, state='readonly')
        self.combobox_lotto.grid(column=0, row=14, padx=15)

        # 選擇模式
        tk.Canvas(self, height=5, width=15).grid(column=0, row=15)  # 空白行，當間格
        label_mode = tk.Label(self, text='模式 :')
        label_mode.grid(column=0, row=16, padx=12, sticky=tk.W)
        self.combobox_mode = ttk.Combobox(self, state='readonly')
        self.combobox_mode.grid(column=0, row=17, padx=15)

        # 選擇玩法
        tk.Canvas(self, height=5, width=15).grid(column=0, row=18)  # 空白行，當間格
        label_play = tk.Label(self, text='選擇玩法 :')
        label_play.grid(column=0, row=19, padx=12, sticky=tk.W)
        self.combobox_play_first = ttk.Combobox(self, state='readonly')
        self.combobox_play_first.grid(column=0, row=20, padx=15)

        # 選擇直選、組選、趣味
        tk.Canvas(self, height=5, width=15).grid(column=0, row=21)  # 空白行，當間格
        self.radioValue = tk.IntVar()
        self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0)
        self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
        self.radio_direct.select()
        self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1)
        self.radio_group.grid(column=0, row=22, padx=12)
        self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2)
        self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
        # 二階玩法
        self.combobox_play_second = ttk.Combobox(self, state='readonly')
        # self.combobox_play_second['values'] = ['直選120', '直選60']
        self.combobox_play_second.grid(column=0, row=23, padx=15)
        # self.combobox_play_second.current(0)

        # 投注模式
        tk.Canvas(self, height=5, width=15).grid(column=0, row=25)  # 空白行，當間格
        label_betting_method = tk.Label(self, text='投注模式')
        label_betting_method.grid(column=0, row=26, padx=12, sticky=tk.W)
        self.combobox_betting_method = ttk.Combobox(self, state='readonly')
        # self.combobox_play_first['values'] = ['']
        self.combobox_betting_method.grid(column=0, row=27, padx=15)
        # self.combobox_play_first.current(0)

        # 輸入帳號測試帳號
        label_account = tk.Label(self, text='測試帳號')
        label_password = tk.Label(self, text='         密碼')
        label_account.grid(column=1, row=1, padx=17, sticky=tk.W)
        label_password.grid(column=1, row=1, padx=17)
        self.textbox_account = tk.Entry(self, show=None, width=11)
        self.textbox_password = tk.Entry(self, show=None, width=11)
        self.textbox_account.grid(column=1, row=2, padx=20, sticky=tk.W)
        self.textbox_password.grid(column=1, row=2, padx=20, sticky=tk.E)

        # 單注投注額
        label_bet = tk.Label(self, text='單注投注額 (預設為1)')
        label_bet.grid(column=1, row=4, padx=17, sticky=tk.W)
        self.textbox_bet = tk.Entry(self, show=None, width=23)
        self.textbox_bet.grid(column=1, row=5, padx=20, sticky=tk.W)

        # 抽水值
        label_pump = tk.Label(self, text='抽水值% (預設為0%)')
        label_pump.grid(column=1, row=7, padx=17, sticky=tk.W)
        self.textbox_pump = tk.Entry(self, show=None, width=23)
        self.textbox_pump.grid(column=1, row=8, padx=20, sticky=tk.W)

        # 測試次數
        label_test_time = tk.Label(self, text='測試次數 (預設為1)')
        label_test_time.grid(column=1, row=10, padx=17, sticky=tk.W)
        self.textbox_test_time = tk.Entry(self, show=None, width=23)
        self.textbox_test_time.grid(column=1, row=11, padx=20, sticky=tk.W)

        # 選擇測試類型
        label_test_type = tk.Label(self, text='選擇測試類型')
        label_test_type.grid(column=1, row=13, padx=17, sticky=tk.W)
        self.combobox_test_type = ttk.Combobox(self, state='readonly')
        self.combobox_test_type['values'] = ['驗證所有選號']
        self.combobox_test_type.grid(column=1, row=14, padx=20)
        self.combobox_test_type.current(0)

        # 輸入Telegram id
        label_telegram_id = tk.Label(self, text='輸入Telegram ID (需經轉換)')
        label_telegram_id.grid(column=1, row=16, padx=17, sticky=tk.W)
        self.textbox_telegram_id = tk.Entry(self, show=None, width=23)
        self.textbox_telegram_id.grid(column=1, row=17, padx=20, sticky=tk.W)

        # 執行鈕
        self.btn_execute = tk.Button(self, text='執行測試', font='標楷體', bd=3, width=18, height=2, command=self.exection)
        self.btn_execute.grid(column=1, row=20, rowspan=3, padx=25, sticky=tk.W)

        self.combobox_vendor.bind('<<ComboboxSelected>>', self.combobox_vendor_selected)
        self.combobox_device_type.bind('<<ComboboxSelected>>', self.combobox_device_type_selected)
        self.combobox_lotto_type.bind('<<ComboboxSelected>>', self.combobox_lotto_type_selected)
        self.combobox_lotto.bind('<<ComboboxSelected>>', self.combobox_lotto_selected)
        self.combobox_mode.bind('<<ComboboxSelected>>', self.combobox_mode_selected)
        self.combobox_play_first.bind('<<ComboboxSelected>>', self.combobox_play_first_selected)
        # self.combobox_play_second.bind('<<ComboboxSelected>>', self.combobox_play_second_selected)

    def combobox_vendor_selected(self, event):
        # VN-gi8、SEA-tcgdemov3
        if self.combobox_vendor.current() == 0 or self.combobox_vendor.current() == 2:
            self.combobox_template.configure(state='disable')
            self.combobox_template['values'] = ['']
            self.combobox_template.grid(column=0, row=8, padx=15)
            self.combobox_template.current(0)

            self.combobox_mode.configure(state='disable')
            self.combobox_mode['values'] = ['']
            self.combobox_mode.grid(column=0, row=17, padx=15)
            self.combobox_mode.current(0)

            self.combobox_betting_method.configure(state='readonly')
            self.combobox_betting_method['values'] = ['標準選號', '單式選號', '複式選號']
            self.combobox_betting_method.grid(column=0, row=27, padx=15)
            self.combobox_betting_method.current(0)
        # CN-tcgdemov3
        else:
            self.combobox_template.configure(state='readonly')
            self.combobox_template['values'] = ['t1', 't2', 't3', 'w4', 'w5', 'b1']
            self.combobox_template.grid(column=0, row=8, padx=15)
            self.combobox_template.current(2)

            self.combobox_lotto_type['values'] = ['時時彩 (SSC)', '六合彩 (LHC)', 'PC蛋蛋 (PCB)', '十一選五 (Eleven_Five)', '低頻彩 (LF)', 'PK10 (PK10)', '快三 (K3)', '快樂8 (KENO)']
            self.combobox_lotto_type.current(0)

            self.combobox_mode.configure(state='readonly')
            self.combobox_mode['values'] = ['官方玩法 (Official)', '娛樂城玩法 (Entertainment)']
            self.combobox_mode.grid(column=0, row=17, padx=15)
            self.combobox_mode.current(0)

            self.combobox_betting_method = ttk.Combobox(self, state='disable')
            self.combobox_betting_method['values'] = ['']
            self.combobox_betting_method.grid(column=0, row=27, padx=15)
            self.combobox_betting_method.current(0)

        self.combobox_lotto_type_selected("<<ComboboxSelected>>")

    # 判斷裝置
    def combobox_device_type_selected(self, event):
        if self.combobox_device_type.get() == 'UI':
            self.combobox_template['values'] = ['t1', 't2', 't3', 'w4', 'w5', 'b1']
            self.combobox_template.current(2)
        else:
            self.combobox_template['values'] = ['t1', 't2', 't3', 'h4', 'h5', 'b1']
            self.combobox_template.current(2)

    def combobox_lotto_type_selected(self, event):
        temp_lotto = list()
        #判斷VN-gi8
        if self.combobox_vendor.current() == 0:
            pass
        # 判斷CN-tcgdemov3
        elif self.combobox_vendor.current() == 1:
            # 匯入時時彩彩種
            if self.combobox_lotto_type.current() == 0:
                for n in ssc:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.radioValue = tk.IntVar()
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0)
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_direct.select()
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1)
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2)
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入六合彩彩種
            elif self.combobox_lotto_type.current() == 1:
                for n in lhc:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.combobox_mode['values'] = ['娛樂城玩法 (Entertainment)']
                self.combobox_mode.current(0)
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入PCB28彩種
            elif self.combobox_lotto_type.current() == 2:
                for n in pcb:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.combobox_mode['values'] = ['娛樂城玩法 (Entertainment)']
                self.combobox_mode.current(0)
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入11選5彩種
            elif self.combobox_lotto_type.current() == 3:
                for n in eleven_5:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.radioValue = tk.IntVar()
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0)
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_direct.select()
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1)
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2)
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入低頻彩彩種
            elif self.combobox_lotto_type.current() == 4:
                for n in lf:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.radioValue = tk.IntVar()
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0)
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_direct.select()
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1)
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2)
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入PK10彩種
            elif self.combobox_lotto_type.current() == 5:
                for n in pk10:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入K3彩種
            elif self.combobox_lotto_type.current() == 6:
                for n in k3:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.combobox_play_second['values'] = ['和值']
                self.combobox_play_second.current(0)
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            # 匯入Keno彩種
            elif self.combobox_lotto_type.current() == 7:
                for n in keno:
                    if type(n) == str:
                        temp_lotto.append(n)
                self.combobox_lotto['values'] = temp_lotto
                self.combobox_lotto.current(0)
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
        # 判斷SEA-tcgdemov3
        elif self.combobox_vendor.current() == 2:
            pass
        self.combobox_lotto_selected("<<ComboboxSelected>>")

    def combobox_lotto_selected(self, event):
        # 判斷CN-tcgdemov3
        if self.combobox_vendor.current() == 1:
            if self.combobox_lotto_type.current() == 1 or self.combobox_lotto_type.current() == 2 or self.combobox_lotto_type.current() == 7:
                self.combobox_mode['values'] = ['娛樂城玩法 (Entertainment)']
                self.combobox_mode.current(0)
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
                self.combobox_play_second['values'] = ['']
                self.combobox_play_second.current(0)
            elif self.combobox_lotto.get() == '极速快三' or self.combobox_lotto.get() == '体彩P3P5' or\
                    self.combobox_lotto.get() == '海南四星彩' or self.combobox_lotto.get() == '台湾四星彩' or\
                    self.combobox_lotto.get() == '新加坡万字票' or self.combobox_lotto.get() == '天津时时彩' or\
                    self.combobox_lotto.get() == '天秤二分彩' or self.combobox_lotto.get() == '凤凰分分彩' or\
                    self.combobox_lotto.get() == '全關時時彩' or self.combobox_lotto.get() == '加拿大3.5分彩':
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0)
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1)
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2)
                self.radio_interest.grid(column=0, row=16, padx=12, sticky=tk.E)
                self.combobox_mode['values'] = ['官方玩法 (Official)']
                self.combobox_mode.current(0)
            else:
                self.combobox_mode['values'] = ['官方玩法 (Official)', '娛樂城玩法 (Entertainment)']
                self.combobox_mode.current(0)

        self.combobox_mode_selected("<<ComboboxSelected>>")

    def combobox_mode_selected(self, event):
        # 時時彩
        if self.combobox_lotto_type.current() == 0:
            # 官方
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['五星', '前四', '後四', '前三', '後三', '後二', '定位膽', '不定位', '趣味', '龍虎和', '任選']
                self.combobox_play_first.current(0)
            # 娛樂城
            elif self.combobox_mode.current() == 1:
                self.combobox_play_first['values'] = ['整合', '兩面盤', '第一球', '第二球', '第三球', '第四球', '第五球', '龍虎鬥', '全五中一', '牛牛', '梭哈', '百家樂']
                self.combobox_play_first.current(0)
        # 六合彩
        elif self.combobox_lotto_type.current() == 1:
            # 娛樂城
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['特碼', '兩面', '色波', '特肖', '頭尾數', '合肖', '正碼', '正碼特', '正碼1-6', '連碼', '連肖', '平特肖尾', '自選不中']
                self.combobox_play_first.current(0)
        # PC蛋蛋
        elif self.combobox_lotto_type.current() == 2:
            # 娛樂城
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['整合']
                self.combobox_play_first.current(0)
        # 十一選五
        elif self.combobox_lotto_type.current() == 3:
            # 官方
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['任選', '定單雙', '猜中位', '前三', '前二', '不定位', '定位膽', '任選膽拖']
                self.combobox_play_first.current(0)
            # 娛樂城
            elif self.combobox_mode.current() == 1:
                self.combobox_play_first['values'] = ['兩面', '第一球', '第二球', '第三球', '第四球', '第五球', '任選', '組選', '直選', '龍虎鬥']
                self.combobox_play_first.current(0)
        # 低頻彩
        elif self.combobox_lotto_type.current() == 4:
            # 官方
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['三星', '前二', '後二', '不定位', '大小單雙', '定位膽']
                self.combobox_play_first.current(0)
            # 娛樂城
            elif self.combobox_mode.current() == 1:
                self.combobox_play_first['values'] = ['一字定位', '一字組合', '二字定位', '二字組合', '二字合數', '三字定位', '三字組合', '三字和數', '組選三', '組選六', '跨度']
                self.combobox_play_first.current(0)
        # PK10
        elif self.combobox_lotto_type.current() == 5:
            # 官方
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['猜前一', '猜前二', '猜前三', '猜前四', '猜前五', '定位膽', '猜和值', '大小單雙', '龍虎鬥']
                self.combobox_play_first.current(0)
            # 娛樂城
            elif self.combobox_mode.current() == 1:
                self.combobox_play_first['values'] = ['兩面', '猜和值', '第1-10名', '龍虎鬥', '番攤']
                self.combobox_play_first.current(0)
        # 快三
        elif self.combobox_lotto_type.current() == 6:
            # 官方
            if self.combobox_mode.current() == 0:
                play_list = ['和值', '三同號', '三不同號', '三連號', '二同號', '二不同號', '趣味', '單挑一骰', '跨度', '梭哈']
                for i in range(0, len(play_list)):
                    play_list[i] += f' ({k3_official[i]})'
                self.combobox_play_first['values'] = play_list
                self.combobox_play_first.current(0)
            # 娛樂城
            elif self.combobox_mode.current() == 1:
                self.combobox_play_first['values'] = ['整合', '紅黑組合', '龍虎和', '跨度']
                self.combobox_play_first.current(0)
        # 快樂8
        elif self.combobox_lotto_type.current() == 7:
            # 娛樂城
            if self.combobox_mode.current() == 0:
                self.combobox_play_first['values'] = ['任選', '趣味']
                self.combobox_play_first.current(0)

        # 判斷娛樂城玩法，把直選那些disable
        if self.combobox_lotto_type.current() == 0 or self.combobox_lotto_type.current() == 3 or self.combobox_lotto_type.current() == 4:
            if self.combobox_mode.current() == 1:
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0, state='disable')
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1, state='disable')
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2, state='disable')
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)
            else:
                self.radio_direct = tk.Radiobutton(self, text='直選', variable=self.radioValue, value=0)
                self.radio_direct.grid(column=0, row=22, padx=12, sticky=tk.W)
                self.radio_group = tk.Radiobutton(self, text='組選', variable=self.radioValue, value=1)
                self.radio_group.grid(column=0, row=22, padx=12)
                self.radio_interest = tk.Radiobutton(self, text='趣味', variable=self.radioValue, value=2)
                self.radio_interest.grid(column=0, row=22, padx=12, sticky=tk.E)

        self.combobox_play_first_selected("<<ComboboxSelected>>")

    def combobox_play_first_selected(self, event):
        if self.combobox_vendor.current() == 0:
            pass
        elif self.combobox_vendor.current() == 1:
            # 快三-官方模式
            if self.combobox_lotto_type.current() == 6 and self.combobox_mode.current() == 0:
                if self.combobox_play_first.current() == 0:
                    play_second_list = ['和值']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({sum_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 1:
                    play_second_list = ['三同號單選', '三同號通選']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({same_3_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 2:
                    play_second_list = ['三不同號單選', '三不同號通選']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({different_3_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 3:
                    play_second_list = ['三連號通選']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({even_3_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 4:
                    play_second_list = ['二同號單選', '二同號複選', '二同號通選']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({same_2_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 5:
                    play_second_list = ['二不同號']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({different_2_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 6:
                    play_second_list = ['和值大小單雙', '和值組合大小單雙']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({fun_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 7:
                    play_second_list = ['猜必出', '猜必不出']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({any_code_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 8:
                    play_second_list = ['跨度']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({span_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)
                elif self.combobox_play_first.current() == 9:
                    play_second_list = ['豹子', '全順', '對子', '半順', '雜三']
                    for i in range(0, len(play_second_list)):
                        play_second_list[i] += f' ({show_hand_k3[i]})'
                    self.combobox_play_second['values'] = play_second_list
                    self.combobox_play_second.current(0)

    # def combobox_play_second_selected(self, event):
    #     if self.combobox_lotto_type.get() == '快三' and self.combobox_mode.get() == '官方玩法 (Official)'

    def exection(self):
        # 獲取左側玩法資訊類的資訊
        vendor = self.combobox_vendor.get()
        lotto_type = self.combobox_lotto_type.get()
        lotto_name = self.combobox_lotto.get()
        mode = self.combobox_mode.current()
        play_first = self.combobox_play_first.get()
        play_second = self.combobox_play_second.get()
        # 獲取右側資訊。帳密、抽水值、telegram id
        account = self.textbox_account.get()
        password = self.textbox_password.get()
        telegram_id = self.textbox_telegram_id.get()
        test_type = self.combobox_test_type.current()
        test_time = self.textbox_test_time.get()
        single_bet_amount = self.textbox_bet.get()
        pump = self.textbox_pump.get()

        # -------------------左側資訊處理-------------------
        # 判斷商戶，對應開啟網址
        if self.combobox_vendor.current() == 0:
            url = 'http://www.sit-gi8viet.com/index'
            vendor = 'VN'
        elif self.combobox_vendor.current() == 1:
            url = 'http://www.sit-tcgdemov3.com/index'
            vendor = 'CN'
        else:
            url = 'http://www.sit-tcgdemov3.com/index'
            vendor = 'SEA'

        # 僅截取code部分的pattern
        pattern_en = ' .*'
        # 截取彩票分類code，輸入路徑用
        match_lotto_type_en = search(pattern_en, lotto_type)
        lotto_type_en = match_lotto_type_en.group(0)
        lotto_type_en = lotto_type_en.replace(lotto_type_en[-1:], '')
        lotto_type_en = lotto_type_en.replace(lotto_type_en[:2], '')
        # 截取彩種名稱code，輸入路徑用
        match_lotto_name_en = search(pattern_en, lotto_name)
        lotto_name_en = match_lotto_name_en.group(0)
        lotto_name_en = lotto_name_en.replace(lotto_name_en[-1:], '')
        lotto_name_en = lotto_name_en.replace(lotto_name_en[:2], '')
        # 截取第一層玩法code
        match_play_first_en = search(pattern_en, play_first)
        play_first_en = match_play_first_en.group(0)
        play_first_en = play_first_en.replace(play_first_en[-1:], '')
        play_first_en = play_first_en.replace(play_first_en[:2], '')
        # 截取第二層玩法code
        match_play_second_en = search(pattern_en, play_second)
        play_second_en = match_play_second_en.group(0)
        play_second_en = play_second_en.replace(play_second_en[-1:], '')
        play_second_en = play_second_en.replace(play_second_en[:2], '')

        # 僅截取中文部分的pattern
        pattern_cn = '.* '
        # 擷取彩種名稱中文部分，輸入指令用
        match_lotto_name_cn = search(pattern_cn, lotto_name)
        lotto_name_cn = match_lotto_name_cn.group(0)
        lotto_name_cn = lotto_name_cn.replace(lotto_name_cn[-1:], '')
        # 擷取第一層玩法中文部分，輸入指令用
        match_play_first_cn = search(pattern_cn, play_first)
        play_first_cn = match_play_first_cn.group(0)
        play_first_cn = play_first_cn.replace(play_first_cn[-1:], '')
        # 擷取第二層玩法中文部分，輸入指令用
        match_play_second_cn = search(pattern_cn, play_second)
        play_second_cn = match_play_second_cn.group(0)
        play_second_cn = play_second_cn.replace(play_second_cn[-1:], '')

        # 判斷選擇的模式，輸入指令路徑用
        if self.combobox_vendor.current() == 1:
            type_current = self.combobox_lotto_type.current()
            if type_current == 0 or type_current == 3 or type_current == 4 or type_current == 5 or type_current == 6:
                if mode == 0:
                    mode = 'Official'
            else:
                mode = 'Entertainment'
        else:
            # 這個先暫時這樣，SEA.VN有需要再另外更動
            mode = ''

        # if mode == 0:
        #     mode = 'Official'
        # else:
        #     mode = 'Entertainment'

        # -------------------右側資訊處理-------------------
        # 未輸入帳密的警告
        if account == '' or password == '':
            tk.messagebox.showerror('警告', '帳號密碼不能為空！')
            return

        # 處理單注投注金額
        try:
            if single_bet_amount == '':
                single_bet_amount = 1
            elif single_bet_amount == '0':
                tk.messagebox.showerror('錯誤', '投注金額不能為0！')
                return
            float(single_bet_amount)
        except ValueError:
            tk.messagebox.showerror('錯誤', '投注金額僅能數字！')
            return

        # 處理抽水值
        try:
            if pump == '':
                pump = 0
            else:
                pump = float(pump) / 100
        except ValueError:
            tk.messagebox.showerror('警告', '抽水值僅能輸入整數！')
            return

        # 處理測試次數，迴圈起始值是1，所以測試次數要+1才會是輸入的測試次數
        try:
            if test_time == '':
                test_time = 2
            else:
                test_time = int(test_time) + 1

            YamlUtil.write_test_times([{'test_times': test_time}])
            # with open('../../test_times.txt', "w") as f:
            #     f.write(str(test_time))

        except ValueError:
            tk.messagebox.showerror('警告', '測試次數欄位僅能輸入整數！')
            return

        # 未輸入Telegram id的警告
        if telegram_id == '':
            return_value = messagebox.askokcancel(title='提示', message='無輸入Telegram ID，測試結束或有意外狀況將不會寄送提醒訊息！\n確定要繼續測試嗎？')
            if return_value:
                pass
            else:
                return
        elif telegram_id != '':
            try:
                int(telegram_id)
            except ValueError:
                tk.messagebox.showerror('錯誤', 'Telegram ID僅有數字！')
                return

        # 判斷測試類型，輸入指令路徑用 (這裡還要改)
        if test_type == 0:
            test_type = 'verify_all_numbers'
        else:
            test_type = ''

        # -------------------開始路徑判斷、處理-------------------
        # 測試報告路徑
        if vendor == 'CN':
            report_path = f'./reports/allure_reports/{vendor}/{lotto_type_en}/{lotto_name_en}/{mode}/{str(today)}_{play_second_en}_{test_type}_{str(self.count)}'
            while True:
                if path.exists(report_path):
                    self.count += 1
                    report_path = f'./reports/allure_reports/{vendor}/{lotto_type_en}/{lotto_name_en}/{mode}/{str(today)}_{play_second_en}_{test_type}_{str(self.count)}'
                else:
                    break
        else:
            report_path = f'./reports/allure_reports/{vendor}/{lotto_type_en}/{lotto_name_en}/{str(today)}_{play_second_en}_{test_type}_{str(self.count)}'
            while True:
                if path.exists(report_path):
                    self.count += 1
                    report_path = f'./reports/allure_reports/{vendor}/{lotto_type_en}/{lotto_name_en}/{str(today)}_{play_second_en}_{test_type}_{str(self.count)}'
                else:
                    break

        # 登入、進入彩種、測試檔案的腳本路徑
        script_path = ''
        if vendor == 'CN':
            script_path += './CN'
        elif vendor == 'SEA':
            script_path += './SEA'
        else:
            script_path += './VN'

        if self.combobox_device_type.get() == 'UI':
            script_path += '/UI'
        else:
            script_path += '/H5'

        script_path_login = script_path + '/login.py'
        script_path_join_lotto = script_path + '/join_lotto.py'
        script_path_case = f'{script_path}/{self.combobox_template.get()}/{lotto_type_en}/{lotto_name_en}/{mode}/{play_first_en}/{play_second_en}/{test_type}.py'

        # 啟動測試指令
        system(f'pytest -vs {script_path_login} {script_path_join_lotto} {script_path_case} --alluredir={report_path} --url={url} --account={account} --password={password} '
               f'--lotto_name={lotto_name_cn} --play_first={play_first_cn} --play_second={play_second_cn} --single_bet_amount={str(single_bet_amount)} --pump={str(pump)} '
               f'--api_key={API_KEY} --telegram_id={str(telegram_id)}')

        # -------------------測試結束後處理-------------------
        # 測試結束寄送訊息，判斷id是否正確。id錯誤顯示警告視窗
        if telegram_id == '':
            pass
        elif telegram_id != '':
            try:
                bot.send_message(chat_id=telegram_id, text='測試結束')
            except:
                tk.messagebox.showerror('提示', 'Telegram ID不正確，所以無寄送測試結束訊息')
        self.messagebox()

    # messagebox彈窗，測試結束時會出現
    def messagebox(self):
        return_value = messagebox.askokcancel(title='測試完成', message='測試完成，是否關閉程式?')
        if return_value:
            quit()


# 計算視窗居中
def get_system_metrics():
    return GetSystemMetrics(0), GetSystemMetrics(1)


# 傳入視窗大小(解析度)計算出視窗居中的位置
def get_window_positions(width, height):
    system_metrics = get_system_metrics()
    window_x_position = (system_metrics[0] - width) // 2
    window_y_position = (system_metrics[1] - height) // 2
    return window_x_position, window_y_position


if __name__ == '__main__':
    window = tk.Tk()
    window_width = 400
    window_height = 480
    window.resizable(False, False)      # 固定視窗大小，不能自行調整
    window.title('St.Win Automation')
    pos = get_window_positions(window_width, window_height+150)      # 沒有150才是置中
    window.geometry(f'{window_width}x{window_height}+{pos[0]}+{pos[1]}')    # 計算置中

    app = Application(window)
    app.mainloop()
