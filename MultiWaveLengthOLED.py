import SingleWaveLengthOLED
import LuminescenseSpectrum
import MetalRefractionLoading
import time
from tqdm import tqdm


def Calculation_MultiWaveLengthEQE(dipolePosition,
                                   horizontalRatio,
                                   refractIndex_far,
                                   names,
                                   thickLayer,
                                   refractIndex):
    numLambdaSampling = 91

    waveLength = [350 + 450 * i / (numLambdaSampling - 1) for i in range(numLambdaSampling)]
    x = min(LuminescenseSpectrum.intensity)
    intensity = []
    for i in range(numLambdaSampling):
        for j in range(len(LuminescenseSpectrum.waveLength)):
            if waveLength[i] < LuminescenseSpectrum.waveLength[j]:
                intensity.append(LuminescenseSpectrum.intensity[j - 1] - x + (
                        LuminescenseSpectrum.intensity[j] - LuminescenseSpectrum.intensity[j - 1]) * (
                                         waveLength[i] - LuminescenseSpectrum.waveLength[j - 1]))
                break
            if waveLength[i] == LuminescenseSpectrum.waveLength[j]:
                intensity.append(LuminescenseSpectrum.intensity[j] - x)
                break

    refractMetal = []
    metal = []
    metal_index = []
    for i in range(len(refractIndex)):
        if refractIndex[i].imag != 0:
            metal.append(names[i])
            metal_index.append(i)
    for i in range(len(metal)):
        waveLength_MRL, real_MRL, image_MRL = MetalRefractionLoading.findName(metal[i])
        refractMetal.append([])
        for k in range(numLambdaSampling):
            for j in range(len(waveLength_MRL)):
                if waveLength[k] < waveLength_MRL[j]:
                    refractMetal[i].append(real_MRL[j - 1] + (real_MRL[j] - real_MRL[j - 1]) * (
                                           waveLength[k] - waveLength_MRL[j - 1]) + 1j * (image_MRL[j - 1] + (
                                           image_MRL[j] - image_MRL[j - 1]) * (waveLength[k] - waveLength_MRL[j - 1])))
                    break
                if waveLength[k] == waveLength_MRL[j]:
                    refractMetal[i].append(real_MRL[j] + 1j * image_MRL[j])
                    break
    F = []
    effectiveAngle_far = []
    P_far = []
    F_far = []
    specRadIntensity = []
    for i in tqdm(range(numLambdaSampling)):
        for j in range(len(metal)):
            refractIndex[metal_index[j]] = refractMetal[j][i]

        effectiveAngle_far_tmp, F_tmp, P_far_tmp, F_far_tmp = \
            SingleWaveLengthOLED.Calculate_SingleWaveLengthEQE(waveLength[i],
                                                               dipolePosition,
                                                               horizontalRatio,
                                                               refractIndex_far,
                                                               thickLayer,
                                                               refractIndex
                                                               )
        F.append(F_tmp)
        effectiveAngle_far.append([])
        P_far.append([])
        F_far.append(F_far_tmp)
        specRadIntensity.append([])  # 二维数组，第一维度长度为远场有效立体角数目，第二维度为波长采样点数目

        for j in range(len(effectiveAngle_far_tmp)):
            effectiveAngle_far[i].append(effectiveAngle_far_tmp)
            P_far[i].append(P_far_tmp[j])
            specRadIntensity[i].append(intensity[i] * P_far_tmp[j] / F_tmp / waveLength[i])
        time.sleep(0.25)
    return waveLength, intensity, effectiveAngle_far, F, P_far, F_far, specRadIntensity
    # return waveLength, F, P_far, F_far, effectiveAngle_far


def cutDataInMultiWaveLength(waveLength_all, intensity_all, angle_all, F_all, P_far_all, F_far_all, spec_far_all,
                             rangeLam):
    numLambdaSampling = int((rangeLam[1] - rangeLam[0]) / 5 + 1)
    waveLength = []
    for i in range(numLambdaSampling):
        waveLength.append(rangeLam[0] + 5 * i)

    intensity = []
    F = []
    P_far = []
    F_far = []
    spec_far = []

    for i in range(len(waveLength_all)):
        for j in range(numLambdaSampling):
            if waveLength[j] == waveLength_all[i]:
                intensity.append(intensity_all[i])
                F.append(F_all[i])
                P_far.append(P_far_all[i])
                F_far.append(F_far_all[i])
                spec_far.append(spec_far_all[i])

    return numLambdaSampling, waveLength, intensity, angle_all[0], F, P_far, F_far, spec_far

