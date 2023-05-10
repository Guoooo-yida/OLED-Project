import cmath
import numpy as np
import RefractionPCalculation
import RefractionSCalculation
import TransmittanceSCalculation
import TransmittancePCalculation


def Calculate_SingleWaveLengthEQE(waveLength,
                                  dipolePosition,
                                  horizontalRatio,
                                  refractIndex_far,
                                  thickLayer,
                                  refractIndex
                                  ):
    # 采样设置
    numAngleSampling = 1002  # 采样点数目
    angleSampling = [i * 5 / (numAngleSampling - 1) for i in range(numAngleSampling)]  # 角度范围[0,5]
    positionInEML = 0.5

    refractIndex_out = refractIndex[dipolePosition - 1:]  # 有发光层
    refractIndex_in = refractIndex[0:dipolePosition]  # 有发光层
    refractIndex_in = refractIndex_in[::-1]
    refractIndex_in.append(complex(1))
    thickLayer_out = thickLayer[dipolePosition:]  # 无发光层
    thickLayer_in = thickLayer[0:dipolePosition - 1]  # 无发光层
    thickLayer_in = thickLayer_in[::-1]

    # %%
    # 中间参数公式计算

    refractS_out = []
    refractS_in = []
    refractP_out = []
    refractP_in = []
    transmitS_out = []
    transmitP_out = []
    for i in range(numAngleSampling):
        refractS_out.append(
            RefractionSCalculation.Calculate_RS(thickLayer_out, refractIndex_out, angleSampling[i], waveLength))
        refractS_in.append(
            RefractionSCalculation.Calculate_RS(thickLayer_in, refractIndex_in, angleSampling[i], waveLength))
        refractP_out.append(
            RefractionPCalculation.Calculate_RP(thickLayer_out, refractIndex_out, angleSampling[i], waveLength))
        refractP_in.append(
            RefractionPCalculation.Calculate_RP(thickLayer_in, refractIndex_in, angleSampling[i], waveLength))
        transmitS_out.append(
            TransmittanceSCalculation.Calculate_TS(thickLayer_out, refractIndex_out, angleSampling[i], waveLength))
        transmitP_out.append(
            TransmittancePCalculation.Calculate_TP(thickLayer_out, refractIndex_out, angleSampling[i], waveLength))

    k_ze = []  # emitting发光层中的垂直分量
    for i in range(numAngleSampling):
        k_ze.append(
            2 * cmath.pi * refractIndex[dipolePosition - 1] / waveLength * cmath.sqrt(1 - angleSampling[i] ** 2))
    angleSampling_sub = []  # Substrate基板为最后一层，底发射时为玻璃，顶发射时是filter或空气
    for i in range(numAngleSampling):
        angleSampling_sub.append(refractIndex[dipolePosition - 1] * angleSampling[i] / refractIndex[-1])
    k_zs = []  # substrate最后一层中的垂直分量
    for i in range(numAngleSampling):
        k_zs.append(2 * cmath.pi * refractIndex[-1] / waveLength * cmath.sqrt(1 - angleSampling_sub[i] ** 2))
    R_out = [(abs(refractP_out[i])) ** 2 for i in range(numAngleSampling)]
    T_TM_out = [(abs(transmitP_out[i])) ** 2 * k_zs[i] / k_ze[i] for i in range(numAngleSampling)]  # 光从发光层到最后一层的透过率
    T_TE_out = [abs(transmitS_out[i]) ** 2 * k_zs[i] / k_ze[i] for i in range(numAngleSampling)]
    z_out = thickLayer[dipolePosition - 1] * positionInEML  # 出光方向上发光偶极子到EML层边缘的距离
    z_in = thickLayer[dipolePosition - 1] * (1 - positionInEML)  # 背离出光方向上发光偶极子到EML边缘的距离

    a_TE_out = []
    a_TM_out = []
    a_TE_in = []
    a_TM_in = []
    for i in range(numAngleSampling):
        a_TE_out.append(refractS_out[i] * cmath.exp(2 * 1j * k_ze[i] * z_out))
        a_TM_out.append(refractP_out[i] * cmath.exp(2 * 1j * k_ze[i] * z_out))
        a_TE_in.append(refractS_in[i] * cmath.exp(2 * 1j * k_ze[i] * z_in))
        a_TM_in.append(refractP_in[i] * cmath.exp(2 * 1j * k_ze[i] * z_in))

    a_TE = []
    a_TM = []
    for i in range(numAngleSampling):
        a_TE.append(a_TE_out[i] * a_TE_in[i])
        a_TM.append(a_TM_out[i] * a_TM_in[i])

    # %%
    # EML总辐射功率计算

    K_TMv = []  # 垂直偶极子源vTM模辐射的功率分数
    K_TMh = []  # 水平偶极子源hTM模辐射的功率分数
    K_TEh = []  # 水平偶极子源hTE模辐射的功率分数
    for i in range(numAngleSampling):
        K_TMv.append((3 / 4 * angleSampling[i] ** 2 / cmath.sqrt(1 - angleSampling[i] ** 2) * (1 + a_TM_out[i]) * (
                1 + a_TM_in[i]) / (1 - a_TM[i])).real)
        K_TMh.append((3 / 8 * cmath.sqrt(1 - angleSampling[i] ** 2) * (1 - a_TM_out[i]) * (1 - a_TM_in[i]) / (
                1 - a_TM[i])).real)
        K_TEh.append((3 / 8 / cmath.sqrt(1 - angleSampling[i] ** 2) * (1 + a_TE_out[i]) * (1 + a_TE_in[i]) / (
                1 - a_TE[i])).real)

    K = []
    for i in range(numAngleSampling):
        K.append(horizontalRatio * (K_TMh[i] + K_TEh[i]) + (1 - horizontalRatio) * K_TMv[i])

    F = 0  # EML总辐射功率
    for i in range(numAngleSampling):
        F += K[i] * 2 * angleSampling[i] * 5 / numAngleSampling
    F = abs(F)

    # %%
    # 基板上辐射功率计算

    K_TMv_sub = []
    K_TMh_sub = []
    K_TEh_sub = []
    for i in range(numAngleSampling):
        K_TMv_sub.append(
            3 / 8 * angleSampling[i] ** 2 / cmath.sqrt(1 - angleSampling[i] ** 2) * abs(1 + a_TM_in[i]) ** 2 / abs(
                1 - a_TM[i]) ** 2 * T_TM_out[i])
        K_TMh_sub.append(
            3 / 16 * cmath.sqrt(1 - angleSampling[i] ** 2) * abs(1 - a_TM_in[i]) ** 2 / abs(1 - a_TM[i]) ** 2 *
            T_TM_out[i])
        K_TEh_sub.append(
            3 / 16 / cmath.sqrt(1 - angleSampling[i] ** 2) * abs(1 + a_TE_in[i]) ** 2 / abs(1 - a_TE[i]) ** 2 *
            T_TE_out[i])

    K_sub = []
    for i in range(numAngleSampling):
        K_sub.append(horizontalRatio * (K_TMh_sub[i] + K_TEh_sub[i]) + (1 - horizontalRatio) * K_TMv_sub[i])
    temp1 = []
    for i in range(numAngleSampling):
        temp1.append(abs(angleSampling[i] - refractIndex[-1] / refractIndex[dipolePosition - 1]))
    temp2 = np.argsort(temp1)
    K_temp = K_sub[0:temp2[0] + 1]  # 对K_sub进行截断，只留下全反射角以内的区域
    K_sub = K_temp

    # %%
    # 远场辐射功率计算

    angleSampling_far = []  # 入射到远场时的辐射角正弦值
    for i in range(numAngleSampling):
        angleSampling_far.append(angleSampling[i] * refractIndex[dipolePosition - 1] / refractIndex_far)
    temp3 = []
    for i in range(numAngleSampling):
        temp3.append(abs(angleSampling_far[i] - 1))  # 只留下全反射角以内的区域
    temp3 = np.argsort(temp3)
    # 判断与远场折射率的大小关系，若远场折射率大，则所有的光都可以进入远场，折射率小，则考虑全反射
    if abs(refractIndex[-1]) < refractIndex_far:
        temp3[0] = len(K_sub)

    ReverseRefractIndex = refractIndex[::-1]
    ReverseRefractIndex.append(complex(1))

    refractP_oled = []
    refractS_oled = []
    refractP_far = []
    refractS_far = []
    transmitP_far = []
    transmitS_far = []
    for i in range(temp3[0]):
        refractP_oled.append(RefractionPCalculation.Calculate_RP(thickLayer[::-1], ReverseRefractIndex,
                                                                 angleSampling[i] * refractIndex[dipolePosition - 1] /
                                                                 refractIndex[-1], waveLength))
        refractS_oled.append(RefractionSCalculation.Calculate_RS(thickLayer[::-1], ReverseRefractIndex,
                                                                 angleSampling[i] * refractIndex[dipolePosition - 1] /
                                                                 refractIndex[-1], waveLength))
        refractP_far.append(RefractionPCalculation.Calculate_RP([20], [refractIndex[-1], refractIndex_far,
                                                                       refractIndex_far],
                                                                angleSampling[i] * refractIndex[dipolePosition - 1] /
                                                                refractIndex[-1], waveLength))
        refractS_far.append(
            RefractionSCalculation.Calculate_RS([20], [refractIndex[-1], refractIndex_far, refractIndex_far],
                                                angleSampling[i] * refractIndex[dipolePosition - 1] / refractIndex[-1],
                                                waveLength))
        transmitP_far.append(
            TransmittancePCalculation.Calculate_TP([20], [refractIndex[-1], refractIndex_far, refractIndex_far],
                                                   angleSampling[i] * refractIndex[dipolePosition - 1] / refractIndex[
                                                       -1],
                                                   waveLength))
        transmitS_far.append(
            TransmittanceSCalculation.Calculate_TS([20], [refractIndex[-1], refractIndex_far, refractIndex_far],
                                                   angleSampling[i] * refractIndex[dipolePosition - 1] / refractIndex[
                                                       -1],
                                                   waveLength))

    K_TMv_far = []
    K_TMh_far = []
    K_TEh_far = []
    for i in range(temp3[0]):
        K_TMv_far.append(K_TMv_sub[i] * abs(transmitP_far[i]) ** 2 * refractIndex_far / refractIndex[-1] * cmath.sqrt(
            1 - angleSampling_far[i] ** 2) / cmath.sqrt(
            1 - angleSampling_sub[i] ** 2) / (1 - abs(refractP_far[i]) ** 2 * abs(refractP_oled[i]) ** 2))
        K_TMh_far.append(
            K_TMh_sub[i] * transmitP_far[i] * transmitP_far[i].conjugate() * refractIndex_far / refractIndex[
                -1] * cmath.sqrt(1 - angleSampling_far[i] ** 2) / cmath.sqrt(
                1 - angleSampling_sub[i] ** 2) / (1 - abs(refractP_far[i]) ** 2 * abs(refractP_oled[i]) ** 2))
        K_TEh_far.append(
            K_TEh_sub[i] * transmitS_far[i] * transmitS_far[i].conjugate() * refractIndex_far / refractIndex[
                -1] * cmath.sqrt(1 - angleSampling_far[i] ** 2) / cmath.sqrt(
                1 - angleSampling_sub[i] ** 2) / (1 - abs(refractS_far[i]) ** 2 * abs(refractS_oled[i]) ** 2))

    K_far = []
    for i in range(temp3[0]):
        K_far.append(horizontalRatio * (K_TMh_far[i] + K_TEh_far[i]) + (1 - horizontalRatio) * K_TMv_far[i])

    P_far = []
    for i in range(temp3[0]):
        P_far.append(
            abs(refractIndex_far ** 2 / dipolePosition ** 2 * cmath.sqrt(1 - angleSampling_far[i] ** 2) / cmath.pi *
                K_far[i]))

    F_far = 0
    for i in range(temp3[0]):
        F_far += K_far[i] * 2 * angleSampling[i] * 5 / numAngleSampling
    F_far = abs(F_far)
    # EQE = abs(F_far / F)
    # print(EQE)
    effectiveAngle_far = []
    for i in range(temp3[0]):
        effectiveAngle_far.append(angleSampling_far[i])

    return effectiveAngle_far, F, P_far, F_far  # 第2,4项是float,第1项是complex类型数组,第3项是float类型数组


