import MultiWaveLengthOLED
import cmath
import math


def figureLuminance(waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all, lam_lum):
    numLambdaSampling, waveLength, intensity, angle, F, P_far, F_far, spec_far = \
        MultiWaveLengthOLED.cutDataInMultiWaveLength(
            waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all, lam_lum)
    angle = angle[0]
    L = []  # 不同角度下的Luminance亮度值
    for i in range(len(angle)):
        L_tmp = 0
        for j in range(numLambdaSampling):
            L_tmp += spec_far[j][i] / cmath.sqrt(1 - angle[i] ** 2) / (numLambdaSampling - 1)
        L.append(abs(L_tmp))
    for i in range(len(angle)):
        angle[i] = 360 * abs(cmath.asin(angle[i])) / (2 * math.pi)  # 把横坐标转换成角度制

    return angle, L
