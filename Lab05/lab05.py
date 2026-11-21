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

        mc = None
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

        if PSI is not None:
            # After 1.b.ii.2 and 1.b.ii.3, you should apply the noise correlation matrix to the coil sensitivity maps and coil images.
            pass

        coil_comb_img = None
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

        psi = None
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

        y = None

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

        locs = None

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

        i_n = None

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

        C_pinv = None

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

        unwrapped_coeff = None

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

        g = None

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

                # g-factor
                # Your code here ...
                pass

        return unaliased_img, g_map


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab05 import *

    # %% 1.1 Load data
    op = Lab05_op()
    kdata, sens_maps, noise_maps = op.load_data()

    # %% 1.2 Coil combination
    # 1.2.1 Sum-of-square combination
    sos = None

    # 1.2.2 least-squares combination without pre-whitening
    ls = None

    # 1.2.2 least-squares combination with pre-whitening
    PSI = None
    ls_wPSI = None

    # 1.3 plot: complex sum, sos, ls with and without pre-whitening


    # %% 2 SENSE reconstruction
    # simulate acceleration factors
    R = [2, 3, 4]

    # get aliased images
    aliased_img = None

    # SENSE reconstruction
    unaliased, g_maps = None

    # g-factor
    g_factor = None

    # display reconstructed image, reconstruction error w.r.t least-squares combination, g-factor map for each R





