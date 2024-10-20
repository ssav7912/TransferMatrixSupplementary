import numpy as np
import struct
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from symfit import parameters, variables, Fit, Poly, Model
import symfit

def load_lut_from_file(path: str, dim: int):
    with open(path, 'rb') as lut:
        
        
        size = [int.from_bytes(lut.read(4), 'little') for x in range(dim)]
        minmax = [(struct.unpack('f', lut.read(4))[0], struct.unpack('f', lut.read(4))[0]) for x in range(dim)]
        
        buffer = lut.read()


        print(size)
        print(minmax)

        flatarray = np.frombuffer(buffer, dtype=np.float32)
        flatarray = np.reshape(flatarray, size)

        return flatarray



TIR = load_lut_from_file("tm_TIR.bin", 3)



X, Y, Z  = np.mgrid[0:1:64j, 0:1:64j, 0:1:64j]

incident, alpha, ior, energy = variables('incident, alpha, ior, energy')
c1, c2, c3 = parameters('c1,c2,c3')
model_dict = {energy: symfit.Poly( {(1,2,3): c1, (4,5,2): c2, (3,4,7): c3}, incident,alpha,ior)}
model = Model(model_dict)
print(model)

fit = Fit(model, incident=X, alpha=Y, ior=Z, energy=TIR.flatten())
fit_result = fit.execute()

print(fit_result)