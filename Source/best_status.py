import pickle


def main():
    with open("Saves/dino4.obj", "rb") as f:
        best = pickle.load(f)

    best.nn.info_nn()


if __name__ == '__main__':
    main()
