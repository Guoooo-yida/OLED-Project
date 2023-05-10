from tkinter import *
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def GUIfig(shared_angle=None,
           shared_wave=None,
           shared_Luminance=None,
           shared_Spectrum=None,
           shared_Function_flag=None):

    window1 = Toplevel()
    window1.title('figures')
    window1.geometry("{}x{}".format(400, 900))
    while not shared_Function_flag[0]:
        time.sleep(0.5)
        continue
    # Label(window1, text='亮度分布').grid(row=0, column=0)
    # Label(window1, text='远场辐射光谱').grid(row=2, column=0)

    f = Figure(figsize=(4, 9), dpi=100)
    a = f.add_subplot(211)  # 添加子图:2行1列第1个
    a.plot(shared_angle, shared_Luminance)
    b = f.add_subplot(212)
    b.plot(shared_wave, shared_Spectrum[0])

    # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(f, master=window1)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().pack(side=TOP,  # 上对齐
                                fill=BOTH,  # 填充方式
                                expand=YES)  # 随窗口大小调整而调整
    mainloop()
