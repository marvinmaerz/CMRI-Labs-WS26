"""
Computational Magnetic Resonance Imaging (CMRI) 2026/2027 Winter semester

- Author          : Jinho Kim, Haiting Huang
- Email           : <jinho.kim@fau.de>
- Contact         : <haiting.huang@fau.de>
"""

import matplotlib.pyplot as plt
import numpy as np
import utils
from numpy.fft import fft2, fftshift, ifft2, ifftshift
from skimage.filters import window


class Lab02_op:
    def load_kdata(self):
        """
        Load fully sampled kdata
        """
        # task 1.1
        mat = utils.load_data("kdata1.mat")
        return mat["kdata1"]

    def load_kdata_os(self):
        """
        Load oversampled kdata
        """
        # task 1.1
        mat = utils.load_data("kdata2.mat")
        return mat["kdata2"]

    def fft2c(self, x: np.ndarray, axes=(-2, -1)) -> np.ndarray:
        """
        This function calculates the 2D Fourier Transform of the input array x.
        Since the center of the kdata is in the middle of the matrix, we need 
        to shift the center to the top-left corner. 
        Do not forget to preserve the energy of the signal (Keep orthonormality).

        args:
            x:      Input array. shape: [N, N]
            axes:   Axes to perform the Fourier Transform. (tuple of int)

        return:
            The 2D Fourier Transform of the input array x. shape: [N, N], dtype=complex
        """
        # task 1.2
        # Your code here ...

        return None

    def ifft2c(self, x: np.ndarray, axes=(-2, -1)) -> np.ndarray:
        """
        This function calculates the 2D inverse Fourier Transform of the input array x.
        Since the center of the kdata is in the middle of the matrix, we need 
        to shift the center to the top-left corner. 
        Do not forget to preserve the energy of the signal (Keep orthonormality).

        args:
            x:      Input array. shape: [N, N]
            axes:   Axes to perform the inverse Fourier Transform. (tuple of int)

        return:
            The 2D inverse Fourier Transform of the input array x. shape: [N, N], dtype=complex

        """
        # task 1.2
        # Your code here ...

        return None

    def get_square_filter(self, kdata: np.ndarray, mask_size: int) -> np.ndarray:
        """
        This function returns the zero-filled square filter of the same size as kdata.
        The outer values of the filter are zero and the center values of [mask_size x mask_size] are one.

        @param:
            kdata:          k-space data. shape: [N, N]
            mask_size:      size of the filter. 
        @return:
            filter:         Filter. shape: [N, N], dtype=complex | bool
        """
        # task 2.1
        # Your code here ...

        filter = None
        return filter

    def filtering(self, kdata: np.ndarray, filter: np.ndarray) -> np.ndarray:
        """
        This function applies the filter to the ksapce

        @param:
            kdata:              k-space data. shape: [N, N]
            filter:             Cropping filter shape: [N, N]
        @return:
            filtered_kdata:     Filtered k-space data. shape: [N, N], dtype=complex
        """
        # task 2.2
        # Your code here ...

        filtered_kdata = None
        return filtered_kdata

    def get_psf_1d_square(self, kdata: np.ndarray, mask_size: int, **kwargs) -> np.ndarray:
        """
        This function returns the 1D point spread function (PSF) of the square filter.
        For the 1D filter, you take the middle row of the 2D filter.
        The 1D PSF is the absolute value of the inverse Fourier Transform of the 1D filter.

        @param:
            kdata:          K-space data. shape: [N, N]
            mask_size:      Size of the filter. int
        @return:
            psf:            Point spread function. shape: [N], dtype=float
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        get_square_filter = kwargs.get("get_square_filter", self.get_square_filter)
        ifft2c = kwargs.get("ifft2c", self.ifft2c)

        # task 3.1
        # Your code here ...

        psf = None

        return psf

    def get_fwhm(self, psf: np.ndarray) -> int:
        """
        This function calculates the Full Width Half Maximum of the given 1D PSF.

        @param:
            psf:            1D point spread function. shape: [N]
        @return:
            fwhm:           Full Width Half Maximum.
        """
        # task 3.4
        # Your code here ...

        fwhm = None

        return fwhm

    def get_hamming_filter(self, kdata: np.ndarray, mask_size: int) -> np.ndarray:
        """
        This function returns Hamming filter of the same size as kdata.
        The outer values of the filter are zero and the center is a Hamming filter.
        To generate the Hamming filter, use the 'window' function from skimage.filters.

        @param:
            kdata:          k-space data. shape: [N, N]
            mask_size:      size of the filter.
        @return:
            filter:         Filter. shape: [N, N], dtype=complex | bool
        """
        # task 4.1
        # Your code here ...

        filter = None
        return filter

    def get_psf_1d_hamming(self, kdata: np.ndarray, mask_size: int, **kwargs) -> np.ndarray:
        """
        This function returns the 1D point spread function (PSF) of the hamming filter.
        For the 1D filter, you take the middle row of the 2D filter.
        The 1D PSF is the absolute value of the inverse Fourier Transform of the 1D filter.

        @param:
            kdata:          K-space data. shape: [N, N]
            mask_size:      Size of the filter. 
        @return:
            psf:            Point spread function. shape: [N], dtype=float
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        get_hamming_filter = kwargs.get("get_hamming_filter", self.get_hamming_filter)
        ifft2c = kwargs.get("ifft2c", self.ifft2c)

        # task 4.3
        # Your code here ...

        psf = None
        return psf

    def cut_oversampled(self, kdata_os, os_factor, **kwargs) -> np.ndarray:
        """
        This function removes the oversampling by cropping the frequency-encoding dimension in the image domain.

        @param:
            kdata_os:           Oversampled k-space data. shape: [N, M]
            os_factor:          Oversampling factor.
        @return:
            cropped_img:        Cropped image. shape: [N, M//os_factor], dtype=complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        ifft2c = kwargs.get("ifft2c", self.ifft2c)

        # task 5.1
        # Your code here ...

        cropped_img = None
        return cropped_img


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab02 import *

    # %% 1.1 Define the lab02 object and load kdata and kdata_os
    op = Lab02_op()
    kdata = op.load_kdata()
    kdata_os = op.load_kdata_os()

    # %% 1.2 Reconstruct fully sampled k-space
    reconstructed_image = None
    # plot magnitude and phase

    # %% 2.1 Define square filters for [64, 128, 256]
    square_filter64 = None
    square_filter128 = None
    square_filter256 = None

    # %% 2.2 Apply the filter to fully sampled k-space
    filtered_kdata_square64 = None
    filtered_kdata_square128 = None
    filtered_kdata_square256 = None

    # %% 2.3 Reconstruct the filtered k-space
    reconstructed_image_square64 = None
    reconstructed_image_square128 = None
    reconstructed_image_square256 = None

    # plot and compare with reconstructed image from task 1.2


    # %% 3.1, 3.2 Generate 1D PSF for square filter [64, 128, 256]
    psf_square64 = None
    psf_square128 = None
    psf_square256 = None

    # %% 3.3 plot the PSFs


    # %% 3.4 compute full width at half-maximum (FWHM) for each PSF
    fwhm64 = None
    fwhm128 = None
    fwhm256 = None

    # %% 4.1 Define Hamming filters for [64, 128, 256]
    hamming_filter64 = None
    hamming_filter128 = None
    hamming_filter256 = None

    # %% 4.2 Reconstruct filtered k-space and compare them with reconstructions from 1.2, 2.3
    # Apply filter to k-space
    filtered_kdata_hamming64 = None
    filtered_kdata_hamming128 = None
    filtered_kdata_hamming256 = None

    # Reconstruct
    reconstructed_image_hamming64 = None
    reconstructed_image_hamming128 = None
    reconstructed_image_hamming256 = None

    # display and compare

    
    # %% 4.3 Compute PSFs for different patterns, and compare those from 3.1, 3.2
    psf_hamming64 = None
    psf_hamming128 = None
    psf_hamming256 = None

    # %% 4.4 Compute full width at half-maximum for each PSF
    fwhm64 = None
    fwhm128 = None
    fwhm256 = None

    # display and compare the PSFs of hamming and square windows

    # %% 5.1 Reconstruct and remove the oversampling
    # reconstruct oversampled k-space
    reconstructed_image_os = None

    # cropping
    decimated_image = None

    # display reconstructions before and after cropping
    
