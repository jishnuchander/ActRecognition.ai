import numpy as np
import sys
import math
print(sys.executable)
print(sys.version)


def find_dir_relations(X):
    Y = []
    for i in range(1, 11):
        for j in range(1, 11):
            relation = []
            x1 = X[i-1][1]
            y1 = X[i-1][2]
            x2 = X[j-1][4]
            y2 = X[j-1][5]
            if x1 == 0 or y1 == 0 or x2 == 0 or y2 == 0:
                rel = "X"
            else:
                dot = x1*x2 + y1*y2
                det = x1*y2 - x2*y1
                theta = math.degrees(math.atan2(-det, -dot)) + 180
                if theta == 0 or theta == 360:
                    rel = 'Same'
                elif theta > 0 and theta <= 22.5:
                    rel = 'Same+1'
                elif theta > 22.5 and theta <= 45:
                    rel = 'Same+2'
                elif theta > 45 and theta <= 67.5:
                    rel = 'rl-2'
                elif theta > 67.5 and theta < 90:
                    rel = 'rl-1'
                elif theta == 90:
                    rel = 'rl'
                elif theta > 90 and theta <= 112.5:
                    rel = 'rl+1'
                elif theta > 112.5 and theta <= 135:
                    rel = 'rl+2'
                elif theta > 135 and theta <= 157.5:
                    rel = 'Opposite-2'
                elif theta > 157.5 and theta < 180:
                    rel = 'Opposite-1'
                elif theta == 180:
                    rel = 'Opposite'
                elif theta > 180 and theta <= 202.5:
                    rel = 'Opposite+1'
                elif theta > 202.5 and theta <= 225:
                    rel = 'Opposite+2'
                elif theta > 225 and theta <= 247.5:
                    rel = 'lr-2'
                elif theta > 247.5 and theta < 270:
                    rel = 'lr-1'
                elif theta == 270:
                    rel = 'lr'
                elif theta > 270 and theta <= 292.5:
                    rel = 'lr+1'
                elif theta > 292.5 and theta <= 315:
                    rel = 'lr+2'
                elif theta > 315 and theta <= 337.5:
                    rel = 'Same-2'
                elif theta > 337.5 and theta < 360:
                    rel = 'Same-1'
                else:
                    rel = 'Something wrong'

            relation.extend([i, j, rel])
            Y.append(relation)
    return Y


def directional_relation(filename):
    old_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + filename
    old = open(old_filename, 'r')
    new_filename = '/home/jishnu/Desktop/BTP/New_Formalism/ME_New/' + \
        filename[:-4] + '_relations.txt'
    new = open(new_filename, 'w')
    print('Reading', old_filename)
    for line in old:
        if line[0] == 'S':
            new.write(line)
            print('Reading ', line)
        else:
            currentline = line.rstrip('\n').split(' ')
            # print(currentline)
            X = np.zeros(shape=(10, 6))
            row = list(map(float, currentline))
            X[0] = np.array(row)
            for i in range(1, 10):
                currentline = old.readline().split(' ')
                row = list(map(float, currentline))
                X[i] = np.array(row)
            Y = find_dir_relations(X)
            print(len(Y), len(Y[0]))
            for sub_list in Y:
                for item in sub_list:
                    new.write(str(item) + ' ')
                new.write('\n')
            new.write('\n')


directional_relation('Approach/Approach2_T11L_direction.txt')
