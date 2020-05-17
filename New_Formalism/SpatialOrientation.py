import math
import numpy as np


def create_file(filename1, filename2):
    old_filename1 = '/home/jishnu/Desktop/BTP/New_Formalism/ME/' + filename1
    old_filename2 = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + filename2
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + \
        filename1[:-4] + '_original.txt'
    new = open(new_filename, 'w')
    print('Reading: ' + old_filename1 + ' and ' + old_filename2)

    with open(old_filename1) as f1, open(old_filename2) as f2:
        for line1, line2 in zip(f1, f2):
            if line1 == 'Frame:1':
                continue
            elif line1[0] == 'F':
                new.write(line2)
                # print('Reading: ' + line1 + line2)
            else:
                currentline1 = line1.strip('\n').split(',')
                currentline2 = line2.split(' ')
                length = len(currentline1)
                if length == 10:
                    # print("10 values")
                    line1 = line1.rstrip('\n')
                    new.write(line1 + ',' + currentline2[1] + ',' + currentline2[2])
                    new.write('\n')
                elif length == 5:
                    print("5 values")
                    line1 = line1.rstrip('\n')
                    new.write(line1 + ',' + str(0) + ',' + str(0) + ',' +
                              str(0) + ',' + str(0) + ',' + str(0) + ',' +
                              currentline2[1] + ',' + currentline2[2])
                    new.write('\n')
    print('Finished reading files')


def modify_components(X):
    X_new = np.zeros(shape=(10, 12))
    for i in range(1, 11):
        X_new[i-1][0] = i
        X_new[i-1][5] = i
    for i in range(10):
        for j in range(10):
            if X_new[i][0] == X[j][0]:
                X_new[i][1] = X[j][1]
                X_new[i][2] = X[j][2]
                X_new[i][3] = X[j][3]
                X_new[i][4] = X[j][4]
            if X_new[i][5] == X[j][5]:
                X_new[i][6] = X[j][6]
                X_new[i][7] = X[j][7]
                X_new[i][8] = X[j][8]
                X_new[i][9] = X[j][9]
                X_new[i][10] = X[j][10]
                X_new[i][11] = X[j][11]

    return X_new


Sets = []


def modify_original_matrix(filename):
    old_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + filename
    old = open(old_filename, 'r')
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + \
        filename[:-4] + '_modified.txt'
    new = open(new_filename, 'w')
    print('Reading:', old_filename)
    for line in old:
        if line[0] == 'S':
            new.write(line)
            print('Reading ', line)
        else:
            currentline = line.split(',')
            X = np.zeros(shape=(10, 12))
            row = list(map(float, currentline))
            X[0] = np.array(row)
            for i in range(1, 10):
                currentline = old.readline().split(',')
                row = list(map(float, currentline))
                X[i] = np.array(row)
            X = modify_components(X)         # Define separate function
            Sets.append(X)
            # print(X)
            mat = np.matrix(X)
            for row in mat:
                np.savetxt(new, row, fmt='%.2f')
    print('Finished reading file: ', old_filename)


def check_overlap(x1, x2, x3, x4, y1, y2, y3, y4):
    overlap = 0
    if (x1 >= x4 or x3 >= x3):
        overlap = 0
    if (y2 <= y3 or y4 <= y1):
        overlap = 0
    else:
        overlap = 1
    return overlap


def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    angle = math.radians(angle)
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def distance(p1, p2):
    dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    return dist


def intercept(slope, c):
    i1 = (0, c)
    i2 = (-c/slope, 0)
    return i1, i2


def find_spa_relations(X):
    Y = []
    for i in range(1, 11):
        for j in range(1, 11):
            relation = []
            x1 = X[i-1][1]
            y1 = X[i-1][2]
            x2 = x1 + X[i-1][3]
            y2 = y1 + X[i-1][4]
            x3 = X[j-1][6]
            y3 = X[j-1][7]
            x4 = x3 + X[j-1][8]
            y4 = y3 + X[j-1][9]
            dir1 = X[j-1][10]
            dir2 = X[j-1][11]
            # print(i, j)
            if (x1 == 0 and x2 == 0) or (x3 == 0 and x4 == 0) or (y1 == 0 and y2 == 0) or (y3 == 0 and y4 == 0):
                rel = 'X'
            else:
                overlap = check_overlap(x1, x2, x3, x4, y1, y2, y3, y4)

                center1_x = (x1+x2)/2
                center1_y = (y1+y2)/2
                theta = math.degrees(math.atan2(-dir2, -dir1)) + 180
                if theta > 45:
                    theta -= 45
                else:
                    theta = 45 - theta

                x3_shifted = x3 - center1_x   # Shifting to center1 as the origin
                x4_shifted = x4 - center1_x
                y3_shifted = y3 - center1_y
                y4_shifted = y4 - center1_y

                origin = (0, 0)

                point1 = (x3_shifted, y3_shifted)
                point2 = (x3_shifted, y4_shifted)
                point3 = (x4_shifted, y4_shifted)
                point4 = (x4_shifted, y3_shifted)

                pt1 = rotate(origin, point1, theta)  # Rotating about the shifted origin
                pt2 = rotate(origin, point2, theta)
                pt3 = rotate(origin, point3, theta)
                pt4 = rotate(origin, point4, theta)

                slope1 = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
                slope2 = (pt3[1] - pt2[1]) / (pt3[0] - pt2[0])
                slope3 = (pt4[1] - pt3[1]) / (pt4[0] - pt3[0])
                slope4 = (pt1[1] - pt4[1]) / (pt1[0] - pt4[0])

                c1 = pt1[1] - slope1*pt1[0]
                c2 = pt2[1] - slope2*pt2[0]
                c3 = pt3[1] - slope3*pt3[0]
                c4 = pt4[1] - slope4*pt4[0]

                i11, i12 = intercept(slope1, c1)
                i21, i22 = intercept(slope2, c2)
                i31, i32 = intercept(slope3, c3)
                i41, i42 = intercept(slope4, c4)

                ctr = 0
                intercepts = []
                if round(distance(pt1, i11) + distance(i11, pt2), 5) == round(distance(pt1, pt2), 5):
                    intercepts.append(i11)
                    ctr += 1
                if round(distance(pt1, i12) + distance(i12, pt2), 5) == round(distance(pt1, pt2), 5):
                    intercepts.append(i12)
                    ctr += 1
                if round(distance(pt2, i21) + distance(i21, pt3), 5) == round(distance(pt2, pt3), 5):
                    intercepts.append(i21)
                    ctr += 1
                if round(distance(pt2, i22) + distance(i22, pt3), 5) == round(distance(pt2, pt3), 5):
                    intercepts.append(i22)
                    ctr += 1
                if round(distance(pt3, i31) + distance(i31, pt4), 5) == round(distance(pt3, pt4), 5):
                    intercepts.append(i31)
                    ctr += 1
                if round(distance(pt3, i32) + distance(i32, pt4), 5) == round(distance(pt3, pt4), 5):
                    intercepts.append(i32)
                    ctr += 1
                if round(distance(pt4, i41) + distance(i41, pt1), 5) == round(distance(pt4, pt1), 5):
                    intercepts.append(i41)
                    ctr += 1
                if round(distance(pt4, i42) + distance(i42, pt1), 5) == round(distance(pt4, pt1), 5):
                    intercepts.append(i42)
                    ctr += 1

                ctr_x_pos = ctr_x_neg = ctr_y_pos = ctr_y_neg = 0

                if (len(intercepts) == 0):
                    if pt1[0] >= 0 and pt1[1] >= 0:
                        rel = 'Front'
                    elif pt1[0] < 0 and pt1[1] >= 0:
                        rel = 'Left'
                    elif pt1[0] < 0 and pt1[1] < 0:
                        rel = 'Back'
                    elif pt1[0] >= 0 and pt1[1] < 0:
                        rel = 'Right'
                elif (len(intercepts) == 2):
                    if intercepts[1][0] == 0:
                        if intercepts[1][1] >= 0:
                            rel = 'Front&Left'
                        else:
                            rel = 'Back&Right'
                    elif intercepts[1][1] == 0:
                        if intercepts[1][0] >= 0:
                            rel = 'Front&Right'
                        else:
                            rel = 'Back&Left'
                elif (len(intercepts) == 4):
                    for k in range(len(intercepts)):
                        if intercepts[k][1] == 0:
                            if intercepts[k][0] > 0:
                                ctr_x_pos += 1
                            else:
                                ctr_x_neg += 1
                        elif intercepts[k][0] == 0:
                            if intercepts[k][1] > 0:
                                ctr_y_pos += 1
                            else:
                                ctr_y_neg += 1
                    if ctr_x_pos == 1 and ctr_x_neg == 1 and ctr_y_pos == 1 and ctr_y_neg == 1:
                        rel = 'AllRegion'
                    elif ctr_x_pos == 2 and ctr_y_pos == 2:
                        rel = 'ExtendedInFront'
                    elif ctr_x_neg == 2 and ctr_y_pos == 2:
                        rel = 'ExtendedOnLeft'
                    elif ctr_x_neg == 2 and ctr_y_neg == 2:
                        rel = 'ExtendedInBack'
                    elif ctr_x_pos == 2 and ctr_y_neg == 2:
                        rel = 'ExtendedOnRight'
                    # else:
                        # print('Error!')

                if overlap == 1:
                    rel = rel + 'Overlap'

            relation.extend([i, j, rel])
            Y.append(relation)
    return Y


def spatial_relation(filename):
    old_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + filename
    old = open(old_filename, 'r')
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + \
        filename[:-13] + '_spatial_relations.txt'
    new = open(new_filename, 'w')
    print('Reading: ', old_filename)
    for line in old:
        if line[0] == 'S':
            new.write(line)
            print('Reading: ', line)
        else:
            currentline = line.rstrip('\n').split(' ')
            X = np.zeros(shape=(10, 12))
            print(currentline[1])
            row = [float(i) for i in currentline]
            X[0] = np.array(row)
            for i in range(1, 10):
                currentline = old.readline().rstrip('\n').split(' ')
                row = [float(i) for i in currentline]
                X[i] = np.array(row)
            Y = find_spa_relations(X)
            print(len(Y))
            for sub_list in Y:
                for item in sub_list:
                    new.write(str(item) + ' ')
                new.write('\n')
            new.write('\n')


create_file('Approach/Approach2_T11L.txt', 'Approach/Approach2_T11L_direction.txt')
spatial_relation('Approach/Approach2_T11L_original_modified.txt')
modify_original_matrix('Approach/Approach2_T11L_original.txt')
