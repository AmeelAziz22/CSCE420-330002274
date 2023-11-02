import sys

import heapq
from itertools import count


def read_cnf_file(filename):
    clauses = []
    with open(filename, "r") as file:
        current_clause = []
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line == "0":
                clauses.append(current_clause)
                current_clause = []
            else:
                current_clause.append(line)
        if current_clause:
            clauses.append(current_clause)

    return set(clauses[0])


def create_model(clauses):
    symbols = set()
    for clause in clauses:
        literals = clause.split()
        for literal in literals:
            if literal.startswith('-'):
                symbols.add(literal[1:])  # Remove the leading '-'
            else:
                symbols.add(literal)

    # Create a dictionary with all symbols initialized to 0
    model = {symbol: 0 for symbol in symbols}
    return model


def Find_Unit_Clause(clauses, model):
    for clause in clauses:
        literals = clause.split()
        if len(literals) == 1:
            literal = None
            if literals[0].startswith('-'):
                literal = literals[0][1:]
            else:
                literal = literals[0]

            if model[literal] == 0:
                if literals[0].startswith('-'):
                    return literal, -1
                else:
                    return literal, 1
        else:
            false_count = 0
            truth_found = False
            last_literal = None
            for literal in literals:
                model_literal = None
                if literal.startswith('-'):
                    model_literal = literal[1:]
                else:
                    model_literal = literal

                if model[model_literal] == 1:
                    if literal.startswith('-'):
                        false_count += 1
                        continue
                    else:
                        truth_found = True
                        break
                elif model[model_literal] == -1:
                    if literal.startswith('-'):
                        truth_found = True
                        break
                    else:
                        false_count += 1
                        continue
                else:
                    last_literal = literal

            if false_count == (len(literals)-1) and truth_found == False:
                if last_literal.startswith('-'):
                    return last_literal[1:], -1
                else:
                    return last_literal, 1

    return None, 0


def main():
    if len(sys.argv) < 1:
        print("Usage: python DPLL.py <filename>")
        sys.exit(1)
    clauses = read_cnf_file(filename=sys.argv[1])
    for i in range(2, len(sys.argv)):
        clauses.add(sys.argv[i])
    model = create_model(clauses)
    model['wagFido'] = -1
    model['barkFido'] = -1
    print(Find_Unit_Clause(clauses, model))


if __name__ == "__main__":
    main()
