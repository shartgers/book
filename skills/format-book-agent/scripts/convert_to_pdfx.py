#!/usr/bin/env python3
"""
Convert interior PDF to PDF/X-3:2002 (B&W grayscale) for IngramSpark.

Uses Ghostscript to add Output Intent and ensure grayscale color space.
Requires Ghostscript (gswin64c on Windows, gs on macOS/Linux).

Usage:
  python convert_to_pdfx.py [input.pdf] [output.pdf]
  python convert_to_pdfx.py                    # uses output/book-interior.pdf -> output/isb_txt.pdf

The script will:
  1. Find Ghostscript (gswin64c or gs)
  2. Ensure a grayscale ICC profile exists (downloads if needed)
  3. Run Ghostscript with -dPDFX for PDF/X-3:2002 output
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

# Script is at skills/format-book-agent/scripts/convert_to_pdfx.py
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
INPUT_ICC_DIR = REPO_ROOT / "input" / "icc"
PDFX_DEF = INPUT_ICC_DIR / "PDFX_def_gray.ps"

# Adobe ICC profiles (Gray Gamma 2.2 for grayscale)
ADOBE_ICC_ZIP = "https://download.adobe.com/pub/adobe/iccprofiles/win/AdobeICCProfilesWin_end-user.zip"
GRAY_PROFILE_NAME = "Gray Gamma 2.2.icc"


def find_ghostscript() -> str | None:
    """Find Ghostscript executable. Returns path or None."""
    # Windows: gswin64c or gswin32c
    # macOS/Linux: gs
    if platform.system() == "Windows":
        names = ["gswin64c", "gswin32c", "gswin64", "gswin32"]
    else:
        names = ["gs"]

    for name in names:
        path = shutil.which(name)
        if path:
            return path

    # Check common Windows install locations (Chocolatey: C:\Program Files\gs\gs10.x.x\bin\)
    if platform.system() == "Windows":
        for base in [
            Path(os.environ.get("ProgramFiles", "C:\\Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")),
        ]:
            # Chocolatey installs as gs\gs10.06.0\bin\gswin64c.exe
            for gs_dir in base.glob("gs*"):
                if not gs_dir.is_dir():
                    continue
                # Try gs_dir/bin (flat) or gs_dir/gs*/bin (versioned)
                for candidate in [
                    gs_dir / "bin" / "gswin64c.exe",
                    gs_dir / "bin" / "gswin32c.exe",
                ]:
                    if candidate.exists():
                        return str(candidate)
                for ver_dir in gs_dir.glob("gs*"):
                    if ver_dir.is_dir():
                        exe = ver_dir / "bin" / "gswin64c.exe"
                        if exe.exists():
                            return str(exe)
                        exe = ver_dir / "bin" / "gswin32c.exe"
                        if exe.exists():
                            return str(exe)

    return None


def _find_system_gray_profile() -> Path | None:
    """Look for grayscale ICC profile in system color directories."""
    if platform.system() == "Windows":
        color_dirs = [
            Path(os.environ.get("SystemRoot", "C:\\Windows")) / "System32" / "spool" / "drivers" / "color",
        ]
    else:
        color_dirs = [
            Path("/usr/share/color/icc"),
            Path("/Library/ColorSync/Profiles"),
        ]

    for d in color_dirs:
        if not d.exists():
            continue
        for f in d.iterdir():
            if f.suffix.lower() in (".icc", ".icm") and "gray" in f.name.lower():
                return f
    return None


def ensure_icc_profile() -> Path | None:
    """
    Ensure grayscale ICC profile exists. Check input/ and input/icc/ first,
    then try download from Adobe, then system profiles.
    Returns path to ICC file or None if failed.
    """
    # Check project input folders first (user-provided profiles)
    input_dir = REPO_ROOT / "input"
    for name in ["Generic Gray Gamma 2.2 Profile.icc", GRAY_PROFILE_NAME, "GrayGamma2.2.icc"]:
        candidate = input_dir / name
        if candidate.exists():
            return candidate
    INPUT_ICC_DIR.mkdir(parents=True, exist_ok=True)
    icc_path = INPUT_ICC_DIR / GRAY_PROFILE_NAME
    if icc_path.exists():
        return icc_path
    # Also check input/icc/ for any gray-named profile
    if INPUT_ICC_DIR.exists():
        for f in INPUT_ICC_DIR.iterdir():
            if f.suffix.lower() in (".icc", ".icm") and "gray" in f.name.lower():
                return f

    # Try to download from Adobe
    print("Downloading grayscale ICC profile from Adobe...")
    zip_path = INPUT_ICC_DIR / "AdobeICCProfiles.zip"

    try:
        urllib.request.urlretrieve(ADOBE_ICC_ZIP, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                if "gray" in name.lower() and name.endswith((".icc", ".icm")):
                    zf.extract(name, INPUT_ICC_DIR)
                    extracted = INPUT_ICC_DIR / Path(name).name
                    if extracted != icc_path and extracted.exists():
                        extracted.rename(icc_path)
                    break
        zip_path.unlink(missing_ok=True)
        if icc_path.exists():
            return icc_path
    except Exception as e:
        print(f"Download failed: {e}")
        zip_path.unlink(missing_ok=True)

    # Fallback: use system profile
    system_profile = _find_system_gray_profile()
    if system_profile:
        print(f"Using system profile: {system_profile}")
        return system_profile

    return None


def convert_to_pdfx(
    input_pdf: Path,
    output_pdf: Path,
    gs_path: str,
    icc_path: Path | None,
) -> bool:
    """
    Run Ghostscript to convert PDF to PDF/X-3:2002 grayscale.
    """
    if not PDFX_DEF.exists():
        print(f"Error: PDFX definition file not found: {PDFX_DEF}")
        return False

    # Ghostscript command for PDF/X-3:2002 grayscale
    # -dPDFX: enable PDF/X mode
    # -sProcessColorModel=DeviceGray: output grayscale
    # -sColorConversionStrategy=Gray: convert all to gray
    # Downsample all raster images to 300 dpi so IngramSpark validation passes
    # (profile allows max 600 ppi; source may be 720 ppi from WeasyPrint/raster)
    cmd = [
        gs_path,
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOOUTERSAVE",
        "-dPDFX",
        "-sProcessColorModel=DeviceGray",
        "-sColorConversionStrategy=Gray",
        "-sDEVICE=pdfwrite",
        "-dEmbedAllFonts=true",
        "-dPDFACompatibilityPolicy=1",
        "-dDownsampleColorImages=true",
        "-dColorImageResolution=300",
        "-dDownsampleGrayImages=true",
        "-dGrayImageResolution=300",
        "-dDownsampleMonoImages=true",
        "-dMonoImageResolution=300",
        f"-sOutputFile={output_pdf}",
    ]

    # Add ICC profile definition so PDFX_def can use it
    # -I adds directory to search path so -dSAFER allows reading the ICC file
    if icc_path and icc_path.exists():
        icc_dir = str(icc_path.parent.resolve()).replace("\\", "/")
        cmd.extend(["-I", icc_dir])
        icc_path_str = str(icc_path.resolve()).replace("\\", "/")
        cmd.extend(["-c", f"/ICCProfile ({icc_path_str}) def"])

    cmd.extend(["-f", str(PDFX_DEF), str(input_pdf)])

    print(f"Running: {' '.join(cmd[:12])}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Ghostscript stderr:", result.stderr)
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert interior PDF to PDF/X-3:2002 (B&W) for IngramSpark"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(REPO_ROOT / "output" / "book-interior.pdf"),
        help="Input PDF path (default: output/book-interior.pdf)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Output PDF path (default: output/isb_txt.pdf)",
    )
    args = parser.parse_args()

    input_pdf = Path(args.input)
    if args.output:
        output_pdf = Path(args.output)
    else:
        # Default interior PDF/X output name for IngramSpark
        output_pdf = REPO_ROOT / "output" / "isb_txt.pdf"

    if not input_pdf.exists():
        print(f"Error: Input PDF not found: {input_pdf}")
        sys.exit(1)

    gs_path = find_ghostscript()
    if not gs_path:
        print(
            "Error: Ghostscript not found. Install it from https://ghostscript.com/releases/gsdnld.html\n"
            "  Windows: Download and run the installer, or: choco install ghostscript\n"
            "  macOS: brew install ghostscript\n"
            "  Linux: apt install ghostscript  (or equivalent)"
        )
        sys.exit(1)

    print(f"Using Ghostscript: {gs_path}")

    icc_path = ensure_icc_profile()
    if icc_path:
        print(f"Using ICC profile: {icc_path}")
    else:
        print(
            "Warning: No grayscale ICC profile. PDF/X output may not validate.\n"
            f"Download Gray Gamma 2.2.icc and place it in {INPUT_ICC_DIR}"
        )

    if convert_to_pdfx(input_pdf, output_pdf, gs_path, icc_path):
        print(f"Created: {output_pdf}")
    else:
        print("Conversion failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
