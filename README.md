# Project
Covid Project

 It is possible to run main.py to test several different scenarios (with/without restrictions, with/without vaccination and hybrid solutions).
 This file load the data from the Italian repository, then it is possible to select which region evaluate. For each simulation, some plots are drawn.
 
 File runSimulation contains two different function: one to run several simulations to fit the suitable value for beta (on the first "endTrain" days), another to run a simulation given a value for beta and draw the plot SIR vs real Data.
 File utility contains some functions useful to preprocess data (there are no missing data) removing some columns
 File fittingBeta contains the function to fit the suitable value for beta. Such function is then called in runSimulation
 File SirModel contains the definition of SirModel and Network. It also contains functions to initialise the network and to run the simulations. There are also functions implementing restrictive measures and vaccination.
  
 File SEIR is standalone. It contains the definitions useful to run the SEIR model.
 
