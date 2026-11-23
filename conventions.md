---
area: conventions
date: 2026-11-23
verified-against: 61bafdd
specs: [CNV]
---
# Conventions

Notation and units shared by every doc. These follow the MCNuX conventions spec (CNV), which is the authority if the two ever differ.

## Geometry

- Signature $(-,+,+,+)$. Greek indices run over 0 to 3, Latin indices over 1 to 3, with Einstein summation.
- The 3+1 split uses lapse $\alpha$, shift $\beta^i$ and spatial metric $\gamma_{ij}$, with $\gamma = \det \gamma_{ij}$:

$$ds^2 = -\alpha^2 dt^2 + \gamma_{ij}\,(dx^i + \beta^i dt)(dx^j + \beta^j dt)$$

- The unit normal to the slices is $n^\mu = (1/\alpha,\ -\beta^i/\alpha)$.

## Neutrino kinematics

- $p^\mu$ is the packet four-momentum in the coordinate frame.
- $u^\mu$ is the fluid four-velocity.
- $\nu = -p_\mu u^\mu$ is the neutrino energy in the fluid frame.

> [!warning] Symbol collisions
> - $\alpha$ is the lapse unless stated otherwise. The trapped-regime relabeling fraction and a spectral-fit index in arXiv:1806.02349 also use $\alpha$.
> - $\nu$ is the fluid-frame energy, but it also appears as a Greek index and in species names such as $\nu_e$.

## Units

Two systems are in use.

- Geometrized, $G = c = M_\odot = 1$: spacetime, packet positions and momenta, time steps, opacities inside transport, source terms on the grid.
- MeV and cgs: neutrino energies and temperature in MeV, rest-mass density in g/cm³, electron fraction dimensionless.

| Quantity | Derivation | One code unit |
|---|---|---|
| Length | $GM_\odot/c^2$ | 1.476625038e5 cm |
| Time | $GM_\odot/c^3$ | 4.925490948e-6 s |
| Mass | $M_\odot$ | 1.988409871e33 g |
| Energy | $M_\odot c^2$ | 1.787093669e54 erg = 1.115416135e60 MeV |
| Mass density | $M_\odot/L^3$ | 6.175828479e17 g/cm³ |
| Energy density, pressure | $M_\odot c^2/L^3$ | 5.550557829e38 erg/cm³ |
| Opacity | $1/L$ | 6.772199944e-6 cm⁻¹ |
| Rate | $1/t$ | 2.030254467e5 s⁻¹ |
| Emissivity | $M_\odot c^2/(L^3 t)$ | 1.126904483e44 erg cm⁻³ s⁻¹ |

The factors derive from $c$, $k_B$ and $e$ (SI exact), $G$ = 6.67430e-8 cm³ g⁻¹ s⁻² (CODATA 2018) and $GM_\odot$ = 1.3271244e26 cm³ s⁻² (IAU 2015). Length and time are exact; anything involving mass inherits the relative uncertainty of $G$, about 2e-5.

Temperature is held in MeV. The opacity and equation-of-state tables take Kelvin: $T[\mathrm{K}] = T[\mathrm{MeV}] \times 1.160451812 \times 10^{10}$.

## Species

| Index | Species | Represents | Degeneracy $g$ | Lepton number |
|---|---|---|---|---|
| 0 | $\nu_e$ | electron neutrino | 1 | +1 |
| 1 | $\bar\nu_e$ | electron antineutrino | 1 | −1 |
| 2 | $\nu_x$ | $\nu_\mu, \bar\nu_\mu, \nu_\tau, \bar\nu_\tau$ lumped | 4 | 0 |

The factor $g = 4$ for $\nu_x$ enters exactly once, at packet creation.
