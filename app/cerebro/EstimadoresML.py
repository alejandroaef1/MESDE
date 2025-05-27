import numpy as np

class EstimadoresMl:
    
    def __init__(self,t_final,X):

        self.X = np.array(X)
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

        
        # mu
        XultimoInv = 1/self.X[:-1]
        XDif = np.diff(self.X)
        IntegralItoXInv = np.sum(XultimoInv*XDif)
        mu = IntegralItoXInv/self.T

        dicc = {'Precio final':XT,'Precio inicial':X0,'Horizonte de tiempo':self.T,'Número de pasos':N,'Tamaño de paso':self.T/N,'μ':mu,'σ':sigma}
        print('Precio final:')
        print(XT)
        print('Precio inicial:')
        print(X0)
        print('Horizonte de tiempo:')
        print(self.T)
        print('Número de pasos:')
        print(N)
        print('Tamaño de paso:')
        print(self.T/N)
        print('mu:')
        print(mu)
        print('sigma:')
        print(sigma)

        
        return mu, sigma, dicc




        






