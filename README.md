# Docs-MCNuX

Notes on the math and physics of MCNuX, a Monte Carlo neutrino transport code. Each doc covers one concept and is written to be re-read cold.

Start with [[conventions]] for notation and units. Papers are listed in [[references]].

## Areas

| Area | Covers |
|---|---|
| foundations | The transport equation, Monte Carlo as an estimator, 3+1 pieces used everywhere |
| packets | Packet state, weights, emission sampling |
| propagation | Null geodesics in 3+1, tetrads, frame changes |
| interactions | Optical-depth sampling, absorption, scattering |
| trapped-regime | Optically thick treatment, relabeling, stability bound |
| microphysics | Opacities, emissivity, Kirchhoff's law, equation of state |
| coupling | Source terms, the conservation ledger |
| statistics | Random numbers, estimator variance, acceptance tests |

## Docs

Each area gets a heading here when its first doc lands, with one line per doc: the link and its one-sentence takeaway.

### interactions

- [[poisson-scatter-count]]: The scatter count along a path is Poisson, with mean and variance $\kappa_s \ell$.

### statistics

- [[sample-mean-error]]: The mean of $N$ independent scatter counts has standard error $\sqrt{\lambda/N}$.
- [[sample-variance-error]]: The sample variance of $N$ Poisson counts has standard error $\sqrt{(\lambda + 2\lambda^2)/N}$, not the Gaussian $\sqrt{2\lambda^2/N}$.
