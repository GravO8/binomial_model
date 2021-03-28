# Binomial Model

The binomial model is a very simple model used to price options. It makes some assumptions about the price development of the underlying asset:

- time is discreet and in equaly spaced intervals.
- interest is only applied at the end of each time interval, i.e. it's computed as *(1+R) <sup>K</sup>* for *K* intervals.
- The underlying asset price will be up in the next interval with probability *p* and will be down with probability *(1 - p)*.
- When the price goes up, it always goes up by the same fraction *u*.
- Similarly, when the price price goes down, it always goes down by the same fraction *d*.

Furthermore, to avoid arbitrage situaitons we have to set *R* to be such that *d < 1+R < u*.

Check [wikipedia](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) for more details.



## Replicating portfolio

A replicating portfolio of an option is a portfolio (i.e. a given amount of cash and underlying asset) whose value is the same as the option's value at maturity, with probability one. 

One way to price options is to create a replicating portfolio for that option. If we can find such portfolio, we can set the price of that option to *x + yS(0)​* where *x​* is the cash, *y* is the shares of the underlying asset and *S(0)​* is its price at time 0. 

This way of computing an option's price can be acessed with the `get_maturity_price` method of the `Option` class. The corresponding binomial tree can be drawn, setting the `draw` parameter to `True`. 

Here's an example of the tree for a call option with maturity = 2, strike price = 110, 0 interest rate, *S(0)​* = 100, *u​* = 1.2 and *d* = 0.8 : 

![tree](https://user-images.githubusercontent.com/25433159/112751788-a9810180-8fc7-11eb-94ff-a9b8bbc341f9.png)

Each node contains the price of the underlying asset and the corresponding *x* and *y* to make a replicating portfolio. The exceptions are the terminal nodes (the nodes at maturity), which have the payoff instead of the *(x,y)* tuple.



## Risk neutral measure

The problem with the above approach is that it requires the computation of the intire tree in order to set the option's price. 

Thankfully there is another, more efficient method, of getting the option's price, which computes the probability of the price going up or down (the *Martingale probability*) for every time interval. 

This way of computing an option's price can be acessed with `get_quick_maturity_price` method of the `Option` class. 



## Interest rates

An `Option` object can be created with a fixed interest rate by providing a single integer/float. But, the binomial model is flexible enough to price options when *R* is not constant, so you can also provide a list of interest rates to create a `Option` object. This list must have length equal to maturity, because each entry corresponds to the interest rate applied in a given interval.



## License

This program is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
