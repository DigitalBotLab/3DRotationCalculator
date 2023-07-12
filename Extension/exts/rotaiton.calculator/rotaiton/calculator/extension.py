import omni.ext
import omni.ui as ui

from .ui.custom_multifield_widget import CustomMultifieldWidget
from pxr import Gf
import numpy as np
from .numpy_utils import euler_angles_to_quat

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class RotaitonCalculatorExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[rotaiton.calculator] rotaiton calculator startup")

        self._count = 0

        self._window = ui.Window("3D Rotation Calculator", width=300, height=100, visible=True)
        with self._window.frame:
            with ui.VStack():
                with ui.CollapsableFrame("Quaternion mul", collapsed=False, height = 0):
                    with ui.VStack():
                        with ui.HStack(height = 20):
                            self.q1_widget = CustomMultifieldWidget(
                                label="Quaternion 1:",
                                sublabels=[ "w", "x", "y", "z"],
                                default_vals=[1, 0, 0, 0],
                            )
                        with ui.HStack(height = 20):
                            self.q2_widget = CustomMultifieldWidget(
                                label="Quaternion 2:",
                                sublabels=[ "w", "x", "y", "z"],
                                default_vals=[1, 0, 0, 0],
                            )
                        ui.Line(height = 5) 
                        with ui.HStack(height = 20):
                            self.q_widget = CustomMultifieldWidget(
                                label="Result:",
                                sublabels=[ "w", "x", "y", "z"],
                                default_vals=[1, 0, 0, 0],
                                read_only= True
                            )                
                        self.q_str_widget = ui.StringField(width = 200, height = 20)
                        ui.Line(height = 5)
                        with ui.HStack():
                            ui.Button("Quaternion mul", height = 20, clicked_fn=self.quaternioin_mul)

                with ui.CollapsableFrame("Euler to Quaternion", collapsed=False, height = 0):
                    with ui.VStack():
                        with ui.HStack(height = 20):
                            self.euler_widget = CustomMultifieldWidget(
                                label="Euler angles (degree):",
                                sublabels=[ "roll", "pitch", "yaw"],
                                default_vals=[0, 0, 0],
                            )
                        ui.Line(height = 5)
                        with ui.HStack(height = 20):
                            self.quat_widget = CustomMultifieldWidget(
                                label="Quaternion:",
                                sublabels=[ "w", "x", "y", "z"],
                                default_vals=[1, 0, 0, 0],
                                read_only= True
                            )
                        ui.Button("Euler to Quat", height = 20, clicked_fn=self.euler2quat)

    def on_shutdown(self):
        print("[rotaiton.calculator] rotaiton calculator shutdown")

    def quaternioin_mul(self):
        print("quaternioin_mul")
        q1 = [self.q1_widget.multifields[i].model.as_float for i in range(4)] # wxyz
        q1 = Gf.Quatf(q1[0], q1[1], q1[2], q1[3])
        q2 = [self.q2_widget.multifields[i].model.as_float for i in range(4)] # wxyz
        q2 = Gf.Quatf(q2[0], q2[1], q2[2], q2[3])
        q = q1 * q2
        self.q_widget.update([q.GetReal(), *q.GetImaginary()]) 
        self.q_str_widget.model.set_value(str(q))

    def euler2quat(self):
        print("euler2quat")
        euler = [self.euler_widget.multifields[i].model.as_float for i in range(3)] # roll pitch yaw
        q = euler_angles_to_quat(euler, degrees=True).tolist()
        self.quat_widget.update(q)