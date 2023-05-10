from tkinter import ttk
from tkinter import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

global EQE

# 创建窗口、名字、设定大小


def GUI(shared_dipolePosition=None,
        shared_horizontalRatio=None,
        shared_refractIndex_far=None,
        shared_names=None,
        shared_thickLayer=None,
        shared_refractIndex=None,
        shared_waveLength1=None,
        shared_waveLength2=None,
        shared_EQE=None,
        shared_angle=None,
        shared_wave=None,
        shared_Luminance=None,
        shared_Spectrum=None,
        shared_GUI_flag=None,
        lock=None):

    def loopMaker():
        global EQE
        EQE = shared_EQE
        text1.delete(0.0, END)
        text1.insert(INSERT, EQE)
        text1.update()
        window.after(1000, loopMaker)

    window = Tk()
    window.title('GUI')
    window.geometry("{}x{}".format(1400, 900))
    # 分成多个子框架
    frame = Frame(window)
    frame.grid()
    frame_input = Frame(frame)
    frame_input.grid(row=0, column=0)
    frame_refract = Frame(frame_input)
    frame_other = Frame(frame_input)
    frame_refract.grid(row=1, column=0)
    frame_other.grid(row=3, column=0)

    frame_output = Frame(frame)
    frame_output.grid(row=0, column=1)
    text1 = Text(frame_output)
    text1.grid(row=1, column=0)
    window.after(1000, loopMaker)

    Label(frame_input, text='OLED结构').grid(row=0, column=0)
    Label(frame_other, text='其他输入条件').grid(row=2, column=0)
    Label(frame_output, text='外量子效率').grid(row=0, column=0)
    Label(frame_output, text='亮度分布和远场辐射光谱').grid(row=2, column=0)

    # OLED结构表格部分

    columns = ("材料", "厚度(nm)", "折射率(a+bj)")
    struction = ttk.Treeview(frame_refract, height=30, show="headings", columns=columns)
    struction.column(columns[0], width=100, anchor='center')
    struction.column(columns[1], width=100, anchor='center')
    struction.column(columns[2], width=100, anchor='center')
    struction.heading(columns[0], text="材料")
    struction.heading(columns[1], text="厚度(nm)")
    struction.heading(columns[2], text="折射率(a+bj)")
    struction.grid()

    matrial = []
    width = []
    refract = []
    for i in range(min(len(matrial), len(width), len(refract))):
        struction.insert('', i, values=(matrial[i], width[i], refract[i]))

    def set_cell_value(event):
        for item in struction.selection():
            item_text = struction.item(item, "values")
        column = struction.identify_column(event.x)
        row = struction.identify_row(event.y)
        cn = int(str(column).replace('#', ''))
        rn = int(str(row).replace('I', ''))
        entryedit = Text(frame_refract, width=10, height=1)
        entryedit.place(x=20+(cn-1)*100, y=6+rn*20)

        def saveedit():
            struction.set(item, column=column, value=entryedit.get(0.0, "end"))
            entryedit.destroy()
            okb.destroy()
        okb = Button(frame_refract, text="√", width=2, command=saveedit)
        okb.place(x=80+(cn-1)*100, y=2+rn*20)

    def newrow():
        matrial.append('材料名称')
        width.append('厚度(nm)')
        refract.append('折射率(a+bj)')
        struction.insert('', len(matrial)-1, values=(matrial[
                len(matrial)-1], width[len(matrial)-1], refract[len(matrial)-1]))
        struction.update()
        newb.place(x=50, y=(len(matrial)-1)*20+70)
        newb.update()

    struction.bind('<Double-1>', set_cell_value)

    newb = Button(frame_refract, text='+', width=20, command=newrow)
    newb.place(x=50, y=(len(matrial)-1)*20+70)

    Label(frame_other, text="输入发光偶极子处在第几层:").grid(row=0, column=0)
    Label(frame_other, text="输入水平偶极子所占比例（0~1）:").grid(row=1, column=0)
    Label(frame_other, text="远场接收区域的折射率，远场区域不影响偶极子辐射:").grid(row=2, column=0)
    Label(frame_other, text="亮度分布的波长下限:").grid(row=3, column=0)
    Label(frame_other, text="亮度分布的波长上限:").grid(row=4, column=0)
    Label(frame_other, text="远场辐射的波长下限:").grid(row=5, column=0)
    Label(frame_other, text="远场辐射光谱的波长上限:").grid(row=6, column=0)

    dipolePosition1 = StringVar()
    e1 = Entry(frame_other, textvariable=dipolePosition1)
    e1.grid(row=0, column=1)

    horizontalRatio1 = StringVar()
    e2 = Entry(frame_other, textvariable=horizontalRatio1)
    e2.grid(row=1, column=1)

    refractIndex_far1 = StringVar()
    e3 = Entry(frame_other, textvariable=refractIndex_far1)
    e3.grid(row=2, column=1)

    waveLength1_1 = StringVar()
    e4 = Entry(frame_other, textvariable=waveLength1_1)
    e4.grid(row=3, column=1)

    waveLength2_1 = StringVar()
    e5 = Entry(frame_other, textvariable=waveLength2_1)
    e5.grid(row=4, column=1)

    waveLength3_1 = StringVar()
    e6 = Entry(frame_other, textvariable=waveLength3_1)
    e6.grid(row=5, column=1)

    waveLength4_1 = StringVar()
    e7 = Entry(frame_other, textvariable=waveLength4_1)
    e7.grid(row=6, column=1)

    def finish():
        dipolePosition = int(dipolePosition1.get())
        horizontalRatio = float(horizontalRatio1.get())
        refractIndex_far = float(refractIndex_far1.get())
        waveLength1 = int(waveLength1_1.get())
        waveLength2 = int(waveLength2_1.get())
        waveLength3 = int(waveLength3_1.get())
        waveLength4 = int(waveLength4_1.get())
        shared_dipolePosition.append(dipolePosition)
        shared_horizontalRatio.append(horizontalRatio)
        shared_refractIndex_far.append(refractIndex_far)
        shared_waveLength1.append(waveLength1)
        shared_waveLength1.append(waveLength2)
        shared_waveLength2.append(waveLength3)
        shared_waveLength2.append(waveLength4)
        shared_GUI_flag[0] = 1

    def treeviewClick(event):  # 单击
        for item in struction.selection():
            item_text = struction.item(item, "values")
            item_text = [item_text[i].strip() for i in range(len(item_text))]
            item_text[1] = float(item_text[1])
            item_text[2] = complex(item_text[2])
            shared_names.append(item_text[0])
            shared_thickLayer.append(item_text[1])
            shared_refractIndex.append(item_text[2])

    def inputOLED(event):
        # print(list_all)
        # print(len(list_all))
        shared_thickLayer.pop()
        print(shared_names)
        print(shared_thickLayer)
        print(shared_refractIndex)

    # print(dipolePosition)

    with lock:
        struction.bind('<3>', treeviewClick)  # 绑定右键单击离开事件
        struction.bind('<2>', inputOLED)
        Button(frame_other, text="确定", command=finish).grid(row=7)

    f = Figure(figsize=(8, 4), dpi=100)
    a = f.add_subplot(121)
    b = f.add_subplot(122)
    canvas = FigureCanvasTkAgg(f, master=frame_output)
    canvas.get_tk_widget().grid(row=4, column=0)

    def printFigs():
        # global shared_angle, shared_Luminance
        angle = np.array(shared_angle)
        Luminance = np.array(shared_Luminance)
        wave = np.array(shared_wave)
        Spectrum = np.array(shared_Spectrum)
        # print(angle)
        # print(Spectrum)
        a.set_xlabel("angle")
        a.set_ylabel("Luminance")
        # plt.rcParams['axes.unicode_minus'] = False
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        a.set_ylim([0, 1.5 * np.max(Luminance)])

        a.clear()
        a.plot(angle[0], Luminance[0])
        b.clear()
        # b = f.add_subplot(212)

        for i in range(Spectrum.shape[1]):
            b.plot(wave[0], Spectrum[0][i], label=20*i)
        b.legend()

        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上

        canvas.draw()  # 注意show方法已经过时了,这里改用draw

    Button(frame_output, text="绘图", command=printFigs).grid(row=3, column=0)

    window.mainloop()

