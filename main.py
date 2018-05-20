import auth
import json
from threading import Timer

def prime_results_file():
    primer = {}

    with open('search_results.json', 'r+') as f:
        if f.readline() != '{}':
            json.dump(primer, f)

    with open ('final_results.json', 'r+') as o:
        if o.readline() != '{}':
            json.dump(primer, o)

def calc_cum():
    keywords = 'kill myself,die,want to die,kill,suicide'
    auth.stream.stop_loop()

    with open('search_results.json', 'r+') as f:
        data = json.load(f)
        for p in data:
            data[p]['dep_score'] = (data[p]['n_pos'] + data[p]['p_pos'] * 0.5) / 3.0
            print data[p]
        f.seek(0)
        f.truncate()
        primer = {}
        json.dump(primer, f)

    Timer(20.0, calc_cum).start()

    with open('final_results.json', 'r+') as o:
        final_data = json.load(o)
        final_data.update(data)
        # print final_data
        o.seek(0)
        json.dump(final_data, o)

    auth.run_stream(keywords)

if __name__ == "__main__":
    keywords = 'kill myself,die,want to die,kill,suicide'
    prime_results_file()
    calc_cum()
    auth.run_stream(keywords)
