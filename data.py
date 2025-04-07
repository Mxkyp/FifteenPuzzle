import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_data(file_path):
    """Load data from the results file."""
    return pd.read_csv(file_path, sep=r'\s+')


def create_chart(data, strategy, metric, chart_title, filename, use_log_scale=False, filter_invalid=False):
    """Generic function to create bar charts for any strategy and metric."""
    # Define color mapping for parameters
    color_map = {
        # BFS/DFS direction parameters
        'rdul': '#2521ff',
        'rdlu': '#575555',
        'drul': '#03b300',
        'drlu': '#ff584f',
        'ludr': '#d764fa',
        'lurd': '#fff200',
        'uldr': '#ff00b3',
        'ulrd': '#00ffee',
        # A* heuristics
        'hamm': '#a44fff',
        'manh': '#3cface',

        'bfs': '#9000ff',
        'dfs': '#00ff99',
        'astr': '#ff6e69',
    }

    # Define label mapping for legend
    label_map = {
        'rdul': 'RDUL',
        'rdlu': 'RDLU',
        'drul': 'DRUL',
        'drlu': 'DRLU',
        'ludr': 'LUDR',
        'lurd': 'LURD',
        'uldr': 'ULDR',
        'ulrd': 'ULRD',
        'hamm': 'Hamming',
        'manh': 'Manhattan',
        'bfs': 'BFS',
        'dfs': 'DFS',
        'astr': 'A*'
    }

    # Filter data for the specific strategy (if provided)
    if strategy:
        strategy_data = data[data['Strategy'] == strategy]
    else:
        strategy_data = data  # For comparison charts

    # Get unique parameters and depths
    if strategy:
        params = sorted(strategy_data['Param'].unique())
        bar_width = 0.2 if strategy == 'astr' else 0.1
    else:
        params = sorted(strategy_data['Strategy'].unique())
        bar_width = 0.2

    depths = sorted(strategy_data['Depth'].unique())

    # Create figure
    plt.figure(figsize=(12, 7))
    positions = np.arange(len(depths))

    # Plot data for each parameter
    for i, param in enumerate(params):
        if strategy:
            param_data = strategy_data[strategy_data['Param'] == param]
        else:
            param_data = strategy_data[strategy_data['Strategy'] == param]

        # Calculate average values for each depth
        avg_values = []
        for depth in depths:
            depth_data = param_data[param_data['Depth'] == depth]

            if filter_invalid and metric == 'SolutionLength':
                valid_data = depth_data[depth_data['SolutionLength'] > 0]
                avg_values.append(valid_data[metric].mean() if len(valid_data) > 0 else 0)
            else:
                avg_values.append(depth_data[metric].mean())

        # Get param label for legend (uppercase or custom label)
        param_key = param.lower()  # Case-insensitive lookup
        param_label = label_map.get(param_key, param)

        # Draw bars with specified color if available
        pos = positions + (i - len(params) / 2 + 0.5) * bar_width
        color = color_map.get(param_key, None)  # Use mapped color or None for default
        plt.bar(pos, avg_values, width=bar_width, label=param_label, color=color)

    # Set chart properties
    metric_labels = {
        'SolutionLength': 'Średnia długość rozwiązania',
        'Visited': 'Średnia liczba odwiedzonych stanów',
        'Processed': 'Średnia liczba przetworzonych stanów',
        'Depth': 'Średni maksymalny poziom rekursji',
        'Time': 'Średni czas rozwiązania [s]'
    }

    plt.title(chart_title)
    plt.xlabel('Możliwa najkrótsza długość rozwiązania')
    plt.ylabel(metric_labels.get(metric, ''))
    plt.xticks(positions, depths)

    if use_log_scale:
        plt.yscale('log')

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(filename)
    plt.close()


def create_all_charts(data):
    """Create all charts for all strategies and comparisons."""
    strategy_names = {'bfs': 'BFS', 'dfs': 'DFS', 'astr': 'A*'}
    metrics = {
        'SolutionLength': 'średnia_dlugosc_rozwiazania',
        'Visited': 'średnia_liczba_odwiedzonych_stanow',
        'Processed': 'średnia_liczba_przetworzonych_stanow',
        'Depth': 'średni_maksymalny_poziom_rekursji',
        'Time': 'średni_czas_rozwiazania'
    }

    # Create individual strategy charts
    for strategy in strategy_names:
        for metric, metric_file in metrics.items():
            create_chart(
                data,
                strategy,
                metric,
                f'{metrics[metric].replace("_", " ").title()} ({strategy_names[strategy]})',
                f'wykres_{strategy}_{metric_file}.png',
                filter_invalid=(strategy == 'dfs' and metric == 'SolutionLength')
            )

    # Create comparison charts for time and solution length
    for metric, title in [
        ('Time', 'Porównanie średniego czasu rozwiązania dla różnych strategii'),
        ('SolutionLength', 'Porównanie średniej długości rozwiązania dla różnych strategii')
    ]:
        create_chart(
            data,
            None,  # No specific strategy filter
            metric,
            title,
            f'wykres_porownanie_strategii_{metric.lower()}.png',
            filter_invalid=(metric == 'SolutionLength')
        )


def main():
    # Load data and create all charts
    data = load_data('result.txt')
    create_all_charts(data)
    print("Wykresy słupkowe zostały wygenerowane i zapisane jako pliki PNG.")


if __name__ == "__main__":
    main()

