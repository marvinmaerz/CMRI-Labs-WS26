"""
Computational Magnetic Resonance Imaging (CMRI) 2026/2027 Winter semester

- Author          : Jinho Kim, Haiting Huang
- Email           : <jinho.kim@fau.de>
- Contact         : <haiting.huang@fau.de>
"""

from typing import Optional, Tuple

import numpy as np
import utils
from scipy.linalg import fractional_matrix_power, pinv


class Lab05_op:

    def load_data(self):
        """
        Load data, including:
        kdata: fully-sampled kspace data
        sens_maps: coil sensitivity maps
        noise_maps: noise-only scan
        """
        mat = utils.load_data("data_brain_8coils.mat")
        kdata = mat["d"]
        sens_maps = mat["c"]
        noise_maps = mat["n"]
        return kdata, sens_maps, noise_maps

    def sos_comb(self, m: np.ndarray, axis: int = -1) -> np.ndarray:
        """
        Sum of square.

        :param m: multicoil images [nPE, nRO, nCh]

        :return: mc: combined image [nPE, nRO], dtype: float
        """
        # task 1.2.1
        # Your code here ...

        mc = np.sqrt(np.sum(np.abs(m) ** 2, axis=axis))
        return mc

    def ls_comb(
        self, 
        coil_imgs: np.ndarray, 
        sens_maps: np.ndarray, 
        PSI: Optional[np.ndarray] = None, 
        axis: int = -1, 
        **kwargs
    ) -> np.ndarray:
        """
        Least-squares (matched filter)

        :param coil_imgs:               multicoil images [nPE,nRO,nCh]
        :param sens_maps:               coil sensitivity maps [nPE,nRO,nCh]
        :param PSI:                     (Optional) noise correlation matrix [nCh, nCh]

        :return: coil_comb_img:         combined image [nPE,nRO], dtype: complex
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        # Use 'apply_psi' in this method if you need to used it instead of calling it by self.apply_psi.
        apply_psi = kwargs.get("apply_psi", self.apply_psi)

        # task 1.2.2
        # Your code here ...
        # nPE, nRO, nCh = coil_imgs.shape
        # coil_comb_img = np.zeros((nPE, nRO), dtype=complex)

        if PSI is not None:
            # After 1.b.ii.2 and 1.b.ii.3, you should apply the noise correlation matrix to the coil sensitivity maps and coil images.
            coil_imgs = apply_psi(coil_imgs, PSI)
            sens_maps = apply_psi(sens_maps, PSI)

        numerator = np.sum(np.conj(sens_maps) * coil_imgs, axis=axis)
        denominator = np.sum(np.abs(sens_maps) ** 2, axis=axis)
        out = np.zeros_like(numerator)
        coil_comb_img = np.divide(numerator, denominator, out=out, where=(denominator != 0.0))  # "where" avoids division by zero and "out" sets this area to zero instead of nan

        return coil_comb_img

    def get_psi(self, noise_maps: np.ndarray) -> np.ndarray:
        """
        This function calculates the noise covariance matrix
        Use np.cov function to calculate the covariance matrix.

        Args:
            noise_maps (np.ndarray):    noise maps [nPE, nCh]

        Returns:
            psi (np.ndarray):           noise covariance matrix [nCh,nCh], dtype: complex
        """
        # task 1.2.2
        # Your code here ...
        # nCh = noise_maps.shape[1]
        psi = np.cov(noise_maps, rowvar=False).astype(complex)
        # print(f"PSI shape: {psi.shape} (should be [{nCh}, {nCh}])")
        return psi

    def apply_psi(self, x: np.ndarray, psi: np.ndarray) -> np.ndarray:
        """
        This function applies the coil noise covariance matrix to the image
        \Psi^{-1/2}x
        Use fractional_matrix_power function in the scipy.linalg package for fractional matrix power.
        Use @ operator for matrix multiplication.

        @parak
        x:          matrix of shape [nPE,nRO,nCh]
        psi:        matrix of shape [nCh,nCh]

        @return:
        y:          PSI applied matrix of shape [nPE,nRO,nCh], dtype: complex
        """
        # Raise an error if the dimensions are not correct
        assert (
            x.shape[-1] == psi.shape[0]
        ), "The last dimension of x must be equal to the first dimension of psi"

        # task 1.2.2
        # Your code here ...
        psi_pow = fractional_matrix_power(psi, -0.5)

        y = x @ psi_pow.T

        return y

    def sense_locs(self, idx_PE: int, PE: int, R: int) -> np.ndarray:
        """
        Get the unwrapped indices for SENSE reconstruction.
        locs are equivalent to u_1, u_2,... in the lecture note.

        :param idx_PE:      index of PE
        :param PE:          number of PE
        :param R:           acceleration factor

        :return: locs:      indices for SENSE reconstruction [R], dtype: int
        """
        # task 2.2
        # Your code here ...
        aliased_FOV_size = int(np.ceil(PE / R))
        replica_idx = np.arange(R)
        offsets = replica_idx * aliased_FOV_size
        unwrapped_pos = idx_PE + offsets
        locs = unwrapped_pos % PE

        return locs

    def sense_aliased_idx(self, PE: int, R: int, locs: np.ndarray) -> int:
        """
        Get an index in locs that really locates in the aliased image
        i_n is an PE index of I_n in the lecture note.

        @param PE:          Length of phase encoding
        @param R:           Acceleration factor
        @param locs:        Indices for SENSE reconstruction at one point [R]

        @return: i_n:       An PE index for aliased images, I_n
        """
        # task 2.3
        # Your code here ...
        aliased_FOV_size = int(np.ceil(PE/R))
        block_start = PE // 2 - aliased_FOV_size // 2
        in_block = (locs >= block_start) & (locs < block_start + aliased_FOV_size)
        loc_in_block = locs[in_block][0]
        i_n = int(loc_in_block - block_start)

        return i_n

    def sense_sm_pinv(self, sens_maps: np.ndarray, locs: np.ndarray, idx_RO: int) -> np.ndarray:
        """
        Get the pseudo-inverse of coil sensitivity maps
        Use pinv function in the scipy.linalg package for puedo inverse of the matrix.

        :param sens_maps:       coil sensitivity maps [nPE,nRO,nCh]
        :param locs:            indices for SENSE reconstruction [R]
        :param idx_RO:          index of RO

        :return: C_pinv:        pseudo-inverse of coil sensitivity maps [R,nCh], dtype: complex
        """
        # task 2.4
        # Your code here ...
        sens_at_locs = sens_maps[locs, idx_RO, :].T

        C_pinv = pinv(sens_at_locs)

        return C_pinv

    def sense_unwrap(self, aliased_imgs: np.ndarray, sm_pinv: np.ndarray, idx_PE_alias: int, idx_RO: int) -> np.ndarray:
        """
        Unwrap the aliased coefficient to get the unaliased image
        Use @ operator for matrix multiplication.

        :param aliased_imgs:        aliased images [Ceil(nPE/R),nRO,nCh]
        :param sm_pinv:             pseudo-inverse of coil sensitivity maps [R,nCh]
        :param idx_PE_alias:        index of PE for aliased image
        :param idx_RO:              index of RO

        :return: unwrapped_coeff:   unwrapped coefficients [R], dtype: complex

        """
        # task 2.5
        # Your code here ...
        aliased_coil_vals = aliased_imgs[idx_PE_alias, idx_RO, :]

        unwrapped_coeff = sm_pinv @ aliased_coil_vals

        return unwrapped_coeff

    def sense_g_coef(self, sens_maps: np.ndarray, locs: np.ndarray, idx_RO: int) -> np.ndarray:
        """
        Get the g-factor. Use calc_g function in the utils package.

        :param sens_maps:       coil sensitivity maps [nPE,nRO,nCh]
        :param locs:            indices for SENSE reconstruction [R]
        :param idx_RO:          index of RO

        :return: g:             g-factor [R], dtype: float
        """
        # task 2.6
        # Your code here ...
        sens_at_locs = sens_maps[locs, idx_RO, :].T

        g = utils.calc_g(sens_at_locs)

        return g

    def sense_recon(
        self, aliased_imgs: np.ndarray, sens_maps: np.ndarray, PSI: np.ndarray, R: int, **kwargs
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        SENSE reconstruction.

        :param aliased_imgs:        multicoil aliased images [Ceil(nPE/R),nRO,nCh]
        :param sens_maps:           coil sensitivity maps [nPE,nRO,nCh]
        :param PSI:                 noise correlation matrix [nCh, nCh]
        :param R:                   acceleration factor

        :return:
            unaliased_img:          unaliased image [nPE,nRO], dtype: complex
            g_map:                  g-factor map [nPE,nRO], dtype: float
        """
        # PLEASE IGNORE HERE AND DO NOT MODIFY THIS PART.
        apply_psi = kwargs.get("apply_psi", self.apply_psi)
        sense_locs = kwargs.get("sense_locs", self.sense_locs)
        sense_sm_pinv = kwargs.get("sense_sm_pinv", self.sense_sm_pinv)
        sense_g_coef = kwargs.get("sense_g_coef", self.sense_g_coef)
        sense_aliased_idx = kwargs.get("sense_aliased_idx", self.sense_aliased_idx)
        sense_unwrap = kwargs.get("sense_unwrap", self.sense_unwrap)

        # task 2.1

        PE, RO, _ = sens_maps.shape
        sens_maps = apply_psi(sens_maps, PSI)
        aliased_imgs = apply_psi(aliased_imgs, PSI)

        nonzero_idx = np.array(np.nonzero(np.sum(sens_maps, 2)))
        unaliased_img = np.zeros((PE, RO), dtype=aliased_imgs.dtype)
        g_map = np.zeros((PE, RO))

        for idx_PE, idx_RO in zip(*nonzero_idx):
            if not unaliased_img[idx_PE, idx_RO]:
                # SENSE reconstruction
                # Your code here ...
                locs = sense_locs(idx_PE, PE, R)
                aliased_row = sense_aliased_idx(PE, R, locs)
                sm_pinv = sense_sm_pinv(sens_maps, locs, idx_RO)
                unaliased_img[locs, idx_RO] = sense_unwrap(aliased_imgs, sm_pinv, aliased_row, idx_RO)

                # g-factor
                # Your code here ...
                g_map[locs, idx_RO] = sense_g_coef(sens_maps, locs, idx_RO)

        return unaliased_img, g_map


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab05 import *

    save_plots = True
    # %% 1.1 Load data
    op = Lab05_op()
    kdata, sens_maps, noise_maps = op.load_data()

    # %% 1.2 Coil combination
    coil_imgs = utils.ifft2c(kdata, axes=(0, 1))
    complex_recon = utils.cmplx_sum(coil_imgs)

    # 1.2.1 Sum-of-square combination
    sos_recon = op.sos_comb(coil_imgs)

    # 1.2.2 least-squares combination without pre-whitening
    ls = op.ls_comb(coil_imgs, sens_maps)  # no noise

    # 1.2.2 least-squares combination with pre-whitening
    PSI = op.get_psi(noise_maps)
    ls_wPSI = op.ls_comb(coil_imgs, sens_maps, PSI)  # with noise

    # 1.3 plot: complex sum, sos, ls with and without pre-whitening
    utils.imshow(
        [complex_recon, sos_recon, ls, ls_wPSI],
        titles=["Complex Sum", "Sum of Square", "Least Squares (no PSI pre-whitening)", "Least Squares (PSI pre-whitening)"],
        filename="task_1_comparison.png" if save_plots else None,
    )

    # %% 2 SENSE reconstruction
    # simulate acceleration factors
    R = [2, 3, 4]
    senses, gs, title_R, title_g = [], [], [], []

    for r in R:
        # get aliased images
        aliased_img = utils.ifft2c(kdata[::r], axes=(0, 1)) * np.sqrt(r)

        # SENSE reconstruction
        unaliased, g_maps = op.sense_recon(aliased_img, sens_maps, PSI, r)
        senses.append(unaliased)
        gs.append(g_maps)

        # g-factor
        g_factor = np.mean(g_maps[np.nonzero(g_maps)])

        title_R.append(f"R={r}")
        title_g.append(f"g-factor={g_factor:.2f}")

    # display reconstructed image, reconstruction error w.r.t least-squares combination, g-factor map for each R
    utils.imshow(
        senses,
        gt=ls_wPSI,
        titles=title_R,
        filename="task_2_sense.png" if save_plots else None,
    )

    ls_wPSI_norm = utils.normalization(ls_wPSI)
    for i, r in enumerate(R):
        sense_norm = utils.normalization(senses[i])
        utils.imshow(
            [sense_norm, ls_wPSI_norm - sense_norm, gs[i]],
            titles=["SENSE", "Difference to LS", title_g[i]],
            suptitle=title_R[i],
            filename=f"task_2_R{r}.png" if save_plots else None,
        )





