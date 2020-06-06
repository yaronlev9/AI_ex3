import sys


def single_disk_to_empty_peg(disk, first_peg, second_peg):
    result = "Name: M_" + disk + "_in_" + first_peg + "_to_" + second_peg + "\n"
    result += "pre: " + disk + "_in_" + first_peg + " " + disk + "_highest " + disk + "_lowest " + \
              second_peg + "_is_empty\n"
    result += "add: " + disk + "_in_" + second_peg + " " + first_peg + "_is_empty\n"
    result += "delete: " + disk + "_in_" + first_peg + " " + second_peg + "_is_empty\n"
    return result


def single_disk_to_not_empty_peg(disk, first_peg, second_peg, lower_disk1):
    result = "Name: M_" + disk + "_in_" + first_peg + "_to_" + second_peg + "_on_" + lower_disk1 + "\n"
    result += "pre: " + disk + "_in_" + first_peg + " " + disk + "_highest" + " " + disk + "_lowest" + " " + \
              lower_disk1 + "_in_" + second_peg + " " + lower_disk1 + "_highest\n"
    result += "add: " + disk + "_in_" + second_peg + " " + disk + "_on_" + lower_disk1 + " " + \
              first_peg + "_is_empty\n"
    result += "delete: " + disk + "_in_" + first_peg + " " + disk + "_lowest" + " " + lower_disk1 + "_highest\n"
    return result


def disk_to_empty_peg(disk, first_peg, second_peg, lower_disk1):
    result = "Name: M_" + disk + "_in_" + first_peg + "_on_" + lower_disk1 + "_to_" + second_peg + "\n"
    result += "pre: " + disk + "_in_" + first_peg + " " + disk + "_highest" + " " + \
              disk + "_on_" + lower_disk1 + " " + second_peg + "_is_empty\n"
    result += "add: " + disk + "_in_" + second_peg + " " + disk + "_lowest" + " " + lower_disk1 + "_highest\n"
    result += "delete: " + disk + "_in_" + first_peg + " " + disk + "_on_" + lower_disk1 + " " + \
              second_peg + "_is_empty\n"
    return result


def disk_to_not_empty_peg(disk, first_peg, second_peg, lower_disk1, lower_disk2):
    result = "Name: M_" + disk + "_in_" + first_peg + "_on_" + lower_disk1 + "_to_" + second_peg + "_on_" + \
             lower_disk2 + "\n"
    result += "pre: " + disk + "_in_" + first_peg + " " + disk + "_highest" + " " + disk + "_on_" + \
              lower_disk1 + " " + lower_disk2 + "_in_" + second_peg + " " + lower_disk2 + "_highest\n"
    result += "add: " + disk + "_in_" + second_peg + " " + disk + "_on_" + lower_disk2 + " " + \
              lower_disk1 + "_highest\n"
    result += "delete: " + disk + "_in_" + first_peg + " " + disk + "_on_" + lower_disk1 + " " + \
              lower_disk2 + "_highest\n"
    return result


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"
    domain_file.write("Propositions:\n")
    for peg in pegs:
        domain_file.write(peg + "_is_empty ")
    for disk in disks:
        domain_file.write(disk + "_highest ")
        domain_file.write(disk + "_lowest ")
    for disk1 in disks:
        for disk2 in disks:
            if disk1 < disk2:
                domain_file.write(disk1 + "_on_" + disk2 + " ")
    for disk in disks:
        for peg in pegs:
            domain_file.write(disk + "_in_" + peg + " ")
    domain_file.write("\nActions:\n")
    for disk in disks:
        for first_peg in pegs:
            for second_peg in pegs:
                if first_peg == second_peg:
                    continue
                domain_file.write(single_disk_to_empty_peg(disk, first_peg, second_peg))
                for lower_disk_first_peg in disks:
                    if disk >= lower_disk_first_peg:
                        continue
                    domain_file.write(single_disk_to_not_empty_peg(disk, first_peg, second_peg, lower_disk_first_peg))
                    domain_file.write(disk_to_empty_peg(disk, first_peg, second_peg, lower_disk_first_peg))
                    for lower_disk_second_peg in disks:
                        if (lower_disk_first_peg == lower_disk_second_peg) or (disk >= lower_disk_second_peg):
                            continue
                        domain_file.write(disk_to_not_empty_peg(disk, first_peg, second_peg, lower_disk_first_peg,
                                                                lower_disk_second_peg))
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"
    problem_file.write("Initial state: ")
    for i in range(len(disks) - 1):
        problem_file.write(disks[i] + "_on_" + disks[i + 1] + " ")
    for disk in disks:
        problem_file.write(disk + "_in_" + pegs[0] + " ")
    problem_file.write(disks[0] + "_highest ")
    problem_file.write(disks[-1] + "_lowest ")
    for i in range(1, len(pegs)):
        problem_file.write(pegs[i] + "_is_empty ")

    problem_file.write("\nGoal state: ")
    for disk in disks:
        problem_file.write(disk + "_in_" + pegs[-1] + " ")
    for i in range(len(disks) - 1):
        problem_file.write(disks[i] + "_on_" + disks[i + 1] + " ")
    for i in range(len(pegs) - 1):
        problem_file.write(pegs[i] + "_is_empty ")
    problem_file.write("d_0" + "_highest ")
    problem_file.write(disks[-1] + "_lowest")
    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
