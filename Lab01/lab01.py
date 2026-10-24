"""
Computational Magnetic Resonance Imaging (CMRI) 2026/2027 Winter semester

- Author          : Jinho Kim, Haiting Huang
- Email           : <jinho.kim@fau.de>
- Contact         : <haiting.huang@fau.de>
"""

import numpy as np
import utils


class Lab01_op:

    def __init__(self):
        self.label = None
        self.T1_map = None
        self.T2_map = None
        self.PD_map = None
        # task 2.2
        # Define TR and TE as a pair in a list [TR, TE]
        self.PDw_TRTE = [6000, 10]  # long TR, short TE
        self.T1w_TRTE = [500, 15]  # short TR, short TE
        self.T2w_TRTE = [6000, 200]  # long TR, long TE (CSF has T2 of 329, so increase TE to show T2 decay of other tissue more cleanly)

    def load_data(self, path="../tests/digital_brain_phantom.mat"):
        """
        Args:
        path: Path to the input data file.
              Please keep the default path unchanged, and
              use "digital_brain_phantom.mat" as the input when calling the method

        label: Label map of the digital brain phantom
            - 1: Cerebrospinal fluid (CSF)
            - 2: Gray matter (GM)
            - 3: White matter (WM)
        T1_map: Predefined T1 Values
        T2_map: Predefined T2 Values
        PD_map: Proton Density Values
        """
        mat = utils.load_data(path)
        self.label = mat["ph"]["label"][0][0]  # (128, 128)
        self.T1_map = mat["ph"]["t1"][0][0]  # (128, 128)
        self.T2_map = mat["ph"]["t2"][0][0]  # (128, 128)
        self.PD_map = mat["ph"]["sd"][0][0]  # (128, 128)

    def get_csf_mask(self) -> np.ndarray:
        """
        Get CSF region from the label map
        Return:
            A mask of CSF, shape: (128, 128), dtype: bool
        """
        # task 1.2
        return np.where(self.label == 1, True, False)

    def get_gm_mask(self) -> np.ndarray:
        """
        Get GM region from the label map
        Return:
            A mask of GM, shape: (128, 128), dtype: bool
        """
        # task 1.2
        return np.where(self.label == 2, True, False)

    def get_wm_mask(self) -> np.ndarray:
        """
        Get WM region from the label map
        Return:
            A mask of WM, shape: (128, 128), dtype: bool
        """
        # task 1.2
        return np.where(self.label == 3, True, False)

    def get_T1(self, target) -> int | float:
        """
        Returns the T1 value of the target region

        Args:
            target: A mask of the target region (CSF, GM, WM), shape: (128, 128)
        Return:
            T1 value of the target region in [ms]
        """
        # task 1.3.3
        T1_ms = np.mean(self.T1_map[target.astype(bool)])
        return T1_ms

    def get_T2(self, target) -> int | float:
        """
        Returns the T2 value of the target region

        Args:
            target: A mask of the target region (CSF, GM, WM), shape: (128, 128)
        Return:
            T2 value of the target region in [ms]
        """
        # task 1.3.3
        T2_ms = np.mean(self.T2_map[target.astype(bool)])
        return T2_ms

    def get_PD(self, target) -> int | float:
        """
        Returns the PD value of the target region

        Args:
            target: A mask of the target region (CSF, GM, WM), shape: (128, 128)
        Return:
            PD value of the target region
        """
        # task 1.3.3
        PD = np.mean(self.PD_map[target.astype(bool)])
        return PD

    def spin_echo(self, TR, TE) -> np.ndarray:
        """
        Simulate a spin echo sequence

        Args:
            TR: Repetition time in [ms]
            TE: Echo time in [ms]
        Return:
            A 2D image of the spin echo sequence, shape: (128, 128), dtype: float
        """
        # task 2.1
        M0 = self.PD_map
        SE = M0 * (1 - 2 * np.exp(-(TR - TE / 2) / self.T1_map) + np.exp(- TR / self.T1_map)) * np.exp(- TE / self.T2_map)
        return SE


if __name__ == "__main__":
    # %% Load modules
    # This import is necessary to run the code cell-by-cell
    from lab01 import *

    # %% Define the object
    op = Lab01_op()

    # %% 1.1.	Load the file digital_brain_phantom.mat by calling load_data method.
    op.load_data(path="digital_brain_phantom.mat")

    # %% 1.2 Display the regions: Cerebrospinal Fluid (CSF), Gray Matter (GM), and White Matter (WM)
    csf_mask = op.get_csf_mask()
    gm_mask = op.get_gm_mask()
    wm_mask = op.get_wm_mask()
    # display each mask
    utils.imshow([op.label], titles=["Whole label map"])
    utils.imshow([csf_mask, gm_mask, wm_mask], titles=["CSF mask", "GM mask", "WM mask"])

    # %% 1.3 Explore T1, T2, PD values
    # 1.3.1 display T1_, T2_, and PD_map
    utils.imshow([op.T1_map, op.T2_map, op.PD_map], titles=["T1 map", "T2_map", "PD_map"])

    # 1.3.2 print unique values of T1_, T2_, PD_map
    print("T1 unique values: ", np.unique(op.T1_map))
    print("T2 unique values: ", np.unique(op.T2_map))
    print("PD unique values: ", np.unique(op.PD_map))

    # 1.3.3 print corresponding T1, T2, and PD values for CSF, GM, and WM
    # T1 map for CSF, GM, and WM, respectively
    T1_map_csf = op.get_T1(csf_mask)
    T1_map_gm = op.get_T1(gm_mask)
    T1_map_wm = op.get_T1(wm_mask)

    # T2 map for CSF, GM, and WM, respectively
    T2_map_csf = op.get_T2(csf_mask)
    T2_map_gm = op.get_T2(gm_mask)
    T2_map_wm = op.get_T2(wm_mask)

    # PD map for CSF, GM, and WM, respectively
    PD_map_csf = op.get_PD(csf_mask)
    PD_map_gm = op.get_PD(gm_mask)
    PD_map_wm = op.get_PD(wm_mask)

    print("Values for CSF: ", T1_map_csf, T2_map_csf, PD_map_csf, "\n", "Values for GM", T1_map_gm, T2_map_gm, PD_map_gm, "\n", "Values for WM",
          T1_map_wm, T2_map_wm, PD_map_wm)

    # %% 2.1 Simulated spin-echo signal equation
    se = op.spin_echo(6000, 10)  # TR, TE values from lecture for PD contrast

    # 2.2 define TR, TE values for proton density weighted "PDw_TRTE", 
    # T1-weighted "T1w_TRTE", and T2-weighted "T2w_TRTE" images in the constructor
    # done

    # 2.3 plot PDw, T1w, and T2w images
    utils.imshow([op.spin_echo(*op.T1w_TRTE), op.spin_echo(*op.T2w_TRTE), op.spin_echo(*op.PDw_TRTE)], titles=["T1w", "T2w", "PDw"])


