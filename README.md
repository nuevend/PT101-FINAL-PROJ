# CPU SCHEDULING PROGRAM

## 1. Project Description

CPU Scheduling is a Python program that demonstrates how a CPU manages and executes different processes. It allows users to enter process information, select a scheduling algorithm, and view the scheduling results.

## 2. Main Features

- Supports FCFS, SJF, SRTF, and Round Robin.
- Allows users to enter process information.
- Displays a Gantt Chart.
- Calculates Completion Time, Turnaround Time, Waiting Time, and Response Time.
- Displays average scheduling results.
- Compares the four scheduling algorithms.

## 3. User Guide

### A. Execution (How to Run the Program)

1. Open Visual Studio Code or any Python editor.
2. Open the project folder.
3. Open the Python file named `cpu_scheduling.py`.
4. Open the terminal.
5. Type the following command:
 **`python cpu_scheduling.py`**
6. Press Enter to run the program.
7. The CPU Scheduling menu will appear on the screen.

### B. Step-by-Step Process (How to Use the Program)

**Step 1: Choose a Scheduling Algorithm**

Select one option from the menu:

- 1 – FCFS
- 2 – SJF
- 3 – SRTF
- 4 – Round Robin
- 5 – Compare Algorithms
- 6 – Exit

**Step 2: Enter the Number of Processes**

Enter the total number of processes you want to schedule.

Example: `3`

**Step 3: Enter the Process Information**

For each process, enter the following:

- Process ID – Name or identification of the process (example: P1).
- Arrival Time – Time when the process arrives.
- Burst Time – CPU time required by the process.

Example:

| Process ID | Arrival Time | Burst Time |
|------------|-------------:|-----------:|
| P1         | 0            | 5          |
| P2         | 1            | 3          |
| P3         | 2            | 4          |

**Step 4: Enter the Time Quantum (If Required)**

If you choose Round Robin or Compare Algorithms, enter a time quantum greater than zero.

Example: `2`

**Step 5: View the Results**

The program will display the Gantt Chart and scheduling computations for the selected algorithm.

**Step 6: Choose What to Do Next**

After viewing the results:

- Enter `Y` to use the same processes with another scheduling algorithm.
- Enter `N` to stop using the program.

### C. Inputs (Information Needed)

The program requires:

- Scheduling Algorithm
- Number of Processes
- Process ID
- Arrival Time (0 or greater)
- Burst Time (greater than 0)
- Time Quantum (greater than 0, when required)

### D. Output Interpretation (Understanding the Results)

- **Gantt Chart** – Shows the order and execution time of processes.
- **AT (Arrival Time)** – When the process arrives.
- **BT (Burst Time)** – CPU time needed by the process.
- **CT (Completion Time)** – When the process finishes.
- **TAT (Turnaround Time)** – Total time from arrival until completion.
- **WT (Waiting Time)** – Total time the process waits.
- **RT (Response Time)** – Time from arrival until its first execution.
- **Average Results** – Shows the average waiting time, turnaround time, and response time.
- **Algorithm Comparison** – Shows the average results of all four scheduling algorithms.
