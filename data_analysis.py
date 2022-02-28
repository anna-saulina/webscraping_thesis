import json
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt

#
# with open('trial_data.json', 'r', encoding='utf-8') as infile:
#     trial_data = json.load(infile)


# Анализ данных

def process_data(trial_list):
    # Количество поялений нежелательных явлений в исследованиях
    events_occurances = []

    # Набор уникальных явлений
    event_set = set()

    # Количество случаев каждого явления
    event_count = []
    total_event_count = {}

    for trial in trial_list:
        event_keys = trial['events'].keys()
        events_occurances.extend(event_keys)

        for key in event_keys:
            inner_keys = trial['events'][key].keys()
            event_dict = {key: 0}

            for inner_key in inner_keys:
                value = trial['events'][key][inner_key].get('Events', 0)

                if value:
                    event_dict[key] += value

            event_count.append(event_dict)

    count_events = Counter(events_occurances)
    event_set.update(events_occurances)

    for event in event_count:
        key = list(event.keys())[0]
        value = list(event.values())[0]

        if key not in total_event_count:
            total_event_count.update(event)
        else:
            total_event_count[key] += value

    return total_event_count


def visualize_data(prepared_data):
    series_data = pd.Series(prepared_data)
    # print(series_data)
    series_data.plot(kind='bar', figsize=(12, 10)).grid(axis='y', linestyle='dotted')
    plt.title('Frequency of Serious Adverse Events')
    plt.margins(0.2, tight=False)
    plt.subplots_adjust(bottom=0.35)
    plt.savefig("trial-data-plot.pdf", dpi=600)


# if __name__ == '__main__':
#     processed_data = process_data(trial_data)
#     visualize_data(processed_data)
#     print(len(processed_data))