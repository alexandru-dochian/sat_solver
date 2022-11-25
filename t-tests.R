
#4x4 t-tests
df4 = read.csv("C:/Users/Domantas/Desktop/VU AI/knowledge representation/sat_solver/sudoku4x4_results_expirement2.csv")
df4 = df4[df4$heuristic != 'h1',]

df4$heuristic <- as.factor(df4$heuristic)
unique(df4$heuristic)


t_test4_dpll_jw1 = t.test(df4[df4$heuristic == 'h2',]$number_of_backtracks  ,df4[df4$heuristic == 'jw_one_sided',]$number_of_backtracks, alternative = 'greater' )
print(t_test4_dpll_jw1)

t_test4_dpll_jw2 = t.test(df4[df4$heuristic == 'h2',]$number_of_backtracks  ,df4[df4$heuristic == 'jw_two_sided',]$number_of_backtracks, alternative = 'greater' )
print(t_test4_dpll_jw2)

t_test4_jw1_jw2 = t.test(df4[df4$heuristic == 'jw_one_sided',]$number_of_backtracks, df4[df4$heuristic == 'jw_two_sided',]$number_of_backtracks, alternative = 'greater' )
print(t_test4_jw1_jw2)





#for 9x9
df9 = read.csv("C:/Users/Domantas/Desktop/VU AI/knowledge representation/sat_solver/sudoku9x9_results_expirement2.csv")

df9$heuristic <- as.factor(df9$heuristic)
unique(df9$heuristic)



t_test9_dpll_jw1 = t.test(df9[df9$heuristic == 'h2',]$number_of_backtracks  ,df9[df9$heuristic == 'jw_one_sided',]$number_of_backtracks, alternative = 'greater' )
print(t_test9_dpll_jw1)

t_test9_dpll_jw2 = t.test(df9[df9$heuristic == 'jw_two_sided',]$number_of_backtracks, df9[df9$heuristic == 'h2',]$number_of_backtracks, alternative = 'greater' )
print(t_test9_dpll_jw2)

t_test9_jw1_jw2 = t.test(df9[df9$heuristic == 'jw_two_sided',]$number_of_backtracks, df9[df9$heuristic == 'jw_one_sided',]$number_of_backtracks, alternative = 'greater' )
print(t_test9_jw1_jw2)



