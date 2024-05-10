gmx traj -f step7_production.xtc -n index.ndx  -s step7_production.pdb

gmx trjconv -s ./step7_production.tpr -f ./step7_production.xtc -o final_1.xtc -pbc mol -center



