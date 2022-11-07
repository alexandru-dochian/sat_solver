# Logs format
```
{
    "heuristic" : 1, // // 1(default), 2, 3
    "execution_time" : 666, // ms
    "input_file" : "xxx",
    
    // OPTIONAL
    "history_on_solution_path" : [
        {
            "number_of_clauses_history" : [],
            "number_of_literals_history" : [],
        }
    ],
    "number_of_nodes_on_each_level: {
        "0" : 1,
        "1" : 2,
        "2" : 4,
        ...
        "9" : 14,
    }
}
```