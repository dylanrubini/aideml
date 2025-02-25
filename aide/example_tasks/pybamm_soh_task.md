## Goal
Analyze carefully the content of this research article.
I want you to provide me a complete stack of code that can be run without errors in which the electrochemical modelling package PyBaMM is extended and used to implement the pybamm-eis library and to reproduce the corresponding simulation results displayed in Figure 5 of the article. To do this, implement the frequency domain pybamm-eis extension of pybamm library. **TO BE VERY CLEAR, the pybamm-eis does not yet exist, you have to implement it by leverging pybamm**. **Do NOT implement time-domain brute-force method**, instead implement new frequency domain method. A subtask to achieve this is to implement a new pybamm.Simulation() class called EISSimulation(). Make sure you plan and reason step by step in collecting all simulations details and parameters before writing the python script. Reproduce the figure as faithfully as possible.

## Detailed Description of Figure to be Reproduced

Figure 5 presents a Nyquist plot comparing the electrochemical impedance spectra (EIS) of three different battery models—the Single Particle Model (SPM), the Single Particle Model with electrolyte dynamics (SPMe), and the Doyle–Fuller–Newman (DFN) model—computed using a numerical frequency‐domain approach. All simulations are performed at a 50% state-of-charge (SOC) for an LG M50 cell (using the Chen2020 parameter set) at 25 °C, with frequencies ranging from 200 µHz to 1 kHz.

Key features of the plot include:

•Semicircular Arc (High-Frequency Region):
– This arc reflects the charge-transfer kinetics at the electrode–electrolyte interface.
– The diameter of the semicircle is related to the charge-transfer resistance, while the curvature reflects the double-layer capacitance effects.
– Note that for a fair comparison, the SPM’s contact resistance was adjusted to align its high-frequency behavior with that of the SPMe and DFN models.

•Diffusion Tail (Low-Frequency Region):
– All models display a low-frequency tail indicative of mass transport processes.
– In the SPM, which does not include electrolyte dynamics, the tail follows a characteristic 45° slope (typical of solid-state diffusion) before transitioning into a capacitive (vertical) behavior.
– In contrast, the SPMe and DFN models show an additional “bump” in the diffusion tail. This bump arises from the inclusion of electrolyte diffusion dynamics—an effect that is also frequently observed in experimental impedance measurements but is absent in the simpler SPM.

•Model Comparison:
– The DFN model’s impedance nearly overlaps with the SPMe’s across the frequency range except at high frequencies, where subtle differences emerge due to the DFN’s added complexity.
– The SPM, lacking electrolyte dynamics, deviates noticeably in the low-frequency region by not capturing the bump seen in the SPMe and DFN spectra.

In summary, Figure 5 visually demonstrates how incorporating electrolyte dynamics (as in the SPMe and DFN models) modifies the impedance response—particularly by introducing an extra feature (the bump) in the diffusion tail—that is absent in the SPM. This comparison highlights the importance of including such dynamics when seeking to accurately model and interpret measured EIS data.
