from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from math import factorial

def C(n,r):
    return factorial(n)/(factorial(r)*factorial(n-r))

class Node(ABC):
    def __init__(self, option):
        self.option = option
        self.value = None
    def get_value(self):
        if self.value is not None:
            return self.value
        if self.t == self.option.T:
            self.value = self.option.g(self.s)
        else:
            self.up = UpNode(self.option, self)
            self.down = DownNode(self.option, self)
            delta = self.option.u - self.option.d
            self.x = (1/(1+self.option.R))*(self.option.u*self.down.get_value() - self.option.d*self.up.get_value())/delta
            self.y = (1/self.s)*(self.up.get_value() - self.down.get_value())/delta
            self.value = self.x + self.y*self.s
            if self.t < self.option.T-1:
                self.up.down = self.down.up
        return self.value
    def draw(self, plt, h = 0, already_ploted = []):
        pt = (self.t,h)
        if pt not in already_ploted:
            already_ploted.append(pt)
            plt.plot(self.t, h, "o", color = "blue", alpha = .2, markersize = 40)
            plt.annotate(str(round(self.s,1)), xy = (self.t,h+.038*self.option.T+.01), ha = "center", va = "center")
            if self.t < self.option.T:
                plt.annotate("x={}".format(round(self.x,1)), xy = (self.t,h-.0065*self.option.T-.006), ha = "center", va = "center", size = "small")
                plt.annotate("y={}".format(round(self.y,1)), xy = (self.t,h-.0415*self.option.T-.015), ha = "center", va = "center", size = "small")
            else:
                plt.annotate("payoff=\n{}".format(round(self.value,1)), xy = (self.t,h-.027*self.option.T-.018), ha = "center", va = "center", size = "small")
        if self.t < self.option.T:
            self.up.draw(plt, h+1, already_ploted)
            self.down.draw(plt, h-1, already_ploted)
            props = dict(arrowstyle = "-|>, head_width = 0.4, head_length = 0.8", shrinkA = 0, shrinkB = 0, color = "black")
            e = .0223*self.option.T - .0015
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
            plt.tight_layout()
            plt.show()
        return self.price
    def get_martingale_probability(self):
        delta = self.u - self.d
        q_u = (1+self.R-self.d)/delta
        q_d = (self.u-(1+self.R))/delta
        return q_u, q_d
    def get_quick_maturity_price(self):
        q_u, q_d = self.get_martingale_probability()
        self.price = (1 + self.R)**(-self.T)
        sum = 0
        for k in range(self.T+1):
            sum += (self.g(self.s0*(self.u**k)*(self.d**(self.T-k))) * C(self.T,k) * (q_u**k) * (q_d**(self.T-k)))
        self.price *= sum
        return self.price
        
class Put(Option):
    def g(self, asset_price):
        return max(self.K - asset_price,0)
class Call(Option):
    def g(self, asset_price):
        return max(asset_price - self.K,0)
        
        
if __name__ == "__main__":
    option = Call(10,110,0,100,1.2,.8)
    print(option.get_maturity_price(True))
    # print(option.get_quick_maturity_price())
