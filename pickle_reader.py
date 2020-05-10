import pickle

with open('telegram_data.pickle', 'rb') as f:
    print(pickle.load(f))
