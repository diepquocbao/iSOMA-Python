# --- SOMA Simple Program --- Version: iSOMA (V1.0) August 25, 2020 -------
# ------ Written by: Quoc Bao DIEP ---  Email: diepquocbao@gmail.com   ----
# -----------  See more details at the end of this file  ------------------
import numpy
import time
from List_of_CostFunctions import Schwefel as CostFunction

starttime = time.time()                                             # Start the timer
print('Hello! iSOMA is working, please wait... ')
dimension = 10                                                      # Number of dimensions of the problem
# -------------- Control Parameters of SOMA -------------------------------
N_jump, Step = 10, 0.3                                              # Assign values ​​to variables: Step, PRT, PathLength
PopSize, Max_Migration, Max_FEs = 100, 100, dimension*10**4         # Assign values ​​to variables: PopSize, Max_Migration
m, n, k = 10, 5, 15
# -------------- The domain (search space) --------------------------------
VarMin, VarMax = -500, 500   # for Schwefel's function.                    # Define the search range
# %%%%%%%%%%%%%%      B E G I N    S O M A    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ------------- Create the initial Population -----------------------------
pop = VarMin + numpy.random.rand(dimension, PopSize) * (VarMax - VarMin) # Create the initial Population
fitness = CostFunction(pop)                                         # Evaluate the initial population
FEs = PopSize                                                       # Count the number of function evaluations
the_best_cost = min(fitness)                                        # Find the Global minimum fitness value
# ---------------- SOMA MIGRATIONS ----------------------------------------
best_cost_old = the_best_cost
Migration, Count = 0, 0                                             # Assign values ​​to variables: Migration
while FEs < Max_FEs:                                                # Terminate when reaching Max_Migration / User can change to Max_FEs
    Migration = Migration + 1                                       # Increase Migration value
    # ------------ Migrant selection: m -----------------------------------
    M = numpy.random.choice(range(PopSize),m,replace=False)         # Migrant selection: m
    M_sort = numpy.argsort(fitness[M])
    for j in range(n):                                              # Choose n individuals move toward the Leader
        Migrant = pop[:, M[M_sort[j]]].reshape(dimension, 1)        # Get the Migrant position (solution values) in the current population
        # ------------ Leader selection: k --------------------------------
        K = numpy.random.choice(range(PopSize),k,replace=False)     # Leader selection: k
        K_sort = numpy.argsort(fitness[K])
        Leader = pop[:, K[K_sort[1]]].reshape(dimension, 1)         # Get the Migrant position (solution values) in the current population
        if M[M_sort[j]] == K[K_sort[1]]:                            # Don't move if it is itself
            Leader = pop[:, K[K_sort[2]]].reshape(dimension, 1)     # Get the Migrant position (solution values) in the current population
        # ------ Migrant move to Leader: Jumping --------------------------
        flag, move = 0, 1
        while (flag == 0) and (move <= N_jump):
            nstep = (N_jump-move+1) * Step
            # ------ Update Control parameters: PRT -----------------------
            PRT = 0.1 + 0.9*(FEs / Max_FEs);                        # Update PRT parameter
            # ----- SOMA Mutation -----------------------------------------
            PRTVector = (numpy.random.rand(dimension,1)<PRT)*1      # If rand() < PRT, PRTVector = 1, else, 0
            #PRTVector = (PRTVector - 1) * (1 - FEs/Max_FEs) + 1     # If rand() < PRT, PRTVector = 1, else, FEs/Max_FEs
            offspring = Migrant + (Leader - Migrant) * nstep * PRTVector # Jumping towards the Leader
            # ------------ Check and put individuals inside the search range if it's outside
            for rw in range(dimension):                             # From row: Check
                if offspring[rw]<VarMin or offspring[rw]>VarMax:    # if outside the search range
                    offspring[rw] = VarMin + numpy.random.rand() * (VarMax - VarMin) # Randomly put it inside
            # ------------ Evaluate the offspring and Update --------------
            new_cost = CostFunction(offspring)                      # Evaluate the offspring
            FEs = FEs + 1                                           # Count the number of function evaluations
            # ----- SOMA Accepting: Place the Best Offspring to Pop -------
            if new_cost <= fitness[M[M_sort[j]]]:                   # Compare min_new_cost with fitness value of the moving individual
                flag = 1
                fitness[M[M_sort[j]]] = new_cost                    # Replace the moving individual fitness value
                pop[:, [M[M_sort[j]]]] = offspring                  # Replace the moving individual position (solution values)
                if new_cost < the_best_cost:                        # Compare Current minimum fitness with Global minimum fitness
                    the_best_cost = new_cost                        # Update Global minimun fitness value
                    the_best_value = offspring                      # Update Global minimun position
                else:
                    Count = Count + 1
            move = move + 1
    if Count > PopSize*50:
        if the_best_cost == best_cost_old:
            rat = round(0.1*PopSize)
            pop_temp = VarMin + numpy.random.rand(dimension, rat)*(VarMax-VarMin)
            fit_temp = CostFunction(pop_temp)
            FEs = FEs + rat
            D = numpy.random.choice(range(PopSize),rat,replace=False)
            pop[:,D] = pop_temp
            fitness[D] = fit_temp
        else:
            best_cost_old = the_best_cost
        Count = 0
# %%%%%%%%%%%%%%%%%%    E N D    S O M A     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
endtime = time.time()                                               # Stop the timer
caltime = endtime - starttime                                       # Caculate the processing time
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Show the information to User
print('Stop at Migration :  ', Migration)
print('The number of FEs :  ', FEs)
print('Processing time   :  ', caltime, '(s)')
print('The best cost     :  ', the_best_cost)
print('Solution values   :  ', the_best_value)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


"""
This algorithm is programmed according to the descriptions in the article:

Link of the article:

https://www.sciencedirect.com/science/article/pii/S1568494621010851

Please cite the article if you refer to them, as follows:

	Diep, Quoc Bao, Thanh Cong Truong, Swagatam Das, and Ivan Zelinka. "Self-Organizing Migrating Algorithm with narrowing search space strategy for robot path planning." Applied Soft Computing (2021), doi: https://doi.org/10.1016/j.asoc.2021.108270

OR:
	@article{DIEP2021108270,
	title = {Self-Organizing Migrating Algorithm with narrowing search space strategy for robot path planning},
	journal = {Applied Soft Computing},
	pages = {108270},
	year = {2021},
	issn = {1568-4946},
	doi = {https://doi.org/10.1016/j.asoc.2021.108270},
	url = {https://www.sciencedirect.com/science/article/pii/S1568494621010851},
	author = {Quoc Bao Diep and Thanh Cong Truong and Swagatam Das and Ivan Zelinka}
	}


The control parameters PopSize, N_jump, m, n, and k are closely related 
and greatly affect the performance of the algorithm. Please refer to the 
above paper to use the correct control parameters.

The iSOMA will be adjusted in the near future for faster execution (using Vectorization)
and rebuilt to address more complex computational functions (a few minutes to complete one FEs)
that take advantage of Parallel Computing Toolbox to execute on supercomputer.

The iSOMA is also available in Matlab, python, and C# version, alongside some other versions like SOMA T3A and SOMA Pareto.

If you encounter any problems in executing these codes, please do not hesitate to contact:
Dr. Quoc Bao Diep (diepquocbao@gmaill.com.)
"""