class Cell:

    # kwargs.get('nameOfParametr', defaultValue)
    ### --- constructor of class Cell --- ###
    def __init__(self,**kwargs): 
       
        ### --- cordinates and basic parametrs of the cell --- ###
        
        self.myX = kwargs.get('myX', -1) 
        self.myY = kwargs.get('myY', -1)  
        self.myZ = kwargs.get('myZ', -1)

        self.myState = 0 # at the beginning all cells are healthy
        self.newState = self.myState # newState is to update states of cells at the same time
        self.stateChanged = False

        self.numberOfI2Iterations = 0  # only infected cell type 2 

        ### --- cell's neighbors --- ###
        self.wallMates = [] # list of the cell's neighbors which directly contact with the cell
        self.lineMates = [] # list of the cell's neighbors which touch the cell by line 
        self.pointMates = [] # list of the cell's neighbors which touch the cell by point (in the corners)

        ### --- rules of game --- ###
        # Healthy Cell --> Infected type 1 (one of the rules) -> fromWhatTOWhat_whichStateCounts_whichTypeOfNeighbor
        self.healthyTOI1_I1_1N = 1 # min. 1 I1 cell
        self.healthyTOI1_I2_1N = 5 # min. 5 I2 cell
        self.healthyTOI1_I2_2N = 9 # min. 9 I2 cell
        self.healthyTOI1_I2_3N = 4 # min. 4 I2 cell
        # I1 --> I2 (next iteration)
        # I2 --> D (after next 2 iteration)
        # D --> I1 (with probability of infection)
        # D --> H (with probability of replenision - probability of infection)


    ### --- counting number of cell' neighbors in specific state --- ###
    def matesInSpecificState(self,listOfCell, specificState):
        states = [] # list of cell's neighbors' states
        for c in listOfCell:
            states.append(c.myState)
        return states.count(specificState)

    def __repr__(self):
        return str(self.myState)
    