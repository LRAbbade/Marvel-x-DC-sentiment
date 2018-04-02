from streamer import Streamer

keywords = ['python',
            'c++',
            'java',
            'javascript']

threads = {}

for word in keywords:
    threads[word] = Streamer(word)
    print('Starting stream on term', word)
    threads[word].start()
