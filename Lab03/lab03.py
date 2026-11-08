"""
Computational Magnetic Resonance Imaging (CMRI) 2026/2027 Winter semester

- Author          : Jinho Kim, Haiting Huang
- Email           : <jinho.kim@fau.de>
- Contact         : <haiting.huang@fau.de>
"""

import numpy as np
import utils
from skimage.filters import window


class Lab03_op:
    def __init__(self, PF: float):
        """
        PF: Partial Fourier factor. 
            This factor is used to calculate the original k-space size.
        """
        self.PF = PF

    def load_kdata_pf(self) -> np.ndarray:
        """
        Load partial Fourier sampled kdata
        """
        # task 1.1
        mat = utils.load_data("kdata_phase_error_severe.mat")
        return mat["kdata"]

    def load_kdata_full(self) -> np.ndarray:
        """
        Load fully sampled kdata
        """
        # task 1.1
        mat = utils.load_data("kdata1.mat")
        return mat["kdata1"]

    def get_half_zf_kdata(self, kdata: np.ndarray) -> np.ndarray:
        """
        This function returns a half zero-filled kdata

        @param:
            kdata:          k-space data. shape: [N, M]
        @return:
            zf_kdata:       Half zero-filled kdata. shape: [N, N], dtype=complex
        """
        # task 1.2.1
        # Your code here ...

        N, M = kdata.shape
        center = N // 2
        zf_kdata = np.zeros((N, N), dtype=complex)
        kdata_sliced = kdata[ : , : center]
        zf_kdata[ : , : center] = kdata_sliced
        return zf_kdata

    def hermitian_symmetry(self, zf_kdata: np.ndarray) -> np.ndarray:
        """
        This function returns the Hermitian symmetry of the zero-filled k-space data without phase correction.

        @param:
            zf_kdata:       Zero-filled k-space data. shape: [N, N]
        @return:
            hm_kdata:       Hermitian symmetric kdata. shape: [N, N], dtype=complex
        """
        # task 1.2.2
        # Your code here ...
        N = zf_kdata.shape[0]
        center = N // 2
        hm_kdata = np.zeros_like(zf_kdata, dtype=complex)

        zf_kdata_conj = zf_kdata.conjugate()  # invert sign of imaginary part
        zf_kdata_conj = np.flip(zf_kdata_conj, axis=(0, 1))  # flip along both axes

        hm_kdata[:, : center] = zf_kdata[:, : center]  # left half is from zf_kdata (non-zero half of it)
        hm_kdata[:, center :] = zf_kdata_conj[:, center :]  # right half is from conj
        return hm_kdata

    def estim_phs(self, kdata) -> np.ndarray:
        """
        Phase estimation

        @Param:
            kdata:             asymmetric k-space data, shape: [N, M]
        @Return:
            estimated_phase:    estimated phase of the input kdata, shape: [N, N], dtype=float
        """
        # task 2.1
        # Your code here ...
        N, M = kdata.shape
        symmetric_strip = np.zeros((N, N), dtype=complex)
        win = window("hamming", (N, 2 * M - N))
        symmetric_strip[:, N-M : M] = kdata[:, N-M : M] * win
        symmetric_strip = utils.ifft2c(symmetric_strip)

        estimated_phase = np.zeros((N, N), dtype=float)
        estimated_phase = np.angle(symmetric_strip)

        return estimated_phase

    def get_window(self, kdata, type="ramp") -> np.ndarray:
        """
        This function returns the window for the Hermitian symmetric extension

        @Param:
            kdata:          asymmetric k-space data, shape: [N, M]
            type:           filter type ('ramp' or 'hamm')
        @Return:
            window_filter:  Window filter, shape: [N, N], dtype=complex
        """
        # task 3.1
        # TODO Your code here ...
        N, M = kdata.shape
        L = 2 * M - N + 1  # transition length
        norm_pos = np.linspace(0, 1, L)
        if type == "ramp":
            transition = 1 - norm_pos
        elif type == "hamm":
            h = 0.54 + 0.46 * np.cos(np.pi * norm_pos)
            transition = (h - 0.08) / 0.92
        else:
            raise ValueError("type must be in ['hamm', 'ramp']")

        w_1d = np.zeros(N)
        w_1d[: N-M] = 1
        w_1d[N-M : M+1] = transition
        window_filter = np.tile(w_1d, (N, 1))  #from 1d to 2d: shape [N, N]
        window_filter = window_filter.astype(complex)

        return window_filter

    def pf_margosian(self, kdata, wtype, **kwargs) -> np.ndarray:
        """
        Margosian reconstruction for partial Fourier (PF) MRI

        Param:
            kdata:      asymmetric k-space data, shape: [N, M]
            wtype:      The type of window ('ramp' or 'hamm')
        Return:
            I: reconstructed magnitude image, shape: [N, N], dtype=float
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'estim_phs' and 'get_window' in this method if you need to used them instead of calling them by self.estim_phs and self.get_window.
        estim_phs = kwargs.get("estim_phs", self.estim_phs)
        get_window = kwargs.get("get_window", self.get_window)

        # task 3.2
        # Your code here ...
        N, M = kdata.shape
        S_0 = np.zeros((N, N), dtype=complex)
        S_0[:, :M] = kdata  # from the slides
        win = get_window(kdata, wtype)
        I_0 = S_0 * win
        I_0 = utils.ifft2c(I_0)

        phase = estim_phs(kdata)
        I_0 = I_0 * np.exp(-1j * phase)

        I = np.zeros((N, N), dtype=float)
        I = np.real(I_0)

        return I

    def pf_pocs(self, kdata, Nite, **kwargs) -> np.ndarray:
        """
        POCS reconstruction for partial Fourier (PF) MRI

        Param:
            kdata:      asymmetric k-space data, shape: [N, M]
            Nite:       number of iterations

        Return:
            I: reconstructed magnitude image, shape: [N, N], dtype=complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'estim_phs' in this method if you need to used it instead of calling it by self.estim_phs.
        estim_phs = kwargs.get("estim_phs", self.estim_phs)

        # task 4.1
        # TODO Your code here ...
        N, M = kdata.shape

        # initialization step of slides
        S = np.zeros((N, N), dtype=complex)
        S[:, :M] = kdata  # S_0(k) in slides
        I = utils.ifft2c(S)  # I_0(r) in slides
        phase = estim_phs(kdata)

        # iteration steps of slides
        for _ in range(Nite):
            # phase step
            I = np.abs(I) * np.exp(1j * phase)

            # data consistency step
            S = utils.fft2c(I)
            S[:, :M] = kdata
            I = utils.ifft2c(S)

        return I


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab03 import *

    plots_dir = "plots"
    save_plots = True

    # %% 1.1 Define the lab03 object and load kdata.
    ## The partial Fourier factor is 9/16.
    PF = 9 / 16
    op = Lab03_op(PF)
    kdata = op.load_kdata_pf()
    kdata_full = op.load_kdata_full()

    # %% 1.2 Define half zero-filled kdata and Hermitian symmetric kdata
    half_zf_kdata = op.get_half_zf_kdata(kdata)
    hm_kdata = op.hermitian_symmetry(zf_kdata=half_zf_kdata)

    # plot both kdata
    utils.imshow(
        [kdata, half_zf_kdata, hm_kdata], norm=0.2,
        titles=["kdata", "half zero-filled k-space", "Hermitian symmetry k-space data"],
        filename=f"{plots_dir}/task_1-2_dataviz.png" if save_plots else None
    )

    # %% 1.3 reconstruct both kdata
    half_zf_recon = utils.ifft2c(half_zf_kdata)
    hm_recon = utils.ifft2c(hm_kdata)

    # plot reconstructions
    utils.imshow(
        [half_zf_recon, hm_recon],
        titles=["Half ZF reconstruction", "Hermitian symmetry reconstruction"],
        filename=f"{plots_dir}/task_1-3_reconstructed.png" if save_plots else None
    )
    
    # %% 2 phase estimation function
    # 2.1 define phase estimation function
    # 2.2 Estimate phase of zero-filled kdata
    phs_estimated = op.estim_phs(kdata)

    # 2.3 plot estimated phase
    utils.imshow(
        [phs_estimated], titles=["Estimated phase"], is_mag=False,
        filename=f"{plots_dir}/task_2_phase.png" if save_plots else None
    )

    # %% 3.1 define ramp / Hamming filter
    # 3.2 implement margosian reconstruction
    # 3.3 reconstruct PF kdata using Margosian with Ramp / Hamming filter
    margosian_ramp = op.pf_margosian(kdata, "ramp")
    margosian_hamm = op.pf_margosian(kdata, "hamm")

    # plot both reconstructions
    utils.imshow(
        [margosian_ramp, margosian_hamm],
        titles=["Margosian reconstruction (Ramp)", "Margosian reconstruction (Hamming)"],
        filename=f"{plots_dir}/task_3_margosian.png" if save_plots else None
    )

    # %% 4.1 implement POCS algorithm
    # 4.2 Perform POCS reconstruction on the PF kdata with multiple iterations
    iterations = [2, 4, 6, 8, 10]
    pocs_imgs = []
    for i in iterations:
        pocs_imgs.append(op.pf_pocs(kdata, i))

    # plot all the reconstructed images with different iterations
    utils.imshow(
        pocs_imgs,
        titles=[f"{i} iterations" for i in iterations],
        filename=f"{plots_dir}/task_4-2_pocs_iterations.png" if save_plots else None
    )

    # %% 4.3 determine the minimum number of iterations by ploting the difference image
    # plot difference images by comparing successive reconstructed images



    # %% 5.1 Plots: fully sampled, zero-filled, two Margosian, POCS reconstructions
    # Fully sampled reconstruction
    full_recon = utils.ifft2c(kdata_full)

    # 5.2 plot difference images between above reconstructions and the fully sampled reconstruction
    utils.imshow(
        [full_recon, half_zf_recon, margosian_ramp, margosian_hamm, pocs_imgs[-1]],
        titles=["Ground truth", "Zero-filled reconstruction", "Margosian ramp reconstruction", "Margosian hamming reconstruction", "POCS reconstruction with 10 iterations"],
        filename=f"{plots_dir}/task_5_all_reconstructions.png" if save_plots else None
    )



