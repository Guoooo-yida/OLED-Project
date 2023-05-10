import cmath


def Calculate_RS(thickLayer, refractIndex, angleRad, waveLength):  # u_0是入射角度，在这个函数中是一个数字

    numLayer = len(thickLayer)
    if numLayer == 1:
        if angleRad == 0:
            return Calculate_RS(thickLayer, refractIndex, 1e-14, waveLength)
        else:
            a1 = refractIndex[0] ** 2 - refractIndex[0] ** 2 * angleRad ** 2
            b1 = a1.real
            c1 = a1.imag ** 2 / 4
            mu1 = cmath.sqrt((b1 + cmath.sqrt(b1 ** 2 + 4 * c1)) / 2)
            mv1 = cmath.sqrt((-b1 + cmath.sqrt(b1 ** 2 + 4 * c1)) / 2)

            a2 = refractIndex[1] ** 2 - refractIndex[0] ** 2
            b2 = a2.real + mu1 ** 2 - mv1 ** 2
            c2 = (a2.imag / 2 + mu1 * mv1) ** 2
            mu2 = cmath.sqrt((b2 + cmath.sqrt(b2 ** 2 + 4 * c2)) / 2)
            mv2 = cmath.sqrt((-b2 + cmath.sqrt(b2 ** 2 + 4 * c2)) / 2)

            a3 = refractIndex[2] ** 2 - refractIndex[1] ** 2
            b3 = a3.real + mu2 ** 2 - mv2 ** 2
            c3 = (a3.imag / 2 + mu2 * mv2) ** 2
            mu3 = cmath.sqrt((b3 + cmath.sqrt(b3 ** 2 + 4 * c3)) / 2)
            mv3 = cmath.sqrt((-b3 + cmath.sqrt(b3 ** 2 + 4 * c3)) / 2)

            rs1 = (mu1 + 1j * mv1 - mu2 - 1j * mv2) / (mu1 + 1j * mv1 + mu2 + 1j * mv2)
            rs2 = (mu2 + 1j * mv2 - mu3 - 1j * mv3) / (mu2 + 1j * mv2 + mu3 + 1j * mv3)

            rs = (rs1 + rs2 * cmath.exp(2 * 1j * thickLayer[0] * 2 * cmath.pi * (mu2 + 1j * mv2) / waveLength)) / \
                 (1 + rs1 * rs2 * cmath.exp(2 * 1j * thickLayer[0] * 2 * cmath.pi * (mu2 + 1j * mv2) / waveLength))

    else:
        if angleRad == 0:
            return Calculate_RS(thickLayer, refractIndex, 1e-14, waveLength)
        else:
            u_1 = refractIndex[0] * angleRad / refractIndex[1]
            a1 = refractIndex[0] ** 2 - refractIndex[0] ** 2 * angleRad ** 2
            b1 = a1.real
            c1 = a1.imag ** 2 / 4
            mu1 = cmath.sqrt((b1 + cmath.sqrt(b1 ** 2 + 4 * c1)) / 2)
            mv1 = cmath.sqrt((-b1 + cmath.sqrt(b1 ** 2 + 4 * c1)) / 2)

            a2 = refractIndex[1] ** 2 - refractIndex[0] ** 2
            b2 = a2.real + mu1 ** 2 - mv1 ** 2
            c2 = (a2.imag / 2 + mu1 * mv1) ** 2
            mu2 = cmath.sqrt((b2 + cmath.sqrt(b2 ** 2 + 4 * c2)) / 2)
            mv2 = cmath.sqrt((-b2 + cmath.sqrt(b2 ** 2 + 4 * c2)) / 2)

            rs1 = (mu1 + 1j * mv1 - mu2 - 1j * mv2) / (mu1 + 1j * mv1 + mu2 + 1j * mv2)
            rs = (rs1 + Calculate_RS(thickLayer[1:], refractIndex[1:], u_1, waveLength) * cmath.exp(
                2 * 1j * thickLayer[0] * 2 * cmath.pi * (mu2 + 1j * mv2) / waveLength)) / (
                1 + rs1 * Calculate_RS(thickLayer[1:], refractIndex[1:], u_1, waveLength) * cmath.exp(
                2 * 1j * thickLayer[0] * 2 * cmath.pi * (mu2 + 1j * mv2) / waveLength))

    return rs
