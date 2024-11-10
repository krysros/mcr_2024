# README

## Installation

```console
conda env create -f environment.yml
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