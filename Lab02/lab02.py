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
        mat = utils.load_data("Lab02/kdata1.mat")
        return mat["kdata1"]

    def load_kdata_os(self):
        """
        Load oversampled kdata
        """
        # task 1.1
        mat = utils.load_data("Lab02/kdata2.mat")
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
        x = fftshift(x, axes=axes)
        x = fft2(x, axes=axes, norm="ortho")
        x = ifftshift(x, axes=axes)
        return x

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
        x = ifftshift(x, axes=axes)
        x = ifft2(x, axes=axes, norm="ortho")
        x = fftshift(x, axes=axes)
        return x

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
        N = kdata.shape[0]
        filter = np.zeros_like(kdata, dtype=complex)
        center = N // 2
        m_half = mask_size // 2
        filter[ center - m_half : center + m_half, center - m_half : center + m_half ] = 1
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
        filtered_kdata = kdata * filter  # conv in fourier space is simple multiplication
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
        N = kdata.shape[0]
        filter_2d = get_square_filter(kdata, mask_size)
        center_row = filter_2d.shape[0] // 2
        filter_1d = filter_2d[center_row].reshape((N, 1))
        # print(f"filter_1d shape: {filter_1d.shape}")
        filter_1d_ifft = ifft2c(filter_1d)
        psf = np.abs(filter_1d_ifft).squeeze()
        # print(f"psf shape: {psf.shape}")
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
        peak_idx = psf.argmax()  # index of highest point of psf
        half_max = psf.max() / 2  # half value of that highest peak
        left_idx = np.argmin(np.abs(psf[ : peak_idx] - half_max))  # index of half_max in psf on the left side of the peak
        right_idx = peak_idx + np.argmin(np.abs(psf[ peak_idx : ] - half_max))  # analogously on right side
        fwhm = right_idx - left_idx  # width of the highest psf peak at half its maximum
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
        N = kdata.shape[0]
        center = N // 2
        m_half = mask_size // 2
        filter = np.zeros_like(kdata, dtype=complex)
        hamming_window = window("hamming", (mask_size, mask_size))
        filter[center - m_half: center + m_half, center - m_half: center + m_half] = hamming_window
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
        N = kdata.shape[0]
        filter_2d = get_hamming_filter(kdata, mask_size)
        filter_1d = filter_2d[N//2].reshape((N,1))
        psf = np.abs(ifft2c(filter_1d)).squeeze()
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
        cropped_img = ifft2c(kdata_os)
        M = cropped_img.shape[1]
        M_ds = M // os_factor  # donwsampled M size
        center_idx = cropped_img.shape[1] // 2
        start = center_idx - M_ds // 2
        cropped_img = cropped_img[:, start : start + M_ds ]
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
    reconstructed_image = op.ifft2c(kdata)
    reconstructed_image = op.fft2c(reconstructed_image)
    reconstructed_image = op.ifft2c(reconstructed_image)  # should be same as the first one
    # plot magnitude and phase
    utils.imshow([np.abs(reconstructed_image), np.angle(reconstructed_image)],
                 titles=["Magnitude", "Phase"], is_mag=False)

    # %% 2.1 Define square filters for [64, 128, 256]
    square_filter64 = op.get_square_filter(kdata, 64)
    square_filter128 = op.get_square_filter(kdata, 128)
    square_filter256 = op.get_square_filter(kdata, 256)

    utils.imshow([square_filter64, square_filter128, square_filter256],
        titles=["square_filter64", "square_filter128", "square_filter256"])

    # %% 2.2 Apply the filter to fully sampled k-space
    filtered_kdata_square64 = op.filtering(kdata, square_filter64)
    filtered_kdata_square128 = op.filtering(kdata, square_filter128)
    filtered_kdata_square256 = op.filtering(kdata, square_filter256)

    # %% 2.3 Reconstruct the filtered k-space
    reconstructed_image_square64 = op.ifft2c(filtered_kdata_square64)
    reconstructed_image_square128 = op.ifft2c(filtered_kdata_square128)
    reconstructed_image_square256 = op.ifft2c(filtered_kdata_square256)

    # plot and compare with reconstructed image from task 1.2
    utils.imshow([reconstructed_image, reconstructed_image_square64,
        reconstructed_image_square128, reconstructed_image_square256],
        titles=["Reconstructed", "Square 64x64", "Square 128x128", "Square 256x256"])

    # %% 3.1, 3.2 Generate 1D PSF for square filter [64, 128, 256]
    psf_square64 = op.get_psf_1d_square(kdata, mask_size=64)
    psf_square128 = op.get_psf_1d_square(kdata, mask_size=128)
    psf_square256 = op.get_psf_1d_square(kdata, mask_size=256)

    # %% 3.3 plot the PSFs
    # utils.plot([psf_square64, psf_square128, psf_square256],
    #     titles=["PSF64", "PSF128", "PSF256"], xlim=[256 - 30, 256 + 30])

    # %% 3.4 compute full width at half-maximum (FWHM) for each PSF
    fwhm64 = op.get_fwhm(psf_square64)
    fwhm128 = op.get_fwhm(psf_square128)
    fwhm256 = op.get_fwhm(psf_square256)

    print(f"FWHM for Square 64: {fwhm64:.3f}")
    print(f"FWHM for Square 128: {fwhm128:.3f}")
    print(f"FWHM for Square 256: {fwhm256:.3f}")
    # %% 4.1 Define Hamming filters for [64, 128, 256]
    hamming_filter64 = op.get_hamming_filter(kdata, 64)
    hamming_filter128 = op.get_hamming_filter(kdata, 128)
    hamming_filter256 = op.get_hamming_filter(kdata, 256)

    utils.imshow([hamming_filter64, hamming_filter128, hamming_filter256],
                 titles=["hamming_filter64", "hamming_filter128", "hamming_filter256"])

    # %% 4.2 Reconstruct filtered k-space and compare them with reconstructions from 1.2, 2.3
    # Apply filter to k-space
    filtered_kdata_hamming64 = op.filtering(kdata, hamming_filter64)
    filtered_kdata_hamming128 = op.filtering(kdata, hamming_filter128)
    filtered_kdata_hamming256 = op.filtering(kdata, hamming_filter256)

    # Reconstruct
    reconstructed_image_hamming64 = op.ifft2c(filtered_kdata_hamming64)
    reconstructed_image_hamming128 = op.ifft2c(filtered_kdata_hamming128)
    reconstructed_image_hamming256 = op.ifft2c(filtered_kdata_hamming256)

    # display and compare
    utils.imshow(
        [
            reconstructed_image,
            reconstructed_image_hamming64,
            reconstructed_image_hamming128,
            reconstructed_image_hamming256,
        ],
        titles=["Reconstructed", "Hamming 64x64", "Hamming 128x128", "Hamming 256x256"]
    )

    utils.imshow(
        [
            reconstructed_image_square64,
            reconstructed_image_square128,
            reconstructed_image_square256,
            reconstructed_image_hamming64,
            reconstructed_image_hamming128,
            reconstructed_image_hamming256,
        ],
        titles=[
            "64x64 (Square)",
            "128x128 (Square)",
            "256x256 (Square)",
            "64x64(Hamming)",
            "128x128(Hamming)",
            "256x256(Hamming)",
        ],
        num_rows=2,
        suptitle="Comparison of square and hamming filters"
    )
    
    # %% 4.3 Compute PSFs for different patterns, and compare those from 3.1, 3.2
    psf_hamming64 = op.get_psf_1d_hamming(kdata, 64)
    psf_hamming128 = op.get_psf_1d_hamming(kdata, 128)
    psf_hamming256 = op.get_psf_1d_hamming(kdata, 256)

    # %% 4.4 Compute full width at half-maximum for each PSF
    fwhm64 = op.get_fwhm(psf_hamming64)
    fwhm128 = op.get_fwhm(psf_hamming128)
    fwhm256 = op.get_fwhm(psf_hamming256)

    # display and compare the PSFs of hamming and square windows
    print(f"FWHM for Hamming 64: {fwhm64:.3f}")
    print(f"FWHM for Hamming 128: {fwhm128:.3f}")
    print(f"FWHM for Hamming 256: {fwhm256:.3f}")
    # %% 5.1 Reconstruct and remove the oversampling
    # reconstruct oversampled k-space
    reconstructed_image_os = op.ifft2c(kdata_os)

    # cropping
    decimated_image = op.cut_oversampled(kdata_os, 2)

    # display reconstructions before and after cropping
    utils.imshow([reconstructed_image_os, decimated_image], titles=["reconstructed_image_os", "decimated_image"])
