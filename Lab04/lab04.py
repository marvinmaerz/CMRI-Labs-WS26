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
            trajectories:               trajectory of the k-space data. shape: [Readout, Spokes], dtype=complex
        """
        # task 1.2
        # Your code here ...
        Readout, Spokes = k_radial.shape

        trajectories = np.zeros((Readout, Spokes), dtype=complex)
        spoke = np.linspace(-0.5, 0.5, Readout)  # 1d array with len(Readout)-many values spaced evenly from -0.5 to 0.5
        angle = lambda i: (self.PI / 2) + (i * self.GA)  # gives angle offset for spoke i. Is 90° for spoke 0 (vertical line)

        for i in range(Spokes):
            trajectories[:, i] = spoke * np.exp(1j * angle(i))  # rotates spoke i by the angle for that spoke

        return trajectories

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
        Readout, Spokes = k_radial.shape

        delta_k = 1 / Readout  # constant spacing between dots along each spoke
        half_circ = self.PI * 0.5  # half circumference at the edge (since each spoke contributes twice), with radius 0.5
        spokes = half_circ / delta_k  # Nyquist criterion: delta_k >= half_circ / NSpokes (just rearranged for spokes)

        spokes_nyq = int(np.ceil(spokes))

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
        Readout, Spokes = k_radial.shape

        # k_cart = np.zeros((Readout, Spokes), dtype=complex)
        k_cart = grid(k_radial, traj, Readout)

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
        # TODO Your code here ...
        Readout, Spokes = k_radial.shape
        center = Readout // 2
        min_value = 1 / Spokes

        ramp = np.zeros((Readout, 1), dtype=float)
        ramp[:center, 0] = np.linspace(1.0, min_value, center)
        ramp[center:, 0] = np.linspace(min_value, 1.0, Readout - center)
        # print(f"Ramp values (dtype: {ramp.dtype}, shape: {ramp.shape}):\n{ramp}")
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
        Readout, Spokes = k_radial.shape

        k_cart_ds = np.zeros((Readout, Spokes), dtype=complex)
        ramp = get_ramp(k_radial)
        k_weighted = k_radial * ramp

        k_cart_ds = grid(k_weighted, traj, Readout)

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
        Readout, Spokes = k_radial.shape

        k_cart_ds_os = np.zeros((Readout * os_rate, Spokes * os_rate), dtype=complex)
        ramp = get_ramp(k_radial)
        k_weighted = k_radial * ramp

        k_cart_ds_os = grid(k_weighted, traj, Readout * os_rate)

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
        Readout_os = ov_image.shape[0]
        center_os = Readout_os // 2
        center_dist_x = target_shape[0] // 2
        center_dist_y = target_shape[1] // 2

        image_crop = np.zeros(target_shape, dtype=complex)
        image_crop[:, : ] = ov_image[center_os - center_dist_x : center_os + center_dist_x, center_os - center_dist_y : center_os + center_dist_y]

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
        Readout, Spokes = k_radial.shape
        center = Readout // 2

        delta = np.zeros_like(k_radial)
        delta[center, :] = 1
        delta[center, 0] = 1
        c = np.zeros((Readout * os_rate, Readout * os_rate), dtype=complex)

        kernel = grid(delta, traj, Readout * os_rate)
        c = utils.ifft2c(kernel)

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
        # decimate2d = kwargs.get("decimate2d", self.decimate2d)
        get_c = kwargs.get("get_c", self.get_c)
        center_crop_2d = kwargs.get("center_crop_2d", self.center_crop_2d)

        a = 1

        # task 5.2
        # Your code here ...
        Readout, Spokes = k_radial.shape

        deapod_recon = np.zeros((Readout, Readout), dtype=complex)
        k_os = grid_radial_ds_os(k_radial, traj, os_rate)  # oversampling
        img_os = utils.ifft2c(k_os)  # reconstruction, part in braces in the instructions
        c = get_c(k_radial, traj, os_rate)
        mhat = 1 / (c + a) * img_os # mhat(x,y) formula
        deapod_recon = center_crop_2d(mhat, (Readout, Readout))

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
        Readout, Spokes = k_radial.shape

        traj: np.ndarray = self.get_traj(k_radial) * 2 * self.PI  # spokes scaled to length 2*PI
        traj = traj.flatten()  # [Readout * Spokes] 1d

        ktraj = np.stack([traj.real, traj.imag])
        ktraj = torch.tensor(ktraj, dtype=torch.float32).to(self.device)

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
        Readout, Spokes = k_radial.shape

        ramp = get_ramp(k_radial)
        k_weighted = k_radial * ramp
        k_weighted = k_weighted.flatten()
        k_weighted = k_weighted.reshape(1, 1, -1)  # [1, 1, Readout*Spokes]

        nufft_kdata = torch.tensor(k_weighted, dtype=torch.complex64).to(self.device)

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
        Readout, Spokes = k_radial.shape

        k_traj = nufft_traj(k_radial)
        k_data = nufft_kdata(k_radial)

        adjnufft = tkbn.KbNufftAdjoint(im_size=im_size).to(self.device)
        recon = adjnufft(k_data, k_traj)

        nufft_recon = recon.squeeze().cpu().numpy()  # [Readout, Readout], 1-dims removed by squeeze()

        return nufft_recon


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab04 import *
    import matplotlib.pyplot as plt

    save_plots = False
    # %% 1.1 Load data
    op = Lab04_op()
    k_radial = op.load_kdata()
    utils.imshow([k_radial], norm=0.3, titles=["k_radial"],
        filename="task_1-1_k_radial.png" if save_plots else None
    )

    # %% 1.2 Radial sampling pattern
    trajectories = op.get_traj(k_radial)

    # plot trajectory
    utils.plot_spokes(trajectories, 100)

    # %% 1.3 Calculate Nyquist rate of radial sampling
    spokes_nyq = op.calc_nyquist(k_radial)

    # print the Nyquist rate
    print(f"Nyquist rate for k_radial: {spokes_nyq}")

    # %% 2.1, 2.2 Mapping radial-kspace to Cartesian k-space
    k_cart = op.grid_radial(k_radial, trajectories)

    # reconstruct the Cartesian k-space
    k_cart_recon = utils.ifft2c(k_cart)

    # plot
    utils.imshow([k_cart], norm=0.2, titles=["k_cart"],
        filename="task_2-1_grid.png" if save_plots else None
    )
    utils.imshow([k_cart_recon], titles=["k_cart_recon"],
        filename="task_2-2_grid_recon.png" if save_plots else None
    )

    # %% 3.1 ramp filter
    ramp = op.get_ramp(k_radial)
    plt.plot(ramp)
    plt.show()

    # 3.2 density compensation to get density compensated Cartesian k-space
    k_cart_ds =  op.grid_radial_ds(k_radial, trajectories)

    # plot the density compensated Cartesian k-space
    utils.imshow([k_cart_ds], norm=0.2, titles=["k_cart_ds (ramp filter)"],
        filename="task_3-1.png" if save_plots else None
    )

    # reconstruct the density compensated Cartesian k-space
    k_cart_ds_recon = utils.ifft2c(k_cart_ds)

    # plot the reconstructed image
    utils.imshow([k_cart_ds_recon], titles=["Gridded k-space with ramp filter"],
        filename="task_3-2.png" if save_plots else None
    )

    # %% 4.1 apply oversampling to density compensated k-space
    k_cart_ds_os = op.grid_radial_ds_os(k_radial, trajectories, 2)

    # reconstruct the oversampled k-space
    k_cart_ds_os_recon = utils.ifft2c(k_cart_ds_os)

    # 4.2 cropping
    k_cart_ds_os_recon_cropped = op.center_crop_2d(k_cart_ds_os_recon, (384, 384))

    # plot the above data
    utils.imshow(
        [k_cart_ds_os], norm=0.2, titles=["Oversampled k-space"], filename="task_4-1_os.png" if save_plots else None
    )
    utils.imshow(
        [k_cart_ds_os_recon], titles=["Oversampled k-space reconstruction"], filename="task_4-1_os_recon.png" if save_plots else None
    )
    utils.imshow(
        [k_cart_ds_os_recon_cropped, k_cart_ds_recon], titles=["Oversampled", "Non-oversampled"],
        filename="task_4-1_os_non_os.png" if save_plots else None
    )

    # %% 5.1 get the griding kernel
    c = op.get_c(k_radial, trajectories, 2)
    utils.imshow([c], titles=["deapodization factor c"])

    # 5.2 apply deapodization
    k_cart_ds_os_recon_deapod_cropped = op.deapodization(k_radial, trajectories, 2)

    # plot the reconstructions with and without deapodization
    utils.imshow([k_cart_ds_os_recon_deapod_cropped, k_cart_ds_os_recon_deapod_cropped], titles=["deapodized", "non-deapodized"],
        filename="task_5-1_deadodized_non_deapo.png" if save_plots else None
    )

    # %% 6.1 NUFFT radial trajectory
    nufft_traj = op.nufft_traj(k_radial)

    # 6.2 NUFFT k-data
    nufft_k = op.nufft_kdata(k_radial)

    # 6.3 NUFFT reconstruction
    nufft_recon = op.nufft_recon(k_radial, (384, 384))

    # plot reconstructions: without density compensation, with density compensation,
    # oversampled, de-apodized, NUFFT


