import os
import json
import unicodedata
import matplotlib.pyplot as plt

from datetime import datetime

graph_images = []
# directories
BASE_DIR = '/cfcore'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# file paths
TEMPLATEPATH = os.path.join(OUTPUT_DIR, 'index.html')
FILEPATH = os.path.join(BASE_DIR, 'weather_data.json')

CONTENT = """<p align=center>
<img src='{}' border=1 width=500>
</p>"""


def remove_foreign_characters(str):
    escaped_str = unicodedata.normalize('NFKD', str).encode('ASCII', 'ignore')
    return escaped_str


def create_template(paths):
    with open(TEMPLATEPATH, 'w') as tmpl:
        for path in paths:
            html_tags = CONTENT.format(path)
            tmpl.write(html_tags)


def main():
    with open(FILEPATH) as data_file:
        for obj in data_file:
            data = json.loads(obj)
            # extract list of all dates for each object
            val = [key['dt'] for key in data['data']]

            # convert unix times to dates
            dates = [datetime.fromtimestamp(value).strftime('%Y-%m-%d')
                     for value in val]

            # extract list of average temperature
            avg_temp = [key['temp']['day'] for key in data['data']]
            avg_max_temp = max(avg_temp)
            avg_min_temp = min(avg_temp)

            # extract list of max & min temperatures
            # max_temp = [key['temp']['max'] for key in data['data']]
            # min_temp = [key['temp']['min'] for key in data['data']]

            # extract the city name
            city_name = remove_foreign_characters(data['city']['name'])

            # file name and file path
            filename = '{}.png'.format(city_name)
            path = os.path.join(OUTPUT_DIR, filename)
            # filepath = filename

            plt.plot(avg_temp, marker="o", color="green")

            xticks = [x for x in range(len(dates))]

            plt.xticks(xticks, dates, rotation=30)
            plt.ylim(avg_min_temp, avg_max_temp)

            # graph customization
            plt.title(city_name, color='red')
            plt.ylabel('Average temperature')
            plt.xlabel('Day')

            # prevent graph trimming
            plt.tight_layout()
            plt.savefig(path)

            # clear graph for next iteration
            plt.clf()

            # create a list with all the images path's
            graph_images.append(filename)

    create_template(graph_images)


if __name__ == '__main__':
    main()
