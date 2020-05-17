import numpy as np
import sys
print(sys.executable)
print(sys.version)


def calculate_centre(filename):
    old_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME/' + filename
    old = open(old_filename, 'r')
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + filename
    new = open(new_filename, 'w')
    print('Reading ', old_filename)
    for line in old:
        if line[0] == 'F':
            new.write(line)
            # print('Reading ', line)
        else:
            currentline = line.split(',')
            length = len(currentline)
            if length == 10:
                # print("10 values")
                A_x = int(currentline[1]) + int(currentline[3])/2
                A_y = int(currentline[2]) + int(currentline[4])/2
                B_x = int(currentline[6]) + int(currentline[8])/2
                B_y = int(currentline[7]) + int(currentline[9])/2
                new.write(str(currentline[0]) + ',' + str(A_x) + ',' + str(A_y) +
                          ',' + str(currentline[5])+','+str(B_x)+','+str(B_y))
                new.write('\n')
            elif length == 5:
                # print("5 values")
                A_x = int(currentline[1]) + int(currentline[3])/2
                A_y = int(currentline[2]) + int(currentline[4])/2
                new.write(str(currentline[0]) + ',' + str(A_x) + ',' + str(A_y) +
                          ',' + str(0) + ',' + str(0.0) + ',' + str(0.0))
                new.write('\n')
    print('Finished reading file: ', old_filename)


def components(X):
    X_new = np.zeros(shape=(10, 6))
    for i in range(1, 11):
        X_new[i-1][0] = i
        X_new[i-1][3] = i
    for i in range(10):
        for j in range(10):
            if X_new[i][0] == X[j][0]:
                X_new[i][1] = X[j][1]
                X_new[i][2] = X[j][2]
            if X_new[i][3] == X[j][3]:
                X_new[i][4] = X[j][4]
                X_new[i][5] = X[j][5]

    return X_new


Frames = []


def modify_matrix(filename):
    old_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + filename
    old = open(old_filename, 'r')
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + \
        filename[:-4] + '_modified.txt'
    new = open(new_filename, 'w')
    print('Reading:', old_filename)
    for line in old:
        if line[0] == 'F':
            new.write(line)
            # print('Reading ', line)
        else:
            currentline = line.split(',')
            X = np.zeros(shape=(10, 6))
            row = list(map(float, currentline))
            X[0] = np.array(row)
            for i in range(1, 10):
                currentline = old.readline().split(',')
                row = list(map(float, currentline))
                X[i] = np.array(row)
            X = components(X)
            Frames.append(X)
            # print(X)
            mat = np.matrix(X)
            for row in mat:
                np.savetxt(new, row, fmt='%.2f')
    print('Finished reading file: ', old_filename)


def calculate_direction(filename):
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + \
        filename[:-4] + '_direction.txt'
    new = open(new_filename, 'w')
    Directions = []
    length = len(Frames) - 1
    for i in range(length):
        new.write("Set: " + str(i+1))
        new.write("\n")
        X = np.zeros(shape=(10, 6))
        X = Frames[i+1] - Frames[i]
        for j in range(1, 11):
            X[j-1][0] = j
            X[j-1][3] = j
        # print(X)
        Directions.append(X)
        mat = np.matrix(X)
        for row in mat:
            np.savetxt(new, row, fmt='%.2f')
        # new.write("\n")
    print('Finished calculating directions ', len(Directions))


calculate_centre('Approach/Approach2_T11L.txt')
modify_matrix('Approach/Approach2_T11L.txt')
calculate_direction('Approach/Approach2_T11L.txt')
