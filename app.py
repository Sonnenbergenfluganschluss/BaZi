
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from itertools import cycle
from PIL import Image
import re
import matplotlib.pyplot as plt
import numpy as np
import csv

mal = ["крыса", "бык", "тигр", "кролик", "дракон", "змея", "лошадь", "коза", "обезьяна", "петух", "собака", "свинья"]
stihiya = ["дерево", "дерево", "огонь", "огонь", "почва", "почва",  "металл",  "металл", "вода", "вода"]
in_yan = ["ян", "инь"]


@st.cache_data




def read_files():       
    cities = pd.read_csv("data/cities.csv")
    return cities


def get_year():
    stih = cycle(stihiya)
    anim = cycle(animal)
    inyan = cycle(in_yan)
    global our_date  
    global start_year
    year_china = our_date.year
    if our_date.month < 2:
        year_china = year_china-1
    lst = []
    for i in range(year_china - start_year):
        start_year+=1
        lst.append(f"Год: {start_year} {next(anim)} {next(inyan)} {next(stih)}")
    return lst[-1]


def get_month():
    stih = cycle(stihiya)
    anim = cycle(animal)
    inyan = cycle(in_yan)
    global our_date  
    global start_month
    end_months=(our_date.year-start_month.year)*12 + our_date.month+1
    lst = []
    for i in range(end_months):
        lst.append(f"Месяц: {next(anim)} {next(inyan)} {next(stih)}")
    return lst[-1]


def get_day():
    stih = cycle(stihiya)
    anim = cycle(animal)
    inyan = cycle(in_yan)
    global our_date  
    global start_day
    lst = []
    for i in range(((our_date - start_day).days+1) % 60):
        lst.append(f"Месяц: {next(anim)} {next(inyan)} {next(stih)}")
    return lst[-1]




########################################  Создаём приложение ######################################

cities = read_files()

st.title("Китайский новый год")
st.markdown(f'Дата: **{datetime.now().strftime("%d.%m.%Y")}**')
# ddate = st.sidebar.text_input('Введите дату приёма', '')
# Вводим имя пациента
patient = st.sidebar.text_input('Введите Ф.И.О. пациента', '')

st.header(patient)


# Вводим дату рождения
our_date = st.sidebar.text_input('Введите интересующую дату', '')
if our_date:
    try:
        our_date = pd.to_datetime(our_date, dayfirst=True).strftime("%d.%m.%Y")
        our_date = str(pd.to_datetime(our_date, dayfirst=True)).split()[0]
        st.markdown(f'Дата рождения: **{pd.to_datetime(our_date, dayfirst=True).strftime("%d.%m.%Y")}**')
    except:
        st.error("Некорректная дата. Попробуйте снова")
        
    # Получаем год и полугодие по китайскому календарю
    year = int(our_date[:4])


#     if birthday in polugodie.loc[year, "I полугодие"]:
#         st.markdown(f"I полугодие {year} года")
#         polugodie_true = "I полугодие"
#         polugodie_false = "II полугодие"
#     elif birthday in polugodie.loc[year, "II полугодие"]:
#         st.markdown(f"II полугодие {year} года")
#         polugodie_true = "II полугодие"
#         polugodie_false = "I полугодие"
#     else:
#         st.markdown(f"II полугодие {year-1} года")
#         polugodie_true = "II полугодие"
#         polugodie_false = "I полугодие"
#         year = year-1

#     df = get_cart(year=year)
    
#     if df.loc["Zang Fu Xu", "Используем"] == None:
#         Zang_Fu_Xu = set()
#     else:
#         Zang_Fu_Xu = set(df.loc["Zang Fu Xu", "Используем"])
        
        
#     # Выводим DataFrame в интерфейсе
#     st.dataframe(df, use_container_width=True)

#     use = set([df.loc['Ствол', 'Используем'], df.loc['Ветвь', 'Используем']]) | (Zang_Fu_Xu)
        
#     dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем']]) 

#     neutral = set(u_sin_pitanie.keys()) ^ (set([df.loc['Ствол', 'Не используем'], 
#                                             df.loc['Ветвь', 'Не используем']]) |  
#                                         set([df.loc['Ствол', 'Используем'], 
#                                             df.loc['Ветвь', 'Используем']]) |
#                                             Zang_Fu_Xu)
                                            
#     st.markdown(f"""Нейтральные каналы: **{', '.join(list(neutral))}**""")

#     if st.checkbox("Показать предыдущую запись"):
#         try:
#             patients = pd.read_csv("patients/patients.csv", index_col='Дата')
#             patients = patients[patients['ФИО']==patient][-1:].dropna(axis=1)
#             if patients['метод лечения'].values[0] == "Питание и Ке":
#                 st.markdown("""====================================================================================""")
#                 try:
#                     st.markdown(f"##### :blue[Жалобы на {patients.index[0]}:]")
#                     st.markdown(f"{patients['жалобы'].values[0]}")
#                 except:
#                     st.markdown("")

#                 id = patients[patients['ФИО']==patient][-1:].dropna(axis=1).index[0]
#                 canals_plus = re.sub("\[|\]|'", "", patients.loc[id, "застой"]).split(", ")   
#                 canals_minus = re.sub("\[|\]|'", "", patients.loc[id, "недостаток"]).split(", ")   
#                 block = re.sub("\[|\]|'", "", patients.loc[id, "блок"]).split(", ") 
#                 wind = re.sub("\[|\]|'", "", patients.loc[id, "Gui"]).split(", ") 
#                 protivotok = re.sub("\[|\]|'", "", patients.loc[id, "противоток"]).split(", ") 
#                 xue = re.sub("\[|\]|'", "", patients.loc[id, "xue"]).split(", ") 
#                 tree = re.sub("\[|\]|'", "", patients.loc[id, "пат.рост"]).split(", ") 
#                 fire = re.sub("\[|\]|'", "", patients.loc[id, "жар"]).split(", ") 
#                 water = re.sub("\[|\]|'", "", patients.loc[id, "холод"]).split(", ") 
#                 earth = re.sub("\[|\]|'", "", patients.loc[id, "сырость"]).split(", ") 
#                 metall = re.sub("\[|\]|'", "", patients.loc[id, "сухость"]).split(", ") 

#                 di = {'+':canals_plus,
#                 '__':canals_minus,
#                 '>>>':protivotok,
#                 '+/-':block,
#                 'Gui':wind,
#                 'tree':tree,
#                 'Xue':xue,
#                 'жар':fire,
#                 'холод':water,
#                 'сырость':earth,
#                 'сухость':metall
#                 }

#                 ander = dict()

#                 for k in di.keys():
#                     for v in di[k]:
#                         v=v.lower()
#                         if v in ander.keys():
#                             ander[v].append(k)
#                         else:
#                             ander[v] = [k]

#                 ###################################### Рисуем карту патогенов ###################################


#                 # Генерируем случайные знаки и цвета
#                 def random_sign(channel, table=ander):
#                     if channel in table.keys():
#                         return table[channel]
#                     else:
#                         return ''

#                 # Устанавливаем базовые параметры
#                 num_vertices = 5
#                 radius = 1
#                 circle_radius = 0.08  # Радиус небольших кружков
#                 colors = {'жар':'red', 'сырость':'orange', 'сухость':'grey', 'холод':'blue', 'tree':'green', 
#                     "+":"#800080", "__":"#800080", "Gui":"dimgrey", "Xue":"#800000", "+/-":"#800080", ">>>":"#000000"}  # Цвета для символов


#                 # Создание графика
#                 fig, ax = plt.subplots(figsize=(15,8), )
#                 ax.axis('equal')  # Одинаковые масштабы по осям
#                 ax.axis('off')  # Отключаем оси

#                 # Открывающие углы для каждой вершины
#                 angles = np.linspace(0, 360, num_vertices+1)

#                 # Рисуем вершины: одна с 4 секторами, остальные с 2
#                 draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 0, 90, random_sign('th'))
#                 draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 90, 180, random_sign('si'))
#                 draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 180, 270, random_sign('ht'))
#                 draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 270, 360, random_sign('hg'))  # 4 сектора для первой вершины

#                 draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('sp'))
#                 draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('st'))

#                 draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('lu'))
#                 draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('co'))

#                 draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('kid'))
#                 draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('bl'))

#                 draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('liv'))
#                 draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('gb'))

#                 # Отображаем график
#                 # plt.title(f"{patients.index[0]}", loc='left', fontdict={'fontsize':20})

#                 st.write(fig)
#                 st.markdown(""":blue[Проведённое лечение: ]""")
#                 st.markdown(f"""{patients['лечение'].values[0]}""")
#                 st.markdown("""====================================================================================""")

#             else:
#                 st.dataframe(patients.T, use_container_width=True)
#         except:
#             st.markdown(f':red[Пациент **{patient}** отсутствует в базе данных]')


#     if st.checkbox("Показать все записи"):
#         try:
#             df_save = pd.read_csv(f"patients/patients.csv", index_col='Дата')
#             df_save_2 = df_save[df_save['ФИО']==patient]
#             st.dataframe(df_save_2, use_container_width=True)
#         except:
#             st.markdown(f':red[Пациент **{patient}** отсутствует в базе данных]')        

#     st.markdown("""--------------------------------------------------""")


#     complaints = st.sidebar.text_area("Жалобы", "")


    
    
#     ###################################   Выбираем метод лечения:   ##########################################


#     method = st.sidebar.selectbox(
#     "Выберете метод лечения",
#     (" ", "Питание и Ке", "Лунные дворцы"))
    

#     ###################################   Вводим канал в застое:    ###########################################
        
#     if method=="Питание и Ке":
        
#         plus = st.sidebar.text_input('Введите основной канал в застое', '')
#         canals_plus = get_chan(plus)
                    
#         if canals_plus:
#             # st.dataframe(ke[canals_plus][:4]) 
            
#             a = get_list_of_channels(canals_plus, ke, 4)

#             st.sidebar.markdown(f"""Возможные каналы в недостатке:""")
#             st.sidebar.markdown(f""":blue[**{', '.join(list(set(a)))}**]""")
            


#     ###################################   Для канала в недостатке:  ########################################
        
#         minus = st.sidebar.text_input('Введите канал в недостатке', '')
#         canals_minus = get_chan(minus)
 
#         if canals_minus:
#             zastoi = get_list_of_channels(canals_minus, ke, 4)
#             st.sidebar.markdown(f"""Возможные каналы в застое:""")
#             st.sidebar.markdown(f""":blue[**{', '.join(list(set(zastoi)))}**]""")

#         block = get_chan(st.sidebar.text_input('Введите каналы в блоке', ''))
#         wind = get_chan(st.sidebar.text_input('Введите каналы с ветром', ''))
#         protivotok = get_chan(st.sidebar.text_input('Введите каналы с противотоком', ''))
#         xue = get_chan(st.sidebar.text_input('Xue', ''))
#         if st.sidebar.checkbox("Работа с качеством"):
#             tree = get_chan(st.sidebar.text_input('Патологический рост', ''))
#             fire = get_chan(st.sidebar.text_input('Жар', ''))
#             water = get_chan(st.sidebar.text_input('Холод', ''))
#             earth = get_chan(st.sidebar.text_input('Сырость', ''))
#             metall = get_chan(st.sidebar.text_input('Сухость', ''))
#         else:
#             tree, fire, water, earth, metall = [], [], [], [], []

#         di = {'+':canals_plus,
#             '__':canals_minus,
#             '>>>':protivotok,
#             '+/-':block,
#             'Gui':wind,
#             'tree':tree,
#             'Xue':xue,
#             'жар':fire,
#             'холод':water,
#             'сырость':earth,
#             'сухость':metall
#             }

#         ander = dict()

#         for k in di.keys():
#             for v in di[k]:
#                 v=v.lower()
#                 if v in ander.keys():
#                     ander[v].append(k)
#                 else:
#                     ander[v] = [k]

#         ###################################### Рисуем карту патогенов ###################################

#         # Генерируем случайные знаки и цвета
#         def random_sign(channel, table=ander):
#             if channel in table.keys():
#                 return table[channel]
#             else:
#                 return ''
            
#         # Устанавливаем базовые параметры
#         num_vertices = 5
#         radius = 1
#         circle_radius = 0.08  # Радиус небольших кружков
#         colors = {'жар':'red', 'сырость':'orange', 'сухость':'grey', 'холод':'blue', 'tree':'green', 
#                   "+":"#800080", "__":"#800080", "Gui":"dimgrey", "Xue":"#800000", "+/-":"#800080", ">>>":"#000000"}  # Цвета для символов


#         # Создание графика
#         fig, ax = plt.subplots(figsize=(15, 8))
#         ax.axis('equal')  # Одинаковые масштабы по осям
#         ax.axis('off')  # Отключаем оси

#         # Открывающие углы для каждой вершины
#         angles = np.linspace(0, 360, num_vertices+1)

#         # Рисуем вершины: одна с 4 секторами, остальные с 2
#         draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 0, 90, random_sign('th'))
#         draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 90, 180, random_sign('si'))
#         draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 180, 270, random_sign('ht'))
#         draw_sector(ax, (np.sin(np.radians(angles[0])) * 2, np.cos(np.radians(angles[0])) * 2), radius, 270, 360, random_sign('hg'))  # 4 сектора для первой вершины

#         draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('sp'))
#         draw_sector(ax, (np.sin(np.radians(angles[1])) * 2, np.cos(np.radians(angles[1])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('st'))

#         draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 0 * 180, angles[1] + (0 + 1) * 180, random_sign('lu'))
#         draw_sector(ax, (np.sin(np.radians(angles[2])) * 2, np.cos(np.radians(angles[2])) * 2), radius, angles[1] + 1 * 180, angles[1] + (1 + 1) * 180, random_sign('co'))

#         draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('kid'))
#         draw_sector(ax, (np.sin(np.radians(angles[3])) * 2, np.cos(np.radians(angles[3])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('bl'))

#         draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 0 * 180, angles[4] + (0 + 1) * 180, random_sign('liv'))
#         draw_sector(ax, (np.sin(np.radians(angles[4])) * 2, np.cos(np.radians(angles[4])) * 2), radius, angles[4] + 1 * 180, angles[4] + (1 + 1) * 180, random_sign('gb'))

#         # Отображаем график
#         # plt.title(patient)
#         st.write(fig)

#         st.markdown("""--------------------------------------------------""")

#         ##### Питание #####

#         if canals_minus:            
#             st.markdown(f"""#### Основной недостаток выявлен в канале {canals_minus[0]}:""")
#             # Выводим DataFrame в интерфейсе:
#             st.dataframe(pitanie[canals_minus], use_container_width=True)  
                
#             m = get_list_of_channels(canals_minus, pitanie, 5)  

#             st.markdown("""#### Возможные каналы для питания:""")
#             st.markdown(f"""**:blue[{', '.join(list(set(m)))}]**""") 
            
#             dnt_use = set([df.loc['Ствол', 'Не используем'], df.loc['Ветвь', 'Не используем']]) | set(canals_minus) | set(canals_plus)
            
#             if (set(m) & dnt_use):
#                 st.warning(f""":red[!!!  Конфликт с запрещёнными каналами: **{', '.join(list(set(m) & dnt_use))}** !!!]""")
#             else:
#                 st.markdown("""Конфликт с запрещёнными каналами: :green[*Конфликта нет*]""")

            
#             one_spine = []
#             for i in list((set(m) & set(a))):
#                 if (i not in dnt_use):
#                     one_spine.append(i)

#             if one_spine:
#                 chan_pit = ' '.join(one_spine)
#                 st.markdown(f"""Одновременно питание недостатка и Ке на застой: :green[**{chan_pit}**]""")  
#                 point_pit = []
#                 for i in canals_minus:
#                     pp = pitanie[i][:5].to_list() 
#                     point_pit+=pp

#                 point_pit = " ".join(point_pit).replace(",", '')
#                 point_pit = point_pit.replace(",", '')
#                 try:
#                     point_pit = re.search(f"{chan_pit}\d+", point_pit)[0]
#                     st.markdown(f"""#### Подходящие точки для питания в этом случае:""")
#                     st.markdown(f"""#### :green[{point_pit}]""")
#                     st.markdown(f"""*{points.loc[point_pit, "Локализация"]}*""")
#                     st.markdown(f"""*{technika['pit']}*""")
#                 except:
#                     chan_pit = chan_pit.split()
#                     st.markdown("""#### Подходящие точки для питания в этом случае:""")
#                     for c in chan_pit:
#                         pp = re.search(f"{c}\d+", point_pit)[0]
#                         st.markdown(f"""#### :green[***{pp}***]""")
#                         try:
#                             st.markdown(f"""*{points.loc[pp, "Локализация"]}*""")
#                         except:
#                             st.markdown(f"""*Точки нет в базе данных*""")
#                     st.markdown(f"""*{technika['pit']}*""")                        

#             else:
#                 st.markdown(f"""*Одной иглой питание недостатка и Ке на застой не получится, - нет пересекающихся каналов*""")  
            
#                 for channal in canals_plus:
#                     st.markdown(f"""Застой в канале {channal} корректируем техникой 'тяни-толкай', точка:""")
#                     st.markdown(f"""**{table.loc[channal, 'Jing_Jin']}**""")
#                     st.markdown(f"""*{technika['JJ']}*""")

#             st.markdown("""--------------------------------------------------""")

#         ##### Gui #####
#         if wind:
#             t_gui = []
#             for i in di['Gui']:
#                 t_gui.append(table.loc[i, 'Gui'])
#             tt_gui = ', '.join(t_gui)
#             st.markdown(f"""#### Работа с Gui: :green[{tt_gui}]""")
#             for t in t_gui:
#                 st.markdown(f"""#### :green[***{t}***]""")            
#                 try:
#                     st.markdown(f"""*{points.loc[t, "Локализация"]}*""")
#                 except:
#                     st.markdown(f"""*Точки нет в базе данных*""")
#             st.markdown(f"""*{technika['gui']}*""") 


#         ##### Xue #####
#         if xue:
#             t_xue = []
#             for i in di['Xue']:
#                 t_xue.append(table.loc[i, 'Xue'])
#             tt_xue = ', '.join(t_xue)
#             st.markdown(f"""#### Работа с Xue: :green[{tt_xue}]""")
#             for t in t_xue:
#                 st.markdown(f"""#### :green[***{t}***]""")            
#                 try:
#                     st.markdown(f"""*{points.loc[t, "Локализация"]}*""")
#                 except:
#                     st.markdown(f"""*Точки нет в базе данных*""")
#             st.markdown(f"""*{technika['xue']}*""") 

#         pp = st.sidebar.text_input("Введите выбранные точки через запятую", "")
#         if pp:
#             st.markdown(f"""#### ***В этом сеансе поставлены точки:***""")
#             st.markdown(f"""#### **:blue[{pp}]**""")
#             # pp = pp.split(",")
#             # show_img = st.radio(
#             #     "Показать точки", ["нет", "да"]
#             # )
#             # if show_img=="да":
#             #     for p in pp:
#             #         p = p.strip().capitalize()
#             #         image_path = f"data/{p}.jpg"
#             #         image = Image.open(image_path)
#             #         st.image(image, width=300)

#             comments = st.text_area("Ваши комментарии", "")

            
#             ################################        Сохраняем пациента         ############################################

#             if st.sidebar.button("Save",type="primary"):
#                 # new_save = pd.DataFrame(
#                 #     index=[],
#                 #     data=[],
#                 #     columns=['Дата', 'ФИО', 'дата рождения', 'жалобы', 'метод лечения', 'застой', 'недостаток', 'блок', 'Gui', 
#                 #             'противоток', 'xue', 'пат.рост', 'жар', 'холод', 'сырость', 'сухость', 'лечение', 'комментарии']
#                 # )
#                 doh = None
#                 new_save = [datetime.now().date(), patient, born, complaints, method, canals_plus, canals_minus, block, wind,
#                         protivotok, xue, tree, fire, water, earth, metall, pp, comments, doh]

#                 with open('patients/patients.csv', 'a', encoding='utf-8') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(new_save) 
#                 file.close()
#                 # save_all = pd.read_csv("patients/patients.csv", index_col='Дата')
#                 # save_all = pd.concat([save_all, new_save], axis=0)#.drop_duplicates()
#                 # save_all.to_csv("patients/patients.csv")
#                 st.sidebar.markdown(""":green[***Файл успешно сохранён!***]""")
                
#                 # try:
#                 #     df_saved = pd.read_csv(f"patients/{patient}.csv", index_col='Unnamed: 0')
#                 #     save = pd.concat([df_saved, new_save], axis=0)#.drop_duplicates()
#                 #     save.to_csv(f"patients/{patient}.csv")
#                 #     # st.dataframe(save)
#                 #     st.sidebar.markdown(""":green[***Файл успешно сохранён!***]""")
#                 # except:
#                 #     new_save.to_csv(f"patients/{patient}.csv")

# ####################################   Лунные дворцы    ############################################


#     if method=="Лунные дворцы":
#         image_path = "data/Лунные дворцы.jpg"
#         image = Image.open(image_path)
#         st.image(image, width=600)
        
#         # Вводим пол пациента
#         sex = st.sidebar.selectbox(
#             "Выберете пол пациента",
#             ("", "Мужчина", "Женщина"),
#         )

#         doh = st.sidebar.text_input('Введите дату события', '')
#         if doh:
#             try:
#                 date = str(pd.to_datetime(doh, dayfirst=True)).split()[0] #input("Введите дату рождения")
#                 year = int(date[:4])
#                 month = int(date[5:7])
#                 day = int(date[8:])
#                 st.markdown(f'Дата события: **{pd.to_datetime(doh, dayfirst=True).strftime("%d.%m.%Y")}**')
#             except:
#                 st.error("*Некорректная дата. Попробуйте снова*")

#             for k, v in moon_palace.items():
#                 if year in v:
#                     first_step = k

#             if (year in vis_yaer) & (pd.to_datetime(date) > pd.to_datetime(f"{year}-02-28")):
#                 first_step = first_step+1

#             lunar_day = first_step + sec_step[month]+ day

#             while lunar_day > 28:
#                 lunar_day+=-28
#             st.markdown(f"Лунный день по дате события: **{lunar_day}**")
#             st.markdown(f"Янские точки дня: \t**{woman[lunar_day-1]}**")
#             st.markdown(f"Иньские точки дня: \t**{man[lunar_day-1]}**")
            
            
#             if lunar_day in range(1, 15):
#                 lunar_day = lunar_day+14
#             else:
#                 lunar_day = lunar_day-14
            
            
#             text_ld = ""
            
#             if sex == "Мужчина":
#                 points_ld = man[lunar_day-1]
#                 st.markdown(f"#### Точки по лунным дворцам: \t:green[{points_ld}]")
            
#             else:
#                 points_ld = woman[lunar_day-1]
#                 st.markdown(f"#### Точки по лунным дворцам: \t:green[{points_ld}]")

#             # points_ld = points_ld.split(', ')
#             # for el in points_ld:
#             #     elem = re.match("\D*", el)[0]
#             #     if elem in dnt_use:
#             #         st.warning(f"Точку **{el}** использовать нельзя!!!")
#             for p in points_ld.split(', '):
#                 st.markdown(f"#### :green[{p}]")
#                 try:
#                     st.markdown(f"""*{points.loc[p, "Локализация"]}*""")
#                 except:
#                     st.markdown(f"""*Точки нет в базе данных*""")
#             st.markdown(f"""*{technika['ld']}*""")

#         #################################################       Выбранные точки      ##################################################
        
#         pp = st.sidebar.text_input("Введите выбранные точки через запятую", "")
#         if pp:
#             st.markdown(f"""#### ***В этом сеансе поставлены точки:***""")
#             st.markdown(f"""#### **:blue[{pp}]**""")
#             # pp = pp.split(",")
#             # show_img = st.radio(
#             #     "Показать точки", ["нет", "да"]
#             # )
#             # if show_img=="да":
#             #     for p in pp:
#             #         p = p.strip().capitalize()
#             #         image_path = f"data/{p}.jpg"
#             #         image = Image.open(image_path)
#             #         st.image(image, width=300)

#             comments = st.text_area("Ваши комментарии", "")

            
#             ################################        Сохраняем пациента         ############################################

#             if st.sidebar.button("Save",type="primary"):
#                 # new_save = pd.DataFrame(
#                 #     index=[datetime.now().date()],
#                 #     data=[[patient, born, complaints, method, doh, pp, comments]],
#                 #     columns=['ФИО', 'дата рождения', 'жалобы', 'метод лечения', 'дата события', 'лечение', 'комментарии']
#                 # )
#                 canals_plus, canals_minus, block, wind, protivotok, xue, tree, fire, water, earth, metall = None, None, None, None, None, None, None, None, None, None, None
#                 new_save = [datetime.now().date(), patient, born, complaints, method, canals_plus, canals_minus, block, wind,
#                         protivotok, xue, tree, fire, water, earth, metall, pp, comments, doh]
#                 with open('patients/patients.csv', 'a', encoding='utf-8') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(new_save) 
#                 file.close()
#                 # save_all = pd.read_csv("patients/patients.csv", index_col='Дата')
#                 # save_all = pd.concat([save_all, new_save], axis=0)#.drop_duplicates()
#                 # save_all.to_csv("patients/patients.csv")               
#                 st.sidebar.markdown(""":green[***Файл успешно сохранён!***]""")
#                 # try:
#                 #     df_saved = pd.read_csv(f"patients/{patient}.csv", index_col='Unnamed: 0')
#                 #     save = pd.concat([df_saved, new_save], axis=0)
#                 #     # st.dataframe(save)
#                 #     save.to_csv(f"patients/{patient}.csv")
#                 #     st.sidebar.markdown(""":green[***Файл успешно сохранён!***]""")
#                 # except:
#                 #     new_save.to_csv(f"patients/{patient}.csv")
