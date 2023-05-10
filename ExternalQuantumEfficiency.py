import MultiWaveLengthOLED
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy


def printEqe(waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all):
    # lam_eqe = input("计算外量子效率的波长范围(nm):")
    # lam_eqe = list(map(int, lam_eqe.split()))
    lam_eqe = [350, 700]

    numLambdaSampling, waveLength, intensity, angle, F, P_far, F_far, spec_far = \
        MultiWaveLengthOLED.cutDataInMultiWaveLength(
            waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all, lam_eqe)
    Eqe = 0
    for i in range(numLambdaSampling):
        Eqe += intensity[i] * F_far[i] / F[i] / (numLambdaSampling - 1)
    # print("EQE=", Eqe)
    # x = waveLength
    # x_smooth = numpy.linspace(min(x), max(x), 300)
    #
    # y = [F_far[i]/F[i] for i in range(len(waveLength))]
    # y_smooth = make_interp_spline(x, y)(x_smooth)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.xlabel('波长/nm')
    # plt.ylabel('外量子效率')
    # plt.plot(x_smooth, y_smooth)
    # plt.show()
    return Eqe
