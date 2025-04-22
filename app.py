
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import re
import os
import pytz

animal = ["крыса", "бык", "тигр", "кролик", "дракон", "змея", "лошадь", "коза", "обезьяна", "петух", "собака", "свинья"]
stihiya = ["дерево", "дерево", "огонь", "огонь", "почва", "почва",  "металл",  "металл", "вода", "вода"]
in_yan = ["ян", "инь"]

vis_yaer = [1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968, 
            1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 
            2024, 2028, 2032, 2036, 2040, 2044, 2048, 2052]

moon_palace = dict({1: [1920, 1942, 0, 1987, 2009, 2032], 2: [0, 1943, 1965, 1988, 2010, 0], 
    3: [1921, 1944, 1966, 0, 2011, 2033], 4: [1922, 0, 1967, 1989, 2012, 2034], 
    5: [1923, 1945, 1968, 1990, 0, 2035], 6: [1924, 1946, 0, 1991, 2013, 2036], 
    7: [0, 1947, 1969, 1992, 2014, 0], 8: [1925, 1948, 1970, 0, 2015, 2037], 
    9: [1926, 0, 1971, 1993, 2016, 2038], 10: [1927, 1949, 1972, 1994, 0, 2039], 
    11: [1928, 1950, 0, 1995, 2017, 2040], 12: [0, 1951, 1973, 1996, 2018, 0], 
    13: [1929, 1952, 1974, 0, 2019, 2041], 14: [1930, 0, 1975, 1997, 2020, 2042], 
    15: [1931, 1953, 1976, 1998, 0, 2043], 16: [1932, 1954, 0, 1999, 2021, 2044], 
    17: [0, 1955, 1977, 2000, 2022, 0], 18: [1933, 1956, 1978, 0, 2023, 2045], 
    19: [1934, 0, 1979, 2001, 2024, 2046], 20: [1935, 1957, 1980, 2002, 0, 2047], 
    21: [1936, 1958, 0, 2003, 2025, 2048], 22: [0, 1959, 1981, 2004, 2026, 0], 
    23: [1937, 1960, 1982, 0, 2027, 2049], 24: [1938, 0, 1983, 2005, 2028, 2050], 
    25: [1939, 1961, 1984, 2006, 0, 2051], 26: [1940, 1962, 0, 2007, 2029, 2052], 
    27: [0, 1963, 1985, 2008, 2030, 0], 28: [1941, 1964, 1986, 0, 2031, 2053]})

sec_step = {1: 27,
            2: 2,
            3: 2,
            4: 5,
            5: 7,
            6: 10,
            7: 12,
            8: 15,
            9: 18,
            10: 20,
            11: 23,
            12: 25}


man = ["Liv.1", "Liv.4", "Liv.3", "Gb.37/Liv.3", "Liv.5/Gb.40", "Liv.2", "Liv.8", 
       "Kid.1", "Kid.7", "Kid.3", "Bl.58/Kid.3", "Kid.4/Bl.64", "Kid.2", "Kid.10", 
       "Lu.11", "Lu.8", "Lu.9", "Co.6/Lu.9", "Co.4/Lu.7", "Lu.10", "Lu.5", 
       "Ht.9/Hg.9", "Ht.4/Hg.5", "Ht.7/Hg.7", "Si.7/Ht.7/Hg.7", 
       "Ht.5/Hg.6/Si.4", "Ht.8/Hg.8", "Ht.3/ Hg.3"]

woman = ["Gb.41", "Gb.44", "Gb.34", "Gb.37/Liv.3", "Liv.5/Gb.40", "Gb.38", "Gb.43", 
       "Bl.65", "Bl.67", "Bl.40", "Bl.58/Kid.3", "Kid.4/Bl.64", "Bl.60", "Bl.66", 
       "Co.3", "Co.1", "Co.11", "Co.6/Lu.9", "Co4/Lu.7", "Co.5", "Co.2", 
       "Si.3", "Si.1", "Si.8", "Si.7/Ht.7/Hg.7", "Ht.5/Hg.6/Si.4", "Si.5", "Si.2"]

sky = {'甲': ':green[甲]',
        '乙': ':green[乙]',
        '丙': ':red[丙]',
        '丁': ':red[丁]',
        '戊': ':orange[戊]',
        '己': ':orange[己]',
        '庚': ':darkgray[庚]',
        '辛': ':darkgray[辛]',
        '壬': ':blue[壬]',
        '癸': ':blue[癸]'}

earth = {'子': ':blue[子]',
        '丑': ':orange[丑]',
        '寅': ':green[寅]',
        '卯': ':green[卯]',
        '辰': ':orange[辰]',
        '巳': ':red[巳]',
        '午': ':red[午]',
        '未': ':orange[未]',
        '申': ':darkgray[申]',
        '酉': ':darkgray[酉]',
        '戌': ':orange[戌]',
        '亥': ':blue[亥]'}

@st.cache_data


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


def read_files():       
    cities = pd.read_csv("data/cities.csv")
    earth_legs = pd.read_csv("data/earth_legs.csv")
    sky_hands = pd.read_csv("data/sky_hands.csv")
    planets = pd.read_csv("data/planets.csv")
    moon_palace_df = pd.read_csv("data/moon_palace.csv")
    calender = pd.read_csv("data/calender.csv")
    cicle = pd.read_csv("data/cicle.csv")
    seasons = pd.read_csv("data/seasons.csv")
    return cities, earth_legs, sky_hands, planets, moon_palace_df, calender, cicle, seasons


########################################  Создаём приложение ######################################

cities, earth_legs, sky_hands, planets, moon_palace_df, calender, cicle, seasons = read_files()
calender['date'] = pd.to_datetime(calender['date'])

st.title("Калькулятор Ба Цзы")

st.header("")

st.markdown(f'Сегодня: **{datetime.now().strftime("%d.%m.%Y")}**')


birthday =  st.text_input(':orange[Введите дату рождения в формате дд.мм.гггг]', '')

if birthday:
    try:
        birthday = pd.to_datetime(birthday, dayfirst=True).strftime("%d.%m.%Y")
        birthday = str(pd.to_datetime(birthday, dayfirst=True)).split()[0]
        st.markdown(f'Дата рождения: **{pd.to_datetime(birthday).strftime("%d.%m.%Y")}**')

        year_v = calender[calender['date']==pd.to_datetime(birthday)]['years'].values[0]
        month_v = calender[calender['date']==pd.to_datetime(birthday)]['months'].values[0]
        day_v = calender[calender['date']==pd.to_datetime(birthday)]['days'].values[0]
        day_ier = cicle[cicle["Название_calender"] == day_v]["Иероглиф"].values[0]
        month_ier = cicle[cicle["Название_calender"] == month_v]["Иероглиф"].values[0]
        year_ier = cicle[cicle["Название_calender"] == year_v]["Иероглиф"].values[0]


        birthday_df = pd.DataFrame(columns=["День", "Месяц", "Год"])
        birthday_df["День"] = [
            f"{cicle[cicle['Название_calender'] == day_v]['Название_Русский'].values[0]} {cicle[cicle['Название_calender'] == day_v]['инь_ян'].values[0]}",
            day_ier
        ]
        birthday_df["Месяц"] = [
            f"{cicle[cicle['Название_calender'] == month_v]['Название_Русский'].values[0]} {cicle[cicle['Название_calender'] == month_v]['инь_ян'].values[0]}",
            month_ier
        ]
        birthday_df["Год"] = [
            f"{cicle[cicle['Название_calender'] == year_v]['Название_Русский'].values[0]} {cicle[cicle['Название_calender'] == year_v]['инь_ян'].values[0]}",
            year_ier
        ]
        st.dataframe(birthday_df, hide_index=True, column_config={
            "День":st.column_config.TextColumn(default="st."),
            "Месяц":st.column_config.TextColumn(default="st."),
            "Год":st.column_config.TextColumn(default="st.")
        }, use_container_width=True)
    except:
        st.error("Некорректная дата. Попробуйте снова")



cit = [""] + cities["Город"].values.tolist() + cities["Регион"].values.tolist() + cities["Н/п"].values.tolist()
city = st.selectbox(':orange[Введите город, где Вы находитесь]', cit)

if city :
    if len(cities[cities["Город"].str.contains(city, regex=True).fillna(False)]) != 0:
            raw = cities[cities["Город"].str.contains(city, regex=True).fillna(False)][["Индекс", "Тип региона", "Регион", "Тип района", 
                                                                                "Район", "Тип города", "Город", "Тип н/п", "Н/п", "Часовой пояс"]].dropna(axis=1)
    elif len(cities[cities["Регион"].str.contains(city, regex=True).fillna(False)]) != 0:
            raw = (cities[cities["Регион"].str.contains(city, regex=True).fillna(False)][["Индекс", "Тип региона", "Регион", 
                "Тип района",	"Район", "Тип города", "Город", "Тип н/п",	"Н/п", "Часовой пояс"]].dropna(axis=1))
    else:
        raw = (cities[cities["Н/п"].str.contains(city, regex=True).fillna(False)][["Индекс", "Тип региона", "Регион", 
                "Тип района",	"Район", "Тип города", "Город", "Тип н/п",	"Н/п", "Часовой пояс"]].dropna(axis=1))

    id_city = raw.index
    long = cities.loc[id_city, "Долгота"].values[0]
    hours = int(long//15)
    minutes = int(round((long/15 - hours)*60))

    utc = int(raw["Часовой пояс"].values[0])

    CURRENT_TIME = (datetime.utcnow() + timedelta(hours=utc)).time().strftime('%H:%M')
    CURRENT_TIME_SOLAR = (datetime.utcnow() + timedelta(hours=hours, minutes=minutes)).time().strftime('%H:%M')


    st.markdown(f"*:rainbow[Текущее административное время]:* **:blue[{CURRENT_TIME}]**")
    st.markdown(f"*:rainbow[Текущее солнечное время]:* **:blue[{CURRENT_TIME_SOLAR}]**")

    st.markdown("Рассчет по умолчанию выполняется по солнечному времени. \
                Если нужен рассчет по времени административному, поставьте галочкуниже:")
    
    if st.checkbox("##### Нужен расчёт по административному времени"):
        our_time = CURRENT_TIME
    else:
        our_time = CURRENT_TIME_SOLAR

    CURRENT_TIME_SOLAR = our_time
    st.markdown(CURRENT_TIME_SOLAR) 

    # Вводим дату рождения
    our_date = st.text_input(':orange[Введите интересующую дату в формате дд.мм.гггг]', '')
    
    if our_date:
        try:
            our_date = vis_date = re.sub('\D', '.', our_date)
            our_date = our_date.split('.')
            d = int(our_date[0])
            m = int(our_date[1])
            y = int(our_date[2])
            our_date = date(y, m, d)

            year_o = calender[calender['date']==pd.to_datetime(our_date)]['years'].values[0]
            month_o = calender[calender['date']==pd.to_datetime(our_date)]['months'].values[0]
            day_o = calender[calender['date']==pd.to_datetime(our_date)]['days'].values[0]
            day = cicle[cicle["Название_calender"] == day_o]["Название_Русский"].values[0]
            day_iero = cicle[cicle["Название_calender"] == day_o]["Иероглиф"].values[0]
            month_iero = cicle[cicle["Название_calender"] == month_o]["Иероглиф"].values[0]
            year_iero = cicle[cicle["Название_calender"] == year_o]["Иероглиф"].values[0]


            our_date_df = pd.DataFrame(columns=["День", "Месяц", "Год"])
            our_date_df["День"] = [
                f"{cicle[cicle['Название_calender'] == day_o]['Название_Русский'].values[0]} {cicle[cicle['Название_calender'] == day_o]['инь_ян'].values[0]}",
                day_iero
            ]
            our_date_df["Месяц"] = [
                f"{cicle[cicle['Название_calender'] == month_o]['Название_Русский'].values[0]} {cicle[cicle['Название_calender'] == month_o]['инь_ян'].values[0]}",
                month_iero
            ]
            our_date_df["Год"] = [
                f"{cicle[cicle['Название_calender'] == year_o]['Название_Русский'].values[0]} {cicle[cicle['Название_calender'] == year_o]['инь_ян'].values[0]}",
                year_iero
            ]
            st.dataframe(our_date_df, hide_index=True, column_config={
                "День":st.column_config.TextColumn(default="st."),
                "Месяц":st.column_config.TextColumn(default="st."),
                "Год":st.column_config.TextColumn(default="st.")
            }, use_container_width=True)
        except:
            st.error("Некорректная дата. Попробуйте снова")
            
        
        feitenbafa = pd.read_csv("data/feitenbafa.csv")
        for_feitenbafa = pd.read_csv("data/for_feitenbafa.csv")


        day_predictions = feitenbafa.merge(for_feitenbafa.rename(columns={"Иероглиф":day_iero[0]}))
        feitenbafa_day = day_predictions[[day_iero[0], 'Иероглиф',	'Время',	'Канал',	'Точки']]

        current_hour = re.search(r"(\d*)", CURRENT_TIME_SOLAR)[0]

        # Определяем час по текущему времени.

        if (int(current_hour) == 23) or (int(current_hour) == 0):
            current_hour_china_list = feitenbafa_day.iloc[0].values
        else:
            for h in range(1,12):
                if (int(current_hour) >= (feitenbafa['Время_int'][h])) & (int(current_hour) < (feitenbafa['Время_int'][h]+2)):
                    current_hour_china_list = feitenbafa_day.iloc[h].values
                    break

        current_hour_china = ''.join(current_hour_china_list[:2])

        # st.markdown(f"**{vis_date}** день: **{day}**")
        # srt_1 = f"День: **{day}**"
        in_yan = cicle[cicle['Название_calender'] == day_o]['инь_ян'].values[0]
        # st.markdown(f"День: **{in_yan.capitalize()}**")
        # str_2 = in_yan.capitalize()

        # st.markdown(f"ЦзяЦзы дня: № **:blue[{cicle[cicle['Название_calender'] == day_o]['Цзя_Цзы'].values[0]}]**")
        # str_3 = cicle[cicle['Название_calender'] == day_o]['Цзя_Цзы'].values[0]
        # st.markdown("--"*80)


        # Определяем сезон по дате
        if (pd.to_datetime(our_date) < pd.to_datetime(seasons[str(our_date.year)][0])) or (pd.to_datetime(our_date) > pd.to_datetime(seasons[str(our_date.year)][23])):
            season = seasons.iloc[23][["Символ", "Название", "Точки_Жэнь_май",	"Название_точки"]].values
        else:
            for d in range(24):
                if (pd.to_datetime(our_date) > pd.to_datetime(seasons[str(our_date.year)][d])) & (pd.to_datetime(our_date)<pd.to_datetime(seasons[str(our_date.year)][d+1])):
                    season = seasons.iloc[d][["Символ", "Название", "Точки_Жэнь_май",	"Название_точки"]].values
                    break

        # st.markdown("*Точки 24 Сезонов (Жэнь май):*")
        # st.markdown(f"**:blue[{'  ||  '.join(season).strip()}]**")
        # str_4 = '  ||  '.join(season).strip()
        # st.markdown("--"*80)
        dow_dict = {0:"Понедельник", 1:"Вторник", 
                2:"Среда", 3:"Четверг",
                4:"Пятница", 5:"Суббота", 6:"Воскресенье"}

        # st.markdown(f"День недели: **{dow_dict[pd.to_datetime(our_date).day_of_week]}**")
        # str_5 = dow_dict[pd.to_datetime(our_date).day_of_week]

        planet = planets[planets['День_недели']==pd.to_datetime(our_date).day_of_week]['Планета'].values[0]
        # st.markdown(f"Планета-покровитель: **:green[{planet.capitalize()}]**")

        st.markdown(f"**{vis_date}** день: **{day}**\
                    \nДень: **{in_yan.capitalize()}**\
                    \nЦзяЦзы дня: № **:blue[{cicle[cicle['Название_calender'] == day_o]['Цзя_Цзы'].values[0]}]**\
                    \nТочки 24 Сезонов (Жэнь май): \t**:blue[{'  ||  '.join(season).strip()}]**\
                    \nДень недели: **{dow_dict[pd.to_datetime(our_date).day_of_week]}**\
                    \nПланета-покровитель: **:green[{planet.capitalize()}]**")



        ##########################

        method = st.selectbox(
                "Выберете метод хронопунктуры",
                (" ", "ЛУННЫЕ ДВОРЦЫ", "ФЭЙ ТЭН БА ФА", "ЛИН ГУЙ БА ФА", "ТАЙ ЯН БА ФА", "ДА СЯО ЧЖОУ ТЯНЬ ЖЭНЬ ФА"))
        
        if method:
            if method=="ЛУННЫЕ ДВОРЦЫ":
                # Считаем лунную стоянку
                for k, v in moon_palace.items():
                    if our_date.year in v:
                        first_step = k
                if (our_date.year in vis_yaer) & (pd.to_datetime(our_date) > pd.to_datetime(f"{our_date.year}-02-28")):
                    first_step = first_step+1

                lunar_day = first_step + sec_step[our_date.month]+ our_date.day

                while lunar_day > 28:
                    lunar_day+=-28
                if lunar_day in range(1, 15):
                    lunar_day_ton = lunar_day+14
                else:
                    lunar_day_ton = lunar_day-14
                symbol = moon_palace_df[moon_palace_df["Лунный_день"]==lunar_day]["Иероглиф"].values[0]
                val = moon_palace_df[moon_palace_df["Лунный_день"]==lunar_day]["Созвездие"].values[0]
                point = moon_palace_df[moon_palace_df["Лунный_день"]==lunar_day][["Точка_Ду_май", "Название"]].values[0][0] + \
                    "||" + moon_palace_df[moon_palace_df["Лунный_день"]==lunar_day][["Точка_Ду_май", "Название"]].values[0][1]

                st.markdown(f"Лунная стоянка: **{str(lunar_day)} :red[{symbol}] {val.capitalize()}**")
                st.markdown(f"Точки 28 Лунных Стоянок (Ду май): **{point}**")
                st.markdown("*Техника 28 Лунных Стоянок*")


                st.markdown(f"Помочь выйти событию (седирование) \
                        \nЯн \t{man[lunar_day-1]}\
                        \nИнь \t{woman[lunar_day-1]}")

                st.markdown(f"Заставийть выйти событие (тонизация) \
                        \nЯн: \t{man[lunar_day_ton-1]}\
                        \nИнь: \t{woman[lunar_day_ton-1]}")
                
                st.markdown("--"*80)
                

        if method:
            if method=="ФЭЙ ТЭН БА ФА":
        
                    
                st.markdown(" || ".join(current_hour_china_list[1:]))
                
                feitenbafa_day_disp = feitenbafa_day.iloc[:, 1:].T
                feitenbafa_day_disp.to_csv("data/feitenbafa_day_disp.csv", index=False)
                feitenbafa_day_disp = pd.read_csv("data/feitenbafa_day_disp.csv", header=1)
                n=90
                st.dataframe(
                    feitenbafa_day_disp,
                    column_config= {
                        feitenbafa_day_disp.columns[0]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[1]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[2]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[3]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[4]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[5]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[6]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[7]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[8]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[9]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[10]:st.column_config.Column(width=n),
                        feitenbafa_day_disp.columns[11]:st.column_config.Column(width=n),
                    },
                    hide_index=True
                )
            
            
            if method=="ЛИН ГУЙ БА ФА":
                for_lin_gui_ba_fa = pd.read_csv("data/for_lin_gui_ba_fa.csv")
                # current_hour = re.search(r"(\d*)", CURRENT_TIME_SOLAR)[0]


                linguibafa = []
                for i in feitenbafa_day.index:
                    summ = sky_hands[sky_hands['Иероглиф']==day_iero[0]]['i_day'].values[0] + \
                                sky_hands[sky_hands['Иероглиф']==feitenbafa_day.iloc[i, 0]]['i_hour'].values[0] + \
                                earth_legs[earth_legs['Иероглиф']==day_iero[1]]['j_day'].values[0] + \
                                earth_legs[earth_legs['Иероглиф']==feitenbafa_day.iloc[i, 1]]['j_hour'].values[0]

                    if cicle[cicle['Иероглиф']==day_iero]['инь_ян'].values[0] == 'ян':
                        res = summ%9
                        if res == 0:
                            res = 9
                    else:
                        res = summ%6
                        if res == 0:
                            res = 6  
                        
                    linguibafa_lst = list(feitenbafa_day.iloc[i,:3].values)
                    linguibafa_lst.extend(for_lin_gui_ba_fa[for_lin_gui_ba_fa['res']==res].values[0][1:])
                    linguibafa.append(linguibafa_lst)

                    
                linguibafa_df = pd.DataFrame(
                    data=linguibafa,
                    columns=[feitenbafa_day.columns[0], feitenbafa_day.columns[1], feitenbafa_day.columns[2],"Канал", "Точка", "Название_точки"]
                )


                linguibafa_df[linguibafa_df.columns[1:]].T.to_csv("data/linguibafa_df_disp.csv", index=False)
                linguibafa_df_disp = pd.read_csv("data/linguibafa_df_disp.csv", header=1)


                linguibafa_current_hour = linguibafa_df[linguibafa_df['Иероглиф']==current_hour_china[1]]
                st.markdown(" || ".join(linguibafa_current_hour.iloc[0,1:].values.tolist()))
                st.dataframe(
                    linguibafa_df_disp,
                    hide_index=True
                )




            if method=="ТАЙ ЯН БА ФА":
                list_tai = os.listdir("data/tai_yan_ba_fa/")
                for l in list_tai:
                    if day_iero[0] in l:
                        file=re.findall(f'(\w*{day_iero[0]}\w*.csv)', l)
                
                tai_yan_ba_fa = pd.read_csv(f"data/tai_yan_ba_fa/{file[0]}")

                try:
                    current_hour_taiyan = tai_yan_ba_fa.iloc[tai_yan_ba_fa[tai_yan_ba_fa["0"]==current_hour_china[1]].index[0]:
                                                             tai_yan_ba_fa[tai_yan_ba_fa["0"]==current_hour_china[1]].index[0] + 2]
                except:
                    current_hour_taiyan = tai_yan_ba_fa.iloc[tai_yan_ba_fa[tai_yan_ba_fa["0"]==current_hour_china[1]].index[0]:]
                
                st.markdown("На текущий час:")
                st.dataframe(
                    current_hour_taiyan,
                    hide_index=True,
                    use_container_width=True
                )

                if st.checkbox("Показать рассчёт на всю дату"):
                    st.markdown("На день:")
                    st.dataframe(
                        tai_yan_ba_fa,
                        hide_index=True,
                        use_container_width=True
                    )


            
            if method=="ДА СЯО ЧЖОУ ТЯНЬ ЖЭНЬ ФА":
                da_syao = pd.read_csv("data/da_syao.csv")
                current_hour_china_list = da_syao[current_hour_china[1]].to_list()
                
                st.markdown(" || ".join(current_hour_china_list))
                
                if st.checkbox("Показать рассчёт на всю дату"):
                    st.markdown("На день:")
                    st.dataframe(
                        da_syao,
                        hide_index=True,
                        use_container_width=True
                    )