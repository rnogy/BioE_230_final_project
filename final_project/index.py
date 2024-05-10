import re
import os
import argparse

def GenIdx(path, atom, lipid):
    try:
        with open(path, "r") as file:
            #Spilt files into array
            line = [line.split(',') for line in file]
    #Quit if cannot open file
    except Exception as reasons:
        print(reasons)
        quit()
    
    NC3 = []
    for i in line:
        #Where in the pdb file contains NC3 for DOPC. NC3 is the nitrogen atom. 
        if atom in str(i) and lipid in str(i):
            #Getting the atom number
            NC3.append(i[0].split()[1])
    
    #Write index file
    with open('./index.ndx', "w") as file:
        file.write('[' + lipid + ']\n')
        #Write all atom
        for i in range(len(NC3)):
            file.write(NC3[i] + " ")
        #skip line is required for gmx to read
        file.write('\n')
        file.close()

    print("successed")

    #generate gmx file
    os.system("gmx traj -f step7_production.xtc -s step7_production.pdb -ox -n index.ndx")
    #rename file
    os.rename('./coord.xvg', './' + lipid + '_coord.xvg')
    print('cord.xvg -> '+ lipid + '_cord.xvg')

#Simple arg phaser
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        help='path of the pdb location. Sometimes topol files works too, if atom number is specified',
        default='./step7_production.pdb',
        required=False)

    parser.add_argument(
        '-a',
        '--atom',
        type=str,
        help='name of atom desired',
        #NC3 is the nitrogen atom. Facing up. 
        default='NC3',
        required=False)
    
    parser.add_argument(
        '-l',
        '--lipid',
        type=str,
        help='name of lipid molecule',
        default='DOPC',
        required=False)

    args = parser.parse_args()
    GenIdx(args.path, args.atom, args.lipid)