
## Article (converted from PDF to markdown)


# Physics-based battery model parametrisation from impedance data  

Noe¨l Hallemansa,d,∗, Nicola E. Courtiera,d, Colin P. Pleaseb,d, Brady Plandena, Rishit Dhoot $\mathbf{b}$ , Robert Timmsc, S. Jon Chapmanb,d, David Howeya,d, Stephen R. Duncana,d  

aDepartment of Engineering Science, University of Oxford, Oxford, OX1 3PJ, UK bMathematical Institute, University of Oxford, Andrew Wiles Building, Woodstock Road, Oxford, OX2 6GG, UK Ionworks Technologies Inc, 5831 Forward Ave #1276 , Pittsburgh, PA, 15217, USA dThe Faraday Institution, Quad One, Becquerel Avenue, Harwell Campus, Didcot, OX11 0RA, UK  

# Abstract  

Non-invasive parametrisation of physics-based battery models can be performed by ftting the model to electrochemical impedance spectroscopy (EIS) data containing features related to the diferent physical processes. However, this requires an impedance model to be derived, which may be complex to obtain analytically. We have developed the open-source software PyBaMM-EIS that provides a fast method to compute the impedance of any PyBaMM model at any operating point using automatic diferentiation. Using PyBaMM-EIS, we investigate the impedance of the single particle model, single particle model with electrolyte (SPMe), and Doyle-Fuller-Newman model, and identify the SPMe as a parsimonious option that shows the typical features of measured lithium-ion cell impedance data. We provide a grouped-parameter SPMe and analyse the features in the impedance related to each parameter. Using the open-source software PyBOP, we estimate 18 grouped parameters both from simulated impedance data and from measured impedance data from a LG M50LT lithium-ion battery. The parameters that directly afect the response of the SPMe can be accurately determined and assigned to the correct electrode. Crucially, parameter ftting must be done simultaneously to measurements across a wide range of states-of-charge. Overall, this work presents a practical way to fnd the parameters of physics-based models.  

Keywords: DFN, SPM, SPMe, P2D, model, EIS, electrochemical impedance spectroscopy, automatic diferentiation, lithium-ion, difusion, system identifcation, battery, grouped parameters, PyBaMM  

Characterisation techniques are essential for understanding physical processes in batteries and monitoring their state. In many applications, such as health estimation in battery management systems (BMS) and recycling facilities, characterisation should be non-invasive and based on current and voltage data. Characterising a battery is often performed by parametrising a model (a relation between terminal voltage and applied current) from measured data, which can then be used for physical interpretation and simulation of the battery.  

The choice of the model may be challenging. Often ad hoc equivalent circuit models [1] are used to ft measured data [2, 3], but these have the disadvantage that the parameters are not always physically meaningful and simulation may be inaccurate. Instead, we choose to parametrise physics-based models [4, 5]. The standard physics-based modelling approach for lithiumion batteries is the Doyle-Fuller-Newman (DFN) framework [6, 7], based on porous-electrode theory, consisting of a set of coupled nonlinear partial diferential equations that are typically too expensive to simulate in a BMS. There also exist reduced-order models, derived from the DFN model, such as the single-particle model (SPM) [8], single-particle model with electrolyte (SPMe) [9, 10, 11], or multi-particle model [12], all of which may be more practical for BMS.  

Model parameters are only identifable from measured datasets that are sufciently informative. One approach uses constant-current or pulse data during cycling to ft the model to the time-domain voltage response, which we refer to as the “time-domain voltage method”. However, this is often not sufciently informative to fully parametrise a physics-based model [13]. Electrochemical impedance spectroscopy (EIS) is therefore often used as a complementary technique [4, 14, 15, 16, 17]. Conventional EIS measurements [18, 19, 20] consist of taking an equilibrated battery at a fxed operating point (state-of-charge (SOC) and temperature) and applying a small sinusoidal current (or voltage) at set amplitude and frequency. The resulting voltage (or current) is measured and the Fourier component of this, at the same frequency as the excitation, is used to calculate the impedance. The process is then repeated at several frequencies. Measuring impedance over a wide frequency range allows physical processes occurring at diferent timescales to be distinguished, and including impedance data for model parametrisation has been shown to improve the identifability of parameters [21].  

To parametrise a physics-based model from impedance data, we need to know the impedance response of the model. There are two basic approaches, one that solves the problem in the time-domain and the other in the frequency-domain.  

In the frst method, the impedance can be computed directly in the time-domain (the “brute-force” approach) by simulating the conventional EIS measurement procedure described above. The advantages of this are that it is easy to implement, the simulation is true to the practical method, and additional information can be extracted, if required. For example, the higher harmonics can be examined for use in nonlinear EIS (NLEIS) [22, 23, 24]. The main drawback of the brute-force method is relatively high computational cost.  

In the second approach, the model is frst linearised about an operating point before being transformed into the frequency-domain, which can sometimes be performed analytically from the model equations. Early examples of this approach include the impedance calculations in Lasia et al. [25] and Meyers et al. [26], and the impedance mode of the classical pseudo two-dimensional Dualfoil code [27]. More recently, Song and Bazant analytically calculated the difusion impedance of battery electrodes for diferent particle geometries [28], Bizeray et al. calculated the impedance of the full SPM [29], and Plett and Trimboli have studied the impedance of the DFN [4]. However, practically extending this to more complicated models is challenging, so numerical approaches are adopted. One method, referred to as numerical diferentiation, uses a fnite diference approximation for the required derivatives such as in Zhu et al. [30]. Alternatively, here we create exact expressions for the derivatives needed for the impedance using automatic diferentiation, leveraging the open-source battery simulation software PyBaMM [31], which stores models as analytical equations. This has been used previously on specifc models such as in Zic et al. [32]. Using these expressions, the impedance of the model can be computed numerically at any operating point at a set of frequencies, and we have developed an open-source Python package, PyBaMM-EIS, that enables simulation of EIS with any PyBaMM model. This “numerical frequencydomain” impedance method has a much lower computational cost than the brute-force method and is therefore suitable for model parametrisation.  

![](images/1375451b002cda86df35475163261be82bfff658ece91cfca62297a6deb260b1.jpg)  
Figure 1: Illustration of a physics-based battery model with single particles and electrolyte.  

Using PyBaMM-EIS, we can easily compare the impedance of many commonly used models (SPM, SPMe, and DFN). We found that including electrolyte dynamics adds a “difusion bump” impedance feature, often present in measured battery data. We study the impedance of the SPMe in more detail and provide a grouped-parameter model to explain how its impedance changes with SOC, and to show the efect of each of the grouped parameters on the impedance features. Using the open-source software PyBOP [33], we study the parametrisation of the SPMe from simulated impedance and voltage data. Finally, we parametrise the SPMe from measured data of a LG M50LT battery, however, obtaining good fts at low frequencies turns out to be diffcult, showing that extensions of the SPMe are required to ft measured impedance data well.  

# 1. Parametrising battery models  

A battery model (Fig. 1) allows us to simulate the terminal voltage $\nu(t)$ as an operator acting on the applied current $i(t)$ and depending on parameters $\theta$ ,  

$$
\nu(t)=F_{\theta}\{i(t)\},
$$  

with the variable $t$ representing time. In this work, we look at physics-based models, such as the SPM, SPMe, or DFN. These relate the terminal voltage to the applied current based on processes occurring within the battery such as difusion and charge transfer. Physicsbased models depend on a set of parameters $\theta$ (Table 2 for the SPMe) and consist of systems of partial diferential equations (in space and time), ordinary diferential equations, diferential algebraic equations (DAEs), and nonlinear operators, as set out in Appendix B for the SPMe. Note that the open circuit potentials (OCPs) of each electrode are also required, and account for a major part of the model. Non-invasive model parametrisation for a specifc battery consists of estimating the parameters $\theta$ from current and voltage data from that battery.  

# 1.1. time-domain voltage method  

Before we look at EIS data, we briefy consider the time-domain method where we parametrise a model by specifying the current and minimising the diference between measured and simulated voltage. An example of such data is in Fig. 2, and one might choose optimal parameter values θˆ to satisfy  

$$
\hat{\theta}=\arg\operatorname*{min}_{\theta}\sum_{n=0}^{N-1}\big(\nu(t_{n})-\nu(t_{n},i(t),\theta,\mathrm{SOC}_{0})\big)^{2},
$$  

with $\nu(t_{n})$ the measured data at discrete times $t_{n}$ and $\nu(t_{n},i(t),\theta,\mathrm{SOC_{0}})$ the voltage simulated by the model with initial condition $\mathrm{{SOC_{0}}}$ (SOC at time $t_{0}$ ).  

In general, when ftting model parameters to data, an alternative to the frequentist approach is the Bayesian approach, which has been used to explore the identifability of the SPMe [34]. Both of these approaches can be performed with the open source Python package PyBOP [33], which fts PyBaMM models to data.  

A drawback of using only time-domain data is that the identifability of some parameters may be poor. Hence, in this paper we will consider how to ft model parameters using impedance data, which is in the frequency-domain, found from EIS measurements. In the next sections we detail how to measure impedance data and use it for model parametrisation.  

# 1.2. Measuring impedance data  

Impedance spectroscopy is a widely applied technique for parametrising models [35], not only in laboratories, but also in BMS. However, one has to be careful to measure valid impedance data, that is, data satisfying the conditions of linearity and stationarity [18, 36].  

A battery is in a stationary condition when it is at a fxed operating point $x_{m}$ (fxed SOC and temperature), typically after a relaxation period of 2 hours or longer. The condition of linearity is satisfed when the amplitudes of the sinusoidal current or voltage perturbations around the operating point are sufciently small. A voltage deviation smaller than $10\;\mathrm{mV}$ is often considered to indicate linearity, however this depends on several factors such as the frequency, temperature, and SOC.  

![](images/e61c99dd1e4116fa82d5e2fc19990473c95cf50bdc78bc3fb0f7a4756d455366.jpg)  
Figure 2: Time-domain simulation of the SPMe in Appendix C. Top: applied current $i(t)$ . Bottom: simulated voltage response $\nu(t)$ .  

We choose the current as excitation,  

$$
i(t)=I_{k}\sin(\omega_{k}t),
$$  

with $I_{k}$ the amplitude, $\omega_{k}=2\pi f_{k}$ the angular frequency, and $f_{k}$ the frequency. When linearity and stationarity are satisfed, the battery behaves as a linear time-invariant system around the operating point $x_{m}$ . Hence, after transients have faded away, the voltage response to the sinusoidal current excitation (3) yields,  

$$
\begin{array}{r}{\nu(t)=\mathrm{OCV}_{m}+\mathcal{F}^{-1}\{Z_{m}(\omega)I(\omega)\}}\\ {=\mathrm{OCV}_{m}+\underbrace{|Z_{m}(\omega_{k})|I_{k}}_{V_{k}}\sin{\left(\omega_{k}t+\underbrace{\angle Z_{m}(\omega_{k})}_{\varphi_{k}}\right)},}\end{array}
$$  

with $\mathrm{OCV}_{m}$ the open circuit voltage at operating point $x_{m}$ , $\mathcal{F}^{-1}\{\cdot\}$ the inverse Fourier transform, $Z_{m}(\omega)$ the impedance at operating point $x_{m}$ , and $I(\omega)$ the Fourier transform of $i(t)$ . The voltage response is thus also a sinusoidal signal, superimposed on the OCV, but with a diferent amplitude $V_{k}$ and a phase shift $\varphi_{k}$ . The impedance at angular frequency $\omega_{k}$ can then be measured from the Fourier spectra of voltage and current as  

$$
Z_{m}(\omega_{k})=\frac{V(\omega_{k})}{I(\omega_{k})}=\frac{V_{k}}{I_{k}}e^{j\varphi_{k}},
$$  

where the complex impedance can be decomposed into its real part $Z_{\mathrm{r}}(\omega_{k})$ and imaginary part $Z_{\mathrm{j}}(\omega_{k})$ , and $j$ is the imaginary unit $\left(j^{2}=-1\right)$ ).  

![](images/0e7ec68f13fdd2ab671078b23139889ad7981fd91dcc988c676ead0c5bbb37ff.jpg)  
Figure 3: Nyquist plot of measured EIS data of the LG M50LT at diferent SOCs and $25^{\circ}\mathbf{C}$ .  

To obtain impedance data over a wide frequency range, this procedure is repeated at diferent angular frequencies $\omega_{k}$ , which are typically logarithmically spaced. The conditions of linearity and stationarity should be checked for every frequency, which can be done by analysing the current and voltage data in the frequency-domain [36], looking at the Lissajous plots [37], or, when all impedance data is collected, by using the Kramers-Kronig relations [38] or a measurement model [39, 40]. Note that for a battery, it is typically more difcult to obtain valid impedance data at low frequencies where nonlinear efects may be stronger [41].  

# 1.3. Parametrising a model from EIS data  

When measured over a wide frequency range, impedance data $Z_{m}(\omega_{k})$ reveals information about physical processes occurring at diferent timescales. Quantitative information about these processes can be obtained by ftting a model to the impedance data.  

To parametrise a physics-based model from measured impedance data we gather a dataset  

$$
\mathcal{D}=\left\{\omega_{k},Z_{m}(\omega_{k})\right\}_{k=1,\ldots,K}^{m=1,\ldots,M},
$$  

where the index $k$ indicates excited frequencies and $m$ indicates operating points (e.g. diferent SOCs). An example of such a dataset with $M=9$ diferent SOC operating points and $K=61$ frequencies, logarithmically spaced between $200\,\mathrm{Hz}$ and $400\,\upmu\mathrm{Hz}$ , is shown in Fig. 3 for an LG M50LT battery. Some of the model parameters $\theta$ can then be estimated by minimising a chosen cost function, for instance, the sum of squares of the difference between the impedance dataset and the model’s impedance $Z_{m}(\omega,\theta)$ ,  

$$
\hat{\boldsymbol{\theta}}=\arg\operatorname*{min}_{\boldsymbol{\theta}}\sum_{m=1}^{M}\sum_{k=1}^{K}\big|Z_{m}(\omega_{k})-Z_{m}(\omega_{k},\boldsymbol{\theta})\big|^{2}.
$$  

While it is common practice to estimate local model parameters from impedance at single operating points (for instance for an equivalent circuit model), we want to estimate global model parameters to ft data at all the operating points. We do this by estimating the parameters simultaneously from impedance data at diferent SOCs.  

For relatively simple models the impedance $Z_{m}(\omega,\theta)$ can be calculated analytically by linearising the model at the operating point $x_{m}$ and transforming it into the frequency-domain. However, for more complicated models, such as the SPMe or DFN, calculating an analytical expression of the impedance is prohibitively complicated. Therefore in this paper we propose a fast numerical frequency-domain method to obtain the model impedance.  

# 2. Computing numerical impedance with PyBaMM  

To simulate physics-based models, the spatial geometry (see Fig. 1) is discretised—for example using the fnite volume method [42]. It is important that sufcient discretisation points are chosen for accurate simulations; we take 100 radial discretisation points in the particles, 100 discretisation points over the thickness of each electrode, and 20 points over the thickness of the separator. Variables evaluated over this discretisation mesh (e.g. lithium concentration at specifc points in the particles and electrolyte) are then converted into a state vector $\mathbf{x}(t)\in\mathbb{R}^{(N_{\mathbf{x}}+2)\times1}$ , with $N_{\mathbf{x}}$ the number of states in the PyBaMM model and the additional two states being the voltage and current. Spatial operators in the original model (such as gradients and divergences) become matrices in the discretised model. The model then becomes a system of DAEs,  

$$
\mathbf{M}_{\theta}(\mathbf{x}(t))\frac{\mathrm{d}\mathbf{x}(t)}{\mathrm{d}t}=\mathbf{F}_{\theta}(\mathbf{x}(t))+\mathbf{B}i(t),
$$  

with $\mathbf{M}_{\theta}$ the mass matrix, $\mathbf{F}_{\theta}$ a vector-valued nonlinear multivariate function, and $\mathbf{B}$ a zero column vector with a unit entry in its last element. It is this system of DAEs that is solved in battery modelling software such as PyBaMM [31] to simulate the terminal voltage of a battery for a given applied current.  

To obtain the impedance of the model, the nonlinear system of DAEs (8) can be linearised around an operating point ${\bf X}_{m}$ and transformed into the frequencydomain. The impedance at angular frequency $\omega_{k}$ can then be obtained as the scalar  

$$
Z_{m}(\omega_{k},\theta)=\left[(j\omega_{k}\mathbf{M}_{\theta,m}-\mathbf{J}_{\theta,m})^{-1}\mathbf{B}\right]_{[N_{\mathbf{x}}+1]},
$$  

where $\mathbf{J}_{\theta,m}$ is the Jacobian of $\mathbf{F}_{\theta}$ at operating point $\mathbf{X}_{m}$  

$$
{\bf J}_{\theta,m}=\frac{\partial{\bf F}_{\theta}({\bf x})}{\partial{\bf x}}\bigg\vert_{{\bf x}={\bf x}_{m}},
$$  

$\mathbf{M}_{\theta,m}$ is the mass matrix evaluated at ${\bf X}_{m}$ , and $N_{\mathbf{x}}+1$ indicates the index for the voltage in the vector. The mathematical derivation for (9) is given in Appendix A.  

We exploit PyBaMM to discretise the model and compute the Jacobian $\mathbf{J}_{\theta,m}$ using automatic diferentiation. In addition, we have developed open-source software called PyBaMM-EIS that implements this numerical frequency-domain method, allowing efcient computation of the impedance of any battery model implemented in $\mathtt{P y B a M M}$ , at any operating point $\mathbf{X}_{m}$ during a simulation. Moreover, users can defne their own model and compute an impedance from it.  

# 3. Validation of the numerical impedance  

To validate the proposed numerical frequencydomain impedance computation method it was compared to a brute-force simulation. The latter consists of simulating the voltage response of the model for a sinusoidal current input at diferent frequencies and computing the impedance (5) from the Fourier spectra of these.  

We consider the SPM, SPMe, and DFN models with double-layer capacitance implemented in PyBaMM with the parameter set of chen2020 [43] for the LG M50 cell. Fig. 4 shows a Bode plot of the EIS spectra of these models calculated using the frequency-domain approach and the relative diference compared to the bruteforce approach. The models were discretised in space using the fnite volume method resulting in a DAE system with the number of states $N_{\mathbf{x}}$ listed in Table 1. The impedance response was computed for an operating point at $50\%$ SOC and $25\,^{\circ}\mathbf{C}$ , with 60 logarithmically spaced frequencies between ${200}\,\upmu\mathrm{Hz}$ and $1\,\mathrm{kHz}$ . For the frequency-domain numerical impedance, we used PyBaMM-EIS. For the brute-force approach, we chose a sinusoidal excitation with amplitude $I_{k}=100\,\mathrm{mA}$ and simulated the response for ten periods. To discard transient efects, only the fve last periods were retained. To obtain accurate simulations over this wide frequency range, we set the absolute tolerance of the solver to $10^{-9}$ . The impedance was computed from the ratio of voltage and current Fourier spectra (5).  

![](images/b90aa0a4910b1ee06fac1e1c450d9a7bb3d9a4e07aeb37c1bd8fb22c03594267.jpg)  
Figure 4: Bode plot of simulated impedance for the LG M50 cell at $50\%$ SOC for the SPM, SPMe, and DFN computed using the numerical frequency-domain method, and relative diference between the frequency-domain and brute-force methods, $\Delta Z(\omega)\;[\%]\;=\;$ $\begin{array}{r}{100\frac{|Z_{\mathrm{bruteforce}}(\omega)-Z_{\mathrm{frequency}}(\omega)|}{|Z_{\mathrm{frequency}}(\omega)|}}\end{array}$ . The brute-force DFN computation time was prohibitively long, and, hence, we don’t show the relative diference for this model.  

<html><body><table><tr><td rowspan="2">Model</td><td rowspan="2">Nx</td><td colspan="2">Computation time</td></tr><tr><td>Brute-force</td><td>Freq. domain</td></tr><tr><td>SPM</td><td>204</td><td>11.8 s</td><td>21.3ms</td></tr><tr><td>SPMe</td><td>424</td><td>32.8 s</td><td>415ms</td></tr><tr><td>DFN</td><td>20422</td><td></td><td>925 ms</td></tr></table></body></html>

Table 1: Number of states $N_{\mathbf{x}}$ and representative computation times for impedance of diferent models and methods (averaged over ten runs). The brute-force DFN computation time was prohibitively long.  

We observe that both methods have excellent agreement, with a relative error smaller than $0.4\%$ for all models over the entire frequency range. Note that the frequency-domain approach computes the exact linearisation, while the brute-force approach is only exact when the amplitude of the sinusoidal excitation is small enough for linear response [36]. Battery models are typically more nonlinear at low frequencies due to the nonlinear OCV, which explains the signifcantly larger error at low frequencies. The computation times for obtaining the data in Fig. 4 are listed in Table 1 (note that the brute-force DFN simulation did not fnish in a reasonable time due to the large number of states). We conclude that the numerical frequency-domain approach is faster and provides us with accurate impedance data.  

# 4. Comparing the impedance of diferent models  

We now compare the impedance response of several models using the chen2020 LG M50 cell parameter set. We needed 100 discretisation points in the particle to adequately resolve the impedance behaviour, especially in the higher frequency part of the difusion region, and doing so made our results slightly difer from those of [30].  

Fig. 5 shows a Nyquist plot of the impedance for the SPM, SPMe, and DFN at $50\%$ SOC and $25\,^{\circ}\mathbf{C}$ (this is the same data as shown in Fig. 4). For each model, we notice two main features: a semi-circle, linked with charge-transfer kinetics, and a low-frequency difusion tail. An analytical form of the SPM solid-state difusion tail can be found in [29], which starts with a $45^{\circ}$ slope and goes towards a capacitive behaviour (vertical line in the Nyquist plot)—we see the same here. The models where electrolyte dynamics are included (SPMe and DFN) have a difusion tail with an additional “bump”, linked with electrolyte difusion. This “bump” is often present in measured impedance (see Fig. 3), indeed, measured data rarely shows a difusion tail with a $45^{\circ}$ slope that can be modelled with a Warburg element [44, 45, 46]. This suggests that it is worthwhile to consider models that include electrolyte dynamics, although they are more complex. Also note that the SPMe and DFN difer only at high frequencies (which matter less for simulations of real battery behaviour), as can be observed in the Bode plot of Fig. $4^{1}$ .  

As the SPM lacks electrolyte dynamics—which are notable in impedance measurements—and the DFN has signifcantly more parameters and needs longer solve times than the SPMe but shows similar impedance response, we will work with the SPMe for the remainder of this paper.  

# 5. Impedance analysis of the SPMe  

We consider the SPMe with double-layer capacitance (Appendix B), which is an extension of Marquis et al. [10] and Brosa Planella et al. [11]. This model depends on the OCPs of both electrodes and has 31 parameters2, listed in Table 2. Note that two of these are physical constants (Faraday constant and ideal gas constant), and one is the measured temperature, so in total 28 unknown parameters remain. Typically, the number of necessary parameters to simulate the model can be reduced by grouping them, which is discussed next. We then study the physical processes occurring at diferent timescales to show how the impedance depends on SOC and changes when varying the grouped parameters.  

![](images/fddc11e487e61201f6c8864de6100589d36f18aae2a894b7946b3cbef2ad318e.jpg)  
Figure 5: Nyquist plot of the EIS spectra of the SPM, SPMe, and DFN model at $50\%$ SOC for the LG M50 cell (Chen2020 dataset) computed using the frequency-domain method. Frequency range: $[200\,\upmu\mathrm{Hz}$ , 1 kHz]. The DFN overlaps with the SPMe, except at high frequencies. Note that we have changed the contact resistance of the SPM to match with the other models.  

# 5.1. Grouping model parameters  

The model parameters cannot all be estimated independently from current and voltage data because some group together. Grouped parameters naturally arise when non-dimensionalising a model, and grouping reduces the total efective number of parameters [47]. This has been done for the SPM by Bizeray et al. [29], for the SPM with double-layer capacitance by Kirk et al. [23], and for the SPMe without double-layer capacitance by Marquis et al. [10]. Grouping the parameters of the DFN model has been studied in Khalik et al. [48] and in Hileman et al. [15] for lithium metal batteries.  

In Appendix C, we group the parameters of the SPMe with double-layer capacitance, keeping only the dimensions of time, current, and voltage, and obtain 22 grouped parameters as listed in Table 2. All grouped parameters have units that depend upon seconds, Amperes, and Volts.  

The theoretical electrode capacities $Q_{\pm}^{\mathrm{th}}$ are related to the stoichiometries at $0\%$ and $100\%$ SOC through [23],  

$$
Q_{\pm}^{\mathrm{th}}=\mp\frac{Q_{\mathrm{meas}}}{c_{\pm}^{100\%}-c_{\pm}^{0\%}},
$$  

where $Q_{\mathrm{meas}}$ is the measured cell capacity (e.g. $Q_{\mathrm{meas}}=$ $5.15\,\mathrm{Ah}=18\,551$ As in the chen2020 LG M50 parameter set). This reduces the number of grouped parameters to be estimated by two when $Q_{\mathrm{meas}}$ is known.  

<html><body><table><tr><td>Modelparameters</td><td colspan="2"></td></tr><tr><td>F</td><td colspan="2">Faraday constant [C/mol]</td></tr><tr><td>Rg</td><td colspan="2">Ideal gas constant [J/(mol.K)]</td></tr><tr><td>T</td><td colspan="2">Ambient temperature [K]</td></tr><tr><td>Q±</td><td colspan="2">Electrode active material volume fraction</td></tr><tr><td>3</td><td colspan="2">Electrode porosity</td></tr><tr><td>Esep</td><td colspan="2">Separator porosity</td></tr><tr><td>x</td><td colspan="2">Electrode active material max. conc. [mol/m3]</td></tr><tr><td>L±</td><td colspan="2">Electrode thickness [m]</td></tr><tr><td>L</td><td colspan="2">Total cell (electrodes & separator) thickness [m]</td></tr><tr><td>A</td><td colspan="2">Electrode area [m²]</td></tr><tr><td>R±</td><td colspan="2">Particle radius [m]</td></tr><tr><td>D± De</td><td colspan="2">Diffusivity in the particles [m2/s]</td></tr><tr><td>Cdl,±</td><td colspan="2">Reference electrolyte diffusivity [m²/s]</td></tr><tr><td>m±</td><td colspan="2">Electrode double-layer capacity [F/m²]</td></tr><tr><td>+1</td><td colspan="2">Ref. exch. current dens. [(A/m2)(m?/mol)1.5] Cation transference number</td></tr><tr><td>b</td><td colspan="2">Bruggeman coefficient</td></tr><tr><td></td><td colspan="2">Particle concentration at 0% SOC [mol/m?]</td></tr><tr><td></td><td colspan="2">Particle concentration at 100% sOC [mol/m3]</td></tr><tr><td>Ce,0</td><td colspan="2">Initial electrolyte concentration [mol/m3]</td></tr><tr><td>Ro</td><td colspan="2"></td></tr><tr><td></td><td colspan="2">Series resistance [Q]</td></tr><tr><td colspan="2">Grouped parameters 0</td><td></td></tr><tr><td colspan="2">Q = Fα±C±,maxL±A</td><td>Theor. electrode capacity [As]</td></tr><tr><td colspan="2">Qe = F&sepCe,oLA</td><td>Ref. electrolyte capacity [As]</td></tr><tr><td colspan="2">R D±</td><td>Particle diff. timescale [s]</td></tr><tr><td colspan="2">EsepL2 ep+De</td><td>Electrolyte diff. timescale [s]</td></tr><tr><td colspan="2">L2 bsep-1 De sep Esep</td><td>Electrol. diff. timescale sep. [s]</td></tr><tr><td colspan="2">FR± ct m± √Ce,0</td><td>Charge transfer timescale [s]</td></tr><tr><td colspan="2">3α±Cdl,±L±A =+ R±</td><td>Double-layer capacitance [F]</td></tr><tr><td colspan="2">S± = 8±/8sep</td><td>Relative electrode porosity</td></tr><tr><td colspan="2">±=L±/L</td><td>Relative electrode thicknesses</td></tr><tr><td colspan="2">C±</td><td>Stoichiometry at 0% SOC</td></tr><tr><td colspan="2"></td><td>Stoichiometry at 100% SOC</td></tr><tr><td colspan="2"></td><td></td></tr><tr><td colspan="2">Ro</td><td>Cation transference number Series resistance [Q]</td></tr></table></body></html>

Table 2: Model parameters of the SPMe with double-layer capacitance detailed in Appendix B and grouped parameters (see Appendix C).  

![](images/41f360c33117168dbd291927b5237fe9ecff9228e81b0dd707a78f85d5ad3f82.jpg)  
Figure 6: Impedance of the SPMe related to diferent physical processes at diferent timescales. The dotted line in the Nyquist plot shows the impedance assuming perfect separation of timescales whereas the black line shows the actual typical impedance.  

The timescales $\tau_{\pm}^{\mathrm{ct}}$ are used to represent the charge transfer kinetics (as these arise when nondimensionalising the model equations). However, representing charge transfer kinetics with a resistance makes more physical sense. Typical charge transfer resistances, which have values on the order of magnitude of the diameter of the semi-circles in the impedance data, can be used instead [23]  

$$
R_{\mathrm{ct,\pm}}^{\mathrm{typ}}=\frac{2R_{\mathrm{g}}T R_{\pm}}{3F A L_{\pm}\alpha_{\pm}m_{\pm}c_{\pm,\mathrm{max}}\sqrt{c_{\mathrm{e,0}}}}=\frac{2R_{\mathrm{g}}T}{F}\frac{\tau_{\pm}^{\mathrm{ct}}}{3Q_{\pm}^{\mathrm{th}}}.
$$  

The SPMe of Appendix C can be simulated from just the grouped parameters of Table 2 and the electrode open circuit potentials (OCPs), and shows identical behaviour to the native SPMe implemented in PyBaMM.  

# 5.2. Model timescales  

Impedance data allows us to distinguish between diferent physical processes that occur at diferent timescales, as illustrated for the grouped SPMe in Fig. 6. The diferent processes are the following:  

• $\tau<1\,\mathrm{ms}$ $(f>1\,\mathrm{kHz})$ : At very short timescales the SPMe acts as a series resistance $R_{0}$ .  

• $\mathrm{1\,ms~<~\tau~<~1\,s~}$ $\mathrm{{1\,Hz}\,<\,\,f\,<\,1\,k H z)}$ : Here, the dominant process is charge transfer, represented by two semi-circles in the Nyquist plot (one for each electrode). The timescale of this process is related to the charge transfer timescales $\tau_{\pm}^{\mathrm{ct}}$ . However, as discussed above, these values do not represent the actual timescale. A more representative value is ${\tilde{\tau}}_{\pm}^{\mathrm{ct}}\,=\,R_{\mathrm{ct,\pm}}^{\mathrm{typ}}C_{\pm}$ (i.e., the timescale related to the corner frequency of the $R C$ -pair). Numerical values for the chen2020 parameter set are $\tilde{\tau}_{+}^{\mathrm{ct}}=1.5\,\mathrm{ms}$ and $\tilde{\tau}_{-}^{\mathrm{ct}}=15\,\mathrm{ms}$ .  

• $1\mathrm{~s~}<\mathrm{~\tau~}<\,1000\mathrm{~s~}$ $\mathrm{(1\,mHz~<~}f\mathrm{~<~}1\,\mathrm{Hz)}$ : In this range we see electrolyte difusion with timescales $\tau_{\pm}^{\mathrm{e}}$ and $\tau_{\mathrm{sep}}^{\mathrm{e}}$ . The efect on the impedance is the “bump” in the difusion tail. Numerical values for the chen2020 parameter set are $\tau_{+}^{\mathrm{e}}\,=\,409\,\mathrm{s}$ , $\tau_{-}^{\mathrm{{e}}}\,=$ $635\,\mathrm{s}$ , and $\tau_{\mathrm{sep}}^{\mathrm{e}}=246\,\mathrm{s}$ .  

• $\tau\,>\,1\,\mathrm{s}$ s $(f<\,1\,\mathrm{Hz})$ : The longest timescales are related to difusion within the particles, $\tau_{\pm}^{\mathrm{d}}$ . The efect on the impedance is the difusion tail. Numerical values for the chen2020 parameter set are $\tau_{+}^{\mathrm{d}}=6812\;\mathrm{s}$ and $\tau_{-}^{\mathrm{d}}=1041\;\mathrm{s}$ .  

The frequency ranges chosen here are not hard bounds and these values vary from battery to battery. Also note that frequency ranges of diferent physical processes may overlap. The electrolyte difusion and particle difusion timescales overlap in this example, and so do the charge transfer timescales in positive and negative electrodes. Due to the overlap in timescales we get the black line in Fig. 6 as the impedance, instead of the (ideal) dotted line.  

# 5.3. Impedance at diferent operating points  

In stationary conditions, the SOC sets the particle stoichiometry $c_{\pm}$ (which is constant over the particle radius) by linear interpolation  

![](images/560a832924ad4045d07390d7933abe55ed0c94fc5adbaee11627c22e9ef5faca.jpg)  
Figure 7: EIS spectra of grouped SPMe (Appendix C) at diferent SOCs, $25\,^{\circ}\mathbf{C}$ , with model parameters $\theta$ in Table 3. Frequency range: $[200\,\upmu\mathrm{Hz}$ , 1 kHz]. The impedance at $10\,\%$ SOC has been truncated.  

$\overline{{\eta_{\pm}}}$ with respect to the current, evaluated at the operating point $x_{m}$ (containing $i=0$ ). From Appendix $\mathrm{D}$ ,  

$$
R_{\mathrm{ct},m,\pm}\approx\frac{R_{\mathrm{ct},\pm}^{\mathrm{typ}}}{2\,\sqrt{c_{m,\pm}(1-c_{m,\pm})}}\frac{1}{\sqrt{c_{\mathrm{e},\pm}}\big|_{x_{m}}}.
$$  

High and low stoichiometries $c_{m,\pm}$ , related to high and low SOC, give higher charge-transfer resistances, while the middle SOC range gives lower charge transfer resistances. This is exactly what we see from the simulated data in Fig. 7, and can also be seen in the measured data of Fig. 3.  

The difusion tail also changes strongly with SOC, and can be explained from (C.7). The difusion tail impedance is related to the derivative  

$$
c_{\pm}=c_{\pm}^{0\%}+\frac{\mathrm{SOC}}{100}\left(c_{\pm}^{100\%}-c_{\pm}^{0\%}\right),
$$  

with $c_{\pm}^{0\%}$ and $c_{\pm}^{100\%}$ , respectively, the stoichiometries at $0\%$ and $100\%$ SOC. Linearising the model at diferent SOC operating points $x_{m}$ (corresponding to diferent stoichiometries $c_{m,\pm,}$ ) results in diferent impedance data, as can be seen in Fig. 7 for the grouped SPMe.  

We note that the diameter of the semi-circles changes with SOC. This diameter is typically called the charge transfer resistance and is the derivative of the voltage contribution from the spatially averaged overpotential  

$$
\frac{\mathrm{d}U_{\pm}(c_{\pm}|_{r=1})}{\mathrm{d}i}\bigg|_{x_{m}}=\underbrace{U_{\pm}^{\prime}(c_{m,\pm})}_{\mathrm{slope\;of\;OCP}}\frac{\mathrm{d}c_{\pm}|_{r=1}}{\mathrm{d}i}\bigg|_{x_{m}},
$$  

and is proportional to the slope of the OCP [23, 29]. This strongly depends on the stoichiometries $c_{m,\pm}$ , and, hence, on the SOC (see Fig. 9). The OCP slopes here are largest at $10\%$ SOC, giving the largest difusion tail. At an SOC where an OCP has zero slope there will be no contribution from this electrode in the difusion tail.  

The series resistance $R_{0}$ in this model does not depend on SOC, and hence, the leftmost intercept with the real axis stays the same for all SOC.  

5.4. Impedance sensitivity to grouped parameters  

Fig. 8 shows the impedance of the SPMe for variations around the grouped parameters $\theta$ of Table 3:  

$\tau_{\pm}^{\mathrm{d}}$ Particle difusion timescales have an efect at low frequencies in the difusion tail, associated with the frequency where the difusion tail changes from the approx. 45 degree slope to capacitative behaviour. Long experiments are needed to estimate these parameters. At $50\%$ SOC $\tau_{-}^{\mathrm{d}}$ seems not to afect the impedance, because the slope of the negative OCP is nearly fat at that SOC [29]. At other SOCs the difusion timescale of diferent electrodes may be more identifable, as can be seen in Fig. 11. This motivates estimating model parameters from impedance at several SOCs, as in (7).  

$R_{0}$ Series resistance simply shifts the impedance horizontally.  

$\tau^{\mathrm{e}}$ Electrolyte difusion timescales impact the timescale of the “bump”, and hence, at which frequencies it interacts with the particle difusion. The electrolyte difusion timescale in the separator $\tau_{\mathrm{sep}}^{\mathrm{e}}$ has almost no efect on the impedance.  

$\tau_{\pm}^{\mathrm{ct}}$ Charge transfer timescales change the diameters of the semi-circles. The change for the negative electrode is observed to be signifcantly larger than for the positive one. The diameter of the semi-circles is larger around 0 and $100\%$ SOC, as can be seen in Fig. 7, making it easier to estimate these parameters. This again supports estimating model parameters from impedance at diferent SOC levels.  

$t^{+}$ Cation transference number slightly changes the initial slope and resistance of the difusion tail.  

$\zeta_{\pm}$ Relative electrode porosities have a small efect in the middle part of the difusion tail.  

$Q_{\mathrm{e}}$ Reference electrolyte capacity changes the initial slope and resistance of the difusion tail.  

$c_{\pm}^{0\%}$ Stoichiometries at 0 and $100\%$ SOC change the stoichiometry at the particular SOC (13), and, hence, the width of the semi-circle (14) and the diffusion tail (15).  

$Q_{\mathrm{meas}}$ Measured capacity changes the total size of the impedance; large capacity implies small impedance and vice versa. The theoretical electrode capacities $Q_{\pm}^{\mathrm{th}}$ can be calculated from $Q_{\mathrm{meas}}$ , c0±% , and c1±00% (11)±.  

$C_{\pm}$ The impact of double-layer capacitance cannot easily be seen on Nyquist charts, because it only changes the frequency dependence of the points on the semi-circle, but it can be seen on a magnitude Bode plot. Here we note that the charge-transfer kinetics at the surface of the positive particles are faster than the negative ones.  

As all grouped parameters have a unique efect on the impedance, they can possibly be estimated from impedance data (depending on the frequency range and how strongly the processes are present in the impedance).  

# 6. Parametrisation of the SPMe from simulations  

We now study estimation of grouped SPMe parameters from impedance data by ftting the model to simulated data where true parameters are known.  

The grouped parameters $c_{\pm}^{0\%}$ and $c_{\pm}^{100\%}$ are typically estimated from OCP and OCV data [23] prior to impedance ftting. However, instead of fxing these from OCP and OCV data, we will estimate them from impedance data at diferent SOCs, and then set $Q_{\pm}^{\mathrm{th}}$ from (11).  

Assuming that the relative thicknesses $\ell_{\pm}$ are known, the remaining grouped model parameters to estimate from impedance data are  

$$
\begin{array}{r}{\theta=[\tau_{+}^{\mathrm{d}},\tau_{+}^{\mathrm{e}},\tau_{+}^{\mathrm{ct}},C_{+},\zeta_{+},\epsilon_{+}^{0\mathcal{H}_{\sigma}},c_{+}^{100\mathcal{H}_{\sigma}},}\\ {\tau_{-}^{\mathrm{d}},\tau_{-}^{\mathrm{e}},\tau_{-}^{\mathrm{ct}},C_{-},\zeta_{-},c_{-}^{0\mathcal{H}_{\sigma}},c_{-}^{100\mathcal{H}_{\sigma}},}\\ {\tau_{\mathrm{sep}}^{\mathrm{e}},Q^{\mathrm{e}},t^{+},R_{0}]\qquad\in\mathbb{R}_{+}^{18\times1}.}\end{array}
$$  

The values of the true grouped parameters $\theta$ for the simulations are calculated from the Chen2020 parameter set and listed in Table 3.  

# 6.1. Estimation from impedance data  

We frst study parameter estimation from simulated SPMe impedance data (shown in Fig. 7). The impedance dataset (6) has $K\ =\ 60$ frequencies, logarithmically spaced between ${200}\,\upmu\mathrm{Hz}$ and $1\,\mathrm{kHz}$ , and $M\,=\,9$ SOC levels $(10\%,\,20\%,...,\,90\%)$ . We estimate the grouped parameters $\theta$ (16) by minimising the leastsquares cost function (7). The optimisation is performed with the multi-ftting problem class in PyBOP, using particle swarm optimisation, with the boundaries for the 18-dimensional search space given in Table 3. We allowed for a maximum of 1000 iterations and ran the optimisation ten times. Although the ftting is done over all SOCs, it is instructive to examine the mean relative ftting errors (FE) at the diferent SOC levels  

![](images/99bc2037588f1c60e65c736abb48db37b19d967dad901eda428e9d6f4e65b992.jpg)  
Figure 8: Impedance of SPMe at $50\%$ SOC, $25\,^{\circ}\mathbf{C}$ , varying grouped parameters one-by-one. Parameters are perturbed with logarithmic spacing in the range [0.5θ, 2θ] (blue to red) with $\theta$ listed in Table 3 (black). Frequency range: $[200\,\upmu\mathrm{Hz}$ , $1\,\mathrm{kHz}]$ . Note that most impedance are shown on Nyquist plots, while the bottom two fgures are Bode magnitude plots.  

<html><body><table><tr><td colspan="4"></td><td colspan="2">Impedance data</td><td colspan="2">Voltage data</td></tr><tr><td>Parameter</td><td>Optimisation bounds</td><td>θ</td><td colspan="2"></td><td colspan="2">08/0 [%]</td><td>0/0[%]</td></tr><tr><td>Qmeas [As] 1+</td><td></td><td>18551 0.4375</td><td colspan="2"></td><td colspan="2"></td><td></td></tr><tr><td>I_ [S]p2</td><td>[5e2,1e4]</td><td>0.4930 6812</td><td colspan="2">6682</td><td colspan="2">0.38 6831</td><td>0.53</td></tr><tr><td>r[s]</td><td>[5e2,1e4]</td><td>1041</td><td>1020</td><td>0.93</td><td>1065</td><td colspan="2">1.48</td></tr><tr><td>t [s]</td><td>[2e2,1e3]</td><td>409.2</td><td>200.0</td><td>0.011</td><td colspan="2">948.0</td><td>1.24</td></tr><tr><td>T [s]</td><td>[2e2,1e3]</td><td>634.7</td><td>403.5</td><td>20.9</td><td colspan="2">209.9</td><td>53.7</td></tr><tr><td>Tsep [s] </td><td>[2e2,1e3]</td><td>246.2</td><td>200.0</td><td>0.61</td><td colspan="2">200.7</td><td>0.59</td></tr><tr><td>+5</td><td>[0.5,1.5]</td><td>0.7128</td><td>0.500</td><td>0.0019</td><td colspan="2">0.7573</td><td>3.13</td></tr><tr><td>-</td><td>[0.5,1.5]</td><td>0.5319</td><td>1.500</td><td>41.9</td><td colspan="2">0.5420</td><td>3.09</td></tr><tr><td>Qe [As]</td><td>[5e2,1e3]</td><td>804.8</td><td>500.0</td><td>8.20</td><td colspan="2">797.9</td><td>2.12</td></tr><tr><td>[s] </td><td>[1e3,5e4]</td><td>4657</td><td>5158</td><td>26.5</td><td>6244</td><td colspan="2">6.92</td></tr><tr><td>T [s]</td><td>[1e3,5e4]</td><td>27592</td><td>27746</td><td>5.07</td><td colspan="2">13255</td><td>8.38</td></tr><tr><td>C+ [F] C-[F]</td><td>[0,1]</td><td>0.5935 0.6719</td><td>0.6178 0.6953</td><td>13.9</td><td></td><td colspan="2">1.2e-4 167</td></tr><tr><td>C0%</td><td>[0,1] [0.8,0.9]</td><td>0.8540</td><td>0.8548</td><td>8.68 0.10</td><td>0.9966 一</td><td></td><td>4.04</td></tr><tr><td>100%</td><td>[0,0.1]</td><td>0.02635</td><td>0.02634</td><td>11.8</td><td></td><td colspan="2"></td></tr><tr><td>Cx</td><td>[0.2,0.3]</td><td>0.2638</td><td>0.2642</td><td>0.22</td><td></td><td colspan="2"></td></tr><tr><td>+1</td><td>[0.85,0.95]</td><td>0.9106</td><td>0.9092 0.2647</td><td>0.31</td><td>一</td><td></td><td>一</td></tr><tr><td>Ro [Ω]</td><td>[0.2,0.5]</td><td>0.2594 0.01</td><td>0.0101</td><td>9.16 1.22</td><td></td><td>0.2025</td><td>28.7</td></tr><tr><td>m</td><td>[0,0.05]</td><td></td><td></td><td></td><td></td><td>0.0148</td><td>8.56</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td>7</td><td></td><td></td></tr><tr><td></td><td>1</td><td>2 3</td><td>4</td><td>5 6</td><td></td><td>8</td><td>9</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td>60</td><td></td><td>90</td></tr><tr><td></td><td>SOCm [%] 10</td><td>20 30</td><td>40</td><td>50</td><td>70</td><td>80</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>FEm [%] 0.87</td><td>0.97</td><td>0.96 0.97</td><td>0.94</td><td>0.94 0.90</td><td>0.86</td><td>0.84</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table></body></html>

Table 3: Parametrisation of the grouped SPMe from simulated impedance and time-domain voltage data with particle swarm optimisation in PyBOP. We list the optimisation bounds, true parameters $\theta$ , estimated parameters $\hat{\boldsymbol{\theta}}$ (lowest cost of ten runs), and relative standard deviation $\sigma_{\hat{\theta}}/\hat{\theta}$ (over ten runs). The impedance data is shown in Fig. 7 and the time-domain voltage data in Fig. 2. The average computation times (run parallel on 16 AMD 7950X cores) are 441 s (impedance) and $613\,\mathrm{s}$ (time-domain voltage). Better estimates for the electrolyte difusion parameters can be obtained using other optimisers at the cost of longer computation times. The ftting errors (17) of the impedance at diferent SOC are also listed.  

$$
\mathrm{FE}_{m}\left[\mathcal{V}_{o}\right]=\frac{100}{K}\sum_{k=1}^{K}\frac{\vert Z_{m}(\omega_{k})-Z_{m}(\omega_{k},\hat{\theta})\vert}{\vert Z_{m}(\omega_{k})\vert}.
$$  

These are listed in Table 3 for the best ft of the ten runs and the data over frequency is shown in Fig. 12. The ftting errors are under $1\%$ for all SOC levels.  

The estimated parameters $\hat{\boldsymbol{\theta}}$ of the best ft of the ten runs are listed in Table 3. As an indication of the identifability of the grouped parameters, we also list the relative standard deviation $\sigma_{\hat{\theta}}/\hat{\theta}$ over the ten runs; we would expect accurately identifable parameters to have a small standard deviation. However, the cost function is highly non-convex, and, hence, this metric for the identifability may depend on the optimiser and initial point. (A better way would be to consider the Fisher information matrix [49].) The parameters related to large features can be identifed accurately from impedance data (e.g.  

the stoichiometry bounds, series resistance, particle diffusion timescales, and charge transfer timescale). The estimated parameters related to the electrolyte difusion and separator are less accurate, but these parameters related to small features in the impedance have little efect on the behaviour of the battery. The grouped model parameters are also all attributed to the correct electrode.  

# 6.2. Comparison with time-domain data  

As a comparison, parameters were also estimated from the simulated SPMe time-domain voltage data of Fig. 2. The dataset consists of 7 minutes resting at $90\%$ SOC, starting from steady-state, then a $-5\,\mathrm{A}$ discharge for 53 minutes, 20 minutes rest, $5\,\mathrm{A}$ charge for $20\;\mathrm{min}\cdot$ - utes, and 20 minutes rest again, resulting in a total experiment time of $2~\mathrm{{h}}$ . The data were simulated with a time step of $10\,\mathrm{s}$ , resulting in $N=720$ points. Note that measuring this dataset would take less time than measuring the impedance dataset from Fig. 7. We estimate the grouped parameters $\theta$ (16) by minimising the leastsquares cost function (2). The ftting was performed in PyBOP, using particle swarm optimisation, with the same boundaries for the 18-dimensional search space given in Table 3. We allow for a maximum of 1000 iterations and run the optimisation ten times. The stoichiometries $c_{\pm}^{0\%}$ and $c_{\pm}^{100\%}$ were not estimated as this led to convergence issues; they were assumed known.  

Accurate fts of the time-domain voltage data were obtained, with the estimated parameters of the best ft and the relative standard deviations over the ten runs listed in Table 3. For this specifc simulation, we conclude that the long timescale parameters are identifed with similar accuracy from the time-domain data and impedance data, while the short timescale parameters are better identifed from impedance data because the sampling period of $10\,\mathrm{s}$ in the voltage time-domain data does not give visibility of the fast processes occurring in the battery.  

The comparison of the diferent sources of data discussed above suggests an extension of the work presented here where one could use both time-domain voltage and EIS data to estimate model parameters.  

# 7. Parametrisation of LG M50LT batteries from measured data  

We now parametrise the grouped SPMe from LG M50LT measured impedance data. This Li-ion cell has a graphite anode and NMC cathode, and operates between $2.5\,\mathrm{V}$ and $4.2\,\mathrm{V}$ . The measured cell capacity was $Q_{\mathrm{meas}}=4.89\,\AA$ Ah. Open circuit potentials were obtained by constructing half cells; this data was provided by About:Energy (personal communication) and is shown in Fig. 9 for the given stoichiometric bounds.  

We performed EIS measurements at diferent operating points, listed in Table 4 and shown as dots in Fig. 9, with a Gamry Interface 5000P potentiostat. The battery was frst charged to $4.2\,\mathrm{V}$ and held there until the current decreased below $50\,\mathrm{mA}$ . It was then discharged at $C/10$ in steps of $10\%$ SOC (with $Q_{\mathrm{meas}}/10\,=\,0.489\,\mathrm{A}$ for periods of $1\,\mathrm{h}$ ), followed by $4\,\mathrm{{h}}$ of open-circuit relaxation to reach steady-state for the EIS measurement. Impedance was measured in the frequency range $[400\,\upmu\mathrm{Hz}$ , $200\,\mathrm{Hz}]$ with ten logarithmically distributed frequencies per decade. Hybrid EIS was used (a current is applied, but a voltage perturbation is chosen by the user) with a DC current of $_{0\,\mathrm{{A}}}$ and a sinusoidal voltage perturbation of $10\,\mathrm{mV}$ amplitude. A Nyquist plot of the measured impedance data is shown in Fig. 3. The conditions of linearity and stationarity were checked from Lissajous curves and using the Orazem toolbox [40].  

![](images/3a47d26b45e2ad5d78444c47f6c03af26be22c9d81a0d75975b1ea8b4dfe5f33.jpg)  
Figure 9: Measured OCV and OCP data for the LG M50LT. Dots indicate points where the impedance spectra of Fig. 3 were measured.  

The grouped SPMe parameters $\theta$ (16) were estimated for the impedance data between $20\%$ and $80\%$ SOC (the $10\%$ and $90\%$ SOC data were hard to ft with the SPMe). The cost function (7), with $M=7$ and $K=61$ , was minimised with 100 iterations of SciPy diferential evolution. The estimated grouped parameters are listed in Table 5, with the fts shown in Fig. 10, and the average ftting errors listed in Table 4. Fits at (very) low frequencies are relatively poor, but for higher frequencies we obtained better results. At low frequencies the impedance is strongly dependent on the slope of the OCPs, and hence on the OCP data and balancing, making it hard to obtain good fts. Moreover, due to hysteresis, the OCPs may be dependent on the direction from which the operating point is approached (charging or discharging). Also, the SPMe may not be general enough to accurately ft measured LG M50LT data.  

We have not explored ftting the measured data with other models but there are many possible extensions (which can be implemented in PyBaMM) that might improve the ft. These include considering the difusivities in the particles to change with SOC (for example based on OCP gradients [50, 51]), or considering a distribution of particle sizes using multi-particle models [12], as well as the many other models available in PyBaMM.  

<html><body><table><tr><td>m</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>SOCm [%]</td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td><td>60</td><td>70</td><td>80</td><td>90</td></tr><tr><td>OCVm [V]</td><td>3.3909</td><td>3.4998</td><td>3.5893</td><td>3.648</td><td>3.728</td><td>3.856</td><td>3.931</td><td>4.038</td><td>4.084</td></tr><tr><td>FEm [%]</td><td>一</td><td>3.51</td><td>3.24</td><td>2.47</td><td>5.79</td><td>3.26</td><td>2.35</td><td>1.78</td><td>一</td></tr></table></body></html>

Table 4: The operating points for the LG M50LT cell that were considered here. Ambient temperature throughout was $25\,^{\circ}\mathbf{C}$  

![](images/bcb69dfac93476f8c0080374f60d1a9c416dbf7ae9b348c17cf945729a32cf1a.jpg)  

Table 5: Estimated grouped parameters LG M50LT.  

# 8. Conclusions  

We have proposed a numerical approach to compute the impedance of physics-based battery models, implemented under PyBaMM-EIS. The method consists of discretising the model in space, locally linearising the resulting nonlinear system of DAEs using automatic differentiation, transforming the linearised equations into the frequency-domain, and solving for the impedance. This tool allows one to evaluate the impedance of any PyBaMM model at any operating point, and is signifcantly faster than doing “brute-force” simulations while giving comparable results.  

We have analysed the impedance of diferent physicsbased models (SPM, SPMe, and DFN), and shown that it is essential to consider electrolyte dynamics, which add a “bump” in the difusion tail that is also present in measured data. The DFN has similar impedance to the SPMe, but is more expensive to simulate and has more parameters. Therefore, we conclude that most of the behaviour of a battery can be explained via the impedance of the SPMe.  

We have provided the model equations for the SPMe including double-layer capacitance, and grouped the parameters of this model to determine a minimal set of parameters required for simulations. The groupedparameter SPMe gives identical results to PyBaMM’s SPMe. We also showed how the impedance depends on SOC and, via a sensitivity analysis, how the grouped parameters afect the impedance in diferent ways.  

We estimated 18 SPMe grouped parameters using simulated impedance data and voltage data. Crucially, we ftted impedance data across diferent SOCs simultaneously in order to increase the identifability of the parameters. Simulated EIS data could be ftted accurately, with most grouped parameters well estimated. The exceptions were parameters related to small features in the impedance, which have little efect on the overall behaviour, for example the parameters of the separator. Hence, EIS can be used as an efective tool to parametrise the SPMe. Comparing the informativity of simulated impedance vs. time-domain voltage data, we found that the long timescale parameters (e.g. particle difusion timescales) can be estimated accurately from both, but the short timescale parameters are better estimated from impedance data. We therefore suggest exploring both sources of data for parameter estimation.  

To demonstrate how the methodology can be used in practice, we performed parametrisation of the SPMe for a commercial LG M50LT battery from measured impedance and OCP data. The ft was good in the higher frequency region, but less good at lower frequencies. This suggests that the SPMe needs extensions to accurately describe battery behaviour (e.g. particle size distributions and functional parameters).  

The methodology presented in this paper gives a practical method for ftting a large class of battery models to EIS data. The use of automatic diferentiation combined with working in the frequency-domain dramatically reduces the computation time, and ftting the parameters across many SOC levels gives accurate estimations for most parameters.  

# Appendix A: Numerical impedance computation  

Software such as PyBaMM simulates a battery by integrating a system of DAEs  

$$
\overline{{\mathbf{M}}}_{\theta}(\overline{{\mathbf{x}}}(t))\frac{\mathrm{d}\overline{{\mathbf{x}}}(t)}{\mathrm{d}t}=\overline{{\mathbf{F}}}_{\theta}(\overline{{\mathbf{x}}}(t),t),
$$  

where $\overline{{\mathbf{M}}}_{\theta}\ \in\ \mathbb{R}^{N_{\mathbf{x}}\times N_{\mathbf{x}}}$ is the mass matrix, which may be singular3, $\overline{{\mathbf{x}}}\,\in\,\mathbb{R}^{N_{\mathbf{x}}\times1}$ is the vector with discretised states, and $\overline{{\mathbf{F}}}_{\theta}:\mathbb{R}^{N_{\mathbf{x}}\times1}\rightarrow\mathbb{R}^{N_{\mathbf{x}}\times1}$ is a nonlinear vectorvalued function. The number of states $N_{\mathbf{x}}$ for diferent models (which depends on the number of discretisation points) are shown in Table 1. Both $\overline{{\mathbf{M}}}_{\theta}$ and $\overline{{\mathbf{F}}}_{\theta}$ depend on the model parameters $\theta$ . This system of DAEs can be solved using a time-stepping algorithm. Note that some models, such as the single particle model [10], result in a system of ordinary diferential equations instead of DAEs.  

PyBaMM does not always use voltage and current as state variables and therefore we need to rewrite (A.1) in a form that allows us to compute an impedance. Assuming that the right-hand side $\mathbf{\bar{F}}_{\theta}$ depends on $t$ explicitly only through the applied current $i(t)$ , the system of DAEs can be rewritten by adding current and voltage to the states,  

$$
\mathbf{M}_{\theta}(\mathbf{x}(t))\frac{\mathrm{d}\mathbf{x}(t)}{\mathrm{d}t}=\mathbf{F}_{\theta}(\mathbf{x}(t))+\mathbf{B}i(t),
$$  

with $\mathbf{B}=[0,0,...,1]^{\intercal}$ and  

$$
\mathbf{x}^{\top}(t)=[\overline{{x}}_{1}(t),\overline{{x}}_{2}(t),\ldots,\overline{{x}}_{N_{\mathrm{x}}}(t),\nu(t),i(t)]\in\mathbb{R}^{(N_{\mathrm{x}}+2)\times1}.
$$  

The last two rows of $\mathbf{M}_{\theta}$ are then zeros and the last two rows in $\mathbf{F}_{\theta}$ correspond to the algebraic equations. The frst of these is the implicit expression for the terminal voltage $\nu(t)$ in terms of the other state variables $G(\mathbf{x}(t))\;=\;0$ (which depends on the particular model) and the last row imposes that $x_{N_{\mathbf{x}}+2}(t)\,=\,i(t)$ by setting $F_{N_{\mathrm{x}}+2}(\mathbf{x}(t))=-x_{N_{\mathrm{x}}+2}(t)$ . In matrix notation we have  

$$
\left[\begin{array}{c c c c c}{M_{1,1}}&{M_{1,2}}&{\ldots}&{M_{1,N_{x}+2}}\\ {M_{2,1}}&{M_{2,2}}&{\ldots}&{M_{2,N_{x}+2}}\\ {\vdots}&{\vdots}&{}&{\vdots}\\ {M_{N_{x},1}}&{M_{N_{x},2}}&{\ldots}&{M_{N_{x},N_{x}+2}}\\ {0}&{0}&{\ldots}&{0}\\ {0}&{0}&{\ldots}&{0}\end{array}\right]\left[\begin{array}{c}{\dot{x}_{1}}\\ {\dot{x}_{2}}\\ {\vdots}\\ {\dot{x}}\\ {\dot{x}_{N_{x}}}\\ {\dot{\nu}}\\ {\dot{i}}\end{array}\right]=\left[\begin{array}{c}{F_{1}(\mathbf{x})}\\ {F_{2}(\mathbf{x})}\\ {\vdots}\\ {F_{N_{x}}(\mathbf{x})}\\ {G(\mathbf{x})}\\ {-i}\end{array}\right]+\left[\begin{array}{l}{0}\\ {0}\\ {\vdots}\\ {i.}\\ {0}\\ {0}\\ {1}\end{array}\right]
$$  

To calculate the impedance from the model, we need to linearise (A.2) and transform the expression into the frequency-domain.  

Linearisation  

To linearise the system of equations (A.2), we Taylor series expand $\mathbf{F}_{\theta}(\mathbf{x}(t))$ around an operating point $\mathbf{X}_{m}$ (depending on SOC, temperature, etc.)  

$$
\mathbf{F}_{\theta}(\mathbf{x}(t))=\mathbf{F}_{\theta}(\mathbf{x}_{m})+\underbrace{\frac{\partial\mathbf{F}_{\theta}(\mathbf{x})}{\partial\mathbf{x}}\bigg|_{\mathbf{x}=\mathbf{x}_{m}}}_{\mathbf{J}_{\theta,m}}\underbrace{(\mathbf{x}(t)-\mathbf{x}_{m})}_{\tilde{\mathbf{x}}(t)}+\mathrm{h.o.t.},
$$  

with $\mathbf{J}_{\theta,m}\;\in\;\mathbb{R}^{(N_{\mathbf{x}}+2)\times(N_{\mathbf{x}}+2)}$ the Jacobian of the system, depending on the operating point $\mathbf{X}_{m}$ , and h.o.t. standing for higher order terms. Note that while the vectorvalued function $\mathbf{F}_{\theta}$ is dependent on all model parameters $\theta_{i}$ , the Jacobian $\mathbf{J}_{\theta,m}$ may not be (that is, model information may be lost during linearisation). The mass matrix can similarly be expanded using a Taylor series. To linearise the system we neglect the higher order terms4 in (A.5) and all except the frst term in $\mathbf{M}_{\theta}$ , and put these into (A.2), yielding  

$$
\mathbf{M}_{\theta}(\mathbf{x}_{m})\frac{\mathrm{d}\tilde{\mathbf{x}}(t)}{\mathrm{d}t}=\mathbf{F}_{\theta}(\mathbf{x}_{m})+\mathbf{B}i_{m}+\mathbf{J}_{\theta,m}\tilde{\mathbf{x}}(t)+\mathbf{B}\tilde{i}(t),
$$  

with $\tilde{i}(t)~=~i(t)\,-\,i_{m}$ and $i_{m}$ the $(N_{\mathbf{x}}\,+\,2)$ -th entry of ${\bf X}_{m}$ . Note that the operating point ${\bf X}_{m}$ does not have to be a steady-state, for instance taking $i_{m}\neq\mathrm{~0~}$ makes it possible to compute the impedance in operando conditions [41, 52]. However, for this paper we only consider impedance in stationary conditions $(i_{m}=0)$ ) where $\mathbf{F}_{\theta}(\mathbf{x}_{m})=0$ , and hence,  

$$
\underbrace{\mathbf{M}_{\theta}(\mathbf{x}_{m})}_{M_{\theta,m}}\frac{\mathrm{d}\tilde{\mathbf{x}}(t)}{\mathrm{d}t}=\mathbf{J}_{\theta,m}\tilde{\mathbf{x}}(t)+\mathbf{B}i(t),
$$  

We have now obtained a linear system of DAEs which is valid for small perturbations at a fxed operating point ${\bf X}_{m}$ of the battery.  

# Frequency-domain transformation  

To transform the linear set of DAEs into the frequency-domain, we take the Fourier transform of (A.7) and obtain  

$$
\begin{array}{r}{j\omega\mathbf{M}_{\theta,m}\tilde{\mathbf{X}}(\omega)=\mathbf{J}_{\theta,m}\tilde{\mathbf{X}}(\omega)+\mathbf{B}I(\omega),}\end{array}
$$  

where $\tilde{\mathbf{X}}(\omega)=\mathcal{F}\{\tilde{\mathbf{x}}(t)\}$ and using the property of Fourier transforms that  

$$
\mathcal{F}\bigg\{\frac{\mathrm{d}\tilde{\mathbf{x}}(t)}{\mathrm{d}t}\bigg\}=j\omega\tilde{\mathbf{X}}(\omega).
$$  

<html><body><table><tr><td colspan="2">Modelvariables</td></tr><tr><td>i(t)</td><td>Applied current [A]</td></tr><tr><td>v(t)</td><td>Terminal voltage [V]</td></tr><tr><td>v(t)</td><td>Electrode-aver. particle surface volt. [V]</td></tr><tr><td>U±(c±)</td><td>Open circuit voltage [V]</td></tr><tr><td>C±(r,t)</td><td>Particle lithium concentration [mol/m3]</td></tr><tr><td>j±(x,t)</td><td>Molar flux [mol/(m?s)]</td></tr><tr><td>n±(x,t)</td><td>Overpotentials [V] Electrolyte lithium concentr. [mol/m3]</td></tr><tr><td>Ce(x, t) Ne(x, t)</td><td>Electrolyte flux [mol/(m²s)]</td></tr><tr><td></td><td></td></tr><tr><td>i0,±(x, t)</td><td>Exchange current density [A/m2]</td></tr><tr><td>r</td><td>Particle radius [m]</td></tr><tr><td>x</td><td>Electrode thickness [m]</td></tr><tr><td>t</td><td>Time [s]</td></tr></table></body></html>

Table 6: Variables of the SPMe with their units.  

Hence, we can write the solution of (A.8) as  

Electrode average operator. For any variable $h$ , we defne an “electrode-average” operator for each electrode, denoted by an overbar and subscript $\left(+/-\right)$ , as  

$$
\overline{{h_{\pm}}}(t)=\frac{1}{L_{\pm}}\int h(x,t)\ \mathrm{d}x_{\pm},
$$  

with the integration domains $\mathrm{d}x_{-}\,\in\,[0,L_{-}]$ and $\mathrm{d}x_{+}\ \in$ $[L-L_{+},L]$ .  

Difusion in the spherical solid particles in each of the electrodes $(\pm)$ .  

$$
\begin{array}{r}{\tilde{\mathbf{X}}(\omega)=\underbrace{(j\omega\mathbf{M}_{\theta,m}-\mathbf{J}_{\theta,m})^{-1}\mathbf{B}}_{\mathbf{K}_{\theta,m}(\omega)\in\mathbb{C}^{(N_{\mathbf{X}}+2)\times1}}I(\omega).}\end{array}
$$  

Finally, we fnd a numerical expression for the impedance scalar at the operating point $\mathbf{X}_{m}$ and angular frequency $\omega$ by selecting the $(N_{\mathbf{x}}+1)$ -th entry of the vector $\mathbf{K}_{\theta,m}(\omega)$ ,  

$$
Z_{m}(\omega,\theta)=\frac{V(\omega)}{I(\omega)}=\mathbf{K}_{\theta,m}(\omega)_{[N_{\mathbf{x}}+1]}.
$$  

Finding the vector $\mathbf{K}_{\theta,m}(\omega)$ involves the inverse matrix operation in (A.10) at the selected set of angular frequencies $\omega_{k}$ so that $Z_{m}(\omega_{k},\theta)$ can be used for the model parameter estimation (7). The simplest approach for fnding this vector is to do a direct solve of (A.8) (e.g. with LU decomposition) which appears to be more computationally efcient than iterative methods (e.g. BicgSTAB [53]) for typical battery models.  

# Appendix B: Dimensional SPMe  

$$
\frac{\partial c_{\pm}}{\partial t}=\frac{1}{r^{2}}\frac{\partial}{\partial r}\left(r^{2}D_{\pm}(c_{\pm})\frac{\partial c_{\pm}}{\partial r}\right)\qquad0\leq r\leq R_{\pm}
$$  

Here, we detail the dimensional SPMe model based on [54, Chapter 3] with improved averaging from [11] and double-layer capacitance from [23]. The variables in this model are listed in Table 6 and the parameters in Table 2. In this model we choose a charging current to be positive (such that the impedance ends up in the right quadrant of the complex plane). Note that this is diferent to the implementations in PyBaMM and PyBOP, where charging currents are negative (and a corresponding minus sign is included in calculations of the impedance).  

with boundary conditions  

$$
D_{\pm}(c_{\pm})\frac{\partial c_{\pm}}{\partial r}\bigg|_{r=0}=0,\qquad-D_{\pm}(c_{\pm})\frac{\partial c_{\pm}}{\partial r}\bigg|_{r=R_{\pm}}=\overline{{{j_{\pm}}}},
$$  

and initial conditions  

$$
c_{\pm}(r,0)=c_{\pm}^{0\%}+\frac{\mathrm{SOC}_{0}}{100}\left(c_{\pm}^{100\%}-c_{\pm}^{0\%}\right).
$$  

Intercalation reaction at the particle surface.  

$$
j_{\pm}(x,t)=\frac{2i_{0,\pm}}{F}\sinh\left(\frac{F\eta_{\pm}}{2R_{\mathrm{g}}T}\right)
$$  

with the exchange current  

$$
\begin{array}{r}{i_{0,\pm}(x.t)=m_{\pm}\,\sqrt{c_{\pm}|_{r=R_{\pm}}}\,\sqrt{c_{\mathrm{e,\pm}}(c_{\pm,\mathrm{max}}-c_{\pm}|_{r=R_{\pm}})},}\end{array}
$$  

the overpotentials  

$$
\eta_{\pm}(x,t)=\nu_{\pm}-U_{\pm}(c_{\pm}|_{r=R_{\pm}}),
$$  

and the particle surface voltage  

$$
\nu_{\pm}(x,t)=\overline{{\nu_{\pm}}}+\frac{2R_{\mathrm{g}}T}{F}(1-t^{+})\left(\overline{{\log\!\left(\frac{c_{\mathrm{e,\pm}}}{c_{\mathrm{e,0}}}\right)}}-\log\!\left(\frac{c_{\mathrm{e,\pm}}}{c_{\mathrm{e,0}}}\right)\right).
$$  

Transfer process at the particle surface with doublelayer.  

$$
C_{\mathrm{dl,\pm}}\frac{\mathrm{d}\overline{{\nu_{\pm}}}}{\mathrm{d}t}=\pm\frac{R_{\pm}}{3\alpha_{\pm}L_{\pm}A}i(t)-F\overline{{j_{\pm}}}
$$  

with initial condition $\overline{{\nu_{\pm}}}(0)=U_{\pm}(c_{\pm,0})$ .  

Difusion in the electrolyte.  

$$
\begin{array}{r l}&{\varepsilon(x)\frac{\partial c_{\mathrm{e}}}{\partial t}=-\frac{\partial N_{\mathrm{e}}}{\partial x}}\\ &{\quad\quad\quad+\left\{\begin{array}{l l}{\frac{3\alpha_{-}}{R_{-}}j_{-}}&{\mathrm{~for~}0<x<L_{-}}\\ {0}&{\mathrm{~for~}L_{-}<x<L-L_{+}}\\ {\frac{3\alpha_{+}}{R_{+}}j_{+}}&{\mathrm{~for~}L-L_{+}<x<L}\end{array}\right.}\end{array}
$$  

where the electrolyte fux  

$$
\begin{array}{l l}{{N_{\mathrm{e}}(x,t)=-\varepsilon(x)^{b}D_{\mathrm{e}}(c_{\mathrm{e}})\frac{\partial c_{\mathrm{e}}}{\partial x}}}\\ {{\phantom{\frac{1}{1}}-\frac{t^{+}i(t)}{F A}\left\{\begin{array}{l l}{{\displaystyle\frac{x}{L_{-}}}}&{{\mathrm{~for~}0<x<L_{-}}}\\ {{\displaystyle\frac{1}{L}}}&{{\mathrm{~for~}L_{-}<x<L-L_{+}}}\\ {{\displaystyle\frac{L-x}{L_{+}}}}&{{\mathrm{~for~}L-L_{+}<x<L}}\end{array}\right.}}\end{array}
$$  

with  

$$
\varepsilon(x)=\left\{\begin{array}{l l}{\varepsilon_{-}}&{\mathrm{~for~}0<x<L_{-}}\\ {\varepsilon_{\mathrm{sep}}}&{\mathrm{~for~}L_{-}<x<L-L_{+}}\\ {\varepsilon_{+}}&{\mathrm{~for~}L-L_{+}<x<L,}\end{array}\right.
$$  

boundary conditions  

$$
\left.\frac{\partial c_{\mathrm{e}}}{\partial x}\right|_{x=0}=0\,\,\,\mathrm{and}\,\,\left.\frac{\partial c_{\mathrm{e}}}{\partial x}\right|_{x=L}=0,
$$  

and initial condition $c_{\mathrm{e}}(x,0)=c_{\mathrm{e},0}$ .  

Terminal voltage.  

$$
\nu(t)=\overline{{\nu_{+}}}-\overline{{\nu_{-}}}+\eta_{\mathrm{e}}+R_{0}i(t)
$$  

where the electrolyte overpotential  

<html><body><table><tr><td>Scaledvariables</td><td>Unit</td></tr><tr><td>r±=r²/R±</td><td>dimensionless</td></tr><tr><td>x=x*/L</td><td>dimensionless</td></tr><tr><td>C± = c*/C±,max</td><td>dimensionless</td></tr><tr><td>Ce = c*/Ce,0</td><td>dimensionless</td></tr><tr><td>Ne = N* /(Ce,oL)</td><td>1/s</td></tr><tr><td>j±= j*/(R±C±,max)</td><td>1/s</td></tr><tr><td>i0,± ± = i,±/(FR±C±,max)</td><td>1/s</td></tr></table></body></html>  

with  

Table 7: Scaling of the variables of the full model. The variables of the full models are denoted with an asterisk in superscript and the new variables without. Other variables are kept the same as in the full dimensional model.  

Difusion in the spherical solid particles in each of the electrodes.  

$$
\frac{\partial c_{\pm}}{\partial t}=\frac{1}{r^{2}}\frac{\partial}{\partial r}\left(\frac{r^{2}}{\tau_{\pm}^{\mathrm{d}}}\frac{\partial c_{\pm}}{\partial r}\right)\qquad0\leq r\leq1
$$  

and initial conditions  

Intercalation reaction at the particle surface.  

$$
j_{\pm}(x,t)=2i_{0,\pm}\sinh\left(\frac{F\eta_{\pm}}{2R_{\mathrm{g}}T}\right)
$$  

$$
\eta_{\mathrm{e}}(t)=\frac{2R_{\mathrm{g}}T(1-t^{+})}{F}\overline{{\log\left(\frac{c_{\mathrm{e,+}}}{c_{\mathrm{e,-}}}\right)}}.
$$  

$$
\left.\frac{\partial c_{\pm}}{\partial r}\right|_{r=0}=0,\qquad\left.-\frac{1}{\tau_{\pm}^{\mathrm{d}}}\frac{\partial c_{\pm}}{\partial r}\right|_{r=1}=\overline{{j_{\pm}}},
$$  

# Appendix C: SPMe with grouped parameters  

with boundary conditions  

We now write the dimensional SPMe of Appendix B with grouped parameters. We do this by scaling some of the variables with parameters as per Table 7. We decide only to retain the dimensions of time, current, and voltage. The SPMe can be reformulated as follows with the grouped parameters listed in Table 2.  

$$
c_{\pm}(r,0)=c_{\pm}^{0\%}+\frac{\mathrm{SOC}_{0}}{100}\left(c_{\pm}^{100\%}-c_{\pm}^{0\%}\right).
$$  

$$
\begin{array}{r l r}&{}&{i_{0,\pm}=\frac{1}{\tau_{\pm}^{\mathrm{ct}}}\,\sqrt{c_{\pm}|_{r=1}}\,\sqrt{c_{\mathrm{e,\pm}}(1-c_{\pm}|_{r=1})},\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad}\\ &{}&{\eta_{\pm}(x,t)=\nu_{\pm}-U_{\pm}(c_{\pm}|_{r=1}),\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad(\mathrm{C.'}}\\ &{}&{\nu_{\pm}(x,t)=\overline{{\nu_{\pm}}}+\frac{2R_{\mathrm{g}}T}{F}(1-t^{+})\left(\overline{{\log(c_{\mathrm{e,\pm}})}}-\log(c_{\mathrm{e,\pm}})\right).}\end{array}
$$  

Transfer process at the particle surface with doublelayer.  

$$
C_{\pm}\frac{\mathrm{d}\overline{{\nu_{\pm}}}}{\mathrm{d}t}=\pm i(t)-3Q_{\pm}^{\mathrm{th}}\overline{{j_{\pm}}}
$$  

with initial condition $\overline{{\nu_{\pm}}}(0)=U_{\pm}(c_{\pm,0})$ .  

Difusion in the electrolyte.  

$$
\begin{array}{r l}&{\zeta(x)\displaystyle\frac{\partial c_{\mathrm{e}}}{\partial t}=-\left.\frac{\partial N_{\mathrm{e}}}{\partial x}\right.}\\ &{\qquad\qquad+\left.\frac{3}{Q^{\mathrm{e}}}\left\{\begin{array}{l l}{\displaystyle\frac{Q_{\mathrm{-}}^{\mathrm{th}}j_{\mathrm{-}}}{\ell_{\mathrm{-}}}}&{\mathrm{~for~}0<x<\ell_{\mathrm{-}}}\\ {\displaystyle\frac{0}{Q_{\mathrm{+}}^{\mathrm{th}}j_{\mathrm{+}}}}&{\mathrm{~for~}\ell_{\mathrm{-}}<x<1-\ell_{\mathrm{+}}}\\ {\displaystyle\frac{Q_{\mathrm{+}}^{\mathrm{th}}j_{\mathrm{+}}}{\ell_{\mathrm{+}}}}&{\mathrm{~for~}1-\ell_{\mathrm{+}}<x<1}\end{array}\right.}\end{array}
$$  

where $Q_{\pm}^{\mathrm{th}}$ are given by (11) and the electrolyte fux  

$$
\begin{array}{r l}{\displaystyle N_{\mathrm{e}}=-\,\frac{1}{\tau_{\mathrm{e}}(x)}\frac{\partial c_{\mathrm{e}}}{\partial x}}&{}\\ {\displaystyle-\,\frac{t^{+}i(t)}{Q^{\mathrm{e}}}\left\{\begin{array}{l l}{\displaystyle\frac{x}{\ell_{-}}}&{\mathrm{~for~}0<x<\ell_{-}}\\ {1}&{\mathrm{~for~}\ell_{-}<x<1-\ell_{+}}\\ {\displaystyle\frac{1-x}{\ell_{+}}}&{\mathrm{~for~}1-\ell_{+}<x<1}\end{array}\right.}\end{array}
$$  

with  

$$
\begin{array}{r}{\zeta(x)=\left\{\begin{array}{l l}{\zeta_{-}}&{\mathrm{~for~}0<x<\ell_{-}}\\ {1}&{\mathrm{~for~}\ell_{-}<x<1-\ell_{+}}\\ {\zeta_{+}}&{\mathrm{~for~}1-\ell_{+}<x<1,}\end{array}\right.}\\ {\tau_{\mathrm{e}}(x)=\left\{\begin{array}{l l}{\tau_{-}^{\mathrm{e}}}&{\mathrm{~for~}0<x<\ell_{-}}\\ {\tau_{\mathrm{sep}}^{\mathrm{e}}}&{\mathrm{~for~}\ell_{-}<x<1-\ell_{+}}\\ {\tau_{+}^{\mathrm{e}}}&{\mathrm{~for~}1-\ell_{+}<x<1,}\end{array}\right.}\end{array}
$$  

boundary conditions  

$$
\frac{\partial c_{\mathrm{e}}}{\partial x}\bigg|_{x=0}=0,\qquad\left.\frac{\partial c_{\mathrm{e}}}{\partial x}\right|_{x=1}=0,
$$  

and initial condition $c_{\mathrm{e}}(x,0)=1$ .  

Terminal voltage.  

$$
\nu(t)=\overline{{\nu_{+}}}-\overline{{\nu_{-}}}+\eta_{\mathrm{e}}+R_{0}i(t)
$$  

where the electrolyte overpotential  

$$
\eta_{\mathrm{e}}(t)=\frac{2R_{\mathrm{g}}T}{F}(1-t^{+})\overline{{\log\left(\frac{c_{\mathrm{e,+}}}{c_{\mathrm{e,-}}}\right)}}.
$$  

# Appendix D: Charge transfer resistance  

The charge transfer resistance at the operating point $x_{m}$ is the derivative of the voltage contribution from the spatially averaged overpotential $\overline{{\eta_{\pm}}}$ , with respect to the current, evaluated at the operating point $x_{m}$ ,  

$$
R_{\mathrm{ct},m,\pm}=\pm\frac{\mathrm{d}\overline{{\eta_{\pm}}}}{\mathrm{d}i}\bigg|_{x_{m}}.
$$  

In general, the average overpotential does not correspond to the average molar fux $\overline{{j_{\pm}}}$ but, from (C.4) and (C.7),  

$$
j_{\pm}=2i_{0,\pm}\sinh\left(\frac{F\overline{{\eta_{\pm}}}}{2R_{\mathrm{g}}T}+(1-t^{+})\left(\overline{{\log(c_{\mathrm{e,\pm}})}}-\log(c_{\mathrm{e,\pm}})\right)\right).
$$  

For small currents, we linearise as  

$$
j_{\pm}\approx2i_{0,\pm}\bigg(\frac{F\overline{{\eta_{\pm}}}}{2R_{\mathrm{g}}T}+(1-t^{+})\left(\overline{{\log(c_{\mathrm{e,\pm}})}}-\log(c_{\mathrm{e,\pm}})\right)\bigg).
$$  

In practice, we fnd that the contribution from the spatial variation of the electrolyte stoichiometry is much smaller than the overpotential, therefore,  

$$
\overline{{j_{\pm}}}\approx2\overline{{i_{0,\pm}}}\bigg(\frac{F\overline{{\eta_{\pm}}}}{2R_{\mathrm{g}}T}\bigg)=\frac{F\overline{{\eta_{\pm}}}}{R_{\mathrm{g}}T}\overline{{i_{0,\pm}}}.
$$  

Noting that $x_{m}$ is a state at which $i=0$ ,  

$$
R_{\mathrm{ct},m,\pm}\approx\pm\frac{R_{\mathrm{g}}T}{F\overline{{i_{0,\pm}}}}\frac{\mathrm{d}\overline{{j_{\pm}}}}{\mathrm{d}i}\bigg|_{x_{m}}.
$$  

From (C.8) (neglecting the double-layer capacitance) this yields the conventional result that  

$$
R_{\mathrm{ct},m,\pm}\approx\frac{R_{\mathrm{ct},\pm}^{\mathrm{typ}}}{2\,\sqrt{c_{m,\pm}(1-c_{m,\pm})}}\frac{1}{\sqrt{c_{\mathrm{e},\pm}}\big|_{x_{m}}}.
$$  

# Acknowledgements  

This research was supported by the Faraday Institution Nextrode (FIRG066) and Multiscale Modelling (MSM) (FIRG059) projects, as well as the EU IntelLiGent (101069765) project through the UKRI Horizon Europe Guarantee (10038031). OCP data of the LG M50LT cell was provided by About:Energy Ltd (London, UK, https://www.aboutenergy.io/). For the purpose of Open Access, the authors have applied a CC BY public copyright licence to any Author Accepted Manuscript (AAM) version arising from this submission.  

# Data and code availability  

# PyBAMM-EIS:  

https://github.com/pybamm-team/pybamm-eis  

PyBOP: https://github.com/pybop-team/PyBOP  

# Competing Interests  

D.A.H. is co-founder of Brill Power Ltd. The other authors have no competing interests to declare.  

![](images/8df586811f3ace60ad03c5e8a80ca081ca82ea4788ad2fab0041bf8d9a2056f9.jpg)  
Figure 11: Sensitivity of the SPMe impedance to particle difusion timescales $\tau_{\pm}^{\mathrm{d}}$ . The impedance is insensitive to $\bar{\tau_{\pm}^{\mathrm{d}}}$ at SOC where the OCP $U_{\pm}$ is fat. The OCP of graphite has several plateaus (see Fig. 9), which explains why $\tau_{-}^{\mathrm{d}}$ is not identifable at certain SOC. Parameters are perturbed in the range [0.5θ, 2θ] (blue to red) with $\theta$ the Chen2020 parameters with contact resistance of $10\;\mathrm{m}\Omega$ (black). Frequency range: $[200\,\mu\mathrm{Hz}$ , $1\ \mathrm{kHz}]$ .  

![](images/23ff5f1017700bdc37b8312fdebcc5cb17cf8b5e964299ce7112e2ad0b986bd8.jpg)  
Figure 12: Fits of simulated SPMe impedance data and relative error. The estimated parameters are listed in Table 3.  

# References  

[1] G. L. Plett, Battery management systems, Volume II: Equivalent-circuit methods, Artech House, 2015.   
[2] X. Hu, S. Li, H. Peng, A comparative study of equivalent circuit models for Li-ion batteries, Journal of Power Sources 198 (2012) 359–367.   
[3] M. Lagnoni, C. Scarpelli, G. Lutzemberger, A. Bertei, Critical comparison of equivalent circuit and physics-based models for lithium-ion batteries: A graphite/lithium-iron-phosphate case study, Journal of Energy Storage 94 (2024) 112326.   
[4] G. L. Plett, M. S. Trimboli, Battery management systems, Volume III: Physics-Based Methods, Artech House, 2023.   
[5] A. Tian, K. Dong, X.-G. Yang, Y. Wang, L. He, Y. Gao, J. Jiang, Physics-based parameter identifcation of an electrochemical model for lithium-ion batteries with two-population optimization method, Applied Energy 378 (2025) 124748.   
[6] M. Doyle, T. F. Fuller, J. Newman, Modeling of galvanostatic charge and discharge of the lithium/polymer/insertion cell, Journal of the Electrochemical society 140 (6) (1993) 1526.   
[7] M. Doyle, J. Newman, A. S. Gozdz, C. N. Schmutz, J.-M. Tarascon, Comparison of modeling predictions with experimental data from plastic lithium ion cells, Journal of the Electrochemical Society 143 (6) (1996) 1890. doi:10.1149/1.1836921.   
[8] M. Guo, G. Sikha, R. E. White, Single-particle model for a lithium-ion cell: Thermal behavior, Journal of The Electrochemical Society 158 (2) (2010) A122.   
[9] S. J. Moura, F. B. Argomedo, R. Klein, A. Mirtabatabaei, M. Krstic, Battery state estimation for a single particle model with electrolyte dynamics, IEEE Transactions on Control Systems Technology 25 (2) (2016) 453–468.   
[10] S. G. Marquis, V. Sulzer, R. Timms, C. P. Please, S. J. Chapman, An asymptotic derivation of a single particle model with electrolyte, Journal of The Electrochemical Society 166 (15) (2019) A3693.   
[11] F. Brosa Planella, M. Sheikh, W. D. Widanage, Systematic derivation and validation of a reduced thermal-electrochemical model for lithium-ion batteries using asymptotic methods, Electrochimica Acta 388 (2021) 138524.   
[12] T. L. Kirk, J. Evans, C. P. Please, S. J. Chapman, Modeling electrode heterogeneity in lithium-ion batteries: Unimodal and bimodal particle-size distributions, SIAM Journal on Applied Mathematics 82 (2) (2022) 625–653.   
[13] D. Lu, M. S. Trimboli, G. Fan, R. Zhang, G. L. Plett, Nondestructive pulse testing to estimate a subset of physics-basedmodel parameter values for lithium-ion cells, Journal of The Electrochemical Society 168 (8) (2021) 080533.   
[14] P. Iurilli, C. Brivio, V. Wood, On the use of electrochemical impedance spectroscopy to characterize and model the aging phenomena of lithium-ion batteries: A critical review, Journal of Power Sources 505 (2021) 229860.   
[15] W. Hileman, M. S. Trimboli, G. Plett, Estimating the values of the pde model parameters of rechargeable lithium-metal battery cells using linear EIS, ASME Letters in Dynamic Systems and Control (2024) 1–7.   
[16] X. Zhu, M. Cazorla Soult, B. Wouters, M. H. Mamme, Study of solid-state difusion impedance in li-ion batteries using paralleldifusion Warburg model, Journal of The Electrochemical Society (2024).   
[17] B. Wimarshana, I. Bin-Mat-Arishad, A. Fly, A multi-step parameter identifcation of a physico-chemical lithium-ion battery model with electrochemical impedance data, Journal of Power Sources 580 (2023) 233400.   
[18] M. E. Orazem, B. Tribollet, Electrochemical Impedance Spectroscopy, Wiley, 2008.   
[19] S. Wang, J. Zhang, O. Gharbi, V. Vivier, M. Gao, M. E. Orazem, Electrochemical impedance spectroscopy, Nature Reviews Methods Primers 1 (1) (2021) 41.   
[20] V. Vivier, M. E. Orazem, Impedance analysis of electrochemical systems, Chemical Reviews 122 (12) (2022) 11131–11168.   
[21] D. Lu, M. S. Trimboli, G. Fan, Y. Wang, G. L. Plett, Nondestructive EIS testing to estimate a subset of physics-based-model parameter values for lithium-ion cells, Journal of The Electrochemical Society 169 (8) (2022) 080504.   
[22] M. D. Murbach, V. W. Hu, D. T. Schwartz, Nonlinear electrochemical impedance spectroscopy of lithium-ion batteries: experimental approach, analysis, and initial fndings, Journal of The Electrochemical Society 165 (11) (2018) A2758.   
[23] T. L. Kirk, A. Lewis-Douglas, D. Howey, C. P. Please, S. J. Chapman, Nonlinear electrochemical impedance spectroscopy for lithium-ion battery model parameterization, Journal of The Electrochemical Society 170 (1) (2023) 010514.   
[24] Y. Ji, D. T. Schwartz, Second-harmonic nonlinear electrochemical impedance spectroscopy: Part II. model-based analysis of lithium-ion battery experiments, Journal of The Electrochemical Society 171 (2) (2024) 023504.   
[25] A. Lasia, Impedance of porous electrodes, Journal of Electroanalytical Chemistry 397 (1-2) (1995) 27–33.   
[26] J. P. Meyers, M. Doyle, R. M. Darling, J. Newman, The impedance response of a porous electrode composed of intercalation particles, Journal of the Electrochemical Society 147 (8) (2000) 2930.   
[27] P. Albertus, J. Newman, Introduction to dualfoil 5.0, University of California Berkeley, Berkeley, CA, Tech. Rep (2007).   
[28] J. Song, M. Z. Bazant, Efects of nanoparticle geometry and size distribution on difusion impedance of battery electrodes, Journal of The Electrochemical Society 160 (1) (2012) A15.   
[29] A. M. Bizeray, J.-H. Kim, S. R. Duncan, D. A. Howey, Identifability and parameter estimation of the single particle lithium-ion battery model, IEEE Transactions on Control Systems Technology 27 (5) (2018) 1862–1877.   
[30] H. Zhu, T. A. Evans, P. J. Weddle, A. M. Colclasure, B.-R. Chen, T. R. Tanim, T. L. Vincent, R. J. Kee, Extracting and interpreting electrochemical impedance spectra (EIS) from physicsbased models of lithium-ion batteries, Journal of the Electrochemical Society 171 (5) (2024) 050512.   
[31] V. Sulzer, S. G. Marquis, R. Timms, M. Robinson, S. J. Chapman, Python battery mathematical modelling (PyBaMM), Journal of Open Research Software 9 (1) (2021).   
[32] M. Zˇ ic, V. Suboti´c, S. Pereverzyev, I. Fajfar, Solving CNLS problems using Levenberg-Marquardt algorithm: A new ftting strategy combining limits and a symbolic Jacobian matrix, Journal of Electroanalytical Chemistry 866 (2020) 114171.   
[33] B. Planden, N. E. Courtier, M. Robinson, A. Khetarpal, F. B. Planella, D. A. Howey, PyBOP: A Python package for battery model optimisation and parameterisation, arXiv preprint arXiv:2412.15859 (2024).   
[34] A. Aitio, S. G. Marquis, P. Ascencio, D. Howey, Bayesian parameter estimation applied to the Li-ion battery single particle model with electrolyte dynamics, IFAC-PapersOnLine 53 (2) (2020) 12497–12504.   
[35] W. Hu, Y. Peng, Y. Wei, Y. Yang, Application of electrochemical impedance spectroscopy to degradation and aging research of lithium-ion batteries, The Journal of Physical Chemistry C 127 (9) (2023) 4465–4495.   
[36] N. Hallemans, D. Howey, A. Battistel, N. F. Saniee, F. Scarpioni, B. Wouters, F. La Mantia, A. Hubin, W. D. Widanage, J. Lataire, Electrochemical impedance spectroscopy beyond linearity and stationarity—A critical review, Electrochimica Acta (2023) 142939.   
[37] M. A. Zabara, J. Goh, V. Gaudio, L. Zou, M. Orazem, B. Ulgut, Utility of Lissajous plots for electrochemical impedance spectroscopy measurements: detection of non-linearity and nonstationarity, Journal of The Electrochemical Society 171 (1) (2024) 010507.   
[38] M. Urquidi-Macdonald, S. Real, D. D. Macdonald, Applications of Kramers—Kronig transforms in the analysis of electrochemical impedance data—iii. stability and linearity, Electrochimica Acta 35 (10) (1990) 1559–1566.   
[39] P. Agarwal, M. E. Orazem, L. H. Garcia-Rubio, Application of measurement models to impedance spectroscopy: III. Evaluation of consistency with the Kramers-Kronig relations, Journal of the Electrochemical Society 142 (12) (1995) 4159.   
[40] M. E. Orazem, Measurement model for analysis of electrochemical impedance data, Journal of Solid State Electrochemistry 28 (3) (2024) 1273–1289.   
[41] N. Hallemans, W. D. Widanage, X. Zhu, S. Moharana, M. Rashid, A. Hubin, J. Lataire, Operando electrochemical impedance spectroscopy and its application to commercial Liion batteries, Journal of Power Sources 547 (2022) 232005.   
[42] R. J. LeVeque, et al., Finite volume methods for hyperbolic problems, Vol. 31, Cambridge University Press, 2002.   
[43] C.-H. Chen, F. Brosa Planella, K. O’regan, D. Gastol, W. D. Widanage, E. Kendrick, Development of experimental techniques for parameterization of multi-scale lithium-ion battery models, Journal of The Electrochemical Society 167 (8) (2020) 080534.   
[44] F. Vandeputte, N. Hallemans, J. A. Kuzhiyil, N. F. Saniee, W. D. Widanage, J. Lataire, Frequency domain parametric estimation of fractional order impedance models for Li-ion batteries, IFACPapersOnLine 56 (2) (2023) 4325–4330.   
[45] M. E. Orazem, B. Ulgut, On the proper use of a Warburg impedance, Journal of The Electrochemical Society 171 (4) (2024) 040526.   
[46] F. Vandeputte, N. Hallemans, J. Lataire, Parametric estimation of arbitrary fractional order models for battery impedances, IFAC-PapersOnLine 58 (15) (2024) 97–102.   
[47] G. L. Plett, M. S. Trimboli, Process for lumping parameters to enable nondestructive parameter estimation for lithium-ion physics-based models, Proceedings of the 35th International Electric Vehicle Symposium and Exhibition (EVS35), Oslo, Norway (2022).   
[48] Z. Khalik, M. Donkers, J. Sturm, H. J. Bergveld, Parameter estimation of the Doyle–Fuller–Newman model for lithium-ion batteries by parameter normalization, grouping, and sensitivity analysis, Journal of Power Sources 499 (2021) 229901.   
[49] J. J. Rissanen, Fisher information and stochastic complexity, IEEE transactions on information theory 42 (1) (1996) 40–47.   
[50] H. Mendoza, S. A. Roberts, V. E. Brunini, A. M. Grillet, Mechanical and electrochemical response of a LiCoO2 cathode using reconstructed microstructures, Electrochimica Acta 190 (2016) 1–15.   
[51] J. S. Horner, G. Whang, D. S. Ashby, I. V. Kolesnichenko, T. N. Lambert, B. S. Dunn, A. A. Talin, S. A. Roberts, Electrochemical modeling of GITT measurements for improved solid-state difusion coefcient evaluation, ACS Applied Energy Materials 4 (10) (2021) 11460–11469.   
[52] X. Zhu, N. Hallemans, B. Wouters, R. Claessens, J. Lataire, A. Hubin, Operando odd random phase electrochemical impedance spectroscopy as a promising tool for monitoring lithium-ion batteries during fast charging, Journal of Power Sources 544 (2022) 231852.   
[53] H. A. van der Vorst, Bi-CGSTAB: A fast and smoothly converging variant of Bi-CG for the solution of nonsymmetric linear systems, SIAM Journal on Scientifc and Statistical Computing 13 (2) (1992) 631–644.   
[54] S. G. Marquis, Long-term degradation of lithium-ion batteries, Ph.D. thesis, University of Oxford (2020).  