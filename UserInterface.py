#!/usr/bin/env python
# coding: utf-8
import PIL.ImageTk
import PIL.Image
import tkinter as tk
from matplotlib.backend_bases import button_press_handler
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import GraphViewer as GV
from tkinter.filedialog import *
from tkinter import filedialog
from Agnes import agnes
from Dbscan import dbscan
from Kmedoid import kmedoid, kmeans
import BasicAlgorithms as BA
import InteractivePlotting as IP


class Page(tk.Tk):
    # This is a global variable which will be used to tranfert data to choosed algorithm
    global data
    data = None

    global user_choice
    user_choice = -1
    def __init__(self, root, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.frame_buttons = Frame(root, width=1, height=1, bg='silver')
        self.frame_buttons.pack(side=TOP)

        self.button_kmeans = Button(self.frame_buttons, width=25, height=2, text=" KMEANS ", bg='snow',
                                     command=lambda: self.user_choice_manager(4))
        self.button_kmeans.pack(side=LEFT, padx=10, pady=10)
        self.button_kmedoid = Button(self.frame_buttons, width=25, height=2, text=" KMEDOID ", bg='snow',
                                     command=lambda:self.user_choice_manager(1))
        self.button_kmedoid.pack(side=LEFT, padx=10, pady=10)
        self.button_agnes = Button(self.frame_buttons, width=25, height=2, text=" AGNES ", bg='snow',
                                   command=lambda:self.user_choice_manager(2))
        self.button_agnes.pack(side=LEFT, padx=10, pady=10)
        self.button_dbscan = Button(self.frame_buttons, width=25, height=2, text=" DBSCAN ", bg='snow',
                                    command=lambda:self.user_choice_manager(3))
        self.button_dbscan.pack(side=LEFT, padx=10, pady=10)
        #
        self.frame_results_performance = Frame(root, width=50, highlightthickness=2, highlightbackground='black')
        self.frame_results_performance.pack(side=RIGHT, fill=Y, padx=5, pady=20)
        ##
        self.frame_results = Frame(self.frame_results_performance, height=100)
        self.frame_results.pack(fill=X, side=TOP)
        ##
        self.label_results = Label(self.frame_results, text='RESULTS', font=("Helvetica", 16))
        self.label_results.pack()
        self.scrollbar_result = Scrollbar(self.frame_results)
        self.scrollbar_result.pack(side=RIGHT, fill=Y)
        self.textfield_results = Text(self.frame_results, yscrollcommand=self.scrollbar_result.set, width=55,
                                      state=DISABLED)
        self.textfield_results.pack(padx=2)
        ##
        self.frame_graph = Frame(self.frame_results_performance, height=100)
        #self.frame_graph.pack(fill=X, side=TOP)
        self.fig_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.fig_graph, self.frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.frame_graph)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        #
        self.frame_inputs = Frame(root, width=300, height=300, highlightthickness=2, highlightbackground='black')
        self.frame_inputs.pack(side=LEFT, fill=BOTH, padx=5, pady=20)
        #
        self.frame_dataset_errors = Frame(root, width=500, height=500, highlightthickness=2,
                                          highlightbackground='black')
        self.frame_dataset_errors.pack(side=RIGHT, fill=BOTH, padx=5, pady=20)
        ##
        self.frame_dataset = Frame(self.frame_dataset_errors, width=50, height=100)
        self.frame_dataset.pack(side=TOP, fill=X, padx=5, pady=5)
        #
        self.frame_execution = Frame(self.frame_dataset_errors)
        self.frame_execution.pack(side=TOP, pady=10, padx=2)
        ##
        image = PIL.Image.open(r'C:\Users\Ilyes\PycharmProjects\DataMining_TP\icons\next_icon_50x50.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo  # keep a reference!
        self.button_next = Button(self.frame_execution, image=photo, width=48, height=48, state=DISABLED,
                                  command=lambda: self.execute_manager())
        self.button_next.pack(side=RIGHT, padx=2)
        ##
        image = PIL.Image.open(r'C:\Users\Ilyes\PycharmProjects\DataMining_TP\icons\previous_icon_50x50.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo  # keep a reference!
        self.button_precedent = Button(self.frame_execution, image=photo, width=48, height=48, state=DISABLED,
                                       command=lambda: self.execute_manager())
        self.button_precedent.pack(side=LEFT, padx=2)
        ##
        image = PIL.Image.open(r'C:\Users\Ilyes\PycharmProjects\DataMining_TP\icons\previous_too_icon_50x50.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo  # keep a reference!
        self.button_previous = Button(self.frame_execution, image=photo, width=48, height=48, state=DISABLED,
                                       command=lambda: self.execute_manager())
        self.button_previous.pack(side=LEFT, padx=2)
        ##
        image = PIL.Image.open(r'C:\Users\Ilyes\PycharmProjects\DataMining_TP\icons\next_too_icon_50x50.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo  # keep a reference!
        self.button_nexious = Button(self.frame_execution, image=photo,  width=48, height=48, state=DISABLED,
                                      command=lambda: self.execute_manager())
        self.button_nexious.pack(side=RIGHT, padx=2)
        ##
        image = PIL.Image.open(r'C:\Users\Ilyes\PycharmProjects\DataMining_TP\icons\play_icon_50x50.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo  # keep a reference!
        self.button_execute = Button(self.frame_execution, image=photo, width=48, height=48, state=DISABLED,
                                     command=lambda: self.execute_manager())
        self.button_execute.pack(side=RIGHT, padx=2, expand=1)
        ##
        image = PIL.Image.open(r'C:\Users\Ilyes\PycharmProjects\DataMining_TP\icons\pause_icon_50x50.jpg')
        photo = PIL.ImageTk.PhotoImage(image)
        label = Label(root, image=photo)
        label.image = photo  # keep a reference!
        self.button_pause = Button(self.frame_execution, image=photo, width=48, height=48, state=DISABLED,
                                   command=lambda: self.execute_manager())
        self.button_pause.pack(side=RIGHT, padx=2)
        ###
        self.label_dataset = Label(self.frame_dataset, text='DATASET', font=("Helvetica", 16))
        self.label_dataset.pack()
        self.scrollbar_dataset = Scrollbar(self.frame_dataset)
        self.scrollbar_dataset.pack(side=RIGHT, fill=Y)
        self.textfield_dataset = Text(self.frame_dataset, yscrollcommand=self.scrollbar_dataset.set, width=55, state=DISABLED)
        self.textfield_dataset.pack(padx=2)
        self.label_error = Label(self.frame_dataset_errors, text="", fg='RED')
        self.label_error.pack(side=BOTTOM)
        ##
        self.frame_visualize_graph = Frame(self.frame_results_performance)
        self.frame_visualize_graph.pack(fill=X)
        ###
        self.graph_text_bit = 1
        self.button_visualize_graph = Button(self.frame_visualize_graph, text='Visualize le graph',
                                             command=lambda:self.graph_viewer_manager())
        self.button_visualize_graph.pack(side=RIGHT)
        ##
        self.frame_performance = Frame(self.frame_results_performance, height=50)
        self.frame_performance.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        ###
        self.frame_label_performance = Frame(self.frame_performance)
        self.frame_label_performance.pack(fill=X)
        self.label_performance = Label(self.frame_label_performance, text='Performances', font=("Helvetica", 16))
        self.label_performance.pack(side=LEFT)
        self.frame_frame_performance = Frame(self.frame_performance)
        self.frame_frame_performance.pack(fill=BOTH)
        self.frame_performance_labels = Frame(self.frame_frame_performance)
        self.frame_performance_labels.pack(side=LEFT, padx=10, pady=3)
        self.label_performance_intraclass = Label(self.frame_performance_labels, text='IntraClass = ',
                                                  font=("Courier New", 12))
        self.label_performance_intraclass.pack()
        self.label_performance_interclass = Label(self.frame_performance_labels, text='InterClass = ',
                                                  font=("Courier New", 12))
        self.label_performance_interclass.pack()
        self.label_performance_silhouette = Label(self.frame_performance_labels, text='Silhouette = ',
                                                  font=("Courier New", 12))
        self.label_performance_silhouette.pack()
        ####
        self.frame_performance_textfields = Frame(self.frame_frame_performance)
        self.frame_performance_textfields.pack(side=LEFT)
        self.textfield_performance_intraclass = Text(self.frame_performance_textfields, width=8, height=1,
                                                     state=DISABLED)
        self.textfield_performance_intraclass.pack(pady=2)
        self.textfield_performance_interclass = Text(self.frame_performance_textfields, width=8, height=1,
                                                     state=DISABLED)
        self.textfield_performance_interclass.pack(pady=2)
        self.textfield_performance_silhouette = Text(self.frame_performance_textfields, width=8, height=1,
                                                     state=DISABLED)
        self.textfield_performance_silhouette.pack(pady=2)
        ####
        self.frame_performance_executiontime = Frame(self.frame_frame_performance)
        self.frame_performance_executiontime.pack(side=LEFT, padx=10, pady=3)
        self.label_performance_executiontime = Label(self.frame_frame_performance, text="Temps d'exection (sec) \n= ",
                                                  font=("Courier New", 12))
        self.label_performance_executiontime.pack()
        self.textfield_performance_executiontime = Text(self.frame_frame_performance, width=16, height=1,
                                                     state=DISABLED)
        self.textfield_performance_executiontime.pack()

        global var
        var = IntVar()
        #
        self.frame_path_all = Frame(self.frame_inputs)
        self.frame_path_all.pack(fill=X)
        ##
        self.radiobutton_managepathframe = Radiobutton(self.frame_path_all, variable=var, value=1,
                                                       command=lambda:self.switch_radiobutton_manager())
        self.radiobutton_managepathframe.pack(side=LEFT)
        self.radiobutton_managepathframe.select() # select it
        ##
        self.frame_path = Frame(self.frame_path_all)
        self.frame_path.pack(side=RIGHT, fill=X)
        ###
        self.entry_path_numsequences_sv = StringVar()
        self.entry_path_numsequences_sv.trace("w", lambda name, index, mode,
                entry_path_numsequences_sv=self.entry_path_numsequences_sv: self.callback_updateDataSet(self.entry_path_numsequences_sv))
        ###
        self.entry_path_numsequences = Entry(self.frame_path, width=5, state=DISABLED, textvariable=self.entry_path_numsequences_sv)
        self.entry_path_numsequences.pack(side=LEFT)
        self.entry_path_numsequences_ready = False
        ###
        self.label_path_numsequences = Label(self.frame_path, text='/####')
        self.label_path_numsequences.pack(side=LEFT, padx=2)
        ###
        self.textfield_filepath = Text(self.frame_path, width=25, height=2, state=DISABLED)
        self.textfield_filepath.pack(side=LEFT, padx=2, pady=3)
        ###
        self.button_open = Button(self.frame_path, text='Ouvrir',
                                  command=lambda: self.open_dialog())
        self.button_open.pack(side=RIGHT, padx=1)
        #
        self.frame_manual_enter_all = Frame(self.frame_inputs)
        self.frame_manual_enter_all.pack(pady=10, fill=X)
        ##
        self.radiobutton_manageframemanual = Radiobutton(self.frame_manual_enter_all, variable=var, value=2,
                                                         command=lambda:self.switch_radiobutton_manager())
        self.radiobutton_manageframemanual.pack(side=LEFT)
        ##
        self.frame_manual_enter = Frame(self.frame_manual_enter_all)
        self.frame_manual_enter.pack(side=RIGHT, fill=X)
        ###
        self.label_manual_enter = Label(self.frame_manual_enter, text='Enter the sequence down here:\t\t\t')
        self.label_manual_enter.pack(padx=2)
        ###
        self.scrollbar_manual_enter = Scrollbar(self.frame_manual_enter)
        self.scrollbar_manual_enter.pack(side=RIGHT, fill=Y)
        ###
        self.textfield_manual_enter = Text(self.frame_manual_enter, yscrollcommand=self.scrollbar_manual_enter.set, width=45, height=15, state=DISABLED)
        self.textfield_manual_enter.pack(side=BOTTOM, padx=2, pady=3)
        #
        self.frame_random_all = Frame(self.frame_inputs)
        self.frame_random_all.pack(fill=X)
        ##
        self.radiobutton_manageframerandom = Radiobutton(self.frame_random_all, variable=var, value=3,
                                                         command=lambda:self.switch_radiobutton_manager())
        self.radiobutton_manageframerandom.pack(side=LEFT)
        ##
        self.frame_random = Frame(self.frame_random_all)
        self.frame_random.pack(fill=X)
        ###
        fig = Figure(figsize=(3, 2), dpi=100);fig.gca().axes.get_yaxis().set_visible(False);fig.gca().axes.get_xaxis().set_visible(False)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, self.frame_random)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.frame_random)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        global deleting
        deleting = False
        points_list = dict()
        def on_plot(event):
            if event.x > 53 and event.x < 342 and event.y > 28 and event.y < 170:
                m_x, m_y = event.x, event.y
                ix, iy = ax.transData.inverted().transform([m_x, m_y])
                ax.plot(ix, iy, marker='o')
                fig.canvas.draw()
                sequence = BA.adding_sequence(m_x, m_y)
                self.adding_sequence_random_UI(sequence)
                points_list[(m_x, m_y)] = sequence
        def on_delete():
            global data
            ax.clear()
            data = None
            self.textfield_dataset.config(state=NORMAL)
            self.textfield_dataset.delete(0.0, END)
            self.textfield_dataset.config(state=DISABLED)
        canvas.mpl_connect('button_press_event', on_plot)
        ###
        self.button_random = Button(self.frame_random, text='choose a random sequence', width=2, height=2, state=DISABLED,
                                    command=lambda:on_delete())
        self.button_random.pack()
        #
        self.frame_kmedoid_parameters = Frame(self.frame_dataset_errors)
        ##
        self.label_kmedoid_numclusters = Label(self.frame_kmedoid_parameters, text='*Nombre de clusters')
        self.label_kmedoid_numclusters.pack(pady=5, side=LEFT)
        ##
        entry_kmedoid_numclusters_sv = StringVar()
        entry_kmedoid_numclusters_sv.trace("w", lambda name, index, mode,
                entry_kmedoid_numclusters_sv=entry_kmedoid_numclusters_sv: self.callback_check_coherance_kmedoid_numclusters(entry_kmedoid_numclusters_sv))
        ##
        self.entry_kmedoid_numclusters = Entry(self.frame_kmedoid_parameters, width=5, textvariable=entry_kmedoid_numclusters_sv)
        self.entry_kmedoid_numclusters.pack(pady=5, side=LEFT)
        ###
        self.kmedoid_ready = False
        #
        self.frame_dbscan_parameters = Frame(self.frame_dataset_errors) #The pack is below self.button_execture.pack
        ##
        self.label_dbscan_minpoints = Label(self.frame_dbscan_parameters, text='*Min Points')
        self.label_dbscan_minpoints.pack(pady=5, side=LEFT)
        ##
        entry_dbscan_minpoints_sv = StringVar()
        entry_dbscan_minpoints_sv.trace("w", lambda name, index, mode,
                        entry_dbscan_minpoints_sv=entry_dbscan_minpoints_sv: self.callback_check_coherance_dbscan_minpoints(entry_dbscan_minpoints_sv))
        ##
        self.entry_dbscan_minpoints = Entry(self.frame_dbscan_parameters, width=5, textvariable=entry_dbscan_minpoints_sv)
        self.entry_dbscan_minpoints.pack(pady=5, side=LEFT)
        ##
        self.label_dbscan_radiun = Label(self.frame_dbscan_parameters, text='*Radiun')
        self.label_dbscan_radiun.pack(pady=5, padx=3, side=LEFT)
        ##
        entry_dbscan_radiun_sv = StringVar()
        entry_dbscan_radiun_sv.trace("w", lambda name, index, mode,
                                                    entry_dbscan_radiun_sv=entry_dbscan_radiun_sv: self.callback_check_coherance_dbscan_radiun(entry_dbscan_radiun_sv))
        ##
        self.entry_dbscan_radiun = Entry(self.frame_dbscan_parameters, width=5, textvariable=entry_dbscan_radiun_sv)
        self.entry_dbscan_radiun.pack(pady=5, side=LEFT)
        ###
        self.dbscan_ready = [False, False]

        #self.frame_dbscan_parameters.pack(side=TOP, pady=20, fill=X)
        #self.frame_kmedoid_parameters.pack(side=TOP, pady=20, fill=X)
        self.dict_distance = None

    def callback_check_coherance_kmedoid_numclusters(self, sv):
        if sv.get().isnumeric():
            self.label_kmedoid_numclusters.config(fg='black')
            self.kmedoid_ready = True
        else:
            self.label_kmedoid_numclusters.config(fg='red')
            self.kmedoid_ready = False
    def callback_check_coherance_dbscan_minpoints(self, sv):
        if sv.get().isnumeric():
            self.label_dbscan_minpoints.config(fg='black')
            self.dbscan_ready[0] = True
        else:
            self.label_dbscan_minpoints.config(fg='red')
            self.dbscan_ready[0] = False
    def callback_check_coherance_dbscan_radiun(self, sv):
        if sv.get().isnumeric():
            self.label_dbscan_radiun.config(fg='black')
            self.dbscan_ready[1] = True
        else:
            self.label_dbscan_radiun.config(fg='red')
            self.dbscan_ready[1] = False

    def callback_updateDataSet(self, sv):
        if sv.get().isnumeric():
            self.entry_path_numsequences.config(fg='BLACK')
            self.entry_path_numsequences_ready = True
        else:
            self.entry_path_numsequences.config(fg='RED')
            self.textfield_dataset.config(state=NORMAL)
            self.textfield_dataset.delete(0.0, END)
            self.textfield_dataset.config(state=DISABLED)
            self.entry_path_numsequences_ready = False
            return

        self.textfield_dataset.config(state=NORMAL)
        self.adding_sequence_dataset(int(sv.get()))
        self.textfield_dataset.config(state=DISABLED)

        global user_choice
        if user_choice == 3:
            self.plot_on_graph_dbscan(int(sv.get()))

    def plot_on_graph_dbscan(self, sv):
        self.coords = dict()
        self.ax_graph.clear()
        for seq in data[:sv]:
            x_coords, y_coords = BA.convert_seq_to_coords(seq)
            self.ax_graph.plot(x_coords, y_coords, 'k^')
            self.fig_graph.canvas.draw()
            self.coords[(x_coords, y_coords)] = seq

    def plot_on_graph_kmedoid_kmeans(self, nbrPoint, dict_data:dict, data):
        colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        self.ax_graph.clear()
        cptColor = 0
        for key in dict_data.keys():
            seq = data[key]
            x_coords, y_coords = BA.convert_seq_to_coords(seq)
            self.ax_graph.plot(x_coords, y_coords, colors[cptColor])
            self.fig_graph.canvas.draw()
            cluster_content = dict_data[key]
            for elm in cluster_content:
                seq = data[elm]
                x_coords, y_coords = BA.convert_seq_to_coords(seq)
                self.ax_graph.plot(x_coords, y_coords, colors[cptColor])
                self.fig_graph.canvas.draw()

            cptColor += 1
            if cptColor >= len(colors):
                cptColor = 0
                print('ATTENTION! Nombre de points superieur à nombre de Keys')


    def adding_sequence_random_UI(self, sequence):
        global data
        if data == None:
            pass
        data = []

        data.append(sequence)

        self.textfield_dataset.config(state=NORMAL)
        self.textfield_dataset.insert(INSERT, sequence)
        self.textfield_dataset.config(state=DISABLED)

    def open_dialog(self):
        global data
        file_path = filedialog.askopenfilename()
        self.textfield_filepath.config(state=NORMAL)
        self.textfield_filepath.delete(0.0, END)
        self.textfield_filepath.insert(INSERT, file_path)
        self.textfield_filepath.config(state=DISABLED)
        try:
            data = BA.import_seq(file_path)
        except:
            self.label_path_numsequences.config(text='/####')
            self.entry_path_numsequences.delete(0, END)
            self.entry_path_numsequences.config(state=DISABLED)

        taille = str(len(data))
        self.label_path_numsequences.config(text='/' + taille)
        self.entry_path_numsequences.config(state=NORMAL)
        self.entry_path_numsequences.delete(0, END)
        self.entry_path_numsequences.insert(INSERT, taille)

    def adding_sequence_dataset(self, taille):
        self.textfield_dataset.delete(0.0, END)
        for i in range(taille):
            self.textfield_dataset.insert(INSERT, str.format('>{0}\n', data[i]))

        self.scrollbar_dataset.config(command=self.textfield_dataset.yview)

    def graph_viewer_manager(self):
        # 0 for graph results
        # 1 for text results
        if self.graph_text_bit == 0:
            self.graph_text_bit = 1
            self.button_visualize_graph.config(text='Visualizer le graphe')
            self.button_visualize_graph.pack_forget()
            self.frame_graph.pack_forget()
            self.frame_results.pack(fill=X, side=TOP)
            self.button_visualize_graph.pack(side=RIGHT)

        else:
            self.graph_text_bit = 0
            self.button_visualize_graph.config(text='Afficher le texte')
            self.button_visualize_graph.pack_forget()
            self.frame_results.pack_forget()
            self.frame_graph.pack(fill=X, side=TOP)
            self.button_visualize_graph.pack(side=RIGHT)

        if self.textfield_results.get(0.0, END).isspace():
            return

        if user_choice == 1:
            # Show Kmedoid graph
            return
        elif user_choice == 2:
            # Show agnes graph
            limit = int(self.entry_path_numsequences.get())
            GV.agnes_graph_viewer(data[:limit], self.dict_distance)
            return
        else:
            # Show dbscan graph
            return

    def switch_radiobutton_manager(self):
        arg = var.get()
        if arg == 1:
            self.manager_radiobutton_path()
        elif arg == 2:
            self.manager_radiobutton_manual()
        else:
            self.manager_radiobutton_random()

    def manager_radiobutton_path(self):
        self.button_random['state'] = 'disabled'
        self.textfield_manual_enter['state'] = 'disabled'

        self.button_open['state'] = 'normal'

    def manager_radiobutton_manual(self):
        self.button_random['state'] = 'disabled'
        self.button_open['state'] = 'disabled'

        self.textfield_manual_enter['state'] = 'normal'
        self.scrollbar_manual_enter.config(command = self.textfield_manual_enter.yview)

    def manager_radiobutton_random(self):
        self.textfield_manual_enter['state'] = 'disabled'
        self.button_open['state'] = 'disabled'

        self.button_random['state'] = 'normal'

    def clean_all(self):
        if self.textfield_results.get(0.0, END).isspace():
            return
        #
        self.textfield_results.config(state=NORMAL)
        self.textfield_results.delete(0.0, END)
        self.textfield_results.config(state=DISABLED)
        #
        self.textfield_performance_silhouette.config(state=NORMAL)
        self.textfield_performance_silhouette.delete(0.0, END)
        self.textfield_performance_silhouette.config(state=DISABLED)
        #
        self.textfield_performance_interclass.config(state=NORMAL)
        self.textfield_performance_interclass.delete(0.0, END)
        self.textfield_performance_interclass.config(state=DISABLED)
        #
        self.textfield_performance_intraclass.config(state=NORMAL)
        self.textfield_performance_intraclass.delete(0.0, END)
        self.textfield_performance_intraclass.config(state=DISABLED)
        #
        self.entry_path_numsequences.config(state=NORMAL)
        self.entry_path_numsequences.delete(0, END)
        self.entry_path_numsequences.config(state=DISABLED)
        #
        self.textfield_manual_enter.config(state=NORMAL)
        self.textfield_manual_enter.delete(0.0, END)
        self.textfield_manual_enter.config(state=DISABLED)
        #
        self.textfield_filepath.config(state=NORMAL)
        self.textfield_filepath.delete(0.0, END)
        self.textfield_filepath.config(state=DISABLED)
        #
        data = None
        #


    def user_choice_manager(self, user_ch):
        global user_choice
        user_choice = user_ch
        self.hide_dbscan_parameters()
        self.hide_kmedoid_kmeans_parameters()

        if user_choice == 3:
            # execute with DBSCAN
            self.show_dbscan_parameters()
            self.button_dbscan.config(bg='forest green')
            self.button_kmedoid.config(bg='snow')
            self.button_kmeans.config(bg='snow')
            self.button_agnes.config(bg='snow')
            self.button_execute.config(state=NORMAL)
            self.clean_all()
            self.callback_updateDataSet(self.entry_path_numsequences_sv)
            return

        if user_choice == 1:
            # execute with KMEDOID
            self.show_kmedoid_kmeans_parameters()
            self.button_kmedoid.config(bg='forest green')
            self.button_kmeans.config(bg='snow')
            self.button_agnes.config(bg='snow')
            self.button_dbscan.config(bg='snow')
            self.button_execute.config(state=NORMAL)
            self.clean_all()
            return

        if user_choice == 4:
            # execute with KMEANS
            self.show_kmedoid_kmeans_parameters()
            self.button_kmeans.config(bg='forest green')
            self.button_agnes.config(bg='snow')
            self.button_dbscan.config(bg='snow')
            self.button_kmedoid.config(bg='snow')

            self.button_execute.config(state=NORMAL)
            self.clean_all()
            return

        if user_choice == 2:
            #execute with AGNES
            self.button_agnes.config(bg='forest green')
            self.button_kmeans.config(bg='snow')
            self.button_dbscan.config(bg='snow')
            self.button_kmedoid.config(bg='snow')

            self.button_execute.config(state=NORMAL)
            self.clean_all()

    def ready_to_execute(self):
        arg = var.get()

        if arg == 1:
            filepath = str(self.textfield_filepath.get(0.0, END))
            if filepath.isspace():
                self.label_error.config(text="MERCI DE CHOISIR UN FICHIER POUR L'EXECUTER")
                return False

            if not self.entry_path_numsequences_ready:
                return False

        if arg == 2:
            global data
            sequences = str(self.textfield_manual_enter.get(0.0, END))
            if sequences.isspace():
                self.label_error.config(text="MERCI D'ENTRER DES SEQUENCES A CLASSIFIER")
                return False
            not_valid_data = sequences.split('\n')
            if len(not_valid_data) < 2:
                self.label_error.config(text="MERCI D'ENTRER PLUS DE DEUX (2) SEQUENCES JUSTES")
                return False

            data = []
            taille_standard = len(not_valid_data[0])
            for d in not_valid_data:
                if BA.valid_sequence(d):
                    if taille_standard != len(d):
                        self.label_error.config(text="MERCI D'ENTRER DES SEQUENCES DE MEME LONGUEUR")
                        return False
                    data.append(d)

            if len(data) < 2:
                self.label_error.config(text="MERCI D'ENTRER PLUS DE DEUX (2) SEQUENCES JUSTES")
                return False

        if user_choice == -1:
            self.label_error.config(text="Merci de choisir un algorithme pour l'executer")
            return False

        return True

    def execute_manager(self):
        if not self.ready_to_execute():
            return

        self.label_error.config(text='')

        if user_choice == 1:
            self.kmedoid_UI()
        elif user_choice == 4:
            self.kmeans_UI()
        elif user_choice== 2:
            self.agnes_UI()
        else:
            self.dbscan_UI()

    def update_results_performances_fields(self, resultat, intra, inter, silhouette):
        #update result
        self.textfield_results.config(state=NORMAL)
        self.textfield_results.delete(0.0, END)
        self.textfield_results.insert(INSERT, resultat)
        self.textfield_results.config(state=DISABLED)
        self.scrollbar_result.config(command=self.textfield_results.yview)
        #update intra
        self.textfield_performance_intraclass.config(state=NORMAL)
        self.textfield_performance_intraclass.delete(0.0, END)
        self.textfield_performance_intraclass.insert(INSERT, intra)
        self.textfield_performance_intraclass.config(state=DISABLED)
        #update inter
        self.textfield_performance_interclass.config(state=NORMAL)
        self.textfield_performance_interclass.delete(0.0, END)
        self.textfield_performance_interclass.insert(INSERT, inter)
        self.textfield_performance_interclass.config(state=DISABLED)
        #update silhoutte
        self.textfield_performance_silhouette.config(state=NORMAL)
        self.textfield_performance_silhouette.delete(0.0, END)
        self.textfield_performance_silhouette.insert(INSERT, silhouette)
        self.textfield_performance_silhouette.config(state=DISABLED)

    def agnes_UI(self):
        if data == None:
            return

        limit = int(self.entry_path_numsequences.get())
        resultat, self.dict_distance, intra, inter, silhouette = agnes(data[:limit])
        self.update_results_performances_fields(resultat, intra, inter, silhouette)

    def kmedoid_UI(self):
        if data == None:
            return

        limit = int(self.entry_path_numsequences.get())
        kclusters = int(self.entry_kmedoid_numclusters.get())
        resultat, intra, inter, silhouette, clusters = kmedoid(data[:limit], kclusters)
        self.update_results_performances_fields(resultat, intra, inter, silhouette)
        self.plot_on_graph_kmedoid_kmeans(kclusters, clusters, data)

    def kmeans_UI(self):
        if data == None:
            return

        limit = int(self.entry_path_numsequences.get())
        kclusters = int(self.entry_kmedoid_numclusters.get())
        resultat, intra, inter, silhouette, clusters = kmeans(data[:limit], kclusters)
        self.update_results_performances_fields(resultat, intra, inter, silhouette)
        self.plot_on_graph_kmedoid_kmeans(kclusters, clusters, data)

    def dbscan_UI(self):
        if data == None:
            return


        if False in self.dbscan_ready:
            return

        rad = int(self.entry_dbscan_radiun.get())
        minpnt = int(self.entry_dbscan_minpoints.get())
        limit = int(self.entry_path_numsequences.get())
        resultat, intra, inter, silhouette = dbscan(data[:limit], rad, minpnt)
        self.update_results_performances_fields(resultat, intra, inter, silhouette)

    def show_dbscan_parameters(self, event=None):
        self.frame_dbscan_parameters.pack(side=TOP, pady=20, fill=X)

    def hide_dbscan_parameters(self, event=None):
        self.frame_dbscan_parameters.pack_forget()

    def show_kmedoid_kmeans_parameters(self, event=None):
        self.frame_kmedoid_parameters.pack(side=TOP, pady=20, fill=X)

    def hide_kmedoid_kmeans_parameters(self, event=None):
        self.frame_kmedoid_parameters.pack_forget()


    def random_sequences(self):
        global data
        data = IP.random_sequences()

def create_window():
    fenetre = Tk()
    fenetre.geometry("1370x700")
    fenetre.title("【D】【a】【t】【a】【Z】【u】【t】")
    fenetre['bg'] = 'silver'

    return fenetre


if __name__ == '__main__':
    fenetre = create_window()

    app = Page(fenetre)
    fenetre.mainloop()
