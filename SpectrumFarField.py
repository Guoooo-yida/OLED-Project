import MultiWaveLengthOLED


def figureSpectrumFarField(waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all, lam_spec):
    numLambdaSampling, waveLength, intensity, angle, F_all, P_far, F_far, spec_far = \
        MultiWaveLengthOLED.cutDataInMultiWaveLength(
            waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all, lam_spec)
    angle = angle[0]
    eyeSenseIndex = []
    for i in range(4):
        tmp = []
        for j in range(len(angle)):
            tmp.append(abs(angle[j] - 20 * i))
        index_tmp = tmp.index(min(list(tmp)))
        eyeSenseIndex.append(index_tmp)
    x = waveLength
    y = []
    y_tmp = []
    for i in range(4):
        y.append([])
        for j in range(numLambdaSampling):
            y[i].append(spec_far[j][eyeSenseIndex[i]])
        y_tmp.append(max(y[i]))
    y_max = max(y_tmp)
    for i in range(4):
        for k in range(numLambdaSampling):
            y[i][k] = y[i][k] / y_max
    return x, y
