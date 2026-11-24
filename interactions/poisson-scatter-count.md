---
area: interactions
date: 2026-11-24
verified-against: 61bafdd
specs: [MCNX-INT-01, MCNX-INT-02]
builds-on: ["[[conventions]]"]
---
# Poisson scatter count

> [!question]
> How many times does a packet scatter along a fixed path length in a uniform medium?

> [!summary]
> The scatter count $k$ follows a Poisson distribution with parameter $\lambda = \kappa_s \ell$. The mean and the variance of $k$ both equal $\lambda$. This equality identifies independent rare events.

## Setup

- $\kappa_s$ is the scattering opacity in cm⁻¹: the scattering probability per unit path length, for a short length.
- $\ell$ is the path length in cm.
- $k$ is the scatter count along $\ell$, a non-negative integer.
- $\lambda = \kappa_s \ell$ is the expected scatter count. It is dimensionless.
- $M$ is the number of equal pieces that divide the path. Each piece scatters with probability $p$.
- $x_j$ is the outcome of piece $j$: 1 for a scatter, 0 otherwise.
- $E[x]$ is the average of $x$. The deviation is $\delta x = x - E[x]$. The variance is $\mathrm{Var}(x) = E[\delta x^2]$.

The medium is uniform. The fluid is at rest in flat spacetime. Scatters in different pieces are independent.

## Derivation

### Main idea

Cut the path into $M$ short pieces. Each piece is a rare yes/no trial. The scatter count is the number of pieces that say yes. The Poisson distribution is the limit of infinitely many pieces.

### Count law

A piece of length $\ell/M$ scatters with probability $p = \kappa_s \ell/M = \lambda/M$. The scatter count over $M$ pieces is binomial:

$$P_M(k) = \binom{M}{k}\, p^k (1-p)^{M-k}$$

Insert $p = \lambda/M$ and regroup:

$$P_M(k) = \frac{M(M-1)\cdots(M-k+1)}{M^k}\;\frac{\lambda^k}{k!}\;\left(1-\frac{\lambda}{M}\right)^{M}\left(1-\frac{\lambda}{M}\right)^{-k}$$

Take $M \to \infty$ at fixed $k$. The first factor tends to 1. The third factor tends to $e^{-\lambda}$. The fourth factor tends to 1.

$$P(k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

The factor $e^{-\lambda}$ is the probability of no scatter along the path.

### Why $\lambda$ stays fixed

The product $Mp = \kappa_s \ell$ does not depend on $M$. A finer cut shortens each piece, and $p$ shrinks in proportion. $M$ is a bookkeeping choice. The medium and the path set $\lambda$.

### Mean and variance

One piece has mean $E[x_j] = p$. Its outcome is 0 or 1, so $x_j^2 = x_j$ and $E[x_j^2] = p$. Its variance is $p - p^2 = p(1-p)$. A rare piece has $p \ll 1$, so its variance equals its mean to leading order.

Means add for any two quantities:

$$E[x+y] = E[x] + E[y]$$

Variances add for independent quantities. The deviation of a sum is $\delta x + \delta y$. Square it and average each term:

$$\mathrm{Var}(x+y) = \mathrm{Var}(x) + \mathrm{Var}(y) + 2\,E[\delta x\,\delta y]$$

Independence makes the average of a product equal the product of the averages. Each deviation averages to zero:

$$E[\delta x\,\delta y] = E[\delta x]\,E[\delta y] = 0$$

Sum the $M$ pieces:

$$E[k] = Mp = \lambda, \qquad \mathrm{Var}(k) = Mp(1-p) = \lambda\left(1-\frac{\lambda}{M}\right) \to \lambda$$

## Assumptions and limits

- Independence: a scatter in one piece does not change the probability in another piece. Correlated scatters break the variance result first.
- Uniform medium: every piece has the same $p$. For varying opacity the count stays Poisson, with $\lambda = \int \kappa_s\, d\ell$.
- Fluid at rest in flat spacetime: the path length equals $c\,\Delta t$ for a time interval $\Delta t$. Otherwise the scattering rate per coordinate time is $\kappa_s \nu/p^t$.
- Finite $M$ allows one scatter per piece at most. The neglected probability is of order $1/M$ and vanishes in the limit.

## Why it matters

- The count law is the prediction of the scattering-box benchmark: packets in a uniform pure scatterer for one time step.
- The mean of $k$ tests the scattering rate. The variance of $k$ tests the independence of scatters.
- The distance to the next scatter is exponential with mean $1/\kappa_s$. The exponential distribution is memoryless. A redraw of the distance at a cell crossing leaves the count law unchanged.

## Pitfalls

- Fixed $\lambda$ is not an extra assumption. It follows from $p$ proportional to the piece length.
- Fixed $p$ with growing $M$ is a different limit. The mean count then grows without bound, and the distribution approaches a Gaussian.
- Means add always. Variances add only when the cross term $E[\delta x\,\delta y]$ vanishes.

## In MCNuX

- [MCNX-INT-01]: draws the interval to the next scatter from an exponential distribution.
- [MCNX-INT-02]: redraws the interval at each cell crossing, exact by memorylessness for piecewise-constant opacity.

## References

- arXiv:1708.08452v2, Eq. 24: the interval draw.
