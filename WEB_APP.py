from flask import Flask, render_template, request
import sympy as sp
import numpy as np
from math import sin, cos, tan

SimbolosTotales = sp.symbols('x y z w g m k')
e = sp.symbols('e')
pi = sp.symbols('pi')
Error = []
Jacobiana = []
Funciones = []
VectorInicial = []
SimbolosUsados = []
FuncionesInvertidas = []
SolucionesJacobiana = []
SolucionesFuncionesNegativas = []
SimboloValor = {e : 2.718281828459045, pi : 3.141592653589793}
X = 0
Iteraciones = 0
Tolerancia = 0
NumVar = 0

app = Flask(__name__)
app.static_folder = 'static'

def Solver():
    
    global SimbolosTotales
    global e
    global pi
    global Jacobiana
    global VectorInicial
    global SimbolosUsados
    global FuncionesInvertidas
    global Error
    global SimboloValor
    global X
    global NumVar
    global Funciones
    global Iteraciones
    global SolucionesJacobiana
    global SolucionesFuncionesNegativas
    global Tolerancia
    
    for i in range (NumVar):
        for Simbolo in SimbolosTotales:
            if (str)(Simbolo) in Funciones[i]:
                if Simbolo not in SimbolosUsados:
                    SimbolosUsados.append(Simbolo)
                Jacobiana.append(sp.diff(Funciones[i], Simbolo))
    Funciones = sp.sympify(Funciones)
    for i in range (len(Funciones)):
        FuncionesInvertidas.append(-1*Funciones[i])
        
    for Iteracion in range(Iteraciones):
        
        for i in range(len(VectorInicial)):
            SimboloValor[SimbolosUsados[i]] = VectorInicial[i]

        VectorH = []
        VectorJ = []
        
        for Funcion in FuncionesInvertidas:
            VectorH.append((float)("{:.5f}".format(Funcion.subs(SimboloValor))))
    
        for Funcion in Jacobiana:
            VectorJ.append((float)("{:.5f}".format(Funcion.subs(SimboloValor))))
    
        VectorH = np.array(VectorH)
        VectorJ = np.array(VectorJ)
        VectorJ = np.reshape(VectorJ, (NumVar, NumVar))
        X = np.linalg.solve(VectorJ, VectorH)
        XAnterior = VectorInicial
        XAnterior = np.array(XAnterior)
        X += XAnterior
        SolucionesJacobiana.append(VectorJ)
        SolucionesFuncionesNegativas.append(VectorH)
        Error.append(np.sqrt(np.sum((X-XAnterior)**2)))
        
        for j in range(len(Error)):
            Error[j] = float("{:.5f}".format(Error[j]))
            
        for i in range(len(X)):
            X[i] = "{:.5f}".format(X[i])
        VectorInicial = X
        if(Error[Iteracion] < Tolerancia):
            break

@app.route('/', methods=['GET', 'POST'])
def Index():
    return render_template('Index.html')

@app.route('/Sistema', methods=['POST'])
def Sistema():
    global NumVar
    NumVar = (int)(request.form['NumVariables'])
    return render_template('Sistema.html', NumVar = NumVar)

@app.route('/Solucion', methods=['POST'])
def Solucion():
    global Funciones
    global NumVar
    global SimbolosTotales
    global VectorInicial
    global Iteraciones
    global Jacobiana
    global Tolerancia
    for i in range(NumVar):
        input_name = 'Funcion' + str(i+1)
        Funciones.append(request.form[input_name])
    for i in range(NumVar):
        input_name = 'ValorVariable' + str(i+1)
        VectorInicial.append((float)(request.form[input_name]))
    Iteraciones = (int)(request.form['Iteraciones'])
    Tolerancia = (float)(request.form['Error'])
    Solver()
    Jacobiana = np.reshape(Jacobiana, (NumVar,NumVar))
    return render_template('Solucion.html', X = X ,SolucionesJacobiana = SolucionesJacobiana, SolucionesFuncionesNegativas = SolucionesFuncionesNegativas, Error = Error, FuncionesInvertidas=FuncionesInvertidas, Jacobiana=Jacobiana)

@app.route('/Jacobiana')
def MatrizJacobiana():
    return render_template('Jacobiana.html', Jacobiana=Jacobiana)

@app.route('/FuncionesInvertidas')
def MatrizFuncionesInvertidas():
    return render_template('FuncionesInvertidas.html', FuncionesInvertidas=FuncionesInvertidas)


if __name__ == '__main__':
    app.run()

#x**2 - 10*x + y**2 + 8
#x*y**2 + x - 10*y + 8

#3*x - cos(y*z) - 0.5
#x**2 - 81* (y + 0.1)**2 + sin(z) + 1.06
#e**(-x*y) + 20*z + ((10*pi-3)/(3))
