from pathlib import Path
import re
import plotly.graph_objects as go


basic_path = Path("CSCI570_Project_Minimum_Jul_14/Output")
efficient_path =Path("CSCI570_Project_Minimum_Jul_14/EfficientOutput")

def main():
        pattern = re.compile(r"^outputin\d+\.txt$")

        basic_files = [file_path for file_path in basic_path.iterdir()
                       if file_path.is_file() and pattern.match(file_path.name)]

        efficient_files = [file_path for file_path in efficient_path.iterdir()
                       if file_path.is_file() and pattern.match(file_path.name)]

        basic_times = [0.0] * (len(basic_files) + 1)
        efficient_times = [0.0] * (len(efficient_files) + 1)

        basic_memory = [0.0] * (len(basic_files) + 1)
        efficient_memory = [0.0] * (len(efficient_files) + 1)

        basic_costs = [0.0] * (len(basic_files) + 1)
        efficient_costs = [0.0] * (len(efficient_files) + 1)

        basic_strings1 = [""] * (len(basic_files) + 1)
        efficient_strings1 = [""] * (len(efficient_files) + 1)

        basic_strings2 = [""] * (len(basic_files) + 1)
        efficient_strings2 = [""] * (len(efficient_files) + 1)

        for basic_file in basic_files:
            with open(basic_file, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                cost = lines[0]
                str1 = lines[1]
                str2 = lines[2]
                time_ms = lines[3]
                mem = lines[4]
                basic_times.append(float(time_ms))
                basic_memory.append(float(mem))
                basic_costs.append(float(cost))
                basic_strings1.append(str(str1))
                basic_strings2.append(str(str2))

        for efficient_file in efficient_files:
            with open(efficient_file, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                cost = lines[0]
                str1 = lines[1]
                str2 = lines[2]
                time_ms = lines[3]
                mem = lines[4]
                efficient_times.append(float(time_ms))
                efficient_memory.append(float(mem))
                efficient_costs.append(float(cost))
                efficient_strings1.append(str(str1))
                efficient_strings2.append(str(str2))

        basic_times_clean = [t for t in basic_times if t != 0.0]
        efficient_times_clean = [t for t in efficient_times if t != 0.0]

        basic_memory_clean = [m for m in basic_memory if m != 0.0]
        efficient_memory_clean = [m for m in efficient_memory if m != 0.0]

        n = min(len(basic_times_clean), len(efficient_times_clean))
        basic_times_clean = basic_times_clean[:n]
        efficient_times_clean = efficient_times_clean[:n]

        m = min(len(basic_memory_clean), len(efficient_memory_clean))
        basic_memory_clean = basic_memory_clean[:m]
        efficient_memory_clean = efficient_memory_clean[:m]

        # ------------------------- PLOT 1: TIME COMPARISON -------------------------
        time_fig = go.Figure()

        time_fig.add_trace(
            go.Scatter(
                x=list(range(1, n + 1)),
                y=basic_times_clean,
                mode="lines+markers",
                name="Basic Times"
            )
        )

        time_fig.add_trace(
            go.Scatter(
                x=list(range(1, n + 1)),
                y=efficient_times_clean,
                mode="lines+markers",
                name="Efficient Times"
            )
        )

        time_fig.update_layout(
            title="Basic vs Efficient — Execution Time Comparison",
            xaxis_title="Test Case Index",
            yaxis_title="Time (ms)",
            template="plotly_white",
        )
        time_fig.show()

        # ------------------------- PLOT 2: MEMORY COMPARISON -------------------------
        mem_fig = go.Figure()

        mem_fig.add_trace(
            go.Scatter(
                x=list(range(1, m + 1)),
                y=basic_memory_clean,
                mode="lines+markers",
                name="Basic Memory"
            )
        )

        mem_fig.add_trace(
            go.Scatter(
                x=list(range(1, m + 1)),
                y=efficient_memory_clean,
                mode="lines+markers",
                name="Efficient Memory"
            )
        )

        mem_fig.update_layout(
            title="Basic vs Efficient — Memory Usage Comparison",
            xaxis_title="Test Case Index",
            yaxis_title="Memory (MB or KB depending on your output)",
            template="plotly_white",
        )
        mem_fig.show()


if __name__ == "__main__":
    main()