# Independent Keplerian Consistency Audit of the NASA Exoplanet Archive: The K2-285 System

**Author:** Aleksandr Grebeshok (`alex.grebeshok@gmail.com`)  
**Date:** November 2026  
**License:** MIT  
**Release:** `v1.0.0`  

---

## 1. Abstract & Scope

This repository provides a reproducible, standalone computational audit of orbital parameters recorded in the **NASA Exoplanet Archive** (Caltech / IPAC) and published in the peer-reviewed astronomical literature.

As part of an automated consistency screening of multi-planetary systems under Newton's formulation of **Kepler's Third Law**, an observational discrepancy was identified in the published semi-major axes of planets **K2-285 c** and **K2-285 e** (EPIC 246471491, Palle et al. 2019, *Astronomy & Astrophysics* 623, A41).

This artifact is published as an open, proof-carrying computational verification note to document the calculation transparently, invite peer feedback, and provide a self-contained reproduction script using only the Python standard library.

---

## 2. Physical & Mathematical Formulation

For a planet of mass $M_p$ orbiting a host star of mass $M_*$ with orbital period $P$, standard Newtonian gravitation uniquely constrains the semi-major axis $a$:

$$a^3 = \frac{G (M_* + M_p) P^2}{4 \pi^2}$$

In astronomical units (AU), adopting nominal IAU constants ($G = 6.67430 \times 10^{-11}\ \text{m}^3\text{kg}^{-1}\text{s}^{-2}$, $M_\odot = 1.98847 \times 10^{30}\ \text{kg}$, $1\ \text{AU} = 149,597,870,700\ \text{m}$), the semi-major axis depends predominantly on the host star mass $M_*$ and the period $P$ (with planetary mass contribution $M_p/M_* < 10^{-4}$ acting as a minor correction).

Uncertainty propagation from stellar mass $\sigma_{M_*}$ and orbital period $\sigma_P$ to the Keplerian semi-major axis is given by:

$$\left(\frac{\sigma_{a,\text{Kepler}}}{a}\right)^2 = \frac{1}{9}\left(\frac{\sigma_{M_*}}{M_*}\right)^2 + \frac{4}{9}\left(\frac{\sigma_P}{P}\right)^2$$

---

## 3. Findings for the K2-285 System

The host star K2-285 has a published spectroscopic mass of $M_* = 0.830 \pm 0.038\ M_\odot$ (Palle et al. 2019). 

Comparing the published parameters against the theoretical Keplerian values:

| Planet | Period $P$ (days) | Published $a$ (AU) | Keplerian $a$ (AU) | Discrepancy $\Delta a$ | Tension ($\sigma$) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **K2-285 b** | $3.471747 \pm 0.00010$ | $0.0416 \pm 0.0010$ | $0.0419$ | $-0.0003\ \text{AU}$ | $\sim 0.3\ \sigma$ (Consistent) |
| **K2-285 c** | $7.138048 \pm 0.00030$ | **$0.0824 \pm 0.0019$** | **$0.0682$** | **$+0.0142\ \text{AU}$** | **$6.56\ \sigma$** (Tension) |
| **K2-285 d** | $10.45564 \pm 0.00045$ | $0.0877 \pm 0.0022$ | $0.0876$ | $+0.0001\ \text{AU}$ | $\sim 0.1\ \sigma$ (Consistent) |
| **K2-285 e** | $14.76300 \pm 0.00090$ | **$0.18041 \pm 0.0044$** | **$0.1107$** | **$+0.0697\ \text{AU}$** | **$14.79\ \sigma$** (Tension) |

### Observation
- For **K2-285 c**, the published value $a = 0.0824\ \text{AU}$ matches $(a/R_*) \times R_*$ ($22.51 \times 0.787\ R_\odot = 0.08235\ \text{AU}$), but deviates by $>6.5\sigma$ from the Keplerian value for $P = 7.138\ \text{d}$ and $M_* = 0.830\ M_\odot$.
- For **K2-285 e**, the published value $a = 0.18041\ \text{AU}$ corresponds to an orbital period of $\approx 29.8\ \text{days}$ around a $0.830\ M_\odot$ star, whereas the reported period is $14.763\ \text{days}$.

---

## 4. Reproducing the Verification

The verification script requires standard Python 3 with zero third-party dependencies:

```bash
python3 verify_kepler.py
```

Expected output:
```text
Baseline Self-Tests PASSED (Earth a=1.000 AU, Jupiter a=5.204 AU).
Target: K2-285 c -> Discrepancy: +0.01421 AU (6.56 σ tension)
Target: K2-285 e -> Discrepancy: +0.06973 AU (14.79 σ tension)
```

---

## 5. Citation & Archiving

This release is archived on **Zenodo** as a citable research object:
- **DOI:** Pending release minting on Zenodo
- **Author:** Aleksandr Grebeshok (`alex.grebeshok@gmail.com`)
- **Primary Literature Reference:** Palle et al., *A&A* 623, A41 (2019), DOI: [10.1051/0004-6361/201834001](https://doi.org/10.1051/0004-6361/201834001)
- **Data Source:** NASA Exoplanet Archive, Caltech / IPAC (Accessed November 2026).
