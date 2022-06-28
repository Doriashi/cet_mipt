import random
import gurobipy as grb
import pandas as pd
import statistics

def main():

    rows = 1270  # берем 1270!
    Excel_name = "2050.xlsx"

    df = pd.read_excel(Excel_name, nrows = rows)  # read data from excel, put into lists
    names = df['Number'].tolist()
    heats = df['Q'].tolist()
    dates = df['Date'].tolist()

    data = {}  # creat dict
    data['Names_str'] = names
    data['Heats'] = heats
    data['Dates'] = dates
    data['Names'] = list(range(len(heats)))

    num_bins = 200  # должно быть 200!
    SFAs_in_bin = 4  # должно быть 4!
    max_bin_heat = 0.6 * 2  # должно быть 1.2!
    Mean_heat = statistics.mean(heats)
    data['Bins'] = list(range(num_bins))  # gave numbers to bins
    data['Bin_capacities'] = [max_bin_heat] * num_bins


    opt_model = grb.Model(name="MIP Model")

    # if x is Binary
    x_vars = {(i, j): opt_model.addVar(vtype=grb.GRB.BINARY, name="x_{0}_{1}".format(i, j)) for i in data['Names'] for j
              in data['Bins']}  # бинарные переменные
    t_vars = {(j):opt_model.addVar(vtype=grb.GRB.CONTINUOUS, lb=0, ub=1.2, name="t_{0}".format(j)) for j in data['Bins']}

    # Constraints
    # Each sfa can be in at most one bin.
    c1 = opt_model.addConstrs(grb.quicksum(x_vars[i, j] for j in data['Bins']) <= 1 for i in data['Names'])

    # Each bin can have exactly 4 sfas
    c2 = opt_model.addConstrs(grb.quicksum(x_vars[i, j] for i in data['Names']) == SFAs_in_bin for j in data['Bins'])

    # The amount packed in each bin cannot exceed its capacity.
    c3 = opt_model.addConstrs(
        grb.quicksum(x_vars[(i, j)] * data['Heats'][i] for i in data['Names']) <= data['Bin_capacities'][j] for j in
        data['Bins'])

    # Each absolute deviation constrains by t_j.

    # Quadratic constraints
    constraints6 = {j:
        opt_model.addQConstr(lhs=((grb.quicksum(
        grb.quicksum(x_vars[(i, k)] * data['Heats'][i] for i in data['Names']) for k in
        data['Bins']) / num_bins - grb.quicksum(x_vars[(i, j)] * data['Heats'][i] for i in data['Names'])) ** 2),
            sense=grb.GRB.LESS_EQUAL,
            rhs=t_vars[j],
            name="constraint_{0}".format(j))
        for j in data['Bins']}

    #opt_model.Params.timeLimit = 100.0

    # Objective
    objective = grb.quicksum(t_vars[j] for j in data['Bins'])

    opt_model.ModelSense = grb.GRB.MINIMIZE
    opt_model.setObjective(objective)
    opt_model.optimize()

    opt_df = pd.DataFrame.from_dict(x_vars, orient="index", columns=["variable_object"])
    opt_df.index = pd.MultiIndex.from_tuples(opt_df.index, names=["Name", "Bin"])

    opt_df.reset_index(inplace=True)
    opt_df["solution"] = opt_df["variable_object"].apply(lambda item: item.X)
    #print(opt_df)

    Array_Bins = []
    Array_SFA = []
    Array_Heat = []
    Array_Date = []

    for i in range(len(opt_df['Name'])):
        if opt_df['solution'][i] > 0:
            i_data = int(opt_df['Name'][i])
            Array_Bins.append(opt_df['Bin'][i])
            Array_SFA.append(data['Names_str'][i_data])
            Array_Date.append(data['Dates'][i_data])
            Array_Heat.append(data['Heats'][i_data])
    dict = {
        'Bin': Array_Bins,
        'Name': Array_SFA,
        'Date': Array_Date,
        'Heat': Array_Heat
    }
    dframe = pd.DataFrame(dict)
    dframe.to_excel('./data2050-27.06_QP.xlsx')


if __name__ == '__main__':
    main()