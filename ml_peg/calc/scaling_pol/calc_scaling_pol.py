"""Run calculations for scaling_pol tests."""

from __future__ import annotations

from copy import copy
from pathlib import Path
from typing import Any

from ase import units
from ase.io import read, write
import numpy as np
import pytest
import json

from ml_peg.calcs.utils.utils import download_s3_data
from ml_peg.models.get_models import load_models
from ml_peg.models.models import current_models

MODELS = load_models(current_models)

DATA_PATH = Path(__file__).parent / "data"
OUT_PATH = Path(__file__).parent / "outputs"


@pytest.mark.parametrize("mlip", MODELS.items())
def test_lattice_energy(mlip: tuple[str, Any]) -> None:
	"""
    Run scaling polarizability of linear organic molecules test.

    Parameters
    ----------
    mlip
        Name of model use and model to get calculator.
    """
	model_name, model = mlip
    clean_calc = model.get_calculator()

    # Download 'linear organic mols' dataset
    scaling_polarizability_dir = (
        download_s3_data(
            key="inputs/electric_field/scaling_polarizability/linear_organic_mols.zip", # I guess we need to upload such a file somewhere
            filename="scaling_polarizability.zip",
        )
        / "scaling_polarizability"
    )

	mols = read(scaling_polarizability_dir / "ORCA_DATA.xyz",':')	# This filename needs to be adjusted to whatever's in the zipfile above
	mol_out = []

	for mol in mols:
	    calc = copy.deepcopy(clean_calc)
	    mol.calc = calc

	    energy = mol.get_potential_energy()
	    forces = mol.get_forces()
	    dipole = np.linalg.norm(calc.results['dipole'])
	    
	    mol_out.append(mol)

    # Write output structures
    write_dir = OUT_PATH / model_name
    write_dir.mkdir(parents=True, exist_ok=True)
    write(write_dir / "ORCA_DATA.xyz", mol_out)	# This filename needs to be adjusted to whatever's in the zipfile above

