import numpy as np
import matplotlib.pyplot as plt



class FWSBlackBox1Plant:


    def __init__(self) -> None:

        # Constants
        self.TIME_STEP  = 0.01
        self.SIM_TIME   = 1500
        
        # Attributes
        self.Kp         = 0.0
        self.Ki         = 0.0
        self.Kd         = 0.0
        self.sum_err    = 0.0
        self.last_err   = 0.0

        self.time = 0.0
        self.x = np.array([
            [0.3]
        ])
        self.A = lambda eps : np.array([
            [0.3 + eps + 7*np.sin(2*np.pi*0.5*self.time)]
        ])
        self.B = lambda eps: np.array([
            [1 + eps + 0.01*np.cos(2*np.pi*0.5*self.time)]
        ])

        self.tot_err    = 0.
        self.power      = 0.
        self.score      = 0.


    def setKpValue(self, kp:float) -> None:
        self.Kp = kp


    def setKiValue(self, ki:float) -> None:
        self.Ki = ki


    def setKdValue(self, kd:float) -> None:
        self.Kd = kd


    def getCurrentState(self) -> float:
        return self.x[0].item() + 0.1*np.random.rand()
    

    def getCurrentTime(self) -> float:
        return self.time
    

    def getCurrentTarget(self) -> float:
        return 0.5*np.sin(2*np.pi*0.5*self.time)


    def getScore(self) -> float:
        score = 1000./self.tot_err + 1000./np.fabs(self.power)
        if score < 1:
            return 0
        else:
            return score*10


    def calcInput(self) -> np.ndarray:
        pass


    def stepSimulation(self) -> None:
        # Calculate control input
        err             = self.getCurrentTarget() - self.getCurrentState()
        self.sum_err    = self.sum_err + err
        u               = np.array([[self.Kp*err + self.Ki*self.sum_err + self.Kd*(err - self.last_err)]])
        self.last_err   = err

        # Calculate next state
        x_dot       = self.A(0.1*np.random.rand())@self.x + self.B(0.1*np.random.rand())@u
        self.x      = self.x + x_dot*self.TIME_STEP
        self.time   += self.TIME_STEP

        # Calculate the score
        self.tot_err    += np.fabs(self.getCurrentTarget() - self.getCurrentState())
        self.power      += np.fabs(u[0].item())