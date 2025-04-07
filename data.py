import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Funkcja do wczytania danych z pliku tekstowego
def load_data(file_path):
    """ Wczytuje dane z pliku wynikowego jako DataFrame. """
    return pd.read_csv(file_path, sep=r'\s+')                       # separator: dowolna liczba białych znaków


def create_chart(data, strategy, metric, chart_title, filename, use_log_scale=False, filter_invalid=False):
    """
    Uniwersalna funkcja do tworzenia wykresów słupkowych dla zadanej strategii i metryki.

    Parametry:
    - data: DataFrame z wynikami
    - strategy: strategia (bfs, dfs, astr), lub None do porównania strategii
    - metric: metryka do analizy (np. Time, SolutionLength)
    - chart_title: tytuł wykresu
    - filename: nazwa pliku PNG do zapisania wykresu
    - use_log_scale: czy użyć skali logarytmicznej na osi Y
    - filter_invalid: czy filtrować błędne dane (np. DFS bez rozwiązania)
    """

    color_map = {                                                   # Mapowanie kolorów dla poszczególnych parametrów/strategii
        # BFS/DFS
        'rdul': '#2521ff',
        'rdlu': '#575555',
        'drul': '#03b300',
        'drlu': '#ff584f',
        'ludr': '#d764fa',
        'lurd': '#fff200',
        'uldr': '#ff00b3',
        'ulrd': '#00ffee',
        # A*
        'hamm': '#a44fff',
        'manh': '#3cface',
        # Do porównania
        'bfs': '#9000ff',
        'dfs': '#00ff99',
        'astr': '#ff6e69',
    }

    label_map = {                                                   # Mapowanie skrótów na czytelne etykiety
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

    # Filtrowanie danych pod kątem strategii (jeśli podana)
    if strategy:
        strategy_data = data[data['Strategy'] == strategy]
    else:
        strategy_data = data  # Dla porównania strategii

    # Lista unikalnych parametrów (kolejności ruchów lub heurystyk)
    if strategy:
        params = sorted(strategy_data['Param'].unique())
        bar_width = 0.2 if strategy == 'astr' else 0.1          # Szerokość słupków
    else:
        params = sorted(strategy_data['Strategy'].unique())     # Dla porównania strategii
        bar_width = 0.2

    # Lista unikalnych głębokości (rozmiar problemu)
    depths = sorted(strategy_data['Depth'].unique())

    # Przygotowanie wykresu
    plt.figure(figsize=(12, 7))
    positions = np.arange(len(depths))                           # Pozycje słupków na osi X

    # Rysowanie słupków dla każdego parametru
    for i, param in enumerate(params):                          # Filtrowanie danych pod dany parametr
        if strategy:
            param_data = strategy_data[strategy_data['Param'] == param]
        else:
            param_data = strategy_data[strategy_data['Strategy'] == param]

        avg_values = []                                         # Średnie wartości metryki dla każdej głębokości
        for depth in depths:
            depth_data = param_data[param_data['Depth'] == depth]

            # Filtrowanie błędnych danych (np. DFS bez rozwiązania)
            if filter_invalid and metric == 'SolutionLength':
                valid_data = depth_data[depth_data['SolutionLength'] > 0]
                avg_values.append(valid_data[metric].mean() if len(valid_data) > 0 else 0)
            else:
                avg_values.append(depth_data[metric].mean())

        # Etykieta i kolor dla legendy
        param_key = param.lower()
        param_label = label_map.get(param_key, param)
        color = color_map.get(param_key, None)

        # Obliczenie pozycji słupków na osi X dla danego parametru
        pos = positions + (i - len(params) / 2 + 0.5) * bar_width

        # Rysowanie słupków
        plt.bar(pos, avg_values, width=bar_width, label=param_label, color=color)

    # Opis osi Y dla metryk
    metric_labels = {
        'SolutionLength': 'Średnia długość rozwiązania',
        'Visited': 'Średnia liczba odwiedzonych stanów',
        'Processed': 'Średnia liczba przetworzonych stanów',
        'Depth': 'Średni maksymalny poziom rekursji',
        'Time': 'Średni czas rozwiązania [s]'
    }

    # Ustawienia wykresu
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

# Funkcja do wygenerowania wszystkich wykresów
def create_all_charts(data):
    """ Tworzy wszystkie wykresy dla każdej strategii oraz porównania między nimi. """

    # Mapowanie nazw strategii do etykiet
    strategy_names = {'bfs': 'BFS', 'dfs': 'DFS', 'astr': 'A*'}

    # Mapowanie metryk na nazwę pliku
    metrics = {
        'SolutionLength': 'średnia_dlugosc_rozwiazania',
        'Visited': 'średnia_liczba_odwiedzonych_stanow',
        'Processed': 'średnia_liczba_przetworzonych_stanow',
        'Depth': 'średni_maksymalny_poziom_rekursji',
        'Time': 'średni_czas_rozwiazania'
    }

    # Tworzenie wykresów dla każdej strategii i metryki
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

    # Porównania strategii pod kątem czasu i długości rozwiązania
    for metric, title in [
        ('Time', 'Porównanie średniego czasu rozwiązania dla różnych strategii'),
        ('SolutionLength', 'Porównanie średniej długości rozwiązania dla różnych strategii')
    ]:
        create_chart(
            data,
            None,   # Brak filtra – porównujemy wszystkie strategie
            metric,
            title,
            f'wykres_porownanie_strategii_{metric.lower()}.png',
            filter_invalid=(metric == 'SolutionLength')
        )

# Główna funkcja programu
def main():
    """ Główna funkcja: wczytuje dane i generuje wszystkie wykresy. """
    data = load_data('result.txt')
    create_all_charts(data)
    print("Wykresy słupkowe zostały wygenerowane i zapisane jako pliki PNG.")


if __name__ == "__main__":
    main()

