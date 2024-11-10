# README

## Installation

### Conda defaults

```console
conda env create -f environment.yml
conda activate mcr
```

### Intel® Distribution for Python

```console
conda create -n idp -c https://software.repos.intel.com/python/conda -c conda-forge --override-channels python=3.12 numpy
conda activate idp
pip install autograd ezdxf matplotlib shapely
```

## Why do we use conda instead of pip?

The NumPy wheels on PyPI, which is what pip installs, are built with OpenBLAS. In the conda defaults channel, NumPy is built against Intel MKL. MKL is typically a little faster and more robust than OpenBLAS.

See: https://numpy.org/install/#numpy-packages--accelerated-linear-algebra-libraries

## Conditional Numerical Reproducibility (CNR)

See: https://www.intel.com/content/www/us/en/developer/articles/technical/introduction-to-the-conditional-numerical-reproducibility-cnr.html

```console
python -c "import numpy; numpy.show_config()"
```

cmd:

```cmd
set MKL_CBWR=AVX
```

PowerShell:

```powershell
$env:MKL_CBWR="AVX"
```

## Help

```console
python main.py --help
```

## Example

```powershell
python .\main.py --filename .\tri_441.dxf --alpha 26.56505117707799 --plot 3D
```