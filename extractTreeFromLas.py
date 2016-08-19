__author__ = 'Kunxuan'

import LAD
import readTrees as rt
import matplotlib.pyplot as plt
import numpy as np
#
# file name definitions for sage bush
fin = r'C:\School\Research\Data\czomi_reynoldCreek\BIN_0410.las'    # large las file
fout = r'C:\School\Research\Data\czomi_reynoldCreek\BIN_0410_sage.las'  # file with extracted tree
fout_txt = r'C:\School\Research\Data\czomi_reynoldCreek\BIN_0410_sage.txt'  # txt version of fout
fout_fixed = r'C:\School\Research\Data\czomi_reynoldCreek\BIN_0410_sage_text.txt'   # txt with missing data added

# # file name definitions for Kunxuan's tree
# fin = r'C:\School\14au\Research\python\LidarCode\365000_4432000.las'    # large las file
# fout = r'C:\School\Research\Data\365000_4432000_tree.las'  # file with extracted tree
# fout_txt = r'C:\School\Research\Data\365000_4432000_tree.txt'  # txt version of fout
# fout_fixed = r'C:\School\Research\Data\365000_4432000_tree_fixed.txt'   # txt with missing data added

extract_code = 'xyzca'  # extract code must be a subset of what the data contains
rt.extractTrees(523452.11, 4777290.45, 2.2, fin, fout)
# rt.extractTrees(365776.835, 4432766.49, 10.1, fin, fout)
rt.las2txt(fout, fout_txt)

# replace missing data in lidar
file = open(fout_txt, 'rb')
outfile = open(fout_fixed, 'wb')

for line in file.read().splitlines():
    # print line
    # split line by ' '
    l_sp = line.split(' ')
    # print l_sp

    # record x, y ,z in a string
    res_str = ' '.join(l_sp[0:3])

    # and make up other data if not avilable
    # current data has classification (c), and scan angle (a) in l_sp[3] and l_sp[4]
    res_str = ' '.join([res_str, '1', l_sp[3], l_sp[4], '\n'])
    # print res_str

    # resulting res_str should be x,y,z,n (number of returns in this pulse), c (class), a (scan angle)
    outfile.write(res_str)

outfile.close()

# finished editing file, use it as input to lad class
sage_lad = LAD.LAD(fout_fixed, 10)
sage_lad.setLAD(fout_fixed, 1)

print 'voxel pt count: ', sage_lad.voxCount
print 'LAD: ', sage_lad.lad
print 'Heights: ', sage_lad.heights

# normalize LAD
lad_fixed = np.array(sage_lad.lad)
lad_fixed = lad_fixed/np.sum(lad_fixed)

# plot LAD
plt.plot(lad_fixed, sage_lad.heights)
plt.xlabel('LAD')
plt.ylabel('Height (m)')
plt.show()
