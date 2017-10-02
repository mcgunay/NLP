import tkinter
import tkinter as tk
import os
from tkinter.scrolledtext import ScrolledText
from doc2vec import TrainDoc2Vec
from doc2vec import TestDoc2VecModel
from tkinter import *

class TestGui:
    timer_id = None

    def __init__(self):
        self.data = []
        self.index = 0
        self.root = tkinter.Tk()
        self.root.geometry('{}x{}'.format(900, 400))
        self.frame_main = tk.Frame(
            master=self.root,
            height=400,
            width=100
        )
        self.frame_main.pack()

        self.frame_train = tk.Frame(
            master=self.frame_main,
            height=200,
            width=100
        )
        self.frame_train.pack()

        self.frame_data = tk.Frame(
            master=self.frame_main,
            height=200,
            width=100
        )

        self.frame_data.pack()

        textl1 = StringVar(self.root, "300")
        textl2 = StringVar(self.root, "10")
        textl3 = StringVar(self.root, "11")
        textl4 = StringVar(self.root, "5")
        textl5 = StringVar(self.root, "0.025")
        textl6 = StringVar(self.root, "10")
        textl7 = StringVar(self.root, "0.002")



        L1 = Label(self.frame_train,  text="Size").grid(row=0, column=0)
        #L1.pack(side=LEFT)
        E1 = Entry(self.frame_train, textvariable=textl1, width=5, bd=1).grid(row=0, column=1)
        #E1.pack(side=LEFT)


        L2 = Label(self.frame_train, text="Window").grid(row=0, column=2)
        #L2.pack(side=LEFT)
        E2 = Entry(self.frame_train, textvariable=textl2, width=5, bd=1).grid(row=0, column=3)
        #E2.pack(side=LEFT)

        L3 = Label(self.frame_train, text="Workers").grid(row=1, column=0)
        E3 = Entry(self.frame_train, textvariable=textl3, width=5, bd=1).grid(row=1, column=1)

        L4 = Label(self.frame_train, text="Min Count").grid(row=1, column=2)
        E4 = Entry(self.frame_train, textvariable=textl4, width=5, bd=1).grid(row=1, column=3)

        L5 = Label(self.frame_train, text="Alpha").grid(row=2, column=0)
        E5 = Entry(self.frame_train, textvariable=textl5,  width=5, bd=1).grid(row=2, column=1)

        L6 = Label(self.frame_train, text="Number of Iteration").grid(row=2, column=2)
        E6 = Entry(self.frame_train, textvariable=textl6, width=5, bd=1).grid(row=2, column=3)

        L7 = Label(self.frame_train, text="Reduce Alpha by").grid(row=2, column=4)
        E7 = Entry(self.frame_train, textvariable=textl7,  width=5, bd=1).grid(row=2, column=5)

        B = Button(self.frame_train, text="Train",
                   command=lambda: self.train(textl1.get(), textl2.get(), textl3.get(),
                                              textl4.get(), textl5.get(), textl6.get(), textl7.get())).grid(row=3, column=6)


        self.root.mainloop()

    def train(self, size, window, workers, min_count, alpha, epoch_count, reduce_alpha_by):
        TrainDoc2Vec.train_model(int(size), int(window), int(workers), int(min_count), float(alpha), int(epoch_count), float(reduce_alpha_by))
        self.data = TestDoc2VecModel.get_model()
        self.show_gui(self.root, self.data[self.index])

    def get_comparison(self, next):
        self.destroy_frame_data()

        if((self.index == len(self.data) - 1 and next == 1) or (next == 0 and self.index == 0)):
            self.show_gui(self.root, self.data[self.index])
        else:
            if(next < len(self.data) and next == 1 ):
                self.index += 1
                self.show_gui(self.root, self.data[self.index])
            else:
                self.index -= 1
                self.show_gui(self.root, self.data[self.index])

    def get_another_10_vec(self):
        self.data = TestDoc2VecModel.get_model()
        self.index = 0
        self.destroy_frame_data()
        self.show_gui(self.root, self.data[self.index])

    def destroy_frame_data(self):
        self.frame_data.destroy()
        self.frame_data = tk.Frame(
            master=self.frame_main,
            height=200,
            width=100
        )

        self.frame_data.pack()

    def show_gui(self, root, comp):

        frame_main = tk.Frame(
            master=self.frame_data,
            height=400,
            width=100
        )

        frame_main.pack(fill='both', expand='yes')

        GetAnother10 = Button(frame_main, text='Get Another 10 Vec', command=lambda s=self: s.get_another_10_vec(),
                         bg='grey', fg='black')

        GetAnother10.pack(side=LEFT)
        # frame_show = tk.Frame(
        #     master=frame_main,
        #     height=100,
        #     width=100
        # )
        #
        # frame_show.pack(fill='both', expand='yes')
        # showdata = Button(frame_show, text='Show Model', command=lambda s=self: s.getModel(),
        #                  bg='grey', fg='black')

        #showdata.pack(side=RIGHT)

        frame_upper = tk.Frame(
            master=self.frame_data,
            height=100,
            width=100
        )

        frame_upper.pack(fill='both', expand='yes')

        var = StringVar()

        L1 = Label(
            master=frame_upper,
            textvariable=var,
            relief=RAISED
        )

        var.set("Cosine similarity between ")
        L1.pack(side=LEFT)

        var2 = StringVar()

        L2 = Label(
            master=frame_upper,
            textvariable=var2,
            relief=RAISED
        )

        L2.pack(side=LEFT)

        var3 = StringVar()

        L3 = Label(
            master=frame_upper,
            textvariable=var3,
            relief=RAISED
        )

        L3.pack(side=LEFT)

        var4 = StringVar()

        L4 = Label(
            master=frame_upper,
            textvariable=var4,
            relief=RAISED
        )

        L4.pack(side=LEFT)


        frame1 = tk.Frame(
            master=self.frame_data,
            height=100,
            width=100
        )

        frame1.pack(fill='both', expand='yes')

        frame2 = tk.Frame(
            master=self.frame_data,
            height=100,
            width=100
        )

        frame2.pack(fill='both', expand='yes')

        textArea1= ScrolledText(
            master = frame1,
            wrap   = tk.WORD,
            width  = 50,
            height = 6
        )

        textArea2 = ScrolledText(
            master = frame1,
            wrap   = tk.WORD,
            width  = 50,
            height = 6
        )

        textArea1.pack(padx=10, pady=10, fill=tk.BOTH, side=LEFT, expand=True)
        textArea2.pack(padx=10, pady=10, fill=tk.BOTH, side=RIGHT, expand=True)

        prevBtn = Button(frame2, text='Previous', command=lambda s=self: s.get_comparison(0),
                        bg='grey', fg='black')


        nextBtn = Button(frame2, text='Next', command=lambda s=self: s.get_comparison(1),
                        bg='grey', fg='black')
        prevBtn.pack(side=LEFT)
        nextBtn.pack(side=RIGHT)

        text1 = comp["text1"]
        text2 = comp["text2"]
        text_ids = comp["textids"]
        result = comp["result"]
        filenames = comp["texts_filename"]

        textArea1.insert(END, text1)
        textArea2.insert(END, text2)
        var2.set(" id=" + str(text_ids[0]) + ", file name = " + filenames[0] + " (left) ")
        var3.set(" id=" + str(text_ids[1]) + ", file name = " + filenames[1] +" (right) ")
        var4.set(" " + str(result))
        self.frame_data.update()
        root.mainloop()

app = TestGui()