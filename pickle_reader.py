import pickle

with open('todobot.py', 'rb') as f:
    data = pickle.load(f)

print(data)