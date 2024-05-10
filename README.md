# BioE_230_final_project
The final project for BioE 230

The assembled membrane can be created with CHARMM-GUI https://www.charmm-gui.org/. You can choose to assemble a membrane with a full-atom configuration or martini representation. Martini is a coarse-grained method that will greatly decrease the run time. Please refer to the CHARMM-GUI library for the available lipids https://www.charmm-gui.org/?doc=archive&lib=lipid. 

The steps to run the MD simulation are included in README. One can simply use the script to run the simulation. 

After downloading the file, modify rcoulomb and rvdw from step6.0_minimization.mdp from 1.1 to 2.0. This will increase the threshold can prevent minimization from blowing up. Many warnings will be generated during the run. To ignore the warnings and prevent fatal execution, add ```-maxwarn 1``` to each gmx grompp command. Sometimes pressure would be impossible to fix. Switch the barostate from Parrinello-Rahman to berendsen. Remove the unsetenv GMX_MAXCONSTRWARN from README due to syntax. To run the MD simulation, one might call csh README to run the simulation. However, I found that the cluster takes the bash command better (see below). 

```
gmx grompp -f step6.0_minimization.mdp -o step6.0_minimization.tpr -c step5_charmm2gmx.pdb -r step5_charmm2gmx.pdb -p system.top -n index.ndx -maxwarn 1
gmx mdrun -deffnm step6.0_minimization

# step6.1
gmx grompp -f step6.1_minimization.mdp -o step6.1_minimization.tpr -c step6.0_minimization.gro -r step5_charmm2gmx.pdb -p system.top -n index.ndx -maxwarn 1
gmx mdrun -deffnm step6.1_minimization

# Equilibration

cnt=2
cntmax=6

while [ ${cnt} -le ${cntmax} ]; do
    pcnt=$((cnt - 1))
    if [ ${cnt} -eq 2 ]; then
        gmx grompp -f step6.${cnt}_equilibration.mdp -o step6.${cnt}_equilibration.tpr -c step6.${pcnt}_minimization.gro -r step5_charmm2gmx.pdb -p system.top -n index.ndx -maxwarn 1
    else
        gmx grompp -f step6.${cnt}_equilibration.mdp -o step6.${cnt}_equilibration.tpr -c step6.${pcnt}_equilibration.gro -r step5_charmm2gmx.pdb -p system.top -n index.ndx -maxwarn 1
    fi
    gmx mdrun -deffnm step6.${cnt}_equilibration
    (( cnt++ ))
done

# Production
gmx grompp -f step7_production.mdp -o step7_production.tpr -c step6.6_equilibration.gro -p system.top -n index.ndx
gmx mdrun -deffnm step7_production
```

To perform simulated annealing, one can add this line to 
```
annealing		 = single single
annealing-npoints	 = 2 2
annealing-time		 = 0 100000 0 100000
annealing-temp		 = 318 293 318 293
```
step7_production.mdp. This will decrease the temperature linearly from 318K at 0 seconds to 293K at 100 ns. One should also increase the run time to 15000000.(20 fs * 15000000 steps -> 300 ns run time).

To analyze the simulation result, I use ipynb. To generate video, I use UCSF Chimera. Using the MD Movie under tools, one can record the movie. To generate a timer, copy and plate the chimera.py into per-frame -> define script. To fix the periodic boundary, type ```echo "1 1" | gmx trjconv -s step7_production.tpr -f step7_production.xtc -o center.xtc -pbc mol -center```. To generate pdb from .gro, type ```gmx editconf -f step7_production.gro -o step7_production.pdb```.

If the lipid is not found in the library, one might choose to use a topology builder such as ATB to parametrize a new molecule https://atb.uq.edu.au/. Furthermore, it is possible to map the molecule into martini representation https://github.com/ricalessandri/Martini3-small-molecules/blob/main/tutorials/M3tutorials--parameterizing-a-new-small-molecule.md. Though, it will not be done in this project due to the complexity of such method.

To assemble the membrane bilayer from ATB, one can download the pdb and itp files from ATB. After which, one can assemble a bilayer with packmol. Place pdb and itp files in a new folder, and download gromos54a7_atb.ff. Configure .inp file. Use ```packmol < bilayer.inp``` to generate pdb file for the assembled bilayer. Manually create a topol.top file, or system.top for convention. Add #include "molecule.itp", [system], [molecules] to the .top file. Follow the GROMACS tutorial until the hydration step, and remove all molecules within the lipid. However, we did not progress beyond the building bilayer step. 

Also please note some of the files are larger than GitHub's liking. I have tried zipping them but doesn't work, so I split them into many smaller pieces. Use ```cat * > zipfile.zip``` to join the big files back together, unzip and place them back in the parent directory. 