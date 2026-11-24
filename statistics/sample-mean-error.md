---
area: statistics
date: 2026-11-24
verified-against: 61bafdd
specs: [MCNX-VER-07, MCNX-RNG-07, MCNX-INT-02]
builds-on: ["[[conventions]]", "[[poisson-scatter-count]]"]
---
# Standard error of the sample mean

> [!question]
> How far does the measured mean scatter count stray from $\lambda$ by chance alone?

> [!summary]
> The sample mean of $N$ independent values has variance $\mu_2/N$, with $\mu_2$ the variance of one value. For the scatter count, the standard error is $\sqrt{\lambda/N}$. The one-packet noise $\sqrt{\lambda}$ shrinks by $\sqrt{N}$.

## Setup

- $N$ is the number of packets. The packet label $i$ runs from 1 to $N$, with no summation convention.
- $k_i$ is the scatter count of packet $i$, from [[poisson-scatter-count]]. Each $k_i$ has mean $\lambda$ and variance $\lambda$.
- $T = \sum_i k_i$ is the total count. $\bar k = T/N$ is the sample mean.
- $\sigma$ is the standard error of an estimate: its standard deviation over repeated runs with different seeds.
- $z = (\text{estimate} - \text{expected})/\sigma$ is the standardized deviation.

All quantities are dimensionless. The packets are independent.

## Derivation

### Main idea

The sample mean is itself random: another seed gives another value. The standard error is the size of that run-to-run scatter. One run cannot measure it, so theory supplies it.

### Total count

Variances add for independent quantities, see [[poisson-scatter-count]]. Apply the rule across the $N$ packets:

$$E[T] = N\lambda, \qquad \mathrm{Var}(T) = N\lambda$$

### Scaling rule

Division by a constant $N$ divides the variance by $N^2$. Let $y = x/N$:

$$\delta y = \frac{x}{N} - \frac{E[x]}{N} = \frac{\delta x}{N}, \qquad \mathrm{Var}(y) = E\!\left[\frac{\delta x^2}{N^2}\right] = \frac{\mathrm{Var}(x)}{N^2}$$

The square appears because variance is a squared deviation. The standard deviation scales by $1/N$, and the variance scales by $1/N^2$.

### Result

$$\mathrm{Var}(\bar k) = \frac{\mathrm{Var}(T)}{N^2} = \frac{\lambda}{N}, \qquad \sigma = \sqrt{\frac{\lambda}{N}}$$

The sum contributes a factor $N$, and the division contributes $1/N^2$.

In total counts, the expected total is $N\lambda$ and its standard deviation is $\sqrt{N\lambda}$. The relative precision is $1/\sqrt{N\lambda}$.

## Assumptions and limits

- The packets are independent. Random numbers shared between packets add cross terms and invalidate the result.
- The formula is exact for every $N$. It needs no large-$N$ approximation.
- The formula uses the predicted $\lambda$, not the measured variance.

## Why it matters

- The scattering-box benchmark compares $\bar k$ with $\lambda$ and accepts $|z| \le 4$.
- Benchmark values: $\kappa_s$ = 2.7e-5 cm⁻¹, $\ell$ = 0.5 code lengths = 7.383e4 cm, $\lambda$ = 1.99344, $N = 2^{20}$.
- The standard error is 1.3788e-3. The measured sample mean is 1.99548, so $z$ = 1.48.
- The check detects a scattering-rate error above $4\sigma/\lambda$ = 0.28%.
- The check is blind to correlated scatters at the correct mean rate. [[sample-variance-error]] covers that case.

## Pitfalls

- Division scales the variance by $1/N^2$, not $1/N$. The net $1/N$ comes from the sum and the division together.
- The total count gains relative precision, not absolute precision. Its standard deviation grows as $\sqrt{N}$.

## In MCNuX

- [MCNX-VER-07]: each statistical check reports the estimate, the expected value, the standard error and $z$.
- [MCNX-RNG-07]: acceptance is $|\text{estimate} - \text{expected}| \le 4\sigma$ at $N = 2^{20}$ and a pinned seed.
- [MCNX-INT-02]: the scattering-box benchmark tests the Poisson count law.

## References

None. The results are standard.
