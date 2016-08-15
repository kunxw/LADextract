__author__ = 'Kunxuan'

import readTrees as rt
import LAD as lad
import math

# defOutName = r"C:\School\14au\Research\CZOSangamonIR\data_products\\"
lasFilename = r"C:\School\14au\Research\CZOSangamonIR\las\box_1_class.las"
treeFilename = r"C:\School\14au\Research\CZOSangamonIR\Tree_Location_Data\Ellipse\CEE550_ParameterEquation_All1.txt"

tree_rd = rt.readTrees(treeFilename, lasFilename, [])  #tree reader object
j = -1
tree_int_list = [63,81,85]  #[7,9,10,18,63,81,85]
# tree_int_list = range(0, 9000)
for line in tree_rd.treeFile.read().splitlines():
    if j in tree_int_list:
        tree = rt.read_line(line)
        FID = int(tree[0])
        x = tree[1]
        y = tree[2]
        height = tree[3]
        radius = tree[4]    # at intersection
        max_radius = tree[5]
        crown_half = tree[6]    #b

        # if max_radius-radius>1:
        #     print j, radius, max_radius

        # extract largest cylinder
        rt.extractTrees(x,y,max_radius, lasFilename, tree_rd.defOutName+"temp_treecloud.las")
        tree_rd.las2txt("temp_treecloud")

        # set up parameters
        tree_name = "t_"+str(FID)
        tree_name_cyn = "t_cyn_"+str(FID)
        out_sub = tree_rd.defOutName + "a1_cloud\\"

        # extract cylindrical
        rt.extractTrees(x,y,radius, tree_rd.defOutName+"temp_treecloud.las",
                        out_sub+tree_name_cyn+".las")


        # extract elliptical
        tree_txt = open(tree_rd.defOutName+"temp_treecloud.txt", 'rb')
        tree_ell_txt = open(out_sub+tree_name+'.txt', 'wb')

        t = lad.LAD(tree_rd.defOutName+"temp_treecloud.txt", 3)
        max_elev = t.limits[-1]
        min_elev = t.limits[0]

        print height, max_elev-min_elev

        # check if each pt is with in radius
        for line in tree_txt:
            pt = tuple([float(i) for i in line.split(" ")])
            z = pt[2]-min_elev
            r = rt.get_radius(height, max_radius, crown_half, z)
            rad_new = max(r, 0.3)
            dist = math.sqrt((pt[0]-x)**2 + (pt[1]-y)**2)
            if dist <= rad_new:
                tree_ell_txt.write(line)

    j += 1