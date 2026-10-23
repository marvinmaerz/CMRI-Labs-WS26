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
        # Define TR and TE as a pair in a list [TR, TE]
        # task 2.2
        self.PDw_TRTE = None  
        self.T1w_TRTE = None  
        self.T2w_TRTE = None  

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
        # Your code here ...

        return None

    def get_gm_mask(self) -> np.ndarray:
        """
        Get GM region from the label map
        Return:
            A mask of GM, shape: (128, 128), dtype: bool
        """
        # task 1.2
        # Your code here ...

        return None

    def get_wm_mask(self) -> np.ndarray:
        """
        Get WM region from the label map
        Return:
            A mask of WM, shape: (128, 128), dtype: bool
        """
        # task 1.2
        # Your code here ...

        return None

    def get_T1(self, target) -> int | float:
        """
        Returns the T1 value of the target region

        Args:
            target: A mask of the target region (CSF, GM, WM), shape: (128, 128)
        Return:
            T1 value of the target region in [ms]
        """
        # task 1.3.3
        # Your code here ...

        T1_ms = None
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
        # Your code here ...

        T2_ms = None
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
        # Your code here ...

        PD = None
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
        # Your code here ...

        SE = None
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
    csf_mask = None
    gm_mask = None
    wm_mask = None
    # display each mask


    # %% 1.3 Explore T1, T2, PD values
    # 1.3.1 display T1_, T2_, and PD_map


    # 1.3.2 print unique values of T1_, T2_, PD_map




    # 1.3.3 print corresponding T1, T2, and PD values for CSF, GM, and WM
    # T1 map for CSF, GM, and WM, respectively
    T1_map_csf = None
    T1_map_gm = None
    T1_map_wm = None

    # T2 map for CSF, GM, and WM, respectively
    T2_map_csf = None
    T2_map_gm = None
    T2_map_wm = None

    # PD map for CSF, GM, and WM, respectively
    PD_map_csf = None
    PD_map_gm = None
    PD_map_wm = None

    # %% 2.1 Simulated spin-echo signall equation

    # 2.2 define TR, TE values for proton density weighted "PDw_TRTE", 
    # T1-weighted "T1w_TRTE", and T2-weighted "T2w_TRTE" images in the constructor

    # 2.3 plot PDw, T1w, and T2w images


