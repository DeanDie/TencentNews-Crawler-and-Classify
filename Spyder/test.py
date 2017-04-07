
import theano.tensor as T
import theano

x = T.dscalar('x')
y = x ** 2
print(theano.pp(y))
gy = T.grad(y, x)
print(theano.pp(gy))
f = theano.function([x], gy)
print(f(4))
print(theano.pp(f.maker.fgraph.outputs[0]))