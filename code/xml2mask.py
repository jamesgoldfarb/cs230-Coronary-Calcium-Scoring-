#!/usr/bin/env python3

"""
This script converts DICOM files to NIfTI format using pydicom and nibabel libraries.
It takes two command-line arguments: the directory containing the DICOM files and the directory to save the converted NIfTI files.
"""

import os
import pydicom
import nibabel as nib
import numpy as np
import argparse

def dicom_to_nifti(dicom_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for patient_id in os.listdir(dicom_dir):
        patient_dir = os.path.join(dicom_dir, patient_id)
        if os.path.isdir(patient_dir):
            dicom_files = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir) if f.endswith('.dcm')]
            dicom_files.sort()
            slices = [pydicom.dcmread(dcm) for dcm in dicom_files]
            pixel_arrays = [s.pixel_array for s in slices]
            volume = np.stack(pixel_arrays, axis=-1)
            affine = np.eye(4)
            nifti_img = nib.Nifti1Image(volume, affine)
            output_path = os.path.join(output_dir, f'{patient_id}.nii.gz')
            nib.save(nifti_img, output_path)

def main():
    parser = argparse.ArgumentParser(description='Convert DICOM files to NIfTI format.')
    parser.add_argument('dicom_dir', type=str, help='Directory containing patient DICOM files.')
    parser.add_argument('output_dir', type=str, help='Directory to save the converted NIfTI files.')
    args = parser.parse_args()

    dicom_to_nifti(args.dicom_dir, args.output_dir)

if __name__ == '__main__':
    main()
