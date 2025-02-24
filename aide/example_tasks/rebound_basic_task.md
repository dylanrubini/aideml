## Goal
Analyze carefully the content of this research article.
I want you to provide me a complete python script in which the astrophysical N-body integration package Rebound is used to reproduce the corresponding simulation results displayed in Figure 1. Make sure you reason step by step in collecting all simulations details and parameters before writing the python script. Reproduce the figure as faithfully as possible.

## Evaluation

todo

## Detailed Description of Figure to be Reproduced

Figure 1 Description:

Figure 1 is composed of two primary sections—a left panel and a right panel—each conveying different aspects of the simulation results from an N-body simulation of a binary merger with an accompanying circumbinary debris disc.
	1.	Left Panel: Time Evolution of Binary Orbital Parameters
	•	Upper Left Sub-panel:
This sub-panel plots the evolution of two key orbital parameters of the binary system over time:
	•	Semimajor Axis (ab): Displayed as a blue line, this curve shows how the binary’s semimajor axis decreases over time due to tidal interactions and orbital decay, leading to a merger.
	•	Eccentricity (eb): Represented by an orange (or yellow) line, this curve tracks the change in eccentricity of the binary’s orbit. The evolution of eb provides insights into how the orbit circularizes as the merger progresses.
In addition, four distinct colored points (each with a different color) are marked on this sub-panel. These points represent snapshot times during the simulation and serve as reference markers for correlating the binary’s orbital state with the disc structure shown in the right panel.
	•	Lower Left Sub-panel:
This sub-panel shows the time evolution of the binary’s argument of periapsis (ωb). The plot illustrates how ωb changes over time, reflecting the precession of the binary orbit. The evolution of ωb is critical as it is linked to the dynamics that drive the binary toward merger.
	2.	Right Panel: Disc Inclination Profile vs. Semimajor Axis
	•	The right panel focuses on the circumbinary debris disc surrounding the binary system.
	•	Horizontal Axis:
This axis represents the orbital semimajor axis of the test particles (or disc elements), normalized to the initial semimajor axis of the binary (ab,0). It shows the radial extent of the disc.
	•	Vertical Axis:
The vertical axis indicates the inclination (i) of the disc particles relative to the binary’s orbital plane. Initially, the disc is polar with inclinations near 90°.
	•	Colored Snapshots:
Four different colors are used in the right panel. Each color corresponds to one of the snapshot times indicated by the colored points in the upper left panel. These snapshots capture how the disc’s inclination profile changes over time. For example, the inner disc regions may exhibit greater variations in inclination due to stronger dynamical interactions with the evolving binary, while the outer regions remain closer to polar.

Overall Interpretation:

Figure 1, as a whole, offers a comprehensive view of the binary merger process and its impact on the circumbinary disc:
	•	The left panel details how the binary’s orbital elements (semimajor axis, eccentricity, and argument of periapsis) evolve during the merger.
	•	The right panel illustrates how these changes influence the disc’s inclination distribution over a range of orbital radii, with time-correlated snapshots that allow one to connect the binary’s evolution with the disc’s dynamical response.

This detailed description provides the necessary context and structure for an LLM to write code that could, for example, generate a multi-panel plot using Python libraries like Matplotlib. The code would need to simulate or plot the time evolution curves on the left and the radial inclination distribution on the right, using distinct colors for the different time snapshots.

## Article (converted from PDF to markdown)

# On the origin of polar planets around single stars  

Cheng Chen , 1 ‹ Stanley A. Baronett , 2,  3 C. J. Nixon 1 and Rebecca G. Martin 2,  3 1 School of Physics and Astronomy, University of Leeds, Sir William Henry Bra g g Building,  Leeds LS2 9JT, UK 2 Department of Physics and Astronomy, University of Nevada, Las Vegas, 4505 South Maryland Parkway, Las Vegas, NV 89154, USA 3 Nevada Center for Astrophysics, University of Nevada, Las Vegas, 4505 South Maryland Parkway, Las Vegas, NV 89154, USA  

Accepted 2024 June 23. Received 2024 June 22; in original form 2024 March 3  

# A B S T R A C T  

The Rossiter–McLaughlin effect measures the misalignment between a planet’s orbital plane and its host star’s rotation plane. Around 10 per cent of planets exhibit misalignments in the approximate range $80^{\circ}{-}125^{\circ}$ , with their origin remaining a mystery. On the other hand, large misalignments may be common in eccentric circumbinary systems due to misaligned discs undergoing polar alignment. If the binary subsequently merges, a polar circumbinary disc – along with any planets that form within it – may remain inclined near $90^{\circ}$ to the merged star’s rotation. To test this hypothesis, we present $N$ -body simulations of the evolution of a polar circumbinary debris disc comprised of test particles around an eccentric binary during a binary merger that is induced by tidal dissipation. After the merger, the disc particles remain on near-polar orbits. Interaction of the binary with the polar-aligned gas disc may be required to bring the binary to the small separations that trigger the merger by tides. Our findings imply that planets forming in discs that are polar-aligned to the orbit of a high-eccentricity binary may, following the merger of the binary, provide a possible origin for the population of near-polar planets around single stars.  

nalytical – methods: numerical – celestial mechanics – planetary system  

# 1  INTRODUCTION  

Standard theories of planet formation suggest that planets orbit in the same plane as the rotational plane of the central star because planets are typically expected to form in a planar disc (e.g. the eight planets in the Solar system). Ho we ver, recent analyses of the online data base TEPCaT (Southworth et al. 2011)  and K2-290 (Hjorth et al. 2021)  hav e rev ealed misaligned planets with 3D obliquity $\psi$ (see F abryck y & Winn 2009,  for more details on geometry) that are between $\psi=80^{\circ}-125^{\circ}$ around single stars in 17 out of 156 systems via the Rossiter–McLaughlin effect during a planet transit (Albrecht et al. 2021) . Recently, there are more plausible planets with nearly polar orbits have been found including GJ 3470b, TOI-858Bb, and WASP-178b (Stef \`ansson et al. 2022;  Hagelberg et al. 2023;  Pagano et al. 2024) .  

Several mechanisms have been proposed to try to explain misaligned planets around single stars. These mechanisms are summarized in the discussion provided by Albrecht et al. ( 2021) . They include (1) the von Zeipel–Kozai–Lidov mechanism (von Zeipel 1910;  Kozai 1962;  Lidov 1962)  triggered by an external, massive perturber, which can excite oscillations between the planet’s inclination and eccentricity if the external perturber has an inclination abo v e the critical inclination of $\approx39^{\circ}$ , (2) for high-mass, short-period (hot Jupiter) planets, tidal dissipation can (in some models) result in the obliquity of the planet being near $90^{\circ}$ for a period of time (Lai, Foucart & Lin 2011;  Rogers & Lin 2013;  Anderson, Winn & Penev 2021) , (3) a secular resonance may occur during the late  

# ⋆ E-mail: Email: c.chen6@leeds.ac.uk  

stage of planet formation as the gas disc disperses which can excite the inclination of an inner planet due to the presence of an outer misaligned massive planet (Petrovich et al. 2020) , and (4) magnetic warping (e.g. Foucart & Lai 2011;  Lai et al. 2011;  Romanova et al. 2021)  could potentially tilt a young protoplanetary disc into an inclined orbit and it is possible for a planet to end up orbiting within such a region of the disc. Ho we ver, Albrecht et al. ( 2021)  note that there are difficulties for each mechanism in explaining the properties of the observed systems in their sample. An additional possibility is that the disc forms warped due to chaotic infall of gas from the parent star-forming region (e.g. Bate, Lodato & Pringle 2010) , and the disc may remain warped for much of its lifetime (e.g. Nixon & Pringle 2010;  and much longer than the early time-scales on which planets are expected to form; Manara, Morbidelli & Guillot 2018; Nixon, King & Pringle 2018;  Tychoniec et al. 2020) . It is plausible that some, or all, of these mechanisms operate in different systems to produce the observed distribution of misaligned planets.  

Here, we explore an alternative formation pathway for nearperpendicular planets to form around single stars. Star formation typically proceeds in a chaotic fashion with the resulting stellar systems comprised of multiple stars that can evolve due to capture and exchange encounters (e.g. Bate 2018) . The discs of gas that form in and around these stellar systems can arrive with uncorrelated angular momentum direction compared to the stellar system they form in (e.g. Bate et al. 2010) . Analytical and numerical work has shown that gas discs which are sufficiently misaligned to an eccentric binary precess pre-dominantly around the binary eccentricity vector, leading to ‘polar alignment’, in which the gas disc rotates around the binary eccentricity vector and therefore orthogonal to the binary angular momentum vector (Aly et al. 2015;  Martin & Lubow 2017) .  

This process is thought to have created the polar aligned gas discs found in $\mathrm{HD}\,98\,800$ (K ennedy et al. 2019) , V773 Tau B (K enworthy et al. 2022) , and the polar aligned debris disc around the binary 99 Herculis (Kennedy et al. 2012;  Small w ood et al. 2020;  which presumably arrived in its current orbital configuration before the gas disc dissipated). See also Ceppi et al. ( 2023,  2024)  and Lepp, Martin & Lubow ( 2023a)  for recent works on this topic.  

There is growing observational evidence for significant misalignments between the binary orbital plane and the disc plane in young stellar systems (e.g. Czekala et al. 2019) . Binaries with short periods (less than around $30\;\mathrm{d}$ ) are more likely to show aligned discs, while those with longer periods show a broad inclination distribution. This is likely to arise due to a combination of effects, including that the alignment time-scale of the disc–binary system grows significantly with increasing binary period and that large misalignments can result in rapid shrinking of the binary orbit (e.g. Nixon et al. 2011;  Nixon, King & Price 2013)  which in short period systems (and particularly those with high eccentricity) could result in the merger of the binary.  

It therefore seems possible that, in some systems, the binary eccentricity is high enough that the disc polar aligns to the binary orbit and the binary subsequently merges due to a combination of disc–binary interaction and tidal dissipation. Thus, in this letter, we propose that highly misaligned planets around single stars may attain their orbits while the stellar system is actually a binary (or multiple) star system. Once the central binary merges, the polar planets are left orbiting close to the polar plane, and the final spin of the merged star is essentially in the plane of the original binary orbit (with only a small offset introduced by the initial spins of each star, which need not be aligned to the original binary orbit).  

To test this hypothesis, we present $N$ -body simulations of an eccentric binary with a distribution of near-polar planets/planetesimals and follow the orbital evolution of the binary due to the tides the stars induce on each other. We follow the simulation beyond the point at which the stars merge to attain the final configuration of the planets. In Section 2,  we describe the set-up of the simulation and present our results. Finally, in Sections 3 and 4,  we present our discussion and conclusions, respectively.  

# 2  SIMULATION  SET-UP  AND  RESULTS  

We present numerical simulations performed with the publicly available $N$ -body simulation code, REBOUND.  Two common options for the choice of numerical integrator used by REBOUND are the WHFAST integrator which is a 2nd-order, fixed time-step symplectic Wisdom–Holman integrator with 11th-order symplectic correctors (Rein & Tamayo 2015)  and IAS15 which is a 15th-order Gauss– Radau integrator with variable time-steps (Rein & Spiegel 2015) . For these simulations we have tested both methods and find that they produce very similar results. As such we present results using the IAS15 integrator.  

We solve the gravitational equations in the frame of the centre of mass of the binary. We also include the REBOUNDX package, an extended library for incorporating additional physics into REBOUND, and we use the constant time lag model for tides between the binary (see Baronett et al. 2022,  for more details). We note that the dynamics of a gas disc are similar to the particle dynamics except that there is communication between different radii in the gas disc through pressure and viscosity (e.g. Nixon & King 2016) .  

The central binary has components of mass $m_{1}$ and $m_{2}$ with a total mass of $m_{\mathrm{b}}=m_{1}+m_{2}$ and a mass ratio of $q_{\mathrm{b}}=m_{2}/m_{1}$ .  The binary orbit has semimajor axis $a_{\mathrm{b}}$ and eccentricity $e_{\mathrm{b}}$ .  We initially consider an equal mass binary with $q_{\mathrm{b}}=1.0$ with initial eccentricity of $e_{\mathrm{b}}=0.8$ and the initial argument of periapsis is $\omega_{\mathrm{b}}=0.0$ . We also present results with different binary parameters in Section 3.  

A key parameter is the physical radius of the stars, $R_{*}$ , because the tidal perturbing force is proportional to $R_{*}^{5}$ (see equation 8 in Hut 1981) . We consider two solar-type main-sequence stars with masses $\mathbf{M}_{\odot}$ and radii $\mathbf{R}_{\odot}$ . The initial binary orbital period $T_{\mathrm{b}}$ must be long enough that the circumbinary gas disc has sufficient time to align to polar before the binary merges. Observations of mainsequence binaries show moderate binary eccentricities for orbital periods $T_{\mathrm{b}}\gtrsim30\,\mathrm{d}$ and a wide range of $e_{\mathrm{b}}$ for $T_{\mathrm{b}}\gtrsim100\,\mathrm{d}$ (see fig. 14 in Raghavan et al. 2010) . This implies that the merger time-scales of moderately eccentric binaries with $T_{\mathrm{b}}\gtrsim30\,\mathrm{d}$ are longer than the stellar lifetime and the merger will not occur for main-sequence binaries with $T_{\mathrm{b}}\gtrsim100\,\mathrm{d}$ . Thus, we take the initial semimajor axis of the binary to be $a_{\mathrm{b},0}=0.1$ au, with initial orbital period $T_{\mathrm{b}}=8.166\,\mathrm{d}$ , and thus, $R_{*}=1\,\mathrm{R}_{\odot}=0.05a_{\mathrm{b},0}$ .  The upper left panel of Fig. 1 shows the time evolution of the binary semimajor axis, $a_{\mathrm{b}}$ ,  (blue line) and the binary eccentricity, $e_{\mathrm{b}}$ ,  (orange line). Due to tidal evolution, both $a_{\mathrm{b}}$ and $e_{\mathrm{b}}$ decrease with time and the binary merges at around $t=1200\,T_{\mathrm{b}}$ .  The lower left panel shows the evolution of the argument of periapsis. The binary apsidal precession rate increases until the binary merges.  

To explore the response of circumbinary planets to the evolution of the binary orbit, we place a disc of 200 test particles on circular orbits around the binary distributed according to a uniform random distribution in the radial range of $3-20\,a_{\mathrm{b},0}$ ,  where $a_{\mathrm{b,0}}$ is the initial binary semimajor axis. The inclinations of these particles follow polar orbits $(i=90^{\circ})$ ), with deviations randomly distributed within $\pm1.0^{\circ}$ . To set the initial conditions of the test particle orbits we set the argument of periapsis $\omega_{\mathrm{p}}=0$ , the true anomaly $\nu_{\mathrm{p}}=0$ , and the longitude of the ascending nodes measured from the binary semimajor axis to $\phi_{\mathrm{p}}=90^{\circ}$ . In the absence of binary orbit evolution, the particles remain on stable polar obits according to three-body numerical simulations (Doolin & Blundell 2011;  Cuello & Giuppone 2019;  Chen, Lubow & Martin 2020;  Childs & Martin 2021;  Nikolaos et al. 2024)  and analytical calculations (e.g. Aly et al. 2015) .  

The upper left sub-panel on the right side of Fig. 1 shows the initial distribution of the inclination of the disc, $i$ , versus orbital radius scaled to the initial binary semimajor axis. The four dots in the top left panel of Fig. 1 mark the times at which the plots of inclination $i$ versus orbital radius $R$ are made (shown on the right-hand side of Fig. 1) . These times are $t=0$ (green), 750 (red), 1500 (purple), and 5000 (brown) $T_{\mathrm{b}}$ .  Initially, the disc is polar $(i=90^{\circ}$ ) at all orbital radii. After the binary merged around $t=1200\,T_{\mathrm{b}}$ $(\approx26.85\,\mathrm{yr})$ , the particle inclinations no longer vary with time. As the particles in our simulations are not subject to tides or frictional forces, the innermost edge of the particle disc remains at around $3.0\,a_{\mathrm{b},0}$ and does not shrink with the binary.1  

A polar aligned test particle around an eccentric binary is in a stationary orbit (meaning there is no nodal precession) with stationary inclination $i_{\mathrm{s}}=90^{\circ}$ . Particles that are slightly misaligned to this stationary inclination undergo nodal precession around this inclination. As a result of the prograde binary apsidal precession, the stationary polar alignment angle increases with the radius of the disc (c.f. Lepp, Martin & Childs 2022;  Childs et al. 2024) . When the stationary inclination becomes higher than the particle inclination, the particles can undergo nodal precession and the inclination of the particles can get excited.  

![](images/a45500567e8bf3b99430b132d019c21a8b1bf2695af27364e29d61b55bd6c020.jpg)  
Figure 1. Upper left panel:  the time evolution of $a_{\mathrm{b}}$ (blue line) and $e_{\mathrm{b}}$ (yellow line). Lower left panel:  the time evolution of $\omega_{\mathrm{b}}$ .  Right panel:  the disc inclination versus the semimajor axis at different times. The four different colours used on the right-hand side represent different times and correspond to the four coloured points in the upper left panel.  

We calculate the apsidal precession rate of the binary $\dot{\omega_{\mathrm{b}}}$ of the binary and employ a modified form of equation 10 in Lepp, Martin & Zhang ( 2023b) , which gives the stationary inclination, $i_{\mathrm{s}}$ ,  as  

$$
\cos(i_{\mathrm{s}})=-\dot{\omega_{\mathrm{b}}}\times\frac{4}{3\sqrt{G}}\frac{(m_{1}+m_{2})^{3/2}}{m_{1}m_{2}}\frac{R^{7/2}}{a_{\mathrm{b}}^{2}}\frac{1}{(1+e_{\mathrm{b}}^{2})},
$$  

where $G$ is the gravitational constant. The stationary inclination is shown by the blue dashed lines in Fig. 2.  The stationary inclination is initially $i_{\mathrm{s}}=90^{\circ}$ for all radii but it increases during the merger. Since the particles can nodally precess about this stationary inclination, the magnitude of the inclination oscillations should increase with radius. Ho we ver, the time-scale for these oscillations also increases with radius. This leads to the two different slopes in the inner and outer parts of the particle disc. The vertical green dashed lines show where the stationary inclination reaches $i_{\mathrm{s}}=180^{\circ}$ . For larger particle semimajor axis, the particle no longer nodally precesses about the stationary inclination and instead undergoes nodal circulation with little inclination excitation (see the lower right panel of fig. 2 in Lepp et al. 2022) .  

Scatter points in each panel of Fig. 2 represent snapshots of the disc inclination $i$ from $t\,=400–1100~T_{\mathrm{b}}$ with the interval of 100 $T_{\mathrm{b}}$ .  If $|\cos i_{\mathrm{s}}|>1$ in equation ( 1) , $i$ can not be excited via this oscillation. The dashed green line has mo v ed inward to $R=12a_{\mathrm{b},0}$ at $\mathfrak{t}=500\,t_{\mathrm{b}}$ and the time-scale for nodal precession in the outer disc is much longer than the merger time-scale, resulting in the outer disc remaining on nearly polar orbits to the end. On the other hand, the middle disc $(R\sim10a_{\mathrm{b}})$ ) stops the oscillation earlier than the inner disc while the middle disc has the longer precession time-scale than the inner disc. As the result, $i$ of the middle disc only increases a little bit to $i=92^{\circ}$ . At the late stage of the binary merging, only the innermost region of the disc still undergoes the oscillation, and the inner disc has a short precession time-scale facilitated by the excitation of $i$ . Consequently, the inner disc has a higher $i=100^{\circ}$ than the middle and outer disc, leaving a slope structure in two lower right panels of Fig. 1.  

# 3  DISCUSSION  

During the binary merger, the binary undergoes rapid apsidal precession as the stars get closer and closer, inducing the stationary inclination of the disc to increase with increasing semimajor axis. This effect is similar to results when general relativity (GR) within the binary is considered. Recently, Lepp et al. ( 2022)  used the REBOUNDX package extension to include GR effects (gr full package) and also found the stationary inclination of the test particle increases with increasing semimajor axis. Ho we ver, when we include the same package in our simulations, the results remain similar to those shown here because the precession time-scale of the binary induced by GR is much longer than that induced by tidal interactions for our parameters (see equation 3 in Lepp et al. 2022) . Therefore, we can ignore the effect of GR in our scenario, and this is consistent with the $N$ -body simulation results in Antonini & Perets ( 2012)  that tidal friction is the main mechanism to cause compact stellar binaries and $\Chi$ -ray binaries to merge.  

The implementation of tides between the stars in the REBOUNDX package that we use here employs the constant time lag approximation, which does not evolve the spins of any tidally interacting bodies (Baronett et al. 2022,  section 3.1). This implementation is suitable when the spins are expected to be either much greater than the orbital angular frequencies or only negligibly affected by any tidally mediated angular momentum exchange. As Lu et al. ( 2023)  have addressed these limitations in a subsequent, separate implementation of self-consistent spin, tidal, and dynamical equations of motion into REBOUNDX,  we may use their updated model in a future investigation to assess the impact of stellar spin on the evolution of binary and circumbinary disc (CBD) configurations.  

Another possible mechanism to facilitate the binary merger, particularly for wider binary separations, is the interaction of the binary with a circumbinary disc. The transfer of energy and angular momentum through orbital resonances can cause the orbit of the binary to shrink with time (e.g. Artymowicz & Lubow 1994) . Howe ver, the orbital e volution of binaries interacting with circumbinary discs is comple x, ev en in the prograde and planar case, and the results can vary depending on the disc and binary properties (e.g.  

![](images/bfc6636f36a3f0c1f078e42c6f2d44630ca542fcb3dad09bdf6fcf218f356488.jpg)  
Figure 2. Snapshots of particle inclination $i$ (blue dots) during the binary merger from $t=400-1100T_{\mathrm{b}}$ with interval of $100T_{\mathrm{b}}$ .  The blue dashed lines are the stationary inclination $i_{\mathrm{s}}$ (equation 1) . The green vertical dashed lines indicate where $i_{\mathrm{s}}=180^{\circ}$ . The excitation of $i$ only occurs within the green vertical dashed line.  

Artymo wicz & Lubo w 1994,  1996;  Miranda, Mu ˜n oz & Lai 2017; Tang, MacFadyen & Haiman 2017;  Moody, Shi & Stone 2019; Mu ˜n oz, Miranda & Lai 2019;  Heath & Nixon 2020;  Mu ˜n oz et al. 2020) . The main competing effects are the removal of energy and angular momentum by (outer Lindblad) resonances and the increase in binary energy and angular momentum due to accretion of material from the inner edge of the circumbinary disc (see the discussion in Heath & Nixon 2020) . In retrograde discs these two effects both result in the decay of the binary orbit (Nixon et al. 2011) .2  While there has not yet been a dedicated study of the orbital evolution of binaries interacting with polar aligned circumbinary discs it is generally found that the binary orbit decays (Aly et al. 2015;  Martin & Lubow 2019) .  

Mergers of stars are thought to play a role in explaining the statistics and properties of stars (e.g. Bally & Zinnecker 2005;  Wang et al. 2022) . In particular, observations of the stellar multiplicity of solar-type stars show that there is a distinct cut in the period– eccentricity relationship for the 127 binaries at an orbital period of 12 d (see fig. 14 in Raghavan et al. 2010) . Binaries with orbital period $\lesssim12\,\mathrm{d}$ are close to circular, while those with larger orbital 30 d period have a wide range of eccentricities. Additionally, statistical trends suggest that binaries which host polar discs have a mean eccentricity of $e_{\mathrm{b}}=0.65$ (Ceppi et al. 2024) .  

We can therefore expect that in some regions of parameter space a stellar binary can be brought to merger via interaction with a polar aligned gas disc. As the disc mass and lifetime are finite, this is potentially restricted to binaries with high eccentricity (which is conducive to the formation of polar aligned circumbinary discs) and short orbital periods. The results of, e.g. Raghavan et al. ( 2010) indicate that there is a lack of binaries with semimajor axes of order 0.1 au (or less) and eccentricities greater than 0.1. It is reasonable to expect that binaries that form in this region of parameter space may subsequently merge either through tidal effects, interaction with a polar aligned circumbinary disc or a combination of these effects.  

To examine the effects of varying the initial binary orbital parameters we consider two additional simulations. First, we rerun the same simulation as presented in Section 2 except with a lower initial binary eccentricity of $e_{\mathrm{b}}=0.2$ . The upper left panel of Fig. 3 shows that the binary merges at a time of around $5.9\!\times\!10^{6}\;T_{\mathrm{b}}$ $(\approx130\,000\,\mathrm{yr})$ . Secondly, we rerun the same simulation as in Section 2,  except with a larger initial semimajor axis of $a_{\mathrm{b},0}=0.2$ au (with initial orbital period of $T_{\mathrm{b}}=32.25\,\mathrm{d},$ . The upper right panel of Fig. 3 shows that in this case the binary merges at a time of around 125 000  

![](images/9925945bac15784da0b190929571a15ac76b433f8b6c3dab50d38b6f05ffb718.jpg)  
Figure 3. Left panels:  The same simulation as Fig. 1 except the binary eccentricity is $e_{\mathrm{b}}=0.2$ and the integration time is longer. Right panels:  The same simulation as Fig. 1 except $a_{\mathrm{,b0}}=0.2$ au. The lower panels are snapshots of the particle inclination $i$ at the end of simulations.  

$T_{\mathrm{b}}$ $\approx11\,000\,\mathrm{yr})$ . Therefore, the merger time-scale of a binary with lower $e_{\mathrm{b}}$ or larger $a_{\mathrm{b}}$ is longer, as expected. The two lower panels show that the particle discs at the end of simulations are close to polar. There are differences in the distributions with orbital radius due to the different binary apsidal precession rates. The innermost region of the particle disc in the lower left panel shows a wide inclination distribution because of the longer merger time-scale. Nodal precession in the innermost region is faster. This effect may explain the wide distribution of inclinations of highly misaligned planets around single stars.  

In addition to apsidal precession, the mass of the third body (or the debris disc), which we do not consider in this study, can also affect $i_{\mathrm{s}}$ .  Analytic solutions and simulations both show that $i_{\mathrm{s}}$ depends on $e_{\mathrm{b}}$ and on the angular momentum ratio $j$ of the circumbinary disc (or the circumbinary planet) to the binary (Lubow & Martin 2018; Martin & Lubow 2018,  2019;  Chen et al. 2019)  and that $i_{\mathrm{s}}$ decreases with increasing $j$ (see equation 17 in Martin & Lubow 2019) . Thus, a CBD or the circumbinary planet which inherits the high tilt of the disc can start precessing (Cuello & Giuppone 2019)  and the final inclination after merging can still be lower than $90^{\circ}$ , and this effect may also explain the wide distribution of inclinations of highly misaligned planets around single stars. On the other hand, the effect of the angular momentum exchange between $e_{\mathrm{b}}$ and the inclination of the misaligned third body plays a role if $j$ is large enough. In figs 3 and 4 of Chen et al. ( 2019) , simulations show that $e_{\mathrm{b}}$ can be excited from 0.2 to above 0.7 if $j$ is large and the mass fraction of the binary is small. Additionally, $e_{\mathrm{b}}$ increases with increasing deviation between $i_{\mathrm{s}}$ and $i$ . Thus, if planet formation occurs while the disc is young, it is likely that planets formed inside the disc could decouple from the disc (e.g. Lubow & Martin 2016;  Martin et al. 2016;  Franchini, Martin & Lubow 2020) . A decoupled yet massive circumbinary planet, inheriting the originally high tilt of the disc aligned to $i_{\mathrm{s}}$ ,  may tremendously excite $e_{\mathrm{b}}$ and speed up the binary merging process even if the binary only has a moderate $e_{\mathrm{b}}$ initially.  

# 4  CONCLUSION  

We present a new mechanism to form highly misaligned planets around a single star. The process is as follows. First, a misaligned gas disc around an eccentric binary settles into a polar aligned configuration. Second, the binary is driven to merge due to the tides between the two stars if they initially formed close enough or through other effects such as interaction with a circumbinary gas disc. Third, the formation of planets in the (near-)polar gas disc results in planets with orbits that are near-perpendicular to the spin plane of the merged star which is approximately in the orbital plane of the original binary system.3  

Using $N$ -body simulations, we consider the tidal dissipation between two solar-type stars, initially in a binary configuration, surrounded by a polar disc of test particles that represent possible planets with an inclination of about $90^{\circ}$ . Tidal dissipation between the stars causes the binary to merge, leaving a polar disc around a single star. Moreo v er, the fast apsidal precession of the binary increases the stationary polar alignment angle of the disc, similar to an effect found with GR (e.g. Lepp et al. 2022) . Thus, the disc angle after the merger can be higher than $90^{\circ}$ . A smaller angle is also possible if the mass of the planet is taken into account (e.g. Chen et al. 2019)  or if the particle nodal precession time-scale is short compared to the merger time-scale. Therefore, it is possible that a range of high-inclination planets can be caused by this mechanism. Future simulations that include the gas dynamics of both the disc–binary interaction and the hydrodynamics of the merger process will provide valuable insights into the details of this scenario.  

# ACKNOWLEDGEMENTS  

Computer support was provided by UNLV’s National Supercomputing Center and DiRAC Data Intensive service at Leicester, operated by the University of Leicester IT Services, which forms part of the STFC DiRAC HPC Facility ( www.dirac.ac.uk). CC and CJN acknowledge support from the Science and Technology Facilities Council (grant number ST/Y000544/1). CJN acknowledges support from the Leverhulme Trust (grant number RPG-2021-380). RGM acknowledges support from NASA through grant 80NSSC19K0443.  

Simulations in this paper made use of the REBOUND code and the REBOUNDX code which can be downloaded freely at http://github.c om/hannorein/rebound and https://github.com/dtamayo/reboundx) .  

# DATA  AVAILABILITY  

The simulations in this paper can be reproduced by using the REBOUND code (Astrophysics Source Code Library identifier ascl.net/1110.016). The data underlying this article will be shared on reasonable request to the corresponding author.  

# REFERENCES  

Albrecht S. H.,  Marcussen M. L., Winn J. N., Dawson R. I., Knudstrup E.,   
2021, ApJ,  916, L1   
Aly H.,  Dehnen W., Nixon C., King A., 2015, MNRAS,  449, 65   
Anderson K. R.,  Winn J. N., Penev K., 2021, ApJ,  914, 56   
Antonini F.,  Perets H. B., 2012, ApJ,  757, 27   
Armitage P. J.,  Natarajan P., 2002, ApJ,  567, L9   
Artymowicz P.,  Lubow S. H., 1994, ApJ,  421, 651   
Artymowicz P.,  Lubow S. H., 1996, ApJ,  467, L77   
Bally J.,  Zinnecker H., 2005, AJ,  129, 2281   
Baronett S. A.,  Ferich N., Tamayo D., Steffen J. H., 2022, MNRAS,  510,   
6001   
Bate M. R.,  2018, MNRAS,  475, 5618   
Bate M. R.,  Lodato G., Pringle J. E., 2010, MNRAS,  401, 1505   
Ceppi S.,  Cuello N., Lodato G., Longarini C., Price D. J., Elsender D., Bate   
M. R., 2024, A&A,  682, A104   
Ceppi S.,  Longarini C., Lodato G., Cuello N., Lubow S. H., 2023, MNRAS,   
520, 5817   
Chen C.,  Franchini A., Lubow S. H., Martin R. G., 2019, MNRAS,  490, 5634   
Chen C.,  Lubow S. H., Martin R. G., 2020, MNRAS,  494, 4645   
Childs A. C.,  Martin R. G., 2021, ApJ,  920, L8   
Childs A. C.,  Martin R. G., Nixon C. J., Geller A. M., Lubow S. H., Zhu Z.,   
Lepp S., 2024, ApJ,  962, 77   
Cuello N.,  Giuppone C. A., 2019, A&A,  628, A119   
Czekala I.,  Chiang E., Andrews S. M., Jensen E. L. N., Torres G., Wilner D.   
J., Stassun K. G., Macintosh B., 2019, ApJ,  883, 22   
Doolin S.,  Blundell K. M., 2011, MNRAS,  418, 2656   
Eberle J.,  Cuntz M., 2010, ApJl,  721, L168   
F abryck y D. C.,  Winn J. N., 2009, ApJ,  696, 1230   
Foucart F.,  Lai D., 2011, MNRAS,  412, 2799   
Franchini A.,  Martin R. G., Lubow S. H., 2020, MNRAS,  491, 5351   
Hagelberg J. et al., 2023, A&A,  679, A70   
Heath R. M.,  Nixon C. J., 2020, A&A,  641, A64   
Hjorth M.,  Albrecht S., Hirano T., Winn J. N., Dawson R. I., Zanazzi J.,   
Knudstrup E., Sato B., 2021, Proc. Natl. Acad. Sci.,  118, e2017418118   
Hut P.,  1981, A&A, 99, 126   
Kennedy G. M. et al., 2012, MNRAS,  421, 2264   
Kennedy G. M. et al., 2019, Nat. Astron.,  3, 278   
Kenworthy M. A. et al., 2022, A&A,  666, A61   
Kozai Y.,  1962, AJ,  67, 591   
Lai D.,  Foucart F., Lin D. N. C., 2011, MNRAS,  412, 2790   
Lepp S.,  Martin R. G., Childs A. C., 2022, ApJ,  929, L5   
Lepp S.,  Martin R. G., Lubow S. H., 2023a, ApJ,  943, L4   
Lepp S.,  Martin R. G., Zhang B., 2023b, ApJ,  958, L23   
Lidov M. L.,  1962, Planet. Space Sci.,  9, 719   
Lu T.,  Rein H., Tamayo D., Hadden S., Mardling R., Millholland S. C.,   
Laughlin G., 2023, ApJ,  948, 41   
Lubow S. H.,  Martin R. G., 2016, ApJ,  817, 30   
Lubow S. H.,  Martin R. G., 2018, MNRAS,  473, 3733   
Manara C. F.,  Morbidelli A., Guillot T., 2018, A&A,  618, L3   
Martin R. G.,  Lubow S. H., 2017, ApJ,  835, L28   
Martin R. G.,  Lubow S. H., 2018, MNRAS,  479, 1297   
Martin R. G.,  Lubow S. H., 2019, MNRAS,  490, 1332   
Martin R. G.,  Lubow S. H., Nixon C., Armitage P. J., 2016, MNRAS,  458,   
4345   
Miranda R.,  Mu n˜ oz D. J., Lai D., 2017, MNRAS,  466, 1170   
Moody M. S. L.,  Shi J.-M., Stone J. M., 2019, ApJ,  875, 66   
Mu n˜ oz D. J.,  Lai D., Kratter K., Miranda R., 2020, ApJ,  889, 114   
Mu n˜ oz D. J.,  Miranda R., Lai D., 2019, ApJ,  871, 84   
Nikolaos G.,  Siegfried E., Mohamad A.-D., Ian D.-D., 2024, preprint   
( arXiv:2404.13746)   
Nixon C. J.,  Cossins P. J., King A. R., Pringle J. E., 2011, MNRAS,  412,   
1591   
Nixon C. J.,  King A. R., Pringle J. E., 2018, MNRAS,  477, 3273   
Nixon C. J.,  Pringle J. E., 2010, MNRAS,  403, 1887   
Nixon C.,  King A., 2016, in Haardt F., Gorini V., Moschella U., Treves A.,   
Colpi M., eds, Lecture Notes in Physics, Vol. 905. Springer Verlag, Berlin,   
p. 45   
Nixon C.,  King A., Price D., 2013, MNRAS,  434, 1946   
Pagano I. et al., 2024, A&A,  682, A102   
Petrovich C.,  Mu n˜ oz D. J., Kratter K. M., Malhotra R., 2020, ApJ,  902, L5   
Raghavan D. et al., 2010, ApJS,  190, 1   
Rein H.,  Spiegel D. S., 2015, MNRAS,  446, 1424   
Rein H.,  Tamayo D., 2015, MNRAS,  452, 376   
Rogers T. M.,  Lin D. N. C., 2013, ApJ,  769, L10   
Romanova M. M.,  Koldoba A. V., Ustyugova G. V., Blinova A. A., Lai D.,   
Lo v elace R. V. E., 2021, MNRAS,  506, 372   
Small w ood J. L.,  Franchini A., Chen C., Becerril E., Lubow S. H., Yang   
C.-C., Martin R. G., 2020, MNRAS,  494, 487   
Southworth J. et al., 2011, A&A,  527, A8   
Stef \`ansson G. et al., 2022, ApJ,  931, L15   
Tang Y.,  MacFadyen A., Haiman Z., 2017, MNRAS,  469, 4258   
Tychoniec Ł. et al., 2020, A&A,  640, A19   
von Zeipel H.,  1910, Astron. Nachr.,  183, 345   
Wang C. et al., 2022, Nat. Astron.,  6, 480  