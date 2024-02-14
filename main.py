from tkinter import *
from tkinter import messagebox as msg
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import keyboard
import os 
import random

try:
    time_selected = 2
    type_selected = 1

    start_main_check = 0
    show_result_check = 0

    quote = ''
    wrt_st = ''
    allowed_chars = [
        "abcdefghijklmnopqrstuvwxyz. \n",
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ. \n",
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[]{}\|;:'\",./<>? \n"
    ]
    arrow_keys = ('Up', 'Down', 'Left', 'Right')

    quote_list = []
    quote_pt = 0

    final_word_count = 0
    current_word_count = 0
    start_time = 0
    current_time = 0
    end_time = 0
    mistake_count = 0
    accuracy = 0
    wpm = 0
    current_wpm = 0
    vis = 0
    y_wpm = np.array([])
    right_now = datetime.now().strftime('Date_%d-%m-%Y_Time_%H-%M-%S')
    now = right_now[21:29]
    today = right_now[5:15]
    box = 0

    def get_time(s):
        return int(s.get()[0])

    def get_type(s):
        global quote_list, quote_pt, quote
        s = s.get()
        if s == 'Only Lowercase':
            file = open('src/lower.txt', 'r')
            quote_list = file.read()
            quote_list = quote_list.split('\n')
            quote_pt = random.randint(0, len(quote_list)-1)
            quote += quote_list[quote_pt]
            file.close()
            return 0
        elif s == 'Lower + Upper':
            file = open('src/lower_upper.txt', 'r')
            quote_list = file.read()
            quote_list = quote_list.split('\n')
            quote_pt = random.randint(0, len(quote_list)-1)
            quote += quote_list[quote_pt]
            file.close()
            return 1
        else:
            file = open('src/ALL.txt', 'r')
            quote_list = file.read()
            quote_list = quote_list.split('\n')
            quote_pt = random.randint(0, len(quote_list)-1)
            quote += quote_list[quote_pt]
            file.close()
            return 2

    def start_main(s1, s2):
        global time_selected, type_selected, start_main_check
        time_selected = get_time(s1)
        type_selected = get_type(s2)
        start.destroy()
        start_main_check = 1
        return None

    start = Tk()
    wid, hei = 500, 400
    start.title('Typing Speed Tester')
    start.geometry(f'{wid}x{hei}+500+150')
    start.minsize(wid, hei)
    start.maxsize(wid, hei)

    title = Frame(start, bg = '#262626', height = 40)
    title_lbl = Label(title, text = 'Welcome to Typing Speed Tester', font = ('Lucida', 17, 'bold'), fg = 'white', bg = '#262626')
    title_lbl.pack()
    title.place(x = 0, y = 0, relwidth = 1)


    timer_list = [str(i)+' min' for i in range(1, 9)]
    timer_value = StringVar()
    timer_value.set('2 min')
    timer_lbl = Label(start, text = 'Time: ', font = ('Times new Roman', 14))
    timer_lbl.place(x = 170, y = 140)
    timer_menu = OptionMenu(start, timer_value, *timer_list)
    timer_menu.config(width = 8)
    timer_menu.place(x = 220, y = 138)

    type_list = ['Only Lowercase', 'Lower + Upper', 'Lower + Upper + Special']
    type_lbl = Label(start, text = 'Type: ', font = ('Times new Roman', 14))
    type_lbl.place(x = 130, y = 185)
    type_value = StringVar()
    type_value.set(type_list[1])
    type_menu = OptionMenu(start, type_value, *type_list)
    type_menu.config(width = 20)
    type_menu.place(x = 180, y = 183)

    ok_btn = Button(start, text = 'OK', command = lambda: start_main(timer_value, type_value), width = 10, bg = 'silver', font = ('Monospace', 12))
    ok_btn.place(x = 200, y = 300)

    start.mainloop()


    last_tag = []

    def click(event):
        return 'break'

    def check(event):
        global wrt_st, last_tag, quote, mistake_count, vis, quote, quote_pt
        wrt_st = txt_area.get('1.0', 'end-1c')
        if event.keysym == 'BackSpace':
            wrt_st = wrt_st[:-1]
        elif event.keysym in arrow_keys or event.char not in allowed_chars[type_selected]:
            return 'break'
        
        wrt_st += event.char
        if len(wrt_st) > vis and event.keysym != 'BackSpace':
            if event.char != quote[vis]:
                mistake_count += 1
            vis += 1
        if len(quote) - len(wrt_st) < 16:
            quote_pt = (quote_pt + 1) % len(quote_list)
            quote += quote_list[quote_pt]
            para_text.config(state = NORMAL)
            para_text.insert(INSERT, quote_list[quote_pt].strip('\n'))
            para_text.see(END)
            para_text.config(state = DISABLED)
            txt_area.focus_set()
        
        for tag in last_tag:
            para_text.tag_remove(tag[0], tag[1], tag[2])
        last_tag.clear()
        
            
        st_len = len(wrt_st)
        for i in range(st_len):
            tag = ['', f'1.{i}', f'1.{i+1}']
            if wrt_st[i] == quote[i]:
                tag[0] = 'correct'
            else:
                tag[0] = 'incorrect'
            para_text.tag_add(tag[0], tag[1], tag[2])
            last_tag.append(tag)

        if event.keysym == 'BackSpace' and len(last_tag):
            tag = last_tag[-1]
            para_text.tag_remove(tag[0], tag[1], tag[2])
            last_tag.pop()


    def countdown():
        global start_time, current_time, current_word_count, current_wpm, y_wpm
        txt_area.config(state=DISABLED)
        while True:
            a = keyboard.read_key()
            if len(a) == 1 and a.isalpha():
                txt_area.config(state=NORMAL)
                break
        start_time = time.time()
        txt_area.focus_force()
        txt_area.focus_set()
        min_time = int(time_selected)
        sec_time = 0
        while min_time > 0 or sec_time > 0:
            if sec_time == 0 and min_time > 0:
                sec_time = 59
                min_time -= 1
            else:
                sec_time -= 1
            min_box.config(text = str(min_time).rjust(2, '0'))
            sec_box.config(text = str(sec_time).rjust(2, '0'))
            time.sleep(1)
            current_time = time.time()
            current_word_count = len(txt_area.get('1.0', 'end-1c').split())
            try:
                current_wpm = (current_word_count / (current_time - start_time) * 60)
            except ZeroDivisionError:
                current_wpm = 1
            
            y_wpm = np.append(y_wpm, current_wpm)
        stop_type()
        

    def stop_type():
        global end_time, final_word_count, wpm, accuracy, mistake_count, show_result_check
        show_result_check = 1
        end_time = time.time()
        
        final_word_count = len(txt_area.get('1.0', 'end-1c').split())
        try:
            wpm = round(y_wpm[-1])
            accuracy = round((1 - (mistake_count/vis))*100)
        except:
            wpm = 0
            accuracy = 0
        
        file = open('data.csv', 'a')
        file.write(f'{today},{now}\n')
        file.close()
        
        results = np.array([wpm, accuracy, mistake_count])
        np.savez(f'History/Date_{today}_Time_{now}.npz', results, y_wpm)
        main.destroy()

    if not start_main_check:
        exit()

    main = Tk()
    main.title('Typing Speed Tester')
    wid, hei = 900, 600
    main.geometry(f'{wid}x{hei}+300+100')
    main.minsize(wid, hei)
    main.maxsize(wid, hei)

    title = Frame(main, bg = '#262626', height = 40)
    title_lbl = Label(title, text = 'Welcome to Typing Speed Tester', font = ('Lucida', 17, 'bold'), fg = 'white', bg = '#262626')
    title_lbl.pack()
    title.place(x = 0, y = 0, relwidth = 1)


    min_box = Label(main, text = str(time_selected).rjust(2, '0'), width=2, font=('Lucida', 20, 'bold'), fg = 'black', bg = 'white')
    min_box.place(x = 750, y = 40)
    sec_box = Label(main, text = '00', width=2, font=('Lucida', 20, 'bold'), fg = 'black', bg = 'white')
    sec_box.place(x = 810, y = 40)
    col_lbl = Label(main, text = ':', font = 30)
    col_lbl.place(x = 795, y = 42)
    min_lbl = Label(main, text = 'min', font = 13, width = 4)
    min_lbl.place(x = 744, y = 73)
    sec_lbl = Label(main, text = 'sec', font = 13, width = 4)
    sec_lbl.place(x = 806, y = 73)


    para_text = Text(main, bg = 'white', font = ('Cascadia Code', 15), width = 65, height = 5, padx = 30, pady = 30, bd = 2, relief = SUNKEN, wrap = 'word')
    para_text.place(x = 30, y = 100)
    para_text.insert(INSERT, quote)
    para_text.tag_config('correct', foreground = 'green')
    para_text.tag_config('incorrect', foreground = 'red')
    para_text.config(state=DISABLED)

    txt_area = Text(main, bg = 'white', height = 6, width = 65, font = ('Cascadia Code', 15), padx = 30, pady = 30, bd = 2, relief = SUNKEN, wrap = 'word')
    txt_area.place(x = 30, y = 310)
    txt_area.bind('<Key>', check)
    txt_area.bind('<Button-1>', click)
    txt_area.focus_force()
    threading.Thread(target=countdown).start()

    stop_btn = Button(main, text = 'Stop', bg = '#DF6969', width = 10, font = 17, command = stop_type)
    stop_btn.place(x = 400, y = 547)

    main.mainloop()

    if show_result_check == 0:
        exit()


    def perf_page(dt, tm):
        try:
            file = np.load(f'History/Date_{dt}_Time_{tm}.npz')
        except:
            Label(main_frame, text = 'No records', font = 30).pack(expand = True, fill = BOTH)
            return
        res = file['arr_0']
        data = file['arr_1']
        x_axis = np.arange(1, len(data)+1)
        
        wpm_res.config(text = res[0])
        acc_res.config(text = str(res[1]) + ' %')
        err_res.config(text = res[2])
        
        fig = Figure(figsize = (5,5), dpi = 100)
        plot = fig.add_subplot(111)
        plot.set_xlabel('Time (seconds)')
        plot.set_ylabel('Words per Minute')
        plot.set_title(f'Perfomance\nDate: {dt}  Time: {tm}')
        plot.plot(x_axis, data)
        
        
        canvas = FigureCanvasTkAgg(fig, master = main_frame)
        canvas.get_tk_widget().pack()
        
        plt.show()

    def hist(event):
        st = box.get(box.curselection()).strip().split()
        dt = st[0]
        tm = st[1]
        indicate(prf_indc, perf_page, dt, tm)

    def hist_page(dt, tm):
        global box
        main_frame.config(bg='#c3c3c3')
        file = pd.read_csv('data.csv')
        
        date_lbl = Label(main_frame, text = 'Date', font = ('bold', 18), bg = '#c3c3c3')
        date_lbl.place(x = 130, y = 0)
        
        time_lbl = Label(main_frame, text = 'Time', font = ('bold', 18), bg = '#c3c3c3')
        time_lbl.place(x = 313, y = 0)
        
        date_fmt_lbl = Label(main_frame, text = '(MM-DD-YYYY)', bg = '#c3c3c3')
        date_fmt_lbl.place(x = 110, y = 28, relwidth=0.2)
        
        time_fmt_lbl = Label(main_frame, text = '(HH-MM-SS)', bg = '#c3c3c3')
        time_fmt_lbl.place(x = 293, y = 28, relwidth=0.2)
        
        f = Frame(main_frame, bg = '#c3c3c3', height= 455)
        f.place(x = 2, y = 50, relwidth=0.99)
        box = Listbox(f, bg = 'white', font = (20), justify = CENTER, height = 20)
        for i in range(len(file)-1, -1, -1):
            box.insert(END, file['Date'][i] + '               ' + file['Time'][i])
        box.place(x = 0, y = 0, relwidth = 1)
        box.bind('<Double-1>', hist)
        
        vsb = Scrollbar(f, orient = VERTICAL, command = box.yview)
        box.configure(yscrollcommand = vsb)
        vsb.place(x = 470, y = 2, relheight=1)
        

    def indicate(lbl, page, dt, tm):
        for frame in main_frame.winfo_children():
            frame.destroy()
        prf_indc.config(bg = '#c3c3c3')
        hst_indc.config(bg = '#c3c3c3')
        lbl.config(bg = '#158aff')
        page(dt, tm)

    def clr_hst():
        flg = msg.askyesno('', 'Are you sure want to clear History?')
        if not flg:
            return
        file = pd.read_csv('data.csv')
        for i in range(len(file)):
            dt = file['Date'][i]
            tm = file['Time'][i]
            os.remove(f'History/Date_{dt}_Time_{tm}.npz')
        file = open('data.csv', 'w')
        file.write('Date,Time\n')
        file.close()
        wpm_res.config(text = '--')
        acc_res.config(text = '--')
        err_res.config(text = '--')
        hist_page(dt, tm)

    result = Tk()
    wid, hei = 900, 550
    result.title('Typing Speed Tester')
    result.geometry(f'{wid}x{hei}+300+100')
    result.minsize(wid, hei)
    result.maxsize(wid, hei)

    title = Frame(result, bg = '#262626', height = 40)
    title_lbl = Label(title, text = 'Results', font = ('Lucida', 17, 'bold'), fg = 'white', bg = '#262626')
    title_lbl.pack()
    title.place(x = 0, y = 0, relwidth = 1)

    menu_frame = Frame(result, bg = '#c3c3c3', width = 200, height=514, bd=3, relief=GROOVE)

    prf_lbl = Button(menu_frame, text = 'Performance', bg = '#c3c3c3', font = ('Times new Roman', 20, 'bold'), bd = 0, command = lambda:indicate(prf_indc, perf_page, today, now))
    prf_lbl.place(x = 12, y = 50)
    hst_lbl = Button(menu_frame, text = 'History', bg = '#c3c3c3', font = ('Times new Roman', 20, 'bold'), bd = 0, command = lambda:indicate(hst_indc, hist_page, today, now))
    hst_lbl.place(x = 12, y = 100)

    prf_indc = Label(menu_frame, text = '', bg = '#c3c3c3', height = 3)
    prf_indc.place(x = 5, y = 50)
    hst_indc = Label(menu_frame, text = '', bg = '#c3c3c3', height = 3)
    hst_indc.place(x = 5, y = 100)

    hst_clr = Button(menu_frame, text = 'Clear History', font = 18, width=13, command = clr_hst)
    hst_clr.place(x = 22, y = 450)

    menu_frame.place(x = 3, y = 35)

    main_frame = Frame(result, bg = '#c3c3c3', width = 500, height=514, bd=3, relief=GROOVE)
    main_frame.pack_propagate(False)
    main_frame.place(x = 207, y = 35)

    data_frame = Frame(result, width = 190, height=514, bd = 3, relief=GROOVE)

    wpm_lbl = Label(data_frame, text = 'WPM', font = ('Lucida', 20, 'bold'))
    wpm_lbl.place(y = 75, relwidth=1)
    wpm_res = Label(data_frame, text = '', font = ('Lucida', 18, 'bold'))
    wpm_res.place(y = 110, relwidth=1)

    acc_lbl = Label(data_frame, text = 'Accuracy', font = ('Lucida', 20, 'bold'))
    acc_lbl.place(y = 195, relwidth=1)
    acc_res = Label(data_frame, text = '', font = ('Lucida', 18, 'bold'))
    acc_res.place(y = 230, relwidth=1)

    err_lbl = Label(data_frame, text = 'Errors', font = ('Lucida', 20, 'bold'))
    err_lbl.place(y = 315, relwidth=1)
    err_res = Label(data_frame, text = '', font = ('Lucida', 18, 'bold'))
    err_res.place(y = 350, relwidth=1)

    data_frame.place(x = 710, y = 35)
    indicate(prf_indc, perf_page, today, now)
    result.mainloop()
except RuntimeError:
    pass