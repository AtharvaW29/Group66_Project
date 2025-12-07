from pathlib import Path
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots

basic_path = Path("CSCI570_Project_Minimum_Jul_14/Output")
efficient_path = Path("CSCI570_Project_Minimum_Jul_14/EfficientOutput")


def extract_file_number(filename):
    """Extract numeric part from filename for sorting"""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def read_output_files(file_paths):
    """Read output files and return sorted data"""
    data = []

    for file_path in file_paths:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) >= 5:
                cost = float(lines[0])
                str1 = lines[1]
                str2 = lines[2]
                time_ms = float(lines[3])
                memory_kb = float(lines[4])

                # Calculate problem size
                size = len(str1) + len(str2)

                data.append({
                    'file': file_path.name,
                    'file_num': extract_file_number(file_path.name),
                    'cost': cost,
                    'str1': str1,
                    'str2': str2,
                    'len1': len(str1),
                    'len2': len(str2),
                    'size': size,
                    'time_ms': time_ms,
                    'memory_kb': memory_kb
                })

    # Sort by problem size
    data.sort(key=lambda x: x['size'])
    return data


def main():
    pattern = re.compile(r"^outputin\d+\.txt$")

    basic_files = [file_path for file_path in basic_path.iterdir()
                   if file_path.is_file() and pattern.match(file_path.name)]

    efficient_files = [file_path for file_path in efficient_path.iterdir()
                       if file_path.is_file() and pattern.match(file_path.name)]

    if not basic_files:
        print(f"No basic output files found in {basic_path}")
        return

    if not efficient_files:
        print(f"No efficient output files found in {efficient_path}")
        return

    # Read and sort data
    basic_data = read_output_files(basic_files)
    efficient_data = read_output_files(efficient_files)

    # Match data points by size
    # Assuming both basic and efficient have the same test cases
    min_length = min(len(basic_data), len(efficient_data))
    basic_data = basic_data[:min_length]
    efficient_data = efficient_data[:min_length]

    # Extract data for plotting
    problem_sizes = [d['size'] for d in basic_data]
    size_labels = [f"{d['len1']}+{d['len2']}" for d in basic_data]

    basic_times = [d['time_ms'] for d in basic_data]
    efficient_times = [d['time_ms'] for d in efficient_data]

    basic_memory = [d['memory_kb'] for d in basic_data]
    efficient_memory = [d['memory_kb'] for d in efficient_data]

    basic_costs = [d['cost'] for d in basic_data]
    efficient_costs = [d['cost'] for d in efficient_data]

    # Print summary
    print(f"\n{'=' * 80}")
    print("DATA SUMMARY (sorted by problem size)")
    print(f"{'=' * 80}")
    print(f"{'Index':<8} {'Size':<12} {'Basic Time':<15} {'Eff Time':<15} {'Basic Mem':<15} {'Eff Mem':<15}")
    print(f"{'-' * 80}")
    for i in range(len(basic_data)):
        print(f"{i + 1:<8} {size_labels[i]:<12} {basic_times[i]:<15.2f} {efficient_times[i]:<15.2f} "
              f"{basic_memory[i]:<15.0f} {efficient_memory[i]:<15.0f}")
    print(f"{'=' * 80}\n")

    # Verify costs match
    cost_mismatches = sum(1 for i in range(len(basic_data)) if basic_costs[i] != efficient_costs[i])
    if cost_mismatches > 0:
        print(f"⚠️  WARNING: {cost_mismatches} cost mismatches found between basic and efficient!")
    else:
        print("✓ All costs match between basic and efficient versions")

    # ------------------------- PLOT 1: TIME COMPARISON -------------------------
    time_fig = go.Figure()

    time_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(basic_times) + 1)),
            y=basic_times,
            mode="lines+markers",
            name="Basic Times",
            line=dict(color='blue', width=2),
            marker=dict(size=8),
            hovertemplate='<b>Test %{x}</b><br>' +
                          'Size: ' + '%{text}<br>' +
                          'Time: %{y:.2f} ms<br>' +
                          '<extra></extra>',
            text=size_labels
        )
    )

    time_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(efficient_times) + 1)),
            y=efficient_times,
            mode="lines+markers",
            name="Efficient Times",
            line=dict(color='red', width=2),
            marker=dict(size=8),
            hovertemplate='<b>Test %{x}</b><br>' +
                          'Size: ' + '%{text}<br>' +
                          'Time: %{y:.2f} ms<br>' +
                          '<extra></extra>',
            text=size_labels
        )
    )

    time_fig.update_layout(
        title={
            'text': "Basic vs Efficient — Execution Time Comparison",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Test Case Index (sorted by problem size)",
        yaxis_title="Time (ms)",
        template="plotly_white",
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    time_fig.show()

    # ------------------------- PLOT 2: MEMORY COMPARISON -------------------------
    mem_fig = go.Figure()

    mem_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(basic_memory) + 1)),
            y=basic_memory,
            mode="lines+markers",
            name="Basic Memory",
            line=dict(color='blue', width=2),
            marker=dict(size=8),
            hovertemplate='<b>Test %{x}</b><br>' +
                          'Size: ' + '%{text}<br>' +
                          'Memory: %{y:.0f} KB<br>' +
                          '<extra></extra>',
            text=size_labels
        )
    )

    mem_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(efficient_memory) + 1)),
            y=efficient_memory,
            mode="lines+markers",
            name="Efficient Memory",
            line=dict(color='red', width=2),
            marker=dict(size=8),
            hovertemplate='<b>Test %{x}</b><br>' +
                          'Size: ' + '%{text}<br>' +
                          'Memory: %{y:.0f} KB<br>' +
                          '<extra></extra>',
            text=size_labels
        )
    )

    mem_fig.update_layout(
        title={
            'text': "Basic vs Efficient — Memory Usage Comparison",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Test Case Index (sorted by problem size)",
        yaxis_title="Memory (KB depending on type ×10³ = MB)",
        template="plotly_white",
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    mem_fig.show()

    # ------------------------- PLOT 3: COMBINED VIEW (2x1 SUBPLOTS) -------------------------
    combined_fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Execution Time Comparison", "Memory Usage Comparison"),
        vertical_spacing=0.12
    )

    # Add time traces
    combined_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(basic_times) + 1)),
            y=basic_times,
            mode="lines+markers",
            name="Basic Times",
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ),
        row=1, col=1
    )

    combined_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(efficient_times) + 1)),
            y=efficient_times,
            mode="lines+markers",
            name="Efficient Times",
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ),
        row=1, col=1
    )

    # Add memory traces
    combined_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(basic_memory) + 1)),
            y=basic_memory,
            mode="lines+markers",
            name="Basic Memory",
            line=dict(color='blue', width=2),
            marker=dict(size=6),
            showlegend=False
        ),
        row=2, col=1
    )

    combined_fig.add_trace(
        go.Scatter(
            x=list(range(1, len(efficient_memory) + 1)),
            y=efficient_memory,
            mode="lines+markers",
            name="Efficient Memory",
            line=dict(color='red', width=2),
            marker=dict(size=6),
            showlegend=False
        ),
        row=2, col=1
    )

    combined_fig.update_xaxes(title_text="Test Case Index (sorted by problem size)", row=1, col=1)
    combined_fig.update_xaxes(title_text="Test Case Index (sorted by problem size)", row=2, col=1)
    combined_fig.update_yaxes(title_text="Time (ms)", row=1, col=1)
    combined_fig.update_yaxes(title_text="Memory (KB)", row=2, col=1)

    combined_fig.update_layout(
        title={
            'text': "Basic vs Efficient Algorithm Comparison",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=800,
        template="plotly_white",
        showlegend=True
    )
    combined_fig.show()

    # ------------------------- PLOT 4: TIME vs PROBLEM SIZE -------------------------
    size_time_fig = go.Figure()

    size_time_fig.add_trace(
        go.Scatter(
            x=problem_sizes,
            y=basic_times,
            mode="lines+markers",
            name="Basic Times",
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        )
    )

    size_time_fig.add_trace(
        go.Scatter(
            x=problem_sizes,
            y=efficient_times,
            mode="lines+markers",
            name="Efficient Times",
            line=dict(color='red', width=2),
            marker=dict(size=8)
        )
    )

    size_time_fig.update_layout(
        title={
            'text': "Execution Time vs Problem Size",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Problem Size (m + n)",
        yaxis_title="Time (ms)",
        template="plotly_white",
        hovermode='x unified'
    )
    size_time_fig.show()

    # ------------------------- PLOT 5: MEMORY vs PROBLEM SIZE -------------------------
    size_mem_fig = go.Figure()

    size_mem_fig.add_trace(
        go.Scatter(
            x=problem_sizes,
            y=basic_memory,
            mode="lines+markers",
            name="Basic Memory",
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        )
    )

    size_mem_fig.add_trace(
        go.Scatter(
            x=problem_sizes,
            y=efficient_memory,
            mode="lines+markers",
            name="Efficient Memory",
            line=dict(color='red', width=2),
            marker=dict(size=8)
        )
    )

    size_mem_fig.update_layout(
        title={
            'text': "Memory Usage vs Problem Size",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Problem Size (m + n)",
        yaxis_title="Memory (KB)",
        template="plotly_white",
        hovermode='x unified'
    )
    size_mem_fig.show()

    # ------------------------- STATISTICS -------------------------
    print(f"\n{'=' * 80}")
    print("PERFORMANCE STATISTICS")
    print(f"{'=' * 80}")

    avg_basic_time = sum(basic_times) / len(basic_times)
    avg_efficient_time = sum(efficient_times) / len(efficient_times)

    avg_basic_mem = sum(basic_memory) / len(basic_memory)
    avg_efficient_mem = sum(efficient_memory) / len(efficient_memory)

    print(f"Average Basic Time:      {avg_basic_time:.2f} ms")
    print(f"Average Efficient Time:  {avg_efficient_time:.2f} ms")
    print(f"Time Ratio (Eff/Basic):  {avg_efficient_time / avg_basic_time:.2f}x")
    print()
    print(f"Average Basic Memory:    {avg_basic_mem:.0f} KB")
    print(f"Average Efficient Memory:{avg_efficient_mem:.0f} KB")
    print(f"Memory Ratio (Eff/Basic):{avg_efficient_mem / avg_basic_mem:.2f}x")
    print(f"Memory Saved:            {avg_basic_mem - avg_efficient_mem:.0f} KB "
          f"({(1 - avg_efficient_mem / avg_basic_mem) * 100:.1f}%)")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()