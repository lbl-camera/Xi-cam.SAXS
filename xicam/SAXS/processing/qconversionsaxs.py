from xicam.plugins import ProcessingPlugin, Input, Output
import numpy as np
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator


class QconversionSAXS(ProcessingPlugin):
    integrator = Input(description='A PyFAI.AzimuthalIntegrator object', type=AzimuthalIntegrator)
    data = Input(description='Frame image data', type=np.ndarray)

    qx = Output(description='qx array with dimension of data', type=np.ndarray)
    qz = Output(description='qz array with dimension of data', type=np.ndarray)

    def evaluate(self):
        self.qx, self.qz = self.qconverion()

    def qconverion(self):
        chi = self.integrator.chiArray()
        twotheta = self.integrator.twoThetaArray()

        # Doble check what is chi = 0
        qx = 2 * np.pi / self.integrator.getvalue('Wavelength') * np.sin(twotheta) * np.sin(chi)
        qz = 2 * np.pi / self.integrator.getvalue('Wavelength') * np.sin(twotheta) * np.cos(chi)

        return qx, qz
