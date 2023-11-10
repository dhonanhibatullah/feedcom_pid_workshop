import numpy as np
import matplotlib.pyplot as plt



class FWSBlackBox1Plant:


    def __init__(self) -> None:

        # Constants
        self.TIME_STEP = 0.01
        
        # Attributes
        self.time = 0.0
        
        self.x = np.array([
            [0],
            [0],
            [0]
        ])

        self.A = lambda eps : np.array([
            [0, 1+eps, 0],
            [0, 0, 1+eps],
            [0, 0, 0]
        ])

        self.B = lambda eps: np.array([
            [0],
            [0],
            [1+eps]
        ])


    def stepSimulation(self, u:np.ndarray) -> None:
        x_dot       = self.A(0.08*np.random.rand())@self.x + self.B(0.08*np.random.rand())@u
        self.x      = self.x + x_dot*self.TIME_STEP
        self.time   += self.TIME_STEP


    def getStateVal(self) -> None:
        return self.x[0].item() + np.random.rand()*0.1
    

    def getCurrentTime(self) -> None:
        return self.time