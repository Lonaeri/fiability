import tkinter as tk
from typing import List

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry('600x600')

    def create_widgets(self):
        self.description = tk.Label(self, text="Attention : Tous les durées doivent être dans la même unité", fg="#f00")
        self.description.pack(side="top")

        # Nb of systems
        self.frame_nb_simulation = tk.Frame(master=self)
        label_nb_simulations = tk.Label(self.frame_nb_simulation, text="Nombre de simulations")
        entry_nb_simulations = tk.Entry(self.frame_nb_simulation)
        label_nb_simulations.pack(side = tk.LEFT)
        entry_nb_simulations.pack(side = tk.LEFT)
        self.frame_nb_simulation.pack()

        # Duration of the simulation
        self.frame_duration = tk.Frame(master=self)
        label_duration = tk.Label(self.frame_duration, text="Durée de la simulation")
        entry_duration = tk.Entry(self.frame_duration)
        label_duration.pack(side = tk.LEFT)
        entry_duration.pack(side = tk.LEFT)
        self.frame_duration.pack()
        
        # MTFF : Mean time to first failure 
        # λ : number of expected occurrences
        self.choose_with_radio = tk.LabelFrame(master=self, text="Choose with radio")

        self.radios = tk.Frame(master=self.choose_with_radio)
        self.radio_value = tk.IntVar()
        radio_lambda = tk.Radiobutton(self.radios, text="Lambda", variable=self.radio_value, value=1, command=self.change_option)
        radio_mtbf = tk.Radiobutton(self.radios, text="MTBF", variable=self.radio_value, value=2, command=self.change_option)
        radio_lambda.pack(side = tk.LEFT)
        radio_mtbf.pack(side = tk.LEFT)
        self.radios.pack()

        self.frame_lambda_mtbf = tk.Frame(master=self.choose_with_radio)
        label_lambda_mtbf = tk.Label(self.frame_lambda_mtbf, text="Cadence des pannes") # TODO : a changer par "Moyenne avant 1ere panne"
        label_lambda_mtbf.pack(side = tk.LEFT)
        entry_lambda_mtbf = tk.Entry(self.frame_lambda_mtbf)
        entry_lambda_mtbf.pack(side = tk.LEFT)
        self.frame_lambda_mtbf.pack()
        self.choose_with_radio.pack()


        self.frame_step = tk.Frame(master=self)
        label_step = tk.Label(self.frame_step, text="Pas de la simulation")
        entry_step = tk.Spinbox(self.frame_step)
        label_step.pack(side = tk.LEFT)
        entry_step.pack(side = tk.LEFT)
        self.frame_step.pack()

        self.simu = tk.Frame(master=self)
        self.simu.pack()
        # l1 = tk.Label(self, text="This", borderwidth=2, relief="groove")
        # l1.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def change_option(self):
        if (self.radio_value.get() == 1) :
            for child in self.frame_lambda_mtbf.winfo_children():
                print("\n=== New Child ===")
                print(child.winfo_class())
                print(child.winfo_id())
                print(child.winfo_name())
                print(child.winfo_parent())
        else :
            self.frame_lambda_mtbf.pack()


    def say_hi(self):
        print("hi there, everyone!")

    def generate_steps_cursor(self, nbSteps):
        self.currentStep = tk.IntVar()
        scale = tk.Scale(master=self.simu, variable = self.currentStep, orient=tk.HORIZONTAL, from_=1, to=nbSteps, command=self.go_to_step)
        scale.pack(side=tk.TOP)

    def generate_steps(self, steps : List[List[List[bool]]]):
        self.generate_steps_cursor(len(steps))
        self.stepsFrame = []
        for stepIndex, stepFrame in enumerate(steps):
            self.stepsFrame.append(tk.LabelFrame(master=self.simu, width = 200, text=("Step #" + str(stepIndex + 1))))
            for lineIndex, lineValues in enumerate(stepFrame):
                for colIndex, colValue in enumerate(lineValues):
                    aLabel = tk.Label(self.stepsFrame[stepIndex], bg = "#0f0", padx=8, bd=1, relief="solid")
                    aLabel.grid(row=lineIndex, column=colIndex)
                    if (False == colValue) :
                        aLabel.configure(bg="#f00")
        self.stepsFrame[0].pack()

    def go_to_step(self, step):
        for stepIndex, stepFrame in enumerate(self.stepsFrame):
            if (stepIndex == int(step) - 1):
                stepFrame.pack()
            else :
                self.stepsFrame[stepIndex].pack_forget()


root = tk.Tk()

app = Application(master=root)

listTest = []
stepA = [
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True]
]
stepB = [
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, False, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, False, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, False, True],
    [True, True, True, True, True, True, True, True, True, True]
] 
stepC = [
    [True, True, False, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, False, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, False, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, False, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, False, True],
    [True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, False, True],
    [True, True, True, True, True, True, True, True, True, True]
]

listTest.append(stepA)
listTest.append(stepB)
listTest.append(stepC)

app.generate_steps(listTest)

app.mainloop()
