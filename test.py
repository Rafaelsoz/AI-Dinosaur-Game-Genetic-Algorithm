import pickle
from GameClasses.dinosaur_ia import DinosaurIA


def load_dino(path: str = "Saves/dino_trained.obj"):
    with open(path, "rb") as f:
        best = pickle.load(f)

    dinosaur = DinosaurIA(color="red")
    dinosaur.neurons = best.nn

    return dinosaur


def main():
    dino = load_dino("dino.obj")
    dino.neurons.info_nn()


if __name__ == "__main__":
    main()
