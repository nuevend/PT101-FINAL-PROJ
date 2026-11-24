from dataclasses import dataclass
from collections import deque

# ==========================================
# DATA STRUCTURES
# ==========================================

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    order: int

@dataclass
class Segment:
    pid: str
    start: int
    end: int
    remaining: int = None

# ==========================================
# USER INPUT
# ==========================================

def get_processes():
    while True:
        try:
            count = int(input("\nEnter Number of Processes: "))
            if count > 0:
                break
            print("Number of processes must be at least 1.")
        except ValueError:
            print("Please enter a valid number.")

    processes = []
    used_ids = set()

    for i in range(count):
        print(f"\nProcess {i + 1}")

        while True:
            pid = input(
                f"Process ID (default P{i + 1}): "
            ).strip()

            if not pid:
                pid = f"P{i + 1}"

            if pid not in used_ids:
                used_ids.add(pid)
                break

            print("Process ID already exists.")

        while True:
            try:
                arrival = int(input("Arrival Time: "))
                if arrival >= 0:
                    break
                print("Arrival time cannot be negative.")
            except ValueError:
                print("Enter a valid number.")

        while True:
            try:
                burst = int(input("Burst Time: "))
                if burst > 0:
                    break
                print("Burst time must be greater than zero.")
            except ValueError:
                print("Enter a valid number.")

        processes.append(
            Process(pid, arrival, burst, i)
        )

    return processes

def get_time_quantum():
    while True:
        try:
            quantum = int(input("\nTime Quantum: "))
            if quantum > 0:
                return quantum
            print("Time quantum must be greater than zero.")
        except ValueError:
            print("Enter a valid number.")

# ==========================================
# METRICS
# ==========================================

def new_metrics(processes):
    return {
        p.pid: {
            "CT": 0,
            "TAT": 0,
            "WT": 0,
            "RT": 0,
            "first_start": None
        }
        for p in processes
    }

def finish_metrics(processes, metrics):

    for p in processes:
        row = metrics[p.pid]

        row["TAT"] = row["CT"] - p.arrival
        row["WT"] = row["TAT"] - p.burst
        row["RT"] = row["first_start"] - p.arrival

    return metrics

def add_segment(timeline, pid, start, end):

    if end <= start:
        return

    if (
        timeline
        and timeline[-1].pid == pid
        and timeline[-1].end == start
        and timeline[-1].remaining is None
    ):
        timeline[-1].end = end

    else:
        timeline.append(
            Segment(pid, start, end)
        )

# ==========================================
# 1. FIRST COME FIRST SERVED (FCFS)
# ==========================================

def simulate_fcfs(processes):

    metrics = new_metrics(processes)
    timeline = []
    time = 0

    ordered = sorted(
        processes,
        key=lambda p: (p.arrival, p.order)
    )

    for p in ordered:

        if time < p.arrival:
            add_segment(
                timeline, "IDLE", time, p.arrival
            )
            time = p.arrival

        start = time

        metrics[p.pid]["first_start"] = start

        time += p.burst

        metrics[p.pid]["CT"] = time

        add_segment(
            timeline, p.pid, start, time
        )

    return finish_metrics(processes, metrics), timeline

# ==========================================
# 2. SHORTEST JOB FIRST (SJF)
# NON-PREEMPTIVE
# ==========================================

def simulate_sjf(processes):

    metrics = new_metrics(processes)
    timeline = []

    completed = set()
    time = 0
    n = len(processes)

    while len(completed) < n:

        ready = [
            p for p in processes
            if p.pid not in completed
            and p.arrival <= time
        ]

        if not ready:

            next_arrival = min(
                p.arrival
                for p in processes
                if p.pid not in completed
            )

            add_segment(
                timeline, "IDLE", time, next_arrival
            )

            time = next_arrival
            continue

        p = min(
            ready,
            key=lambda x: (
                x.burst,
                x.arrival,
                x.order
            )
        )

        start = time

        metrics[p.pid]["first_start"] = start

        time += p.burst

        metrics[p.pid]["CT"] = time

        completed.add(p.pid)

        add_segment(
            timeline, p.pid, start, time
        )

    return finish_metrics(processes, metrics), timeline

# ==========================================
# 3. SHORTEST REMAINING TIME FIRST (SRTF)
# PREEMPTIVE
# ==========================================

def simulate_srtf(processes):

    metrics = new_metrics(processes)
    timeline = []

    remaining = {
        p.pid: p.burst for p in processes
    }

    completed = set()
    time = 0
    n = len(processes)

    while len(completed) < n:

        ready = [
            p for p in processes
            if p.pid not in completed
            and p.arrival <= time
            and remaining[p.pid] > 0
        ]

        if not ready:

            next_arrival = min(
                p.arrival
                for p in processes
                if p.pid not in completed
            )
            add_segment(
                timeline, "IDLE", time, next_arrival
            )

            time = next_arrival
            continue

        p = min(
            ready,
            key=lambda x: (
                remaining[x.pid],
                x.arrival,
                x.order
            )
        )

        if metrics[p.pid]["first_start"] is None:
            metrics[p.pid]["first_start"] = time

        start = time

        time += 1
        remaining[p.pid] -= 1

        add_segment(
            timeline, p.pid, start, time
        )

        if remaining[p.pid] == 0:

            metrics[p.pid]["CT"] = time

            completed.add(p.pid)

    return finish_metrics(processes, metrics), timeline

# ==========================================
# 4. ROUND ROBIN (RR)
# PREEMPTIVE
# ==========================================

def simulate_round_robin(processes, quantum):

    metrics = new_metrics(processes)
    timeline = []

    remaining = {
        p.pid: p.burst for p in processes
    }

    ordered = sorted(
        processes,
        key=lambda p: (p.arrival, p.order)
    )

    ready_queue = deque()

    time = 0
    next_process = 0
    completed = set()
    n = len(processes)

    while len(completed) < n:

        if not ready_queue:

            if (
                next_process < n
                and time < ordered[next_process].arrival
            ):

                next_arrival = ordered[next_process].arrival

                add_segment(
                    timeline, "IDLE", time, next_arrival
                )

                time = next_arrival

            while (
                next_process < n
                and ordered[next_process].arrival <= time
            ):

                ready_queue.append(
                    ordered[next_process].pid
                )

                next_process += 1

            if not ready_queue:
                continue

        pid = ready_queue.popleft()

        start = time

        if metrics[pid]["first_start"] is None:
            metrics[pid]["first_start"] = start

        run_time = min(
            quantum,
            remaining[pid]
        )

        time += run_time

        remaining[pid] -= run_time

        # Record every Round Robin time slice
        timeline.append(
            Segment(
                pid,
                start,
                time,
                remaining[pid]
            )
        )

        # Add newly arrived processes
        while (
            next_process < n
            and ordered[next_process].arrival <= time
        ):

            ready_queue.append(
                ordered[next_process].pid
            )

            next_process += 1

        if remaining[pid] == 0:

            metrics[pid]["CT"] = time

            completed.add(pid)

        else:

            ready_queue.append(pid)

    return finish_metrics(processes, metrics), timeline

# ==========================================
# GANTT CHART
# ==========================================

def print_gantt_chart(timeline):

    print("\nGantt Chart\n")

    if not timeline:
        print("No execution segments.")
        return

    width = 6

    top = " " + ("-" * (width + 2)) * len(timeline)

    middle = "|" + "|".join(
        f" {s.pid:^{width}} "
        for s in timeline
    ) + "|"

    print(top)
    print(middle)
    print(top)

    boundaries = (
        [timeline[0].start]
        + [s.end for s in timeline]
    )

    print("    ".join(str(t) for t in boundaries))

    # Display Round Robin remaining burst time
    if any(s.remaining is not None for s in timeline):

        print("\nRound Robin Execution Details")

        print(
            f"{'Process':<12}"
            f"{'Start':<10}"
            f"{'End':<10}"
            f"{'Remaining BT':<15}"
        )

        for s in timeline:

            print(
                f"{s.pid:<12}"
                f"{s.start:<10}"
                f"{s.end:<10}"
                f"{s.remaining:<15}"
            )

# ==========================================
# PROCESS COMPUTATION TABLE
# ==========================================

def print_metrics_table(processes, metrics):

    print("\nProcess Computation Table\n")

    print(
        f"{'Process':<10}"
        f"{'AT':>6}"
        f"{'BT':>6}"
        f"{'CT':>6}"
        f"{'TAT':>7}"
        f"{'WT':>7}"
        f"{'RT':>7}"
    )

    print("-" * 49)

    for p in sorted(
        processes,
        key=lambda x: x.order
    ):

        m = metrics[p.pid]

        print(
            f"{p.pid:<10}"
            f"{p.arrival:>6}"
            f"{p.burst:>6}"
            f"{m['CT']:>6}"
            f"{m['TAT']:>7}"
            f"{m['WT']:>7}"
            f"{m['RT']:>7}"
        )

    count = len(processes)

    avg_tat = sum(
        metrics[p.pid]["TAT"]
        for p in processes
    ) / count

    avg_wt = sum(
        metrics[p.pid]["WT"]
        for p in processes
    ) / count

    avg_rt = sum(
        metrics[p.pid]["RT"]
        for p in processes
    ) / count

    print("\nAverage Waiting Time    : {:.2f}".format(avg_wt))
    print("Average Turnaround Time : {:.2f}".format(avg_tat))
    print("Average Response Time   : {:.2f}".format(avg_rt))

# ==========================================
# RUN SELECTED ALGORITHM
# ==========================================

def run_algorithm(name, processes, quantum=None):

    print("\n" + "=" * 55)
    print("CPU SCHEDULING -", name)

    if name == "ROUND ROBIN":
        print("Time Quantum:", quantum)

    print("=" * 55)

    if name == "FCFS":

        metrics, timeline = simulate_fcfs(processes)

    elif name == "SJF":

        metrics, timeline = simulate_sjf(processes)

    elif name == "SRTF":

        metrics, timeline = simulate_srtf(processes)

    else:

        metrics, timeline = simulate_round_robin(
            processes, quantum
        )

    print_gantt_chart(timeline)

    print_metrics_table(
        processes, metrics
    )

    return metrics

# ==========================================
# COMPARE ALL ALGORITHMS
# ==========================================

def compare_all(processes, quantum):

    algorithms = [
        ("FCFS", simulate_fcfs(processes)),
        ("SJF", simulate_sjf(processes)),
        ("SRTF", simulate_srtf(processes)),
        (
            "ROUND ROBIN",
            simulate_round_robin(processes, quantum)
        )
    ]

    print("\n" + "=" * 65)
    print("COMPARISON OF CPU SCHEDULING ALGORITHMS")
    print("=" * 65)

    print(
        f"{'Algorithm':<18}"
        f"{'Avg TAT':>14}"
        f"{'Avg WT':>14}"
        f"{'Avg RT':>14}"
    )

    print("-" * 60)

    for name, (metrics, timeline) in algorithms:

        count = len(processes)

        avg_tat = sum(
            metrics[p.pid]["TAT"]
            for p in processes
        ) / count

        avg_wt = sum(
            metrics[p.pid]["WT"]
            for p in processes
        ) / count

        avg_rt = sum(
            metrics[p.pid]["RT"]
            for p in processes
        ) / count

        print(
            f"{name:<18}"
            f"{avg_tat:>14.2f}"
            f"{avg_wt:>14.2f}"
            f"{avg_rt:>14.2f}"
        )

# ==========================================
# ALGORITHM MENU
# ==========================================

def display_menu():

    print("\n" + "=" * 50)
    print("             CPU SCHEDULING SIMULATOR")
    print("=" * 50)

    print("\n1. FCFS")
    print("2. SJF")
    print("3. SRTF")
    print("4. Round Robin")
    print("5. Compare Algorithms")
    print("6. Exit")

# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    # STEP 1: Select algorithm first
    display_menu()

    choice = input("\nSelect Algorithm: ").strip()

    if choice == "6":

        print("\nThank you for using the CPU Scheduling Simulator!")
        return

    while choice not in ["1", "2", "3", "4", "5"]:

        print("\nInvalid selection.")

        choice = input("Select Algorithm: ").strip()

        if choice == "6":
            print("\nProgram terminated.")
            return

    # STEP 2: Enter process information only once
    processes = get_processes()

    # STEP 3: Run selected algorithms
    while True:

        quantum = None

        if choice in ["4", "5"]:
            quantum = get_time_quantum()

        if choice == "1":
            run_algorithm("FCFS", processes)

        elif choice == "2":
            run_algorithm("SJF", processes)

        elif choice == "3":
            run_algorithm("SRTF", processes)

        elif choice == "4":
            run_algorithm(
                "ROUND ROBIN",
                processes,
                quantum
            )

        elif choice == "5":

            compare_all(
                processes,
                quantum
            )

        # STEP 4: Ask whether to reuse processes
        print("\n" + "=" * 50)

        answer = input(
            "\nUse the same processes with another algorithm? (Y/N): "
        ).strip().upper()

        if answer == "N":

            print(
                "\nThank you for using the CPU Scheduling Simulator!"
            )
            break

        elif answer == "Y":

            # STEP 5: Return to algorithm selection
            display_menu()

            choice = input(
                "\nSelect Another Algorithm: "
            ).strip()

            if choice == "6":

                print(
                    "\nThank you for using the CPU Scheduling Simulator!"
                )
                break

            while choice not in ["1", "2", "3", "4", "5"]:

                print("\nInvalid selection.")

                choice = input(
                    "Select Another Algorithm: "
                ).strip()

                if choice == "6":
                    print("\nProgram terminated.")
                    return

        else:

            print("\nPlease enter Y or N.")

# ==========================================
# PROGRAM EXECUTION
# ==========================================

if __name__ == "__main__":

    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram ended.")
