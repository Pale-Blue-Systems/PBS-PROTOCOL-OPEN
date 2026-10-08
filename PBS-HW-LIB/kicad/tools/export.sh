#!/bin/sh
# Regenerate the projects, run the KiCad checkers, and export drawings, renders and 3D models.
#   sh PBS-HW-LIB/kicad/tools/export.sh
set -e
cd "$(dirname "$0")/.."
python3 tools/generate.py
for p in pbs-scm-core pbs-scm-bay pbs-hwid-tag; do
  o="$p/output"; rm -rf "$o"; mkdir -p "$o"
  kicad-cli sch erc --severity-error --exit-code-violations -o "$o/$p-erc.rpt" "$p/$p.kicad_sch"
  kicad-cli pcb drc --severity-error --exit-code-violations -o "$o/$p-drc.rpt" "$p/$p.kicad_pcb"
  kicad-cli sch export pdf -o "$o/$p-schematic.pdf" "$p/$p.kicad_sch"
  kicad-cli pcb export pdf --layers "Edge.Cuts,F.Fab,Dwgs.User" --include-border-title -o "$o/$p-assembly-top.pdf" "$p/$p.kicad_pcb"
  kicad-cli pcb export pdf --layers "Edge.Cuts,B.Fab" --mirror --include-border-title -o "$o/$p-assembly-bottom.pdf" "$p/$p.kicad_pcb"
  kicad-cli pcb render --side top --quality high --width 1800 --height 1400 -o "$o/$p-3d-top.png" "$p/$p.kicad_pcb"
  kicad-cli pcb render --side bottom --quality high --width 1800 --height 1400 -o "$o/$p-3d-bottom.png" "$p/$p.kicad_pcb"
  kicad-cli pcb render --side top --rotate "-45,0,45" --quality high --width 1800 --height 1400 -o "$o/$p-3d-iso.png" "$p/$p.kicad_pcb"
  # labelled view: the same board with the 3D bodies hidden so the part-type labels show
  t="$(mktemp -d)"; cp -r "$p"/. "$t"/
  python3 -c "import pcbnew,sys; b=pcbnew.LoadBoard(sys.argv[1]); [f.Models().clear() for f in b.GetFootprints()]; pcbnew.SaveBoard(sys.argv[1], b)" "$t/$p.kicad_pcb"
  kicad-cli pcb render --side top --quality high --width 2400 --height 1900 -o "$o/$p-labelled-top.png" "$t/$p.kicad_pcb"
  rm -rf "$t"
  kicad-cli pcb export step --subst-models -f -o "$o/$p.step" "$p/$p.kicad_pcb" >/dev/null 2>&1 || kicad-cli pcb export step -f -o "$o/$p.step" "$p/$p.kicad_pcb"
  kicad-cli pcb export vrml --units mm -f -o "$o/$p.wrl" "$p/$p.kicad_pcb"
done
