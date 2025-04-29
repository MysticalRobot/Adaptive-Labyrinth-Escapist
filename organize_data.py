dstar_true_time_path = {}
dstar_false_time_path = {}

bfs_true_time_path = {}
bfs_false_time_path = {}

def addToDict(d, k, v):
    if k in d:
        d[k][0].append(v[0])
        d[k][1].append(v[1])
    else:
        d[k] = ([v[0]], [v[1]])

def avg(l):
    return sum(l) / len(l)

with open('algorithm_data.csv', 'r') as input:
    input.readline()
    for line in input:
        data = line.split(',')
        if data[2] == 'True':
            if data[0] == 'dstar':
                addToDict(dstar_true_time_path, int(data[1]), (int(data[4]), int(data[5])))
            else:
                addToDict(bfs_true_time_path, int(data[1]), (int(data[4]), int(data[5])))
        else:
            if data[0] == 'dstar':
                addToDict(dstar_false_time_path, int(data[1]), (int(data[4]), int(data[5])))
            else:
                addToDict(bfs_false_time_path, int(data[1]), (int(data[4]), int(data[5])))

a = sorted(list(dstar_true_time_path.items()))
b = sorted(list(dstar_false_time_path.items()))
c = sorted(list(bfs_true_time_path.items()))
d = sorted(list(bfs_false_time_path.items()))

with open('organized_data.csv', 'w') as output:
    output.write('n,d* lite diag timing,d* lite diag length,d* lite no diag timing,d* lite no diag length,bfs diag timing,bfs diag length,bfs no diag timing,bfs no diag length\n')
    for row in zip(a, b, c, d):
        print(f'{row[0][0]},{avg(row[0][1][0])},{avg(row[0][1][1])},{avg(row[1][1][0])},{avg(row[1][1][1])},{avg(row[2][1][0])},{avg(row[2][1][1])},{avg(row[3][1][0])},{avg(row[3][1][1])}')
        output.write(f'{row[0][0]},{avg(row[0][1][0])},{avg(row[0][1][1])},{avg(row[1][1][0])},{avg(row[1][1][1])},{avg(row[2][1][0])},{avg(row[2][1][1])},{avg(row[3][1][0])},{avg(row[3][1][1])}\n')