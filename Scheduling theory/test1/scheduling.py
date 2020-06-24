import sys
import pandas as pd
from ortools.sat.python import cp_model

def negated_bounded_span(works, start, length):
  sequence = []
  if start > 0:
    sequence.append(works[start - 1])
  for i in range(length):
    sequence.append(works[start + i].Not())
  if start + length < len(works):
    sequence.append(works[start + length])
  return sequence

def span_with_negated_first_and_last_element(works, start, length):
  sequence = []
  sequence.append(works[start].Not())
  for i in range(1, length - 1):
    sequence.append(works[start + i])
  sequence.append(works[start + length - 1].Not())
  return sequence

def add_soft_sum_constraint(model, works, hard_min, soft_min, min_cost,
                            soft_max, hard_max, max_cost, prefix):
    cost_variables = []
    cost_coefficients = []
    sum_var = model.NewIntVar(hard_min, hard_max, '')
    model.Add(sum_var == sum(works))

    if soft_min > hard_min and min_cost > 0:
        delta = model.NewIntVar(-len(works), len(works), '')
        model.Add(delta == soft_min - sum_var)
        excess = model.NewIntVar(0, len(works), prefix + ': under_sum')
        model.AddMaxEquality(excess, [delta, 0])
        cost_variables.append(excess)
        cost_coefficients.append(min_cost)

    if soft_max < hard_max and max_cost > 0:
        delta = model.NewIntVar(-len(works), len(works), '')
        model.Add(delta == sum_var - soft_max)
        excess = model.NewIntVar(0, len(works), prefix + ': over_sum')
        model.AddMaxEquality(excess, [delta, 0])
        cost_variables.append(excess)
        cost_coefficients.append(max_cost)

    return cost_variables, cost_coefficients

def add_sequence_length_constraint(model, works, hard_min, hard_max):
  for length in range(1, hard_min):
    for start in range(len(works) - length + 1):
      model.AddBoolOr(negated_bounded_span(works, start, length))
  for start in range(len(works) - hard_max):
    model.AddBoolOr([works[i].Not() for i in range(start, start + hard_max + 1)])

def add_sequence_daily_frequency_constraint(model, works):
  for length in range(3, len(works)):
    for start in range(len(works) - length + 1):
      model.AddBoolOr(span_with_negated_first_and_last_element(works, start, length))

def boolean_linear_sum(model, bool_vars, bool_sum):
  for var in bool_vars:
    model.Add(bool_sum >= var)
  model.Add(bool_sum <= sum(bool_vars))

def daynum_in_month_from_weeknum(days_list, week):
  daynums = []
  for day in days_list:
    if day[2] == week:
      daynums.append(day[3])
  return daynums

def weeknum_from_daynum_in_month(days_list, daynum):
  for day in days_list:
    if day[3] == daynum:
      return day[2]

class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):
  def __init__(self, limit):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__solution_count = 0
    self.__solution_limit = limit

  def on_solution_callback(self):
    self.__solution_count += 1
    if self.__solution_count >= self.__solution_limit:
      print('Stop search after %i solutions' % self.__solution_limit)
      self.StopSearch()

  def solution_count(self):
    return self.__solution_count

csv_dir = '/home/seymur/Documents/Scripts/Python/scheduling/csv/'
data = {}
for filename in os.listdir(csv_dir):
  if filename.endswith('.csv'):
    data[filename[:-4]] = pd.read_csv(csv_dir + filename, sep=',', header=0)

temp_list = data['dates'].values.tolist()
days_input = [temp_list[i] + [i + 1] for i in range(len(temp_list))]
num_weeks = max(data['dates']['week_in_month'])
shifts_input = [str(i + 1) for i in range(len(data['workloads']))]
employees_input = list(data['employees']['emp_number'])
starting_week_hours_worked_input = list(data['employees']['current_week_hours_worked'])
shifts_workloads_input = [list(data['workloads']['shift_workload']) for i in range(len(days_input))]
excess_cover_penalties_input = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

def solve_weekly_model(days, shifts, employees, starting_hours_worked, workloads, workloads_penalties, solutions_dict):
  num_days = len(days)
  num_employees = len(employees)
  num_shifts = len(shifts)

  model = cp_model.CpModel()

  work = {}
  for e in range(num_employees):
    for s in range(num_shifts):
      for d in days:
        work[e, s, d] = model.NewBoolVar(f'work{e}_{s}_{d}')

  obj_int_vars = []
  obj_int_coeffs = []
  obj_bool_vars = []
  obj_bool_coeffs = []

  for e in range(num_employees):
    for d in days:
      works = [work[e, s, d] for s in range(num_shifts)]
      add_sequence_daily_frequency_constraint(model, works)

  for e in range(num_employees):
    for d in days:
      works = [work[e, s, d] for s in range(num_shifts)]
      add_sequence_length_constraint(model, works, 8, 24)

  for e in range(num_employees):
    for w in range(num_weeks):
      works = [work[e, s, d] for d in daynum_in_month_from_weeknum(days_input, w + 1) for s in range(num_shifts)]
      add_soft_sum_constraint(model, works, 0, 0, 0, 80, 120, 999, f'weekly_sum_constraint(employee {e}, week {w})')

  for e in range(num_employees):
    for w in range(num_weeks):
      temp_list = daynum_in_month_from_weeknum(days_input, w + 1)
      temp_dict = {}
      for d in temp_list:
        temp_dict[e, w, d] = model.NewBoolVar(f'temp{e}_{w}_{d}')
        works = [work[e, s, d] for s in range(num_shifts)]
        boolean_linear_sum(model, works, temp_dict[e, w, d])
      temp_list = [temp_dict[e, w, d] for d in temp_list]
      model.Add(sum(temp_list) <= 5)

  for s in range(num_shifts):
    for d in days:
      works = [work[e, s, d] for e in range(num_employees)]
      min_demand = workloads[d - 1][s]
      worked = model.NewIntVar(min_demand, num_employees, '')
      model.Add(worked == sum(works))
      over_penalty = workloads_penalties[s]
      if over_penalty > 0:
        name = f'excess_demand(shift={s}, day={d})'
        excess = model.NewIntVar(0, num_employees - min_demand, name)
        model.Add(excess == worked - min_demand)
        obj_int_vars.append(excess)
        obj_int_coeffs.append(over_penalty)

  model.Minimize(
      sum(obj_bool_vars[i] * obj_bool_coeffs[i]
          for i in range(len(obj_bool_vars)))
      + sum(obj_int_vars[i] * obj_int_coeffs[i]
            for i in range(len(obj_int_vars))))

  solver = cp_model.CpSolver()
  solver.parameters.num_search_workers = 8
  #solver.parameters.max_time_in_seconds = 10
  solution_printer = VarArraySolutionPrinterWithLimit(50)
  status = solver.SolveWithSolutionCallback(model, solution_printer)

  if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for e in range(num_employees):
      for s in range(num_shifts):
        for d in days:
          solutions_dict['employee'].append(str(e + 1))
          solutions_dict['shift'].append(str(s + 1))
          solutions_dict['day'].append(int(d))
          solutions_dict['week'].append(int(weeknum_from_daynum_in_month(days_input, d)))
          if solver.BooleanValue(work[e, s, d]):
            solutions_dict['value'].append(1)
          else:
            solutions_dict['value'].append(0)

  return(solutions_dict)

solutions = {'employee':[], 'shift':[], 'day':[], 'week': [], 'value': []}
days_temp_input = [d[3] for d in days_input]
solutions = solve_weekly_model(days_temp_input, shifts_input, employees_input, starting_week_hours_worked_input, shifts_workloads_input, excess_cover_penalties_input, solutions)

df_final = pd.DataFrame.from_dict(solutions)
df_final = df_final.groupby(['employee', 'week', 'day']).sum().reset_index()

#print(df_final.pivot(index='day', columns='employee', values='value'))
#df11=df_final.groupby(['employee', 'week'])['value'].apply(lambda x: (x > 0).sum()).reset_index(name='count')
df11=df_final.groupby(['employee', 'week'])['value'].apply(lambda x: (x/2).sum()).reset_index(name='hours')
print(df11.pivot(index='week', columns='employee', values='hours'))
# Print solution.
# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     # employees, weeks, hours
#     print()
#     header = '     '
#     for e in range(num_employees):
#         header += str(e+1) + ' '
#     print(header)
#     for w in range(num_weeks):
#         schedule = ''
#         dayNums = returnDaynumFromWeek(days, w+1)
#         for e in range(num_employees):
#             counter = 0
#             for d in dayNums:
#                 for s in range(num_shifts):
#                     if solver.BooleanValue(work[e, s, d]):
#                       counter += 1
#             schedule += str(counter) + ' '
#         print(f'{w}: {schedule}')
#     print()
#     print()
#     print()


#     # employees, shifts, days
#     print()
#     header = '     '
#     for e in range(num_employees):
#         header += str(e+1) + ' '
#     print(header)
#     for d in range(num_days):
#         for s in range(num_shifts):
#           schedule = ''
#           for e in range(num_employees):
#             if solver.BooleanValue(work[e, s, d]):
#               schedule += '1 '
#             else:
#               schedule += '0 '
#           print(f'{d}-{s}: {schedule}')
#     print()
#     """
#     print('Penalties:')
#     for i, var in enumerate(obj_bool_vars):
#         if solver.BooleanValue(var):
#             penalty = obj_bool_coeffs[i]
#             if penalty > 0:
#                 print('  %s violated, penalty=%i' % (var.Name(), penalty))
#             else:
#                 print('  %s fulfilled, gain=%i' % (var.Name(), -penalty))

#     for i, var in enumerate(obj_int_vars):
#         if solver.Value(var) > 0:
#             print('  %s violated by %i, linear penalty=%i' %
#                   (var.Name(), solver.Value(var), obj_int_coeffs[i]))
#     """
# print()
# print(solver.ResponseStats())
