from ortools.linear_solver import pywraplp
import pandas as pd
import time

def main():
    start_time = time.time()
    rows = 600  # берем 1270!
    Excel_name = "2050.xlsx"

    df = pd.read_excel(Excel_name, nrows = rows)  # read data from excel, put into lists
    names = df['Number'].tolist()
    heats = df['Q'].tolist()
    dates = df['Date'].tolist()

    data = {}
    data['Names_str'] = names
    data['Heats'] = heats
    data['Dates'] = dates
    data['Names'] = list(range(len(heats)))
    # data['Num_sfas'] = len(heats)
    num_bins = 200  # должно быть 200!
    SFAs_in_bin = 4  # должно быть 4!
    max_bin_heat = 0.6 * 2  # должно быть 1.2!

    data['Bins'] = list(range(num_bins))  # gave numbers to bins
    data['Bin_capacities'] = [max_bin_heat] * num_bins

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['Names']:
        for j in data['Bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))
    # Each absolute deviation constrains by t_j.
    t = {}
    for j in data['Bins']:
        t[j] = solver.NumVar(0, solver.infinity(), 't[%i]' % j)

    # Constraints
    # Each sfa can be in at most one bin.
    for i in data['Names']:
        solver.Add(sum(x[i, j] for j in data['Bins']) <= 1)
    # Each bin can have exactly 4 sfas
    for j in data['Bins']:
        solver.Add(sum(x[i, j] for i in data['Names']) == SFAs_in_bin)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['Bins']:
        solver.Add(sum(x[(i, j)] * data['Heats'][i]
            for i in data['Names']) <= data['Bin_capacities'][j])
    # Each absolute deviation constrains by t_j.
    for j in data['Bins']:
        solver.Add((0.8 - sum(x[(i, j)] * data['Heats'][i] for i in data['Names'])) <= t[j])
    for j in data['Bins']:
        solver.Add((0.8 - sum(x[(i, j)] * data['Heats'][i] for i in data['Names'])) >= -t[j])
    '''for j in data['Bins']:
        solver.Add((sum(sum(x[(i, k)] * data['Heats'][i] for i in data['Names']) for k in data['Bins']) / num_bins
                   - sum(x[(i, j)] * data['Heats'][i] for i in data['Names'])) <= t[j])
    for j in data['Bins']:
        solver.Add((sum(sum(x[(i, k)] * data['Heats'][i] for i in data['Names']) for k in data['Bins']) / num_bins
                   - sum(x[(i, j)] * data['Heats'][i] for i in data['Names'])) >= -t[j])'''


    # Objective
    objective = solver.Objective()
    solver.Minimize(sum(t[j] for j in data['Bins']))

    # Call the solver and print the solution

    status = solver.Solve()

    Array_Bins = []
    Array_SFA = []
    Array_Heat = []
    Array_Date = []

    if status == pywraplp.Solver.OPTIMAL:
        print('Total packed value:', objective.Value())
        total_heat = 0
        for j in data['Bins']:
            bin_heat = 0
            print('Bin ', j, '\n')
            for i in data['Names']:
                if x[i, j].solution_value() > 0:
                    print('SFA', data['Names_str'][i], ', date:', data['Dates'][i], '- heat:', data['Heats'][i])
                    bin_heat += data['Heats'][i]
                    Array_Bins.append(j)
                    Array_SFA.append(data['Names_str'][i])
                    Array_Date.append(data['Dates'][i])
                    Array_Heat.append(data['Heats'][i])
            print('Packed bin heat:', bin_heat)
            print()
            total_heat += bin_heat
        print('Total packed Heat:', total_heat)
        # print(len(Array_Bins), len(Array_SFA), len(Array_Heat))
        dict = {
            'Bin': Array_Bins,
            'Name': Array_SFA,
            'Date': Array_Date,
            'Heat': Array_Heat
        }
        dframe = pd.DataFrame(dict)
        dframe.to_excel('./data2050-27.06_or-tools.xlsx')
    else:
        print('The problem does not have an optimal solution.')

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()