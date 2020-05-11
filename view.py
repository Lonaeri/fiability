import tkinter as tk
from typing import List
from simulationController import *
import tkinter.font as tkFont

class View(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry('600x600')

    def create_widgets(self):
        self.systems_view = []
        self.stepsFrame = []
        
        self.title = tk.Label(self, 
            text="Equipement de Vaisseau Spatial",
            font = tkFont.Font(size=16, weight="bold", underline=1))
        self.title.pack(side="top")

        self.description = tk.Label(self,pady=5,font=tkFont.Font(size=10, slant='italic'), text="Attention : Tous les durées doivent être dans la même unité")
        self.description.pack(side="top")

        errors_frame = tk.Frame(self)
        self.errors = tk.Label(errors_frame, fg="#f00")
        errors_frame.pack()

        # Nb of systems
        self.frame_nb_simulation = tk.Frame(master=self, pady=7)
        tk.Label(self.frame_nb_simulation, text="Nombre de simulations").pack(side = tk.LEFT)
        tk.Entry(self.frame_nb_simulation, name="nbSystems").pack(side = tk.LEFT)
        self.frame_nb_simulation.pack()
        
        # MTFF : Mean time to first failure 
        # λ : number of expected occurrences
        group_radio = tk.LabelFrame(master=self, pady=7, padx=7)
        radios = tk.Frame(master=group_radio)
        self.radio_value = tk.IntVar()
        radio_lambda = tk.Radiobutton(radios, text="Lambda", cursor="hand2", variable=self.radio_value, value=1, command=self.change_option)
        radio_lambda.select()
        radio_lambda.pack(side = tk.LEFT)
        tk.Radiobutton(radios, text="mtff", cursor="hand2", variable=self.radio_value, value=2, command=self.change_option).pack(side = tk.LEFT)
        radios.pack()

        self.frame_lambda_mtff = tk.Frame(master=group_radio)
        tk.Label(self.frame_lambda_mtff, text="Cadence des pannes", name="lambdaMtffLabel").pack(side = tk.LEFT)
        tk.Entry(self.frame_lambda_mtff, name="probability").pack(side = tk.LEFT)
        self.frame_lambda_mtff.pack()
        group_radio.pack()


        self.frame_beta = tk.Frame(master=self, pady=11)
        tk.Label(self.frame_beta, text="Beta (default : 1)").pack(side = tk.LEFT)
        beta = tk.Entry(self.frame_beta, name="beta")
        beta.pack(side = tk.LEFT)
        beta.insert(tk.INSERT, "1")
        self.frame_beta.pack()

        self.frame_step_group = tk.LabelFrame(master=self, text="Pas à pas")
        # Duration of the simulation
        self.frame_duration = tk.Frame(master=self.frame_step_group)
        tk.Label(self.frame_duration, text="Durée de la simulation").pack(side = tk.LEFT)
        tk.Entry(self.frame_duration, name="duration", validatecommand=self.change_recommendation, validate="focusout").pack(side = tk.LEFT)
        self.frame_duration.pack()

        self.frame_step = tk.Frame(master=self.frame_step_group)
        tk.Label(self.frame_step, text="Nombre d'etapes de la simulation").pack(side = tk.LEFT)
        tk.Spinbox(self.frame_step, from_=1, to=NB_MAX_STEPS, name="nb_steps").pack(side = tk.LEFT)
        self.frame_step.pack()
        tk.Label(self.frame_step_group, text="Entre 1 et " + str(NB_MAX_STEPS) + " étapes", font=tkFont.Font(size=8, slant='italic'), name="recommendation").pack()
        self.frame_step_group.pack()

        self.submit = tk.Button(self, text="Envoyer", command=self.submitForm)
        self.submit.pack()
        

        self.simu = tk.Frame(master=self)
        self.scale = tk.Scale(master=self.simu, orient=tk.HORIZONTAL, from_=1, command=self.go_to_step)
        self.text_step = tk.Text(master=self.simu, width=50, height=10)
        self.simu.pack()

    def submitForm(self):
        nb_systems = self.get_nb_systems()
        error, self.cur_simulation = calcul_simulations(
            nb_systems,
            self.get_duration(),
            self.get_probability(),
            self.get_nb_steps(),
            self.get_beta()
        )
        if (error != 0):
            self.errors.configure(text="Format des données entrées invalides")
            self.errors.pack()
            return

        self.errors.pack_forget()

        self.generate_steps_cursor(self.get_nb_steps())
        self.generate_first_step(nb_systems)
        self.go_to_step(1)

    def change_option(self):
        if (self.radio_value.get() == 1) :
            self.frame_lambda_mtff.children['lambdaMtffLabel'].configure(text="Cadence des pannes")
        else :
            self.frame_lambda_mtff.children['lambdaMtffLabel'].configure(text="Moyenne avant 1ere panne")

    def change_recommendation(self):
        duration = self.get_duration()
        if (duration <= 0):
            return False
        nb_recommendation = step_recommendation(duration)
        self.frame_step_group.children['recommendation'].configure(text="Entre 1 et " + str(NB_MAX_STEPS) + " étapes. Recommandé : " + str(nb_recommendation))
        return True

    ##############
    # Draw Steps #
    ##############
    def generate_steps_cursor(self, nb_steps):
        self.scale.configure(to=nb_steps)
        if (False == self.scale.winfo_ismapped()):
            self.scale.pack(side=tk.TOP)
            self.text_step.pack(side=tk.BOTTOM)

    def clean_steps(self):
        self.step_frame.destroy()

    def generate_first_step(self, nb_systems: int):
        if (len(self.systems_view)):
            self.clean_steps()
        MAX_WIDTH = 100
        nb_col = np.ceil(np.sqrt(nb_systems)) # Obtenir un carré où la dernière ligne peut etre incomplete
        # TODO Réduire la largeur selon la taille de la fenêtre
        if (nb_col > MAX_WIDTH):
            nb_col = MAX_WIDTH

        self.step_frame = tk.LabelFrame(master=self.simu, text=("Etape #1"))
        simu_view_frame = tk.Frame(self.step_frame)
        self.systems_view = []
        for index in range(0, nb_systems):
            a_label = tk.Label(simu_view_frame, bg = "#0f0", padx=8, bd=1, relief="solid")
            a_label.grid(row=int(index//nb_col), column=int(index%nb_col))
            self.systems_view.append(a_label)
        simu_view_frame.pack()
        self.step_frame.pack(side=tk.TOP)

    def change_step_description(self, step):
        self.text_step.delete("1.0", tk.END)
        self.text_step.insert(tk.INSERT, f"MTFF réel de la Simu : {self.cur_simulation.real_mtff}\n")
        self.text_step.insert(tk.INSERT, f"\nEtape #{step+1}\n")
        self.text_step.insert(tk.INSERT, f"t : {(self.cur_simulation.duration / self.cur_simulation.nb_steps) * (step + 1)}\n")
        self.text_step.insert(tk.INSERT, f"Nombre de systemes : {self.cur_simulation.nb_systems}\n")
        self.text_step.insert(tk.INSERT, f"  -> defaillants : {self.cur_simulation.breakdowns[step]}\n")
        self.text_step.insert(tk.INSERT, f"  -> OK : {self.cur_simulation.nb_systems - self.cur_simulation.breakdowns[step]}\n")
        self.text_step.insert(tk.INSERT, f"Pannes simulées {round(((self.cur_simulation.breakdowns[step] / self.cur_simulation.nb_systems) * 100), 2)}%\n")

    def go_to_step(self, step):
        step_index = int(step) - 1
        self.step_frame.configure(text=f"Etape #{step}")
        breakdowns = self.cur_simulation.breakdowns[step_index]
        for index, system in enumerate(self.systems_view):
            if (index >= breakdowns):
                system.configure(bg='#0f0')
            else :
                system.configure(bg='#f00')
        self.change_step_description(step_index)

    ################
    # Data Getters #
    ################
    def get_nb_systems(self) : 
        try:
            return int(self.frame_nb_simulation.children['nbSystems'].get())
        except ValueError:
            print("NaN : Nombre de systemes à simuler")
            return -1

    def get_duration(self) : 
        try:
            return int(self.frame_duration.children['duration'].get())
        except ValueError:
            print("NaN : Durée de la simulation")
            return -1
    
    def get_probability(self):
        try:
            return (
                self.radio_value.get(),
                float(self.frame_lambda_mtff.children['probability'].get())
            )
        except ValueError:
            print("NaN : Probabilité")
            return (-1, -1)

    def get_nb_steps(self) : 
        try:
            return int(self.frame_step.children['nb_steps'].get())
        except ValueError:
            print("NaN : Nombre d'etapes")
            return -1

    def get_beta(self) :
        try:
            return float(self.frame_beta.children['beta'].get())
        except ValueError:
            print("NaN : Beta")
            return -1