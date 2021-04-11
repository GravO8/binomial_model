from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from itertools import combinations

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
            self.compute_value()
        return self.value
    def draw(self, plt, h = 0, already_ploted = []):
        pt = (self.t,h)
        if pt not in already_ploted:
            already_ploted.append(pt)
            plt.plot(self.t, h, "o", color = "blue", alpha = .2, markersize = 40)
            plt.annotate(str(round(self.s,1)), xy = (self.t,h+.038*self.option.T+.01), ha = "center", va = "center")
            self.annotate(plt, h)
        if self.t < self.option.T:
            self.up.draw(plt, h+1, already_ploted)
            self.down.draw(plt, h-1, already_ploted)
            props = dict(arrowstyle = "-|>, head_width = 0.4, head_length = 0.8", shrinkA = 0, shrinkB = 0, color = "black")
            e = .0223*self.option.T - .0015
            plt.annotate("", xytext = (self.t+e,h+e), xy = (self.t+1-e,h+1), arrowprops = props)
            plt.annotate("", xytext = (self.t+e,h-e), xy = (self.t+1-e,h-1), arrowprops = props)
    @abstractmethod
    def compute_value(self, plt):
        pass
    @abstractmethod
    def annotate(self, plt, h):
        pass
        
class AmericanNode(Node):
    def compute_value(self):
        self.up     = AmericanUpNode(self.option, self)
        self.down   = AmericanDownNode(self.option, self)
        q_u, q_d    = self.option.get_martingale_probability(self.t)
        self.value  = max(self.option.g(self.s), q_u*self.up.get_value() + q_d*self.down.get_value())
        return self.value
    def annotate(self, plt, h):
        plt.annotate("payoff=\n{}".format(round(self.value,1)), xy = (self.t,h-.027*self.option.T-.018), ha = "center", va = "center", size = "small")

class EuropeanNode(Node):
    def compute_value(self):
        self.up     = EuropeanUpNode(self.option, self)
        self.down   = EuropeanDownNode(self.option, self)
        delta       = self.option.u - self.option.d
        self.x      = (1/(1+self.option.R[self.t]))*(self.option.u*self.down.get_value() - self.option.d*self.up.get_value())/delta
        self.y      = (1/self.s)*(self.up.get_value() - self.down.get_value())/delta
        self.value  = self.x + self.y*self.s
        if self.t < self.option.T-1:
            self.up.down = self.down.up
        return self.value
    def annotate(self, plt, h):
        if self.t < self.option.T:
            plt.annotate("x={}".format(round(self.x,1)), xy = (self.t,h-.0065*self.option.T-.006), ha = "center", va = "center", size = "small")
            plt.annotate("y={}".format(round(self.y,1)), xy = (self.t,h-.0415*self.option.T-.015), ha = "center", va = "center", size = "small")
        else:
            plt.annotate("payoff=\n{}".format(round(self.value,1)), xy = (self.t,h-.027*self.option.T-.018), ha = "center", va = "center", size = "small")

class Node0(Node):
    def __init__(self, option):
        Node.__init__(self,option)
        self.s = self.option.s0
        self.t = 0
class AmericanNode0(AmericanNode, Node0):
    pass
class EuropeanNode0(EuropeanNode, Node0):
    pass
        
class UpNode(Node):
    def __init__(self, option, parent):
        Node.__init__(self,option)
        self.s = parent.s * self.option.u
        self.t = parent.t+1
class AmericanUpNode(AmericanNode, UpNode):
    pass
class EuropeanUpNode(EuropeanNode, UpNode):
    pass
    
class DownNode(Node):
    def __init__(self, option, parent):
        Node.__init__(self,option)
        self.s = parent.s * self.option.d
        self.t = parent.t+1
class AmericanDownNode(AmericanNode, DownNode):
    pass
class EuropeanDownNode(EuropeanNode, DownNode):
    pass
        
class Option(ABC):
    def __init__(self, maturity: int, strike_price: float, interest_rate, s0: float, up_fraction: float, down_fraction: float):
        if type(interest_rate) in (float,int):
            interest_rate = [interest_rate] * maturity
        assert (type(interest_rate) == list and len(interest_rate) == maturity), "Option: interest_rate must be float, int or list with length equal to maturity"
        self.T  = maturity
        self.K  = strike_price
        self.R  = interest_rate
        self.s0 = s0
        self.u  = up_fraction
        self.d  = down_fraction
        self.q  = {} # martingale probabilities
    @abstractmethod
    def g(self, asset_price):
        '''payoff function'''
        pass
    @abstractmethod
    def get_maturity_price(self, draw = False):
        pass
    def get_martingale_probability(self, t):
        if t not in self.q: 
            delta = self.u - self.d
            q_u = (1+self.R[t]-self.d)/delta
            q_d = (self.u-(1+self.R[t]))/delta
            self.q[t] = (q_u, q_d)
        return self.q[t]
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
        
class EuropeanOption(Option):
    def __init__(self, maturity: int, strike_price: float, interest_rate, s0: float, up_fraction: float, down_fraction: float):
        Option.__init__(self, maturity, strike_price, interest_rate, s0, up_fraction, down_fraction)
        self.node0 = EuropeanNode0(self)
    def get_quick_maturity_price(self):
        self.price = 1
        q_u, q_d = [0]*self.T, [0]*self.T
        for t in range(self.T): 
            self.price *= (1/(1+self.R[t]))
            q_u[t], q_d[t] = self.get_martingale_probability(t)
        sum = 0
        indexes = [i for i in range(self.T)]
        for k in range(self.T+1):
            paths = 0
            for comb in combinations(indexes, k):
                path = 1
                for i in range(self.T): path *= q_u[i] if i in comb else q_d[i]
                paths += path
            sum += (self.g(self.s0*(self.u**k)*(self.d**(self.T-k))) * paths)
        self.price *= sum
        return self.price
        
class AmericanOption(Option):
    def __init__(self, maturity: int, strike_price: float, interest_rate, s0: float, up_fraction: float, down_fraction: float):
        Option.__init__(self, maturity, strike_price, interest_rate, s0, up_fraction, down_fraction)
        self.node0 = AmericanNode0(self)
        
class Put(Option):
    def g(self, asset_price):
        return max(self.K - asset_price,0)
class Call(Option):
    def g(self, asset_price):
        return max(asset_price - self.K,0)

class AmericanPut(AmericanOption, Put):
    pass
class AmericanCall(AmericanOption, Call):
    pass
class EuropeanPut(EuropeanOption, Put):
    pass
class EuropeanCall(EuropeanOption, Call):
    pass
        
if __name__ == "__main__":
    maturity = 3
    strike_price = 45
    interest_rate = [.01,.02,.03]
    s0 = 40
    u =  1.3
    d = .8
    put = AmericanPut(maturity, strike_price, interest_rate, s0, u, d)
    # print(call.get_maturity_price(True))
    print(put.get_maturity_price(True))

    # put = Put(3,120,[0,.1,.2],80,1.5,.5)
    # print(put.get_maturity_price(False))
    # print(put.get_quick_maturity_price())
