import random

def readout_layer(data):
    rnd = random.randint(0,3)
    return rnd

if __name__ == "__main__":
    data = [1,2,3,4]
    print(readout_layer(data))

