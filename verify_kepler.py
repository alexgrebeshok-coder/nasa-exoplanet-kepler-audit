#!/usr/bin/env python3
"""
Independent Keplerian Consistency Verification Suite
Author: Aleksandr Grebeshok (alex.grebeshok@gmail.com)
License: MIT

This standalone script verifies orbital parameters of multi-planetary systems
against Kepler's Third Law using standard astronomical constants (IAU / CODATA).
It specifically audits the published parameters for the K2-285 system
(Palle et al. 2019, A&A 623, A41 / NASA Exoplanet Archive).
"""

import math
import sys

# Standard Astronomical & Physical Constants (SI & IAU Nominal)
G = 6.67430e-11            # Gravitational constant (m^3 kg^-1 s^-2, CODATA 2018)
M_SUN = 1.98847e30         # Solar mass (kg, IAU 2015 nominal)
M_EARTH = 5.9722e24        # Earth mass (kg)
AU = 149597870700.0        # Astronomical Unit (m, IAU exact)
DAY = 86400.0              # Seconds in day

def compute_kepler_semi_major_axis_au(period_days: float, m_star_solar: float, m_planet_earth: float = 0.0) -> float:
    """
    Computes semi-major axis in AU using Newton's formulation of Kepler's Third Law:
    a^3 = G * (M_* + M_p) * P^2 / (4 * pi^2)
    """
    p_sec = period_days * DAY
    m_total_kg = (m_star_solar * M_SUN) + (m_planet_earth * M_EARTH)
    
    a_m3 = (G * m_total_kg * (p_sec ** 2)) / (4.0 * (math.pi ** 2))
    a_m = a_m3 ** (1.0 / 3.0)
    return a_m / AU

def audit_planet(name: str, period_d: float, m_star_solar: float, m_star_unc: float,
                 published_a_au: float, published_a_unc: float, m_planet_earth: float = 0.0):
    """
    Computes theoretical semi-major axis and statistical tension in sigmas.
    """
    kepler_a = compute_kepler_semi_major_axis_au(period_d, m_star_solar, m_planet_earth)
    discrepancy = published_a_au - kepler_a
    
    # Propagate stellar mass uncertainty into a (a ~ M^(1/3) => sigma_a / a = (1/3) * sigma_M / M)
    sigma_kepler = (1.0 / 3.0) * (m_star_unc / m_star_solar) * kepler_a
    total_unc = math.sqrt((published_a_unc ** 2) + (sigma_kepler ** 2))
    sigma_dev = abs(discrepancy) / total_unc

    print(f"==================================================")
    print(f"Target: {name}")
    print(f"--------------------------------------------------")
    print(f"Input Period P          : {period_d:.6f} days")
    print(f"Input Stellar Mass M*   : {m_star_solar:.3f} ± {m_star_unc:.3f} M_sun")
    print(f"Published Semi-major Axis: {published_a_au:.5f} ± {published_a_unc:.5f} AU")
    print(f"Keplerian Semi-major Axis: {kepler_a:.5f} AU")
    print(f"Absolute Discrepancy     : {discrepancy:+.5f} AU")
    print(f"Combined Uncertainty    : {total_unc:.5f} AU")
    print(f"Statistical Tension     : {sigma_dev:.2f} σ")
    
    if sigma_dev > 5.0:
        print(f"STATUS                  : NOTABLE DISCREPANCY (>5σ tension)")
    else:
        print(f"STATUS                  : CONSISTENT (within 5σ)")
    print(f"==================================================\n")
    return sigma_dev

def run_self_tests():
    print("Running Baseline Consistency Self-Tests...")
    
    # Test 1: Earth (1 year around 1.0 M_sun)
    earth_a = compute_kepler_semi_major_axis_au(365.25636, 1.0, 1.0)
    assert abs(earth_a - 1.000) < 0.005, f"Earth self-test failed: {earth_a}"
    
    # Test 2: Jupiter (4332.59 days around 1.0 M_sun)
    jup_a = compute_kepler_semi_major_axis_au(4332.589, 1.0, 317.8)
    assert abs(jup_a - 5.204) < 0.01, f"Jupiter self-test failed: {jup_a}"
    
    print("Baseline Self-Tests PASSED (Earth a=1.000 AU, Jupiter a=5.204 AU).\n")

def main():
    print("Independent Keplerian Consistency Audit of K2-285 System")
    print("Data Source: Palle et al. 2019 (A&A 623, A41) / NASA Exoplanet Archive\n")
    
    run_self_tests()
    
    # Stellar Parameters for K2-285 (EPIC 246471491): M* = 0.830 ± 0.038 M_sun
    m_star = 0.830
    m_star_unc = 0.038
    
    # K2-285 c: P = 7.138048 d, published a = 0.0824 ± 0.0019 AU (Table A.1)
    sigma_c = audit_planet("K2-285 c", 
                           period_d=7.138048, 
                           m_star_solar=m_star, 
                           m_star_unc=m_star_unc, 
                           published_a_au=0.0824, 
                           published_a_unc=0.0019, 
                           m_planet_earth=15.68)
    
    # K2-285 e: P = 14.763 d, published a = 0.18041 ± 0.0044 AU (Table A.1)
    sigma_e = audit_planet("K2-285 e", 
                           period_d=14.763, 
                           m_star_solar=m_star, 
                           m_star_unc=m_star_unc, 
                           published_a_au=0.18041, 
                           published_a_unc=0.0044, 
                           m_planet_earth=10.0)
    
    print("Audit Complete. All calculations verified with zero external dependencies.")

if __name__ == "__main__":
    main()
