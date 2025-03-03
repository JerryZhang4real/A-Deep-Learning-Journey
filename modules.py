from engine import Value
import random

class Module:

    def parameters(self):
        return []

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0


class Neuron(Module):

    def __init__ (self, nin, nonlin=True):
        self.wights = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.bias = Value(0)
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum([w*x for w, x in zip(self.wights, x)]) + self.bias

        def act_relu():
            return act if act > 0 else 0

        return act_relu() if self.nonlin else act

    def parameters(self):
        return self.wights + [self.bias]

    def __repr__(self):
        return f"{'ReLU ' if self.nonlin else 'Linear '}Neuron({len(self.wights)})"

class Layer(Module):

    def __init__(self, nin, nout, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]

    def __call__(self, x):
        out  = [n(x) for n in self.neurons]
        return out if len(out) == 1 else out

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

    def __repr__(self):
        return f"Layer of [{', '.join(str(n) for n in self.neurons)}]"


class MLP(Module):

    def __init__(self, nin, nouts):
        sz = [nin] + nouts
        self.layers = [Layer(sz[i],  sz[i+1], nonline=i!=len(nouts)-1) for i in range(len(nouts))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def __repr__(self):
        return f"MLP of [{', '.join(str(layer) for layer in self.layers)}]"