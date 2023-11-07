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


# instead have to dictionaries checking sign or not sign of first and whether it is pure or not

def Find_Pure_Symbol(clauses, model):
    symbols = set()
    for clause in clauses:
        literals = clause.split()
        for literal in literals:
            s = literal
            if literal.startswith('-'):
                s = literal[1:]
            if model[s] == 0:
                symbols.add(s)

    symbol_sign = {symbol: ' ' for symbol in symbols}
    symbol_pure = {symbol: True for symbol in symbols}

    for clause in clauses:
        literals = clause.split()
        for literal in literals:
            if literal.startswith('-') and literal[1:] in symbols:
                if symbol_sign[literal[1:]] == ' ':
                    symbol_sign[literal[1:]] = '-'
                elif symbol_sign[literal[1:]] == '+':
                    symbol_pure[literal[1:]] = False
            elif literal in symbols:
                if symbol_sign[literal] == ' ':
                    symbol_sign[literal] = '+'
                elif symbol_sign[literal] == '-':
                    symbol_pure[literal] = False

    for symbol in symbols:
        if symbol_pure[symbol]:
            if symbol_sign[symbol] == '-':
                return symbol, -1
            else:
                return symbol, 1

    return None, 0


def evaluate_clause(clause, model):
    key_with_value_zero = next(
        (key for key, value in model.items() if value == 0), None)
    literals = clause.split()
    for literal in literals:
        if literal.startswith('-'):
            if model[literal[1:]] == -1:
                return True
        else:
            if model[literal] == 1:
                return True

    if key_with_value_zero == None:
        print(clause)
    return False


def evaluate_all_clauses_to_be_True(clauses, model):
    if any(value == 0 for value in model.values()):
        return None
    return all(evaluate_clause(clause, model) for clause in clauses)


def evaluate_some_clauses_to_be_False(clauses, model):
    false_clause = next(
        (clause for clause in clauses if not evaluate_clause(clause, model)), None)
    if false_clause == None:
        return False
    return True


dpll_count = 0


def DPLL(clauses, model, uch, psh, output):
    global dpll_count
    dpll_count += 1
    print(output)

    if evaluate_all_clauses_to_be_True(clauses, model):
        print(model)
        for key, value in model.items():
            if value == 1:
                print(key)
        return True
    # print("after check every clause is true")
    if evaluate_some_clauses_to_be_False(clauses, model) == False:
        print("Backtracking")
        return False
    # print("after check some clause is false")
    if psh:
        symbol, value = Find_Pure_Symbol(clauses, model)
        if symbol != None:
            new_model = model.copy()
            new_model[symbol] = value
            # print("pure", symbol, value)
            output = "Forcing " + symbol + "=" + str(value) + " by PSH"
            return DPLL(clauses, new_model, uch, psh, output)
    if uch:
        symbol, value = Find_Unit_Clause(clauses, model)
        if symbol != None:
            new_model = model.copy()
            new_model[symbol] = value
            # print("Find Unit")
            output = "Forcing " + symbol + "=" + str(value) + " by UCH"
            return DPLL(clauses, new_model, uch, psh, output)
    model_True = model.copy()
    model_False = model.copy()

    key_with_value_zero = next(
        (key for key, value in model.items() if value == 0), None)
    if key_with_value_zero != None:
        model_True[key_with_value_zero] = 1
        model_False[key_with_value_zero] = -1
        print(key_with_value_zero)
        print("trying shit")
        output1 = "trying " + key_with_value_zero + "=T"
        output2 = "trying " + key_with_value_zero + "=F"
        return DPLL(clauses, model_True, uch, psh, output1) or DPLL(clauses, model_False, uch, psh, output2)
    else:
        print(model)
        return False


def main():
    if len(sys.argv) < 1:
        print("Usage: python DPLL.py <filename>")
        sys.exit(1)
    clauses = read_cnf_file(filename=sys.argv[1])
    uch, psh = False, False
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "+UCH":
            uch = True
        elif sys.argv[i] == "+PSH":
            psh = True
        else:
            clauses.add(sys.argv[i])
    model = create_model(clauses)

    print(model)

    print(DPLL(clauses, model, uch, psh, ""))


if __name__ == "__main__":
    main()
