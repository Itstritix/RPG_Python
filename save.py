import pickle


def save_data(player_data):
    with open('save/save.pickle', 'wb') as file:
        pickle.dump(player_data, file)

def load_save():
    with open('save/save.pickle', 'rb') as file:
        loaded_object = pickle.load(file)
    return loaded_object