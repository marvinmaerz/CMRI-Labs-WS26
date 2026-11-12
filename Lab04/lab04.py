"""
Computational Magnetic Resonance Imaging (CMRI) 2026/2027 Winter semester

- Author          : Jinho Kim, Haiting Huang
- Email           : <jinho.kim@fau.de>
- Contact         : <haiting.huang@fau.de>
"""

from typing import Tuple

import numpy as np
import torch
import torchkbnufft as tkbn
import utils
from grid import grid


class Lab04_op:

    def __init__(self, device_num=0):
        self.PI = np.pi
        self.GA = 111.246117975 * self.PI / 180  # Golden angle

        # For NUFFT operator
        self.device = torch.device(f"cuda:{device_num}") if torch.cuda.is_available() else torch.device("cpu")

    def load_kdata(self) -> np.ndarray:
        """
        Load radial k-space data
        """
        # task 1.1
        mat = utils.load_data("radial_data.mat")
        k_radial = mat["k"]
        return k_radial

    def get_traj(self, k_radial) -> np.ndarray:
        """
        This method returns the trajectory of the radial k-space data.

        Args:
            k_radial:           k-space data. shape: [Readout, Spokes]

        Return:
            traj:               trajectory of the k-space data. shape: [Readout, Spokes], dtype=complex
        """
        # task 1.2
        # Your code here ...

        traj = None

        return traj

    def calc_nyquist(self, k_radial) -> int:
        """
        This method calculates the minimum number of spokes that satisfies Nyquist sampling theorm.

        Args:
            k_radial:        k-space data. shape: [Readout, Spokes]

        Returns:
            spokes_nyq:      minimum number of spokes that satisfy Nyquist sampling theorem. (Ceilling up integer)
        """
        # task 1.3
        # Your code here ...

        spokes_nyq = None

        return spokes_nyq

    def grid_radial(self, k_radial, traj) -> np.ndarray:
        """
        This method maps the radial k-space data to Cartesian coordinate
        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]
            traj:           trajectory of the k-space data. shape: [Readout, Spokes]

        Returns:
            k_cart:         kdata in cartesian coordinate. shape: [Readout, Readout]), dtype=complex
        """
        # task 2.1
        # Your code here ...

        k_cart = None

        return k_cart

    def get_ramp(self, k_radial) -> np.ndarray:
        """
        This method returns a ramp filter that can be used to weight the radial kspace data.
    
        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]

        Returns:
            ramp:           ramp filter. shape: [Readout, 1], dtype=float
        """
        # task 3.1
        # Your code here ...

        ramp = None

        return ramp

    def grid_radial_ds(self, k_radial, traj, **kwargs) -> np.ndarray:
        """
        This method maps the density compensatied radial k-space data to Cartesian k-data using the triangular gridding kernel of width 2.

        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]
            traj:           trajectory of the k-space data. shape: [Readout, Spokes]

        Returns:
            k_cart_ds:      Densitiy compensated Cartesian k-space data. shape: [Readout, Readout]), dtype=complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'get_ramp' in this method if you need to used it instead of calling it by self.get_ramp.
        get_ramp = kwargs.get("get_ramp", self.get_ramp)

        # task 3.2
        # Your code here ...

        k_cart_ds = None

        return k_cart_ds

    def grid_radial_ds_os(self, k_radial, traj, os_rate: int, **kwargs) -> np.ndarray:
        """
        This method maps the density compensatied radial k-space data to Cartesian coordinate

        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]
            traj:           trajectory of the k-space data. shape: [Readout, Spokes]
            os_rate:        oversampling rate

        Returns:
            k_cart_ds_os:   Densitiy compensated oversampled Cartesian k-space data. shape: [Readout * os_rate, Readout * os_rate], dtype=complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'get_ramp' in this method if you need to used it instead of calling it by self.get_ramp.
        get_ramp = kwargs.get("get_ramp", self.get_ramp)

        # task 4.1
        # Your code here ...

        k_cart_ds_os = None

        return k_cart_ds_os

    def center_crop_2d(self, ov_image, target_shape: Tuple[int, int]) -> np.ndarray:
        """
        This method crops the image to the desired size.

        Args:
            ov_image (np.ndarray):          Oversmapled image. shape: [Oversampled_Readout, Oversampled_Readout]
            target_shape (tuple):           Desired shape of the image

        Returns:
            image_crop (np.ndarray):        cropped image. shape: target_shape, dtype=complex
        """
        # task 4.2
        # Your code here ...

        image_crop = None

        return image_crop

    def get_c(self, k_radial, traj, os_rate) -> np.ndarray:
        """
        This method calculates the deapodization factor c(x,y) for the deapodization.
        Think about how to utilize the grid function to calculate c(x,y).
        If you want to use delta function, set 1 of the delta function at the center of the k-space. (ex. at Readout//2)

        Args:
            k_radial (np.ndarray):      k-space data. shape: [Readout, Spokes]
            traj (np..ndarray):         trajectory of the k-space data. shape: [Readout, Spokes]
            os_rate (int):              oversampling rate

        Returns:
            c:                          deapodization factor c(x,y). shape: [Oversampled_Readout, Oversampled_Readout], dtype=complex
        """
        # task 5.1
        # Your code here ...
        c = None

        return c

    def deapodization(self, k_radial, traj, os_rate, **kwargs) -> np.ndarray:
        """
        This method performs deapodization in the image domain.

        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]
            traj:           trajectory of the k-space data. shape: [Readout, Spokes]
            os_rate:        oversampling rate

        Returns:
            deapod_recon:   De-apodized reconstruction image. shape: [Readout, Readout], dtype=complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'grid_radial_ds_os' and 'decimate2d' in this method if you need to used them instead of calling them by self.grid_radial_ds_os and self.decimate2d.
        grid_radial_ds_os = kwargs.get("grid_radial_ds_os", self.grid_radial_ds_os)
        decimate2d = kwargs.get("decimate2d", self.decimate2d)
        get_c = kwargs.get("get_c", self.get_c)

        a = 1

        # task 5.2
        # Your code here ...

        deapod_recon = None

        return deapod_recon

    def nufft_traj(self, k_radial) -> torch.Tensor:
        """
        This method returns the trajectory of the radial k-space data for NUFFT.

        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]

        Returns:
            ktraj:          trajectory of the k-space data for NUFFT. shape: [2, Readout * Spokes], dtype=float
                            Do not forget to set the self.device for the tensor.
        """
        # task 6.1
        # Your code here ...

        ktraj = None

        return ktraj

    def nufft_kdata(self, k_radial, **kwargs) -> torch.Tensor:
        """
        This method prepares the k-space data for NUFFT.
        - Use density commpenstated k-space data for NUFFT.

        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]

        Returns:
            nufft_kdata:    NUFFT k-space data. shape: [Batch(1), Coil(1), Readout*Spokes], dtype=complex
                            Do not forget to set the self.device for the tensor.
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'get_ramp' in this method if you need to used it instead of calling it by self.get_ramp.
        get_ramp = kwargs.get("get_ramp", self.get_ramp)

        # task 6.2
        # Your code here ...

        nufft_kdata = None

        return nufft_kdata

    def nufft_recon(self, k_radial, im_size: Tuple[int, int], **kwargs) -> np.ndarray:
        """
        This method reconstructs the image from the k-space data using NUFFT.

        Args:
            k_radial:       k-space data. shape: [Readout, Spokes]
            im_size:        size of the desired reconstruction image.

        Returns:
            nufft_recon:    NUFFT reconstructed image. shape: [im_size], dtype=complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'nufft_traj' and 'nufft_kdata' in this method if you need to used them instead of calling them by self.nufft_traj and self.nufft_kdata.
        nufft_traj = kwargs.get("nufft_traj", self.nufft_traj)
        nufft_kdata = kwargs.get("nufft_kdata", self.nufft_kdata)

        # task 6.3
        # Your code here ...

        nufft_recon = None

        return nufft_recon


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab04 import *

    # %% 1.1 Load data
    op = Lab04_op()
    k_radial = op.load_kdata()
    utils.imshow([k_radial], norm=0.3)

    # %% 1.2 Radial sampling pattern
    traj = None

    # plot trajectory
    

    # %% 1.3 Calculate Nyquist rate of radial sampling
    spokes_nyq = None

    # print the Nyquist rate


    # %% 2.1, 2.2 Mapping radial-kspace to Cartesian k-space
    k_cart = None

    # reconstruct the Cartesian k-space
    k_cart_recon = None

    # plot


    # %% 3.1 ramp filter
    # 3.2 density compensation to get density compensated Cartesian k-space
    k_cart_ds = None

    # plot the density compensated Cartesian k-space

    # reconstruct the density compensated Cartesian k-space
    k_cart_ds_recon = None

    # plot the reconstructed image


    # %% 4.1 apply oversampling to density compensated k-space
    k_cart_ds_os = None

    # reconstruct the oversampled k-space
    k_cart_ds_os_recon = None

    # 4.2 cropping
    k_cart_ds_os_recon_cropped = None

    # plot the above data


    # %% 5.1 get the griding kernel

    # 5.2 apply deapodization
    k_cart_ds_os_recon_deapod_cropped = None

    # plot the reconstructions with and without deapodization


    # %% 6.1 NUFFT radial trajectory
    nufft_traj = None

    # 6.2 NUFFT k-data
    nufft_k = None

    # 6.3 NUFFT reconstruction
    nufft_recon = None

    # plot reconstructions: without density compensation, with density compensation,
    # oversampled, de-apodized, NUFFT


