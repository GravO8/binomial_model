from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Node(ABC):
    def __init__(self, option):
        self.option = option
        self.value = None
    def get_value(self):
        if self.value is not None:
            return self.value
        if self.t == self.option.T:
            self.value = max(self.option.g(self.s),0)
        else:
            self.up = UpNode(self.option, self)
            self.down = DownNode(self.option, self)
            delta = self.option.u - self.option.d
            x = (1/(1+self.option.R))*(self.option.u*self.down.get_value() - self.option.d*self.up.get_value())/delta
            y = (1/self.s)*(self.up.get_value() - self.down.get_value())/delta
            self.value = x + y*self.s
            if self.t < self.option.T-1:
                self.up.down = self.down.up
        return self.value
    def draw(self, plt, h = 0, already_ploted = []):
        pt = (self.t,h)
        if pt not in already_ploted:
            already_ploted.append(pt)
            plt.plot(self.t, h, "o", color = "blue", alpha = .2, markersize = 40)
            text = str( round(self.s,1) )
            plt.annotate(text, xy = (self.t,h), ha = "center", va = "center")
        if self.t < self.option.T:
            self.up.draw(plt, h+1, already_ploted)
            self.down.draw(plt, h-1, already_ploted)
            props = dict(arrowstyle="-|>,head_width=0.4,head_length=0.8",shrinkA=0,shrinkB=0,color="black")
            e = .0277*self.option.T - .0015
            plt.annotate("", xytext = (self.t+e,h+e), xy = (self.t+1-e,h+1), arrowprops = props)
            plt.annotate("", xytext = (self.t+e,h-e), xy = (self.t+1-e,h-1), arrowprops = props)

class Node0(Node):
    def __init__(self, option):
        Node.__init__(self,option)
        self.s = self.option.s0
        self.t = 0
        
class UpNode(Node):
    def __init__(self, option, parent):
        Node.__init__(self,option)
        self.s = parent.s * self.option.u
        self.t = parent.t+1
    
class DownNode(Node):
    def __init__(self, option, parent):
        Node.__init__(self,option)
        self.s = parent.s * self.option.d
        self.t = parent.t+1
        
class Option(ABC):
    def __init__(self, maturity, strike_price, interest_rate, s0, up_fraction, down_fraction):
        self.T = maturity
        self.K = strike_price
        self.R = interest_rate
        self.s0 = s0
        self.u = up_fraction
        self.d = down_fraction
        self.node0 = Node0(self)
    @abstractmethod
    def g(self, asset_price):
        '''payoff function'''
        pass
    def get_maturity_price(self, draw = False):
        self.price = self.node0.get_value()
        if draw:
            plt.figure(figsize = (20,7))
            self.node0.draw(plt)
            plt.xticks([i for i in range(self.T+1)], [i for i in range(self.T+1)])
            plt.yticks([],[])
            plt.xlabel("time")
            plt.show()
        return self.price
        
class Put(Option):
    def g(self, asset_price):
        return self.K - asset_price
class Call(Option):
    def g(self, asset_price):
        return asset_price - self.K
        
        
if __name__ == "__main__":
    option = Call(10,110,0,100,1.2,.8)
    print(option.get_maturity_price(True))
