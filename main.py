from streamer import Streamer
from db_analyzer import Analyzer

keyword_sets = {
    "DC" : [
        "batman",
        "wonder woman",
        "aquaman",
        "the flash",
        "superman",
        "man of steel"
    ],
    "Marvel" : [
        "iron man",
        "black widow",
        "thor",
        "hulk",
        "spider-man",
        "black panther"
    ]
}
threads = {}

for name, set in keyword_sets.items():
    threads[name] = Streamer(name, set)
    print('Starting stream on publisher', name)
    threads[name].start()

print('Starting analyzer')
threads['Analyzer'] = Analyzer()
threads['Analyzer'].start()

for name, thread in threads.items():
    print("joining on", name)
    thread.join()

for name in keyword_sets:
    print("stream", name, "status:", threads[name].status_code)
