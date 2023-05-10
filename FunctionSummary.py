import MultiWaveLengthOLED
import ExternalQuantumEfficiency
import Luminance
import SpectrumFarField
import time


def function(shared_dipolePosition,
             shared_horizontalRatio,
             shared_refractIndex_far,
             shared_names,
             shared_thickLayer,
             shared_refractIndex,
             shared_waveLength1,
             shared_waveLength2,
             shared_EQE,
             shared_angle,
             shared_wave,
             shared_Luminance,
             shared_Spectrum,
             shared_Function_flag,
             shared_GUI_flag,
             lock):
    while shared_GUI_flag[0] == 0:
        time.sleep(0.5)
        continue
    # print("1111111")
    with lock:
        waveLength_all, \
        intensity_all, \
        angle_all, \
        F_all, \
        P_far_all, \
        F_far_all, \
        spec_far_all = MultiWaveLengthOLED.Calculation_MultiWaveLengthEQE(shared_dipolePosition[0],
                                                                          shared_horizontalRatio[0],
                                                                          shared_refractIndex_far[0],
                                                                          shared_names,
                                                                          shared_thickLayer,
                                                                          shared_refractIndex)
        shared_EQE.append(ExternalQuantumEfficiency.printEqe(waveLength_all, intensity_all, angle_all, F_all,
                                                             P_far_all, F_far_all, spec_far_all,
                                                             ))
        x1, y1 = Luminance.figureLuminance(waveLength_all, intensity_all, angle_all, F_all,
                                           P_far_all, F_far_all, spec_far_all,
                                           [shared_waveLength1[0], shared_waveLength1[1]])
        shared_angle.append(x1)
        shared_Luminance.append(y1)

        x2, y2 = SpectrumFarField.figureSpectrumFarField(waveLength_all, intensity_all, angle_all, F_all,
                                                         P_far_all, F_far_all, spec_far_all,
                                                         [shared_waveLength2[0], shared_waveLength2[1]])
        shared_wave.append(x2)
        shared_Spectrum.append(y2)
        # print(shared_Spectrum)
    shared_Function_flag[0] = True
