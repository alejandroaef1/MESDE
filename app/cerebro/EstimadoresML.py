import numpy as np

class EstimadoresMl:
    
    def __init__(self,t_final,X):

        self.X = X
        self.T = t_final

    def estimaciones(self):
        
        # Parámetros de tiempo
        N = len(self.X)
        XT = self.X[-1]
        X0 =self.X[0]
  
        # sigma
        VarCuadX = np.sum(np.diff(self.X)**2)
        Deltat = self.T/N
        IntegralDif = Deltat*sum(self.X**2)
        sigma = np.sqrt(VarCuadX/IntegralDif)

        
        # m
        XultimoInv = 1/self.X[:-1]
        XDif = np.diff(self.X)
        IntegralItoXInv = np.sum(XultimoInv*XDif)
        mu = IntegralItoXInv/self.T
        
        return mu, sigma




        






