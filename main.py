import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from database import *
import csv

window = tk.Tk()
window.title('Учёт автодеталей')
window.geometry('1000x600')

frame_add_details = tk.Frame(window, width=150, height=150)
frame_filter = tk.Frame(window, width=150, height=150)
frame_list = tk.Frame(window, width=300, height=200)

frame_add_details.place(relx=0, rely=0, relwidth=0.5, relheight=0.4)
frame_filter.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.4)
frame_list.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

min_price = -1000
max_price = 9999999999999
min_amount = -1000
max_amount = 9999999999999
chosen_makers = makers_list
search_substr = ''
search_substr_cap = ''


def create_list():
    frame_list = tk.Frame(window, width=300, height=200, bg='blue')
    frame_list.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
    global res
    with db:
        res = Component.select().where(Component.amount != 0)
        comp_list = []
        for row in res:
            comp_list.append((row.id, row.title, row.article, row.maker, row.amount, row.price))

    table = ttk.Treeview(frame_list, show='headings')
    heads = ['id', 'Название', 'Артикул', 'Производитель', 'Количество', 'Цена']
    table['columns'] = heads
    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')
    for row in comp_list:
        table.insert('', tk.END, values=row)
    table.column('id', width=40)
    table.column('Артикул', width=100)
    table.column('Количество', width=40)
    scroll_pane = ttk.Scrollbar(frame_list, command=table.yview)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.configure(yscrollcommand=scroll_pane.set)
    table.pack(expand=tk.YES, fill=tk.BOTH)


create_list()


def create_filtered_list(res):
    frame_list = tk.Frame(window, width=300, height=200, bg='blue')
    frame_list.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
    with db:
        # res = Component.select().where(Component.amount != 0)
        comp_list = []
        for row in res:
            comp_list.append((row.id, row.title, row.article, row.maker, row.amount, row.price))

    table = ttk.Treeview(frame_list, show='headings')
    heads = ['id', 'Название', 'Артикул', 'Производитель', 'Количество', 'Цена']
    table['columns'] = heads
    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')
    for row in comp_list:
        table.insert('', tk.END, values=row)
    table.column('id', width=40)
    table.column('Артикул', width=100)
    table.column('Количество', width=40)
    scroll_pane = ttk.Scrollbar(frame_list, command=table.yview)
    scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
    table.configure(yscrollcommand=scroll_pane.set)
    table.pack(expand=tk.YES, fill=tk.BOTH)


def start_window_add():
    window_add = tk.Toplevel(window)
    window_add.title('Добавление товара')
    window_add.geometry('400x250')

    add_title_f = ttk.Entry(window_add, width=35)
    add_title_f.place(relx=0.4, rely=0.1)
    add_title_l = ttk.Label(window_add, text='Введите название')
    add_title_l.place(relx=0.1, rely=0.1)

    add_maker_f = ttk.Entry(window_add, width=25)
    add_maker_f.place(relx=0.5, rely=0.2)
    add_maker_l = ttk.Label(window_add, text='Введите производителя')
    add_maker_l.place(relx=0.1, rely=0.2)

    add_article_f = ttk.Entry(window_add, width=25)
    add_article_f.place(relx=0.5, rely=0.3)
    add_article_l = ttk.Label(window_add, text='Введите артикул')
    add_article_l.place(relx=0.1, rely=0.3)

    add_price_f = ttk.Entry(window_add, width=25)
    add_price_f.place(relx=0.5, rely=0.4)
    add_price_l = ttk.Label(window_add, text='Введите цену')
    add_price_l.place(relx=0.1, rely=0.4)

    add_amount_f = ttk.Entry(window_add, width=25)
    add_amount_f.place(relx=0.5, rely=0.5)
    add_amount_l = ttk.Label(window_add, text='Введите количество')
    add_amount_l.place(relx=0.1, rely=0.5)

    def add_components():
        add_component_dict = {
            'title': add_title_f.get().capitalize(),
            'article': add_article_f.get(),
            'maker': add_maker_f.get().capitalize(),
            'price': add_price_f.get(),
            'amount': add_amount_f.get(),
            'updated_date': datetime.datetime.now()
        }
        if add_article_f.get() == '' or add_maker_f.get() == '' or add_title_f.get() == '' or add_amount_f.get() == '':
            mbox.askokcancel('Ошибка при добавлении товара', 'Не заполнены некоторые поля')
        elif add_article_f.get().isdigit() and add_price_f.get().isdigit() and add_amount_f.get().isdigit()\
                and not add_maker_f.get().isdigit() and not add_title_f.get().isdigit():
            mbox.askokcancel('Ошибка при добавлении товара',
                             'Возможно, вы ввели числа туда, где должен быть текст или наоборот')
        else:
            with db:
                query = Component.select().where(add_article_f.get() == Component.article &
                                                 add_maker_f.get() == Component.maker &
                                                 add_title_f.get() == Component.title)
            if len(query) > 0:  # сделал тут Shift+Tab до create_list
                Component.update(amount=Component.amount + add_amount_f.get(),
                                 updated_date=datetime.datetime.now()).where(
                    Component.article == add_article_f.get()).execute()
            else:
                Component.insert(add_component_dict).execute()
            frame_list.destroy()
            create_list()

    button_add_final = tk.Button(window_add, text='Добавить', command=add_components)
    button_add_final.place(relx=0.4, rely=0.7)


button_add = tk.Button(frame_add_details, text='Добавить товар', command=start_window_add)
button_add.place(relx=0.1, rely=0.1)


def start_window_del():
    window_del = tk.Toplevel(window)
    window_del.title('Удаление товара')
    window_del.geometry('400x300')

    del_article_f = ttk.Entry(window_del, width=25)
    del_article_f.place(relx=0.5, rely=0.1)
    del_article_l = ttk.Label(window_del, text='Введите артикул')
    del_article_l.place(relx=0.1, rely=0.1)

    del_amount_f = ttk.Entry(window_del, width=25)
    del_amount_f.place(relx=0.5, rely=0.2)
    del_amount_l = ttk.Label(window_del, text='Введите количество')
    del_amount_l.place(relx=0.1, rely=0.2)

    def del_components():
        if del_article_f.get() == '' or del_amount_f.get() == '':
            mbox.askokcancel('Ошибка при удалении товара', 'Не заполнены некоторые поля')
        elif not (del_article_f.get().isdigit() and del_amount_f.get().isdigit()):
            mbox.askokcancel('Ошибка при удалении товара',
                             'Возможно, вы ввели числа туда, где должен быть текст или наоборот')
        else:
            with db:
                query = Component.select().where(del_article_f.get() == Component.article)
            if len(query) > 0:
                Component.update(amount=Component.amount - del_amount_f.get(),
                                 updated_date=datetime.datetime.now()).where(
                    Component.article == del_article_f.get()).execute()
                Component.update(amount=0, updated_date=datetime.datetime.now()).where(Component.amount < 0).execute()
            else:
                mbox.askokcancel('Ошибка при удалении товара', 'Несуществующий артикул')
            frame_list.destroy()
            create_list()

    button_del_final = tk.Button(window_del, text='Удалить', command=del_components)
    button_del_final.place(relx=0.4, rely=0.7)


button_del = tk.Button(frame_add_details, text='Удалить товар (по артикулу)', command=start_window_del)
button_del.place(relx=0.1, rely=0.25)


def start_window_edit():
    window_edit = tk.Toplevel(window)
    window_edit.title('Редактирование товара')
    window_edit.geometry('550x300')

    edit_title_f = ttk.Entry(window_edit, width=35)
    edit_title_f.place(relx=0.4, rely=0.1)
    edit_title_l = ttk.Label(window_edit, text='Введите новое название')
    edit_title_l.place(relx=0.1, rely=0.1)

    edit_maker_f = ttk.Entry(window_edit, width=25)
    edit_maker_f.place(relx=0.5, rely=0.2)
    edit_maker_l = ttk.Label(window_edit, text='Введите нового производителя')
    edit_maker_l.place(relx=0.1, rely=0.2)

    edit_article_f = ttk.Entry(window_edit, width=25)
    edit_article_f.place(relx=0.5, rely=0.3)
    edit_article_l = ttk.Label(window_edit, text='Введите новый артикул')
    edit_article_l.place(relx=0.1, rely=0.3)

    edit_price_f = ttk.Entry(window_edit, width=25)
    edit_price_f.place(relx=0.5, rely=0.4)
    edit_price_l = ttk.Label(window_edit, text='Введите новую цену')
    edit_price_l.place(relx=0.1, rely=0.4)

    edit_amount_f = ttk.Entry(window_edit, width=25)
    edit_amount_f.place(relx=0.5, rely=0.5)
    edit_amount_l = ttk.Label(window_edit, text='Введите новое количество')
    edit_amount_l.place(relx=0.1, rely=0.5)

    edit_id_f = ttk.Entry(window_edit, width=25)
    edit_id_f.place(relx=0.5, rely=0.6)
    edit_id_l = ttk.Label(window_edit, text='Введите id. Это значение не изменится!')
    edit_id_l.place(relx=0.1, rely=0.6)

    def edit_components():
        if edit_article_f.get() == '' or edit_amount_f.get() == '' or edit_maker_f.get() == '' \
                or edit_price_f.get() == '' or edit_title_f.get() == '' or edit_id_f.get() == '':
            mbox.askokcancel('Ошибка при редактировании товара', 'Не заполнены некоторые поля')
        elif not (edit_article_f.get().isdigit() and edit_amount_f.get().isdigit() and not edit_maker_f.get().isdigit()
        and edit_price_f.get().isdigit() and not edit_title_f.get().isdigit() and edit_id_f.get().isdigit()):
            mbox.askokcancel('Ошибка при редактировании товара',
                             'Возможно, вы ввели числа туда, где должен быть текст или наоборот')
        else:
            with db:
                query = Component.select().where(Component.id == edit_id_f.get())
            if len(query) > 0:
                Component.update(title=edit_title_f.get(), maker=edit_maker_f.get(), article=edit_article_f.get(),
                                 price=edit_price_f.get(), amount=edit_amount_f.get(),
                                 updated_date=datetime.datetime.now())\
                    .where(Component.id == edit_id_f.get()).execute()
            else:
                mbox.askokcancel('Ошибка при редактировании товара', 'Несуществующий id')
            frame_list.destroy()
            create_list()

    button_edit_final = tk.Button(window_edit, text='Сохранить значения', command=edit_components)
    button_edit_final.place(relx=0.4, rely=0.7)


button_edit = tk.Button(frame_add_details, text='Редактировать товар (по id)', command=start_window_edit)
button_edit.place(relx=0.1, rely=0.40)


def start_window_filter():
    window_filter = tk.Toplevel(window)
    window_filter.title('Настройка фильтра')
    window_filter.geometry('550x300')

    filter_maker_l = ttk.Label(window_filter, text='Зажав Ctrl, отберите нужных производителей. Листайте колёсиком')
    filter_maker_l.place(relx=0.05, rely=0)

    filter_amount_l = ttk.Label(window_filter, text='MIN и MAX значения количества')
    filter_amount_l.place(relx=0.35, rely=0.2)
    filter_amount_f_min = ttk.Entry(window_filter, width=5)
    filter_amount_f_min.place(relx=0.75, rely=0.2)
    filter_amount_f_max = ttk.Entry(window_filter, width=5)
    filter_amount_f_max.place(relx=0.85, rely=0.2)

    filter_price_l = ttk.Label(window_filter, text='MIN и MAX значения цены')
    filter_price_l.place(relx=0.35, rely=0.3)
    filter_price_f_min = ttk.Entry(window_filter, width=10)
    filter_price_f_min.place(relx=0.65, rely=0.3)
    filter_price_f_max = ttk.Entry(window_filter, width=10)
    filter_price_f_max.place(relx=0.85, rely=0.3)

    lb = tk.Listbox(window_filter, selectmode='extended')
    for item in makers_list:
        lb.insert(tk.END, item)
    lb.place(relx=0.1, rely=0.1)

    def filter_ex():
        global chosen_makers
        for item in lb.curselection():
            chosen_makers.append(makers_list[item])
        if len(chosen_makers) == 0:
            chosen_makers = makers_list
        global min_price
        global max_price
        global min_amount
        global max_amount
        min_price = filter_price_f_min.get()
        max_price = filter_price_f_max.get()
        min_amount = filter_amount_f_min.get()
        max_amount = filter_amount_f_max.get()
        if not (min_price.isdigit() and max_price.isdigit() and min_amount.isdigit() and max_amount.isdigit()):
            mbox.askokcancel('Ошибка при настройке фильтра',
                             'Возможно, вы ввели числа туда, где должен быть текст или наоборот')
        if min_price == '':
            min_price = -1000.0
        if max_price == '':
            max_price = 9999999999999
        if min_amount == '':
            min_amount = -1000
        if max_amount == '':
            max_amount = 9999999999999
        with db:
            res = Component.select().where((Component.maker << chosen_makers)
                                            & (Component.price.between(min_price, max_price))
                                           & (Component.amount.between(min_amount, max_amount)))
        frame_list.destroy()
        create_filtered_list(res)
        print(len(chosen_makers))

    button_filter_ex = tk.Button(window_filter, text='Применить фильтр', command=filter_ex)
    button_filter_ex.place(relx=0.45, rely=0.8)


button_filter = tk.Button(frame_add_details, text='Настроить фильтр', command=start_window_filter)
button_filter.place(relx=0.1, rely=0.55)


def restart_list():
    frame_list.destroy()
    create_list()

    global min_price
    global max_price
    global min_amount
    global max_amount
    global chosen_makers
    global search_substr

    min_price = -1000
    max_price = 9999999999999
    min_amount = -1000
    max_amount = 9999999999999
    chosen_makers = makers_list
    search_substr = ''


button_filter_reset = tk.Button(frame_add_details, text='Сбросить фильтр и поиск', command=restart_list)
button_filter_reset.place(relx=0.6, rely=0.55)

def search():
    global min_price
    global max_price
    global min_amount
    global max_amount
    global chosen_makers
    global search_substr
    global search_substr_cap

    search_substr = search_f.get().lower()
    search_substr_cap = search_substr.capitalize()

    with db:
        res = Component.select().where((Component.maker << chosen_makers)
                                       & (Component.price.between(min_price, max_price))
                                       & (Component.amount.between(min_amount, max_amount))
                                       & (Component.title.contains(search_substr) |
                                          Component.title.contains(search_substr_cap) |
                                          Component.maker.contains(search_substr) |
                                          Component.maker.contains(search_substr_cap) |
                                          Component.article.contains(search_substr) |
                                          Component.id.contains(search_substr)))

    frame_list.destroy()
    create_filtered_list(res)


search_f = ttk.Entry(window, width=50)
search_f.place(relx=0.6, rely=0.15)
button_search = tk.Button(window, text='Поиск', command=search)
button_search.place(relx=0.6, rely=0.2)


def save_csv():
    with open("saved_components.csv", mode="w", encoding='cp1251') as w_file:
        global min_price
        global max_price
        global min_amount
        global max_amount
        global chosen_makers
        global search_substr
        global search_substr_cap

        with db:
            res = Component.select().where((Component.maker << chosen_makers)
                                           & (Component.price.between(min_price, max_price))
                                           & (Component.amount.between(min_amount, max_amount))
                                           & (Component.title.contains(search_substr) |
                                              Component.title.contains(search_substr_cap) |
                                              Component.maker.contains(search_substr) |
                                              Component.maker.contains(search_substr_cap) |
                                              Component.article.contains(search_substr) |
                                              Component.id.contains(search_substr)))
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow(['id', 'Название', 'Артикул', 'Производитель', 'Количество', 'Цена'])
        for row in res:
            file_writer.writerow([row.id, row.title, row.article, row.maker, row.amount, row.price])

button_save = tk.Button(window, text='Сохранить результат в csv-файл', command=save_csv)
button_save.place(relx=0.6, rely=0.3)

window.mainloop()
