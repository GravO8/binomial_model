# Binomial Model

The binomial model is a very simple model used to price options. It makes some assumptions about the price development of the underlying asset:

- time is discreet and in equaly spaced intervals.
- interest are only applied at the end of each time interval, i.e. they're computed as<img src="https://latex.codecogs.com/gif.latex?(1+R)^K" /> for <img src="https://latex.codecogs.com/gif.latex?K" /> intervals.
- The underlying asset price will be up in the next interval with probability <img src="https://latex.codecogs.com/gif.latex?p"/> and will be down with probability <img src="https://latex.codecogs.com/gif.latex?(1-p)"/>.
- When the price goes up, it always goes up by the same fraction <img src="https://latex.codecogs.com/gif.latex?u"/>.
- Similarly, when the price price goes down, it always goes down by the same fraction <img src="https://latex.codecogs.com/gif.latex?d"/>.



