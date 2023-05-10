waveLength = []
intensity = []
with open("Alq.txt", "r") as f:

    while True:
        lines = f.readline()
        if lines:
            x = lines.split()
            waveLength.append(float(x[0]))
            intensity.append(float(x[1]))
        else:
            break
