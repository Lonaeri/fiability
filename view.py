import tkinter as tk
from typing import List
from simulationController import *

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

        self.description = tk.Label(self, text="Attention : Tous les durées doivent être dans la même unité")
        self.description.pack(side="top")

        errors_frame = tk.Frame(self)
        self.errors = tk.Label(errors_frame, fg="#f00")
        errors_frame.pack()

        # Nb of systems
        self.frame_nb_simulation = tk.Frame(master=self)
        tk.Label(self.frame_nb_simulation, text="Nombre de simulations").pack(side = tk.LEFT)
        tk.Entry(self.frame_nb_simulation, name="nbSystems").pack(side = tk.LEFT)
        self.frame_nb_simulation.pack()

        # Duration of the simulation
        self.frame_duration = tk.Frame(master=self)
        tk.Label(self.frame_duration, text="Durée de la simulation").pack(side = tk.LEFT)
        tk.Entry(self.frame_duration, name="duration", validatecommand=self.changeRecommendation, validate="focusout").pack(side = tk.LEFT)
        self.frame_duration.pack()
        
        # MTFF : Mean time to first failure 
        # λ : number of expected occurrences
        radios = tk.Frame(master=self)
        self.radio_value = tk.IntVar()
        radio_lambda = tk.Radiobutton(radios, text="Lambda", cursor="hand2", variable=self.radio_value, value=1, command=self.change_option)
        radio_lambda.select()
        radio_lambda.pack(side = tk.LEFT)
        tk.Radiobutton(radios, text="mtff", cursor="hand2", variable=self.radio_value, value=2, command=self.change_option).pack(side = tk.LEFT)
        radios.pack()

        self.frame_lambda_mtff = tk.Frame(master=self)
        tk.Label(self.frame_lambda_mtff, text="Cadence des pannes", name="lambdaMtffLabel").pack(side = tk.LEFT)
        tk.Entry(self.frame_lambda_mtff, name="probability").pack(side = tk.LEFT)
        self.frame_lambda_mtff.pack()

        self.frame_step = tk.Frame(master=self)
        tk.Label(self.frame_step, text="Nombre d'etapes de la simulation").pack(side = tk.LEFT)
        tk.Spinbox(self.frame_step, from_=1, to=NB_MAX_STEPS, name="nbSteps").pack(side = tk.LEFT)
        tk.Label(self.frame_step, text="Entre 1 et " + str(NB_MAX_STEPS) + " étapes", name="recommendation").pack(side=tk.BOTTOM)
        self.frame_step.pack()

        self.submit = tk.Button(self, text="Envoyer", command=self.submitForm)
        self.submit.pack()

        self.simu = tk.Frame(master=self)
        self.scale = tk.Scale(master=self.simu, orient=tk.HORIZONTAL, from_=1, command=self.go_to_step)
        self.simu.pack()

    def submitForm(self):
        nb_systems = self.getNbSystems()
        error, self.all_steps = calculSimulations(
            nb_systems,
            self.getDuration(),
            self.getProbability(),
            self.getNbSteps()
        )
        if (error != 0):
            self.errors.configure(text="Format des données entrées invalides")
            self.errors.pack()
            return

        self.errors.pack_forget()

        self.generate_steps_cursor(self.getNbSteps())
        self.generate_first_step(nb_systems)

    def change_option(self):
        if (self.radio_value.get() == 1) :
            self.frame_lambda_mtff.children['lambdaMtffLabel'].configure(text="Cadence des pannes")
        else :
            self.frame_lambda_mtff.children['lambdaMtffLabel'].configure(text="Moyenne avant 1ere panne")

    def changeRecommendation(self):
        duration = self.getDuration()
        if (duration <= 0):
            return False
        recommendationNb = stepRecommendation(duration)
        self.frame_step.children['recommendation'].configure(text="Entre 1 et " + str(NB_MAX_STEPS) + " étapes. Recommandé : " + str(recommendationNb))
        return True

    ##############
    # Draw Steps #
    ##############
    def generate_steps_cursor(self, nbSteps):
        if (self.scale):
            self.scale.configure(to=nbSteps)
            self.scale.pack(side=tk.TOP)

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
            aLabel = tk.Label(simu_view_frame, bg = "#0f0", padx=8, bd=1, relief="solid")
            aLabel.grid(row=int(index//nb_col), column=int(index%nb_col))
            self.systems_view.append(aLabel)
        simu_view_frame.pack()
        self.step_frame.pack()

    def go_to_step(self, step):
        self.step_frame.configure(text=f"Etape #{step}")
        nb_remains, reliability = self.all_steps[int(step) - 1]
        for index, system in enumerate(self.systems_view):
            if (index >= nb_remains):
                system.configure(bg='#f00')
            else :
                system.configure(bg='#0f0')

    ################
    # Data Getters #
    ################
    def getNbSystems(self) : 
        try:
            return int(self.frame_nb_simulation.children['nbSystems'].get())
        except ValueError:
            print("NaN : Nombre de systemes à simuler")
            return -1

    def getDuration(self) : 
        try:
            return int(self.frame_duration.children['duration'].get())
        except ValueError:
            print("NaN : Durée de la simulation")
            return -1
    
    def getProbability(self):
        try:
            return (
                self.radio_value.get(),
                float(self.frame_lambda_mtff.children['probability'].get())
            )
        except ValueError:
            print("NaN : Probabilité")
            return (-1, -1)

    def getNbSteps(self) : 
        try:
            return int(self.frame_step.children['nbSteps'].get())
        except ValueError:
            print("NaN : Nombre d'etapes")
            return -1