f = open('squares.txt')
lines = f.read().strip().split("\n")
boxes = []

def split_line(file_line):
    inner_lines = [
        full_line.strip() for full_line in file_line.strip().split("    ")
    ]
    results = [
        [int(number.strip()) for number in inner.replace("  ", " ").split(" ")]
        for inner in inner_lines
    ]
    return results


for index in range(len(lines))[::5]:
    first_line = split_line(lines[index])
    second_line = split_line(lines[index + 1])
    third_line = split_line(lines[index + 2])
    fourth_line = split_line(lines[index + 3])
    boxes.append([
        first_line[0],
        second_line[0],
        third_line[0],
        fourth_line[0]
    ])
    boxes.append([
        first_line[1],
        second_line[1],
        third_line[1],
        fourth_line[1]
    ])
    boxes.append([
        first_line[2],
        second_line[2],
        third_line[2],
        fourth_line[2]
    ])
    boxes.append([
        first_line[3],
        second_line[3],
        third_line[3],
        fourth_line[3]
    ])

looking_d_1 = [4, 7, 11, 12]
looking_d_2 = [5, 6, 9, 14]

for box in boxes:
    diagonal_1 = sorted([box[0][0], box[1][1], box[2][2], box[3][3]])
    diagonal_2 = sorted([box[0][3], box[1][2], box[2][1], box[3][0]])
    if (
        diagonal_1 in [looking_d_1, looking_d_2]
        and diagonal_2 in [looking_d_1, looking_d_2]
    ):
        for row in box:
            print " ".join(format(x, '02') for x in row)
        print "MATCH"
