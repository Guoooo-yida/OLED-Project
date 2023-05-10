import FunctionSummary
from multiprocessing import Process, Manager, Lock
import GUI
# import GUIfigure


def run(shared_dipolePosition=None,
        shared_horizontalRatio=None,
        shared_refractIndex_far=None,
        shared_names=None,
        shared_thickLayer=None,
        shared_refractIndex=None,
        shared_waveLength1=None,
        shared_waveLength2=None,
        shared_EQE=None,
        shared_angle=None,
        shared_wave=None,
        shared_Luminance=None,
        shared_Spectrum=None,
        shared_Function_flag=None,
        shared_GUI_flag=None
        ):

    lock = Lock()
    shared_GUI_flag.append(0)

    p1 = Process(target=GUI.GUI, args=(shared_dipolePosition,
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
                                       # shared_Function_flag,
                                       shared_GUI_flag,
                                       lock
                                       ))

    p2 = Process(target=FunctionSummary.function, args=(shared_dipolePosition,
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
                                                        lock
                                                        ))

    # p3 = Process(target=GUIfigure.GUIfig, args=(shared_angle,
    #                                             shared_wave,
    #                                             shared_Luminance,
    #                                             shared_Spectrum,
    #                                             shared_Function_flag
    #                                             ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    # p3.start()
    # p3.join()


if __name__ == '__main__':
    manager = Manager()
    shared_dipolePosition = manager.list([])  #
    shared_horizontalRatio = manager.list([])  #
    shared_refractIndex_far = manager.list([])  #
    shared_names = manager.list([])
    shared_thickLayer = manager.list([])  # ####
    shared_refractIndex = manager.list([])  # ####
    shared_waveLength1 = manager.list([])  # #
    shared_waveLength2 = manager.list([])  # #

    shared_EQE = manager.list([])  #
    shared_angle = manager.list([])  # ####
    shared_wave = manager.list([])  # ####
    shared_Luminance = manager.list([])  # ####
    shared_Spectrum = manager.list([])  # ####

    shared_Function_flag = manager.list([False])
    shared_GUI_flag = manager.list([])

    run(shared_dipolePosition=shared_dipolePosition,
        shared_horizontalRatio=shared_horizontalRatio,
        shared_refractIndex_far=shared_refractIndex_far,
        shared_names=shared_names,
        shared_thickLayer=shared_thickLayer,
        shared_refractIndex=shared_refractIndex,
        shared_waveLength1=shared_waveLength1,
        shared_waveLength2=shared_waveLength2,
        shared_EQE=shared_EQE,
        shared_angle=shared_angle,
        shared_wave=shared_wave,
        shared_Luminance=shared_Luminance,
        shared_Spectrum=shared_Spectrum,
        shared_Function_flag=shared_Function_flag,
        shared_GUI_flag=shared_GUI_flag)


