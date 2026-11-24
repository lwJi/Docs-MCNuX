---
area: statistics
date: 2026-11-24
verified-against: 61bafdd
specs: [MCNX-VER-07, MCNX-RNG-07, MCNX-INT-02]
builds-on: ["[[conventions]]", "[[poisson-scatter-count]]", "[[sample-mean-error]]"]
---
# Standard error of the sample variance

> [!question]
> How far does the measured variance of the scatter counts stray from $\lambda$ by chance alone?

> [!summary]
> The sample variance $S^2$ with divisor $N-1$ averages exactly to the true variance. Its standard error is $\sqrt{(\mu_4 - \mu_2^2)/N}$ to leading order in $1/N$. For the scatter count this is $\sqrt{(\lambda + 2\lambda^2)/N}$. The Gaussian formula $\sqrt{2\lambda^2/N}$ omits the $\lambda$ term.

## Setup

- $N$, $k_i$, $\bar k$, $\sigma$ and $z$ are defined in [[sample-mean-error]].
- $S^2 = \frac{1}{N-1}\sum_i (k_i - \bar k)^2$ is the sample variance.
- $\mu_n = E[(k-\lambda)^n]$ is the $n$-th central moment of one scatter count, with $\mu_2 = \lambda$.
- $d_i = (k_i - \lambda)^2$ is the squared deviation of packet $i$.

All quantities are dimensionless.

## Derivation

### Main idea

The sample variance is an average of squared deviations over packets. The rule of [[sample-mean-error]] applies again, with $d_i$ in place of $k_i$. The task reduces to the variance of one squared deviation.

### Two sums suffice

Expand the square and use $\sum_i k_i = N\bar k$:

$$\sum_i (k_i - \bar k)^2 = \sum_i k_i^2 - N\bar k^2$$

The estimate needs only $\sum_i k_i$ and $\sum_i k_i^2$, with no per-packet storage.

### Divisor $N-1$

The sample mean is the point closest to the data. Deviations from $\bar k$ are therefore smaller than deviations from $\lambda$.

Split the deviation as $k_i - \lambda = (k_i - \bar k) + (\bar k - \lambda)$, then square and sum. The cross term vanishes because $\sum_i (k_i - \bar k) = 0$:

$$\sum_i (k_i - \bar k)^2 = \sum_i (k_i - \lambda)^2 - N(\bar k - \lambda)^2$$

Average both sides. The first term gives $N\lambda$. The second term gives $N\,\mathrm{Var}(\bar k) = \lambda$.

$$E\!\left[\sum_i (k_i - \bar k)^2\right] = (N-1)\lambda$$

Division by $N-1$ makes $E[S^2] = \lambda$. Equivalently, the $N$ deviations from $\bar k$ sum to zero, so only $N-1$ are free.

### Standard error

For large $N$, replace $\bar k$ by $\lambda$ and $N-1$ by $N$:

$$S^2 \approx \frac{1}{N}\sum_i d_i, \qquad \mathrm{Var}(S^2) \approx \frac{\mathrm{Var}(d)}{N}$$

Expand the definition of the variance of one term:

$$\mathrm{Var}(d) = E\!\left[(d - E[d])^2\right] = E[d^2] - E[d]^2 = \mu_4 - \mu_2^2$$

For the Poisson distribution, $\mu_4 = \lambda + 3\lambda^2$:

$$\sigma = \sqrt{\frac{\mu_4 - \mu_2^2}{N}} = \sqrt{\frac{\lambda + 2\lambda^2}{N}}$$

### Fourth central moment

Use the pieces of [[poisson-scatter-count]], with $\delta k = \sum_j \delta x_j$. The fourth power is a sum of products of four piece deviations. A product survives the average only if no piece appears alone.

- Four factors from one piece: a rare piece has $E[\delta x^4] \approx p$. The $M$ pieces give $Mp = \lambda$.
- Two pairs from two pieces: each pair gives $E[\delta x^2] \approx p$. Four factors form two pairs in 3 ways, over $M(M-1)$ ordered piece pairs. The total is $3\lambda^2$.

A Gaussian has only the pair term, $\mu_4 = 3\mu_2^2$. The single-piece term $\lambda$ comes from discrete rare events.

## Assumptions and limits

- The standard error is the leading order in $1/N$. The exact variance is $\lambda/N + 2\lambda^2/(N-1)$.
- The relative difference between the two is about 1e-6 at $N = 2^{20}$.
- The packets are independent.
- The form $(\mu_4 - \mu_2^2)/N$ holds for any distribution with finite $\mu_4$.

## Why it matters

- The scattering-box benchmark compares $S^2$ with $\lambda$ and accepts $|z| \le 4$.
- At $\lambda$ = 1.99344 and $N = 2^{20}$, the standard error is 3.0791e-3. The measured $S^2$ is 1.99392, so $z$ = 0.16.
- The check detects a count variance that differs from $\lambda$ by more than $4\sigma/\lambda$ = 0.62%.
- Correlated scatters change the variance while the mean stays at $\lambda$. This check sees them, and the sample-mean check does not.

## Pitfalls

- The Gaussian formula underestimates the standard error by 11% at $\lambda$ = 1.99344.
- A simulation of 4000 runs at $N$ = 1024 gives a standard error of 0.0971 ± 0.0011. The Poisson formula gives 0.0985, and the Gaussian formula gives 0.0881.
- Divisor $N$ biases $S^2$ by the factor $(N-1)/N$. The shift is 1e-6 here, below the standard error but above the golden-data tolerance.
- $\bar k$ and $S^2$ share the same counts. Their covariance is $\mu_3/N = \lambda/N$, so the two checks are not independent.

## In MCNuX

- [MCNX-VER-07]: each statistical check reports the estimate, the expected value, the standard error and $z$.
- [MCNX-RNG-07]: acceptance is $|\text{estimate} - \text{expected}| \le 4\sigma$ at $N = 2^{20}$ and a pinned seed.
- [MCNX-INT-02]: the scattering-box benchmark tests the Poisson count law.

## References

None. The results are standard.
