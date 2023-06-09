# ATMI - Atmospheric Impact Simulation

ATMI (Atmospheric Impact Simulation) is a project aiming to develop a generic pipeline for the simulation of the atmospheric impact on CMB ground-based experiments. In fact, CMB observations from the ground are strongly limited by the atmosphere: its presence results in both absorption and emission of new signal. Despite the effect of the absorption of the incoming signal is negligible, atmospheric emission constitutes a noise for CMB measurements. 
This project is divided into several sections, responsable of different tasks:

1. Some routines to implement the atmospheric sampling according to the data.
2. Reconstruction of the atmospheric model structure, based on the previous sampling.
3. Calculations to determine the brightness temperature of the atmosphere, thanks to the <a href="https://lweb.cfa.harvard.edu/~spaine/am/">am tool</a> (Atmospheric Model - CfA Harvard) for the radiative transfer computation. 

Usage of the `atmi` bash script: 

```
	atmi [-p PATH_TO_CONFIG] [-s PATH_TO_CONFIG] [-a PATH_TO_CONFIG] [-t PATH_TO_CONFIG] [-i PATH_TO_CONFIG] [-f METHOD] [-h]
```

List of all the possible commands:

<table>
<tr><th>Command			            <th>Name		    <th>What it does?
<tr><td>atmi -p [PATH_TO_CONFIG]	<td>Plot	   	    <td>Extract and plot the PDF for a given variable at a given hour of a given day of the month (see the documentation for more details).
<tr><td>atmi -s [PATH_TO_CONFIG]	<td>Sampling	    <td>Sample an atmospheric realization for the given dates (see the documentation for more details).
<tr><td>atmi -a [PATH_TO_CONFIG]	<td>Am		        <td>Generate the am configuration file for the given atmosphere realization an run am (see the documentation for more details).
<tr><td>atmi -t [PATH_TO_CONFIG]	<td>Temperature	    <td>Generate the am configuration file for the given atmosphere samplings (from file) an run am (see the documentation for more details).
<tr><td>atmi -i [PATH_TO_CONFIG]	<td>Instrument      <td>Calculate the antenna temperature and do the frequency band integration (see the documentation for more details).
<tr><td>atmi -f [METHOD]	        <td>Configuration   <td>Display the configuration file format for the given method.
<tr><td>atmi -h			            <td>Help		    <td>Display the manual.
</table>

In order to install <i>am</i> you can download it from <a href="https://zenodo.org/record/6774378">here</a> and follow the instructions on the <a href="https://zenodo.org/record/6774376">manual</a>.

# How to set up

Clone the repository:

`git clone https://github.com/cintuluca/atmi` <br/>

Move to the `atmi` directory:

`cd atmi` <br/>

Run the initialization script:

`./init.sh` <br/>

The `atmi` bash script can be moved anywhere but anytime the `atmi` directory is moved, you need to move into the directory and run again the initialization script `./init.sh`.

## ATMI requirements:

`matplotlib (>=3.6.3)` <br/>
`numpy (>=1.22.4)` <br/>
`pandas (>=1.5.2)` <br/>
`scipy (>=1.7.3)` <br/>
`termplotlib (>=0.3.9)` <br/>
`xarray (>=2022.11.0)` <br/>

# AUTHOR

Luca Cintura <luca.cintura@gmail.com> <br />

# License

Atmospheric Impact Simulation (ATMI)

Copyright (c) 2023, Luca Cintura

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
