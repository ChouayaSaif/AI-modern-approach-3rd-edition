import os
import sys
from tkinter import *
from tkinter import ttk

# Ensure the search module is independent
import random

def init_population(size, gene_pool, target_length):
    return [[random.choice(gene_pool) for _ in range(target_length)] for _ in range(size)]

def fitness_fn(individual, target):
    return sum(1 for i, j in zip(individual, target) if i == j)

def select(population, target):
    return sorted(population, key=lambda x: fitness_fn(x, target), reverse=True)[:2]

def recombine(parent1, parent2):
    crossover = random.randint(0, len(parent1) - 1)
    return parent1[:crossover] + parent2[crossover:]

def mutate(individual, gene_pool, mutation_rate):
    return [random.choice(gene_pool) if random.random() < mutation_rate else gene for gene in individual]

def fitness_threshold(population, target):
    for individual in population:
        if fitness_fn(individual, target) == len(target):
            return individual
    return None

# GUI Settings
LARGE_FONT = ('Verdana', 12)
EXTRA_LARGE_FONT = ('Consolas', 36, 'bold')
canvas_width, canvas_height = 800, 600
black, white, p_blue, lp_blue = '#000000', '#ffffff', '#042533', '#0c394c'

target = 'Genetic Algorithm'
max_population = 100
mutation_rate = 0.1
f_thres = len(target)
ngen = 1200

generation = 0

u_case = [chr(x) for x in range(65, 91)]
l_case = [chr(x) for x in range(97, 123)]

# Extend the gene pool
gene_pool = u_case + l_case + [' ']

# Callbacks
def update_max_population(value):
    global max_population
    max_population = int(value)

def update_mutation_rate(value):
    global mutation_rate
    mutation_rate = float(value)

def update_f_thres(value):
    global f_thres
    f_thres = int(value)

def update_ngen(value):
    global ngen
    ngen = int(value)

def raise_frame(frame, init=False, update_target=False, target_entry=None, f_thres_slider=None):
    frame.tkraise()
    global target
    if update_target and target_entry is not None:
        target = target_entry.get()
        f_thres_slider.config(to=len(target))
    if init:
        population = init_population(max_population, gene_pool, len(target))
        genetic_algorithm_stepwise(population)

# GUI
root = Tk()
f1, f2 = Frame(root), Frame(root)
for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')

target_entry = Entry(f1, font=('Consolas 46 bold'), justify=CENTER)
target_entry.insert(0, target)
target_entry.pack(expand=YES, side=TOP, fill=X, padx=50)

def genetic_algorithm_stepwise(population):
    root.title('Genetic Algorithm')
    for generation in range(ngen):
        population = [mutate(recombine(*select(population, target)), gene_pool, mutation_rate) for _ in range(len(population))]
        best = ''.join(max(population, key=lambda x: fitness_fn(x, target)))
        canvas.delete('all')
        canvas.create_text(canvas_width / 2, 40, fill=p_blue, font='Consolas 46 bold', text=best)
        canvas.create_text((canvas_width * 0.5), (canvas_height * 0.95), fill=p_blue, font='Consolas 18 bold', text=f'Generation {generation}')
        canvas.update()
        if fitness_threshold(population, target):
            break

button = ttk.Button(f1, text='RUN', command=lambda: raise_frame(f2, init=True)).pack(side=BOTTOM, pady=50)
canvas = Canvas(f2, width=canvas_width, height=canvas_height)
canvas.pack(expand=YES, fill=BOTH, padx=20, pady=15)
button = ttk.Button(f2, text='EXIT', command=lambda: raise_frame(f1)).pack(side=BOTTOM, pady=15)
raise_frame(f1)
root.mainloop()