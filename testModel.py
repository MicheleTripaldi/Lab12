
from model.model import Model

mymodel = Model()

g = mymodel.buildGraph("France",2015)
print(mymodel.getNumNodi(), mymodel.getNumArchi())
print(mymodel.getVolumi())
