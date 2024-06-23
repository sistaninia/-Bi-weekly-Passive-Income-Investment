import tkinter  as tk 
from tkinter import * 
from tkinter import filedialog
from tkinter import Canvas
class MyStock:
    def __init__(self):
        my_w=Tk()
        my_w.title("Stock Screener")
        #my_w.geometry("450x600")
        self.my_w=my_w
        self.mincap=0 
        self.maxcap=None
        self.A3y=3
        self.dele='Yes'
        self.Reg='Europ'
        self.Count=None
        self.filename=None
        self.MB='s'
        self.LPno=40
        self.MPno=30
        self.SPno=15
        self.Backd=0
        self.mkb_no='Inf'
        rr=1
        l0 = tk.Label(my_w,  text='Investment Risk',
                      font=('Helvetica', 10), width=30,height=2,anchor="c" )  
        l0.grid(row=rr,column=1,columnspan=5) 

        
        rr+=2
        # l1 = tk.Label(my_w,  text='Market Behaviour:', anchor="c" )  
        # l1.grid(row=rr,column=1)
        Lowcap = Button(my_w, text = " Low Cap", bg='white', command=self.Lowcap).grid(row=rr,column=0)
        Normal = Button(my_w, text = "4 Stocks", bg='white', command=self.b4stocks).grid(row=rr,column=1)
        VShrink = Button(my_w, text = "8 Stocks", bg='white', command=self.b8stocks).grid(row=rr,column=2)
        Shrink = Button(my_w, text = "15 Stocks", bg='white', command=self.b15stocks).grid(row=rr,column=3)
        Growth = Button(my_w, text = "  test   ", bg='white', command=self.test).grid(row=rr,column=4)
        rr+=1
        canvas = Canvas(my_w,width=400,height=10)
        canvas.create_line(15,10, 400, 10)
        canvas.grid(row=rr,column=1,columnspan=5)
        rr+=1
        l0 = tk.Label(my_w,  text='Tickers to be considered',
                      font=('Helvetica', 10), width=30,height=1,anchor="c" )  
        l0.grid(row=rr,column=1,columnspan=4) 

        rr+=1
        l1 = tk.Label(my_w,  text='Market cap(Min-Max):', anchor="c" )  
        l1.grid(row=rr,column=1) 
        # add one text box
        self.t1=tk.Entry(my_w,width=9)
        self.t1.grid(row=rr,column=2) 
        self.t1.insert(END, 10000)
        self.t2=tk.Entry(my_w,width=9)
        self.t2.grid(row=rr,column=3) 
        self.t2.insert(END, 'Inf') 
        self.t3=tk.Entry(my_w,width=9)
        self.t3.grid(row=rr,column=4) 
        self.t3.insert(END, 900)
        
        # add one text box
        rr+=1
        # add list box for selection of class
        l2 = tk.Label(my_w,  text='Which region:')  
        l2.grid(row=rr,column=1) 
        self.options = StringVar(my_w)
        self.options.set("All") # default value
        opt1 = OptionMenu(my_w, self.options, "All", "Europ", "China")
        opt1.grid(row=rr,column=2)
        # add list box for selection of class
        self.Cont =tk.Entry(my_w,)
        self.Cont.grid(row=rr,column=3) 
        self.Cont.insert(END, "Country(all)")
        
        self.TickL =tk.Entry(my_w,)
        self.TickL.grid(row=rr,column=4) 
        self.TickL.insert(END, "all_tickers")		
        # add list box for selection of Large period
        # Create a File Explorer label 
        rr+=1
        self.label_file_explorer = Label(my_w,  
                            text = "List of Tickers", 
                            width = 20, height = 4,  
                            fg = "blue") 
        self.label_file_explorer.grid(row=rr,column=2,columnspan=2)
        button_explore = Button(my_w,  
                        text = "File Explorer", 
                        command = self.browseFiles)
        button_explore.grid(column = 1, row = rr) 
        #add
        rr+=1
        canvas = Canvas(my_w,width=400,height=20)
        canvas.create_line(15, 10, 400, 10)
        canvas.grid(row=rr,column=1,columnspan=5)

        #filters
#add

        #filters
                
#        frame = Frame(my_w, relief=RAISED, borderwidth=1)
#        frame.pack(fill=BOTH, expand=True)
        #add
        rr+=2       
        l3 = tk.Label(my_w,  text='3year filter:')  
        l3.grid(row=rr,column=1) 
        self.YP = StringVar(my_w)
        self.YP.set(0) # default value        
        opt1 = OptionMenu(my_w, self.YP, 0,0.5, 2, 3, 4)
        opt1.grid(row=rr,column=2) 
        self.YPno=tk.Entry(my_w,width=9)
        self.YPno.grid(row=rr,column=3) 
        self.YPno.insert(END, 830)
        self.YPD=tk.Entry(my_w,width=3)
        self.YPD.grid(row=rr,column=4) 
        self.YPD.insert(END, 'r')
        
        rr+=1
        l3 = tk.Label(my_w,  text='LP filter:')  
        l3.grid(row=rr,column=1) 
        self.LP = StringVar(my_w)
        self.LP.set("6m") # default value        
        opt1 = OptionMenu(my_w, self.LP, "No", "24m", "18m", "11m", "6m", "5m","2m", "1m", "2wk")
        opt1.grid(row=rr,column=2) 
        self.LPno=tk.Entry(my_w,width=9)
        self.LPno.grid(row=rr,column=3) 
        self.LPno.insert(END, 500)
        self.LPD=tk.Entry(my_w,width=3)
        self.LPD.grid(row=rr,column=4) 
        self.LPD.insert(END, 'r')

        # add list box for selection of Medium period
        rr+=1
        l4 = tk.Label(my_w,  text='MP filter:')  
        l4.grid(row=rr,column=1) 
        self.MP = StringVar(my_w)
        self.MP.set("2m") # default value        
        opt1 = OptionMenu(my_w, self.MP, "No", "6m","3m", "2m", "1m")
        opt1.grid(row=rr,column=2) 
        self.MPno=tk.Entry(my_w,width=9)
        self.MPno.grid(row=rr,column=3) 
        self.MPno.insert(END, 470)
        self.MPD=tk.Entry(my_w,width=3)
        self.MPD.grid(row=rr,column=4) 
        self.MPD.insert(END, 'r')

        # add list box for selection of Medium period
        rr+=1
        l5 = tk.Label(my_w,  text='SP filter:')  
        l5.grid(row=rr,column=1) 
        self.SP = StringVar(my_w)
        self.SP.set("2wk") # default value        
        opt1 = OptionMenu(my_w, self.SP, "No", "2m", "1m", "20d", "2wk", "1wk")
        opt1.grid(row=rr,column=2)
        self.SPno=tk.Entry(my_w,width=9)
        self.SPno.grid(row=rr,column=3) 
        self.SPno.insert(END, 70)
        self.SPD=tk.Entry(my_w,width=3)
        self.SPD.grid(row=rr,column=4) 
        self.SPD.insert(END, 'r')
        # add list box for selection of Medium period
        rr+=1
        l5 = tk.Label(my_w,  text='No of Stocks:')  
        l5.grid(row=rr,column=1) 
        self.NoStock=tk.Entry(my_w,width=9)
        self.NoStock.grid(row=rr,column=3) 
        self.NoStock.insert(END, 4)
        rr+=1
        canvas = Canvas(my_w,width=400,height=10)
        canvas.create_line(15, 5, 400, 5)
        canvas.grid(row=rr,column=1,columnspan=5)
        rr+=1
        l0 = tk.Label(my_w,  text='Run market forcast for \n^IXIC, ^DJI, BTC-USD, ^CMC200',
                      font=('Helvetica', 10),anchor="c" )  
        l0.grid(row=rr,column=1,columnspan=2) 

        
        self.MAN = tk.StringVar()
        self.MAN.set('No')
        r1 = tk.Radiobutton(my_w, text='Yes', variable=self.MAN, value='Yes')
        r1.grid(row=rr,column=3)
        
        r2 = tk.Radiobutton(my_w, text='No', variable=self.MAN, value='No')
        r2.grid(row=rr,column=4)

        rr+=1
        canvas = Canvas(my_w,width=400,height=10)
        canvas.create_line(15, 5, 400, 5)
        canvas.grid(row=rr,column=1,columnspan=5)
        rr+=1
        l0 = tk.Label(my_w,  text='Back test:    Days,    interval, and    Duration',
                      font=('Helvetica', 10),anchor="c" )
        l0.grid(row=rr,column=1,columnspan=5) 
        rr+=1
        
        # add one text box
        self.Backd=tk.Entry(my_w,width=9)
        self.Backd.grid(row=rr,column=2) 
        self.Backd.insert(END, 0)
        self.Backint=tk.Entry(my_w,width=9)
        self.Backint.grid(row=rr,column=3) 
        self.Backint.insert(END,7) 
        self.Backdu=tk.Entry(my_w,width=9)
        self.Backdu.grid(row=rr,column=4) 
        self.Backdu.insert(END,28)


        rr+=1
        canvas = Canvas(my_w,width=400,height=20)
        canvas.create_line(15, 10, 400, 10)
        canvas.grid(row=rr,column=1,columnspan=5)
        #add
        rr+=1        
        l2=tk.Label(my_w,  text='Delete Previous folder:\n',anchor="c" )
        l2.grid(row=rr,column=1) 
        self.radio_v = tk.StringVar()
        self.radio_v.set('Yes')
        r1 = tk.Radiobutton(my_w, text='Yes', variable=self.radio_v, value='Yes')
        r1.grid(row=rr,column=2)
        
        r2 = tk.Radiobutton(my_w, text='No', variable=self.radio_v, value='No')
        r2.grid(row=rr,column=3)

        rr+=2
        sbmitbtn = Button(my_w, text = "Submit", fg = "blue",font=('Helvetica', 12),bg='white', command=self.submit).grid(row=rr,column=2)  
        cancle = Button(my_w, text = "Cancle", fg = "blue",font=('Helvetica', 12),bg='white', command=self.cancle).grid(row=rr,column=3) 
        my_w.mainloop()

    def submit(self):
        if self.t1.get()!='':
            self.mincap=int(self.t1.get())
        if self.t2.get()!='Inf':
            self.maxcap=int(self.t2.get())
        if self.t3.get()!='Inf':
            self.mkb_no=int(self.t3.get())
        else:
            self.mkb_no='Inf'
        self.Backd=self.Backd.get()
        self.Backdu=self.Backdu.get()
        self.Backint=self.Backint.get()
        dataI={'d':'download','r':'read'}
        tp={'24m':24,'14m':14,'11m':11,'6m':6,'5m':5,'2m':2,'1m':1,'20d':0.7, "2wk":0.5,"1wk":0.4,'No':0}
        self.dele=self.radio_v.get()
        self.MAN=self.MAN.get()
        self.Reg=self.options.get()
        self.LP=tp[self.LP.get()]
        self.MP=tp[self.MP.get()]
        self.SP=tp[self.SP.get()]
        self.LPno=self.LPno.get()
        self.LPD=dataI[self.LPD.get()]
        self.MPD=dataI[self.MPD.get()]
        self.SPD=dataI[self.SPD.get()]
        self.MPno=self.MPno.get()
        self.YPno=self.YPno.get()
        self.SPno=self.SPno.get()
        self.NoStock=self.NoStock.get()
        self.YP=self.YP.get()
        if self.filename=='':
            self.filename=None
            
        if self.Cont.get()!="Country(all)":
           self.Count=self.Cont.get()
        else:
            self.Count=None
        self.TickL=self.TickL.get()+".csv"								   
           
        self.my_w.destroy()
    def browseFiles(self): 
        self.filename = filedialog.askopenfilename(initialdir = "/", 
                title = "Select a File",filetypes = (("CSV files","*.CSV*"), ("all files","*.*"))) 
        # Change label contents 
        self.label_file_explorer.configure(text=self.filename) 
    def cancle(self):
        self.filename='Cancle' 
        self.Backdu=self.Backdu.get()
        self.Backd=self.Backd.get()
        self.MAN=self.MAN.get()
        self.LPno=500
        self.MPno=200
        self.SPno=60        
        self.my_w.destroy()
    def Lowcap(self):
        self.t1.delete(0,END)
        self.t1.insert(0,1000)  
        self.t2.delete(0,END)
        self.t2.insert(0,5000) 
        self.LP.set("2m")
        self.SP.set("2wk")
        self.MP.set("No")
        self.YP.set(0)
        self.LPno.delete(0,END)
        self.LPno.insert(0,1000)  
        self.MPno.delete(0,END)
        self.MPno.insert(0,1000)  
        self.SPno.delete(0,END)
        self.SPno.insert(0,60)  
        self.MB='vg'
    def test(self):
        self.t1.delete(0,END)
        self.t1.insert(0,10000)  
        self.t3.delete(0,END)
        self.t3.insert(0,450)     
        self.MB='s'
        #self.YP.set("3")
        self.LP.set("6m")
        self.SP.set("2wk")
        self.MP.set("2m")
        self.YP.set(0)
        self.LPno.delete(0,END)
        self.LPno.insert(0,250)  
        self.MPno.delete(0,END)
        self.MPno.insert(0,230)  
        self.SPno.delete(0,END)
        self.SPno.insert(0,70) 
        self.YPno.delete(0,END)
        self.YPno.insert(0,400) 
        self.NoStock.delete(0,END)
        self.NoStock.insert(END, 4)
    def b4stocks(self):
        self.t1.delete(0,END)
        self.t1.insert(0,10000)  
        self.t3.delete(0,END)
        self.t3.insert(0,900)     
        self.MB='s'
        #self.YP.set("3")
        self.LP.set("6m")
        self.SP.set("2wk")
        self.MP.set("2m")
        self.YP.set(0)
        self.LPno.delete(0,END)
        self.LPno.insert(0,500)  
        self.MPno.delete(0,END)
        self.MPno.insert(0,470)  
        self.SPno.delete(0,END)
        self.SPno.insert(0,70) 
        self.YPno.delete(0,END)
        self.YPno.insert(0,830) 
        self.NoStock.delete(0,END)
        self.NoStock.insert(END, 4)
    def b15stocks(self):
        self.t1.delete(0,END)
        self.t1.insert(0,10000)  
        self.t3.delete(0,END)
        self.t3.insert(0,835)         
        self.MB='s'
        #self.YP.set("3")
        self.LP.set("6m")
        self.SP.set("2wk")
        self.MP.set("2m")
        self.LPno.delete(0,END)
        self.LPno.insert(0,500)  
        self.MPno.delete(0,END)
        self.MPno.insert(0,470)  
        self.SPno.delete(0,END)
        self.SPno.insert(0,80) 
        self.YPno.delete(0,END)
        self.YPno.insert(0,830)  
        self.NoStock.delete(0,END)
        self.NoStock.insert(END, 15)
    def b8stocks(self):
        self.t1.delete(0,END)
        self.t1.insert(0,10000)  
        self.t3.delete(0,END)
        self.t3.insert(0,900)       
        self.MB='s'
        #self.YP.set("3")
        self.LP.set("6m")
        self.SP.set("2wk")
        self.MP.set("2m")
        self.LPno.delete(0,END)
        self.LPno.insert(0,500)  
        self.MPno.delete(0,END)
        self.MPno.insert(0,470)  
        self.SPno.delete(0,END)
        self.SPno.insert(0,70) 
        self.YPno.delete(0,END)
        self.YPno.insert(0,830) 
        self.NoStock.delete(0,END)
        self.NoStock.insert(END, 8)
    # def VeryLow(self):
    #     self.t1.delete(0,END)
    #     self.t1.insert(0,20000)  
    #     #self.t2.delete(0,END)
    #     #self.t2.insert(0,5000) 
    #     self.LP.set("6m")
    #     self.SP.set("2wk")
    #     self.MP.set("2m")
    #     self.YP.set(0)
    #     self.LPno.delete(0,END)
    #     self.LPno.insert(0,150)  
    #     self.MPno.delete(0,END)
    #     self.MPno.insert(0,150)  
    #     self.SPno.delete(0,END)
    #     self.SPno.insert(0,60)  
    #     self.MB='vs'
class Display:
    def __init__(self):
        my_w=Tk()
        self.my_w=my_w
        self.Prise=True
        self.Update=''
        self.Period=60
        self.yaxis='NonUniform'
        l0 = tk.Label(my_w,  text='Update the curves?',
                      font=('Helvetica', 16), width=30,anchor="c" )  
        l0.grid(row=1,column=1,columnspan=4) 
        l1 = tk.Label(my_w,  text=' Period (days):', width=13,anchor="c" )  
        l1.grid(row=3,column=1) 
        # add one text box
        self.t1=tk.Entry(my_w,width=9)
        self.t1.grid(row=3,column=2) 
        self.t1.insert(END, 60)  


        l2=tk.Label(my_w,  text='Vertical Axis(Prise):', width=13,anchor="c" )
        l2.grid(row=6,column=1) 
        self.radio_v3 = tk.StringVar()
        self.radio_v3.set('Relative')
        r1 = tk.Radiobutton(my_w, text='Relative', variable=self.radio_v3, value='Relative')
        r1.grid(row=6,column=2)
        
        r2 = tk.Radiobutton(my_w, text='Absolute', variable=self.radio_v3, value='Absolute')
        r2.grid(row=6,column=3)
        
        l3=tk.Label(my_w,  text='Vertical Axis Scale:', width=13,anchor="c" )
        l3.grid(row=7,column=1) 
        self.radio_v4 = tk.StringVar()
        self.radio_v4.set('NonUniform')
        r3 = tk.Radiobutton(my_w, text='Uniform', variable=self.radio_v4, value='Uniform')
        r3.grid(row=7,column=2)
        
        r4 = tk.Radiobutton(my_w, text='Non Uniform', variable=self.radio_v4, value='NonUniform')
        r4.grid(row=7,column=3)        
        
        Updateg = Button(my_w, text = "Update",activebackground = "pink", activeforeground = "blue", command=self.update).grid(row=9,column=1,columnspan=2)  
        cancle = Button(my_w, text = "Cancle",activebackground = "pink", activeforeground = "blue", command=self.cancle).grid(row=9,column=3,columnspan=2) 
        my_w.mainloop()

    def update(self):
        self.Prise=self.radio_v3.get()
        self.yaxis=self.radio_v4.get() 
        self.Period=self.t1.get()
        self.my_w.destroy()
    def cancle(self):
        self.Update='Cancle'          
        self.my_w.destroy()        
        
#        self.my_w.destroy()
#DS=Display()
"""
    def growth(self):
        self.t1.delete(0,END)
        self.t1.insert(0,15000)  
#        self.t2.delete(0,END)
#        self.t2.insert(0,5000)        
        self.MB='g'
        #self.YP.set("3")
        self.LP.set("6m")
        self.SP.set("2wk")
        self.MP.set("2m")
        self.LPno.delete(0,END)
        self.LPno.insert(0,500)  
        self.MPno.delete(0,END)
        self.MPno.insert(0,500)  
        self.SPno.delete(0,END)
        self.SPno.insert(0,150) 
        self.YPno.delete(0,END)
        self.YPno.insert(0,3000) 
"""

