#!/bin/csh
#
# a script to convert bin diag files to nc4 format using Will's converter
# 
########################################################################

#-------
# inputs
#-------
# path to GMAO FP (GEOS ADAS 5_17) output
set GMAO_FP=f517_fp

# date
set yyyy=2018
set mm=04
set dd=15
set hh=00

# diag ges (i.e., o-b, outer loop it=1)
set outerLoopIt=ges

set sensor    = $1
set satellite = $2

if ( $#argv < 2 ) then
  echo " "
  echo " Example of valid command line:"
  echo convert_bin2nc.csh airs aqua
  echo " "
  exit(0)
endif

# path to GMAO FP output
#-----------------------
setenv FP_PATH  /archive/u/dao_ops/GEOS-5.17/GEOSadas-5_17/${GMAO_FP}/obs/
setenv FPOUTPUT ${FP_PATH}'/Y'${yyyy}'/M'${mm}'/D'${dd}'/H'${hh}'/'
#echo ${FPOUTPUT}

# get Will's converter: to convert bin diag file to nc4
#------------------------------------------------------
if (! -e gsidiag_rad_bin2nc4.x) /bin/cp /discover/nobackup/wrmccart/progress_cvs/EnADAS-5_17_0p9/Linux/bin/gsidiag_rad_bin2nc4.x .

setenv obsfile ${GMAO_FP}.diag_${sensor}_${satellite}_${outerLoopIt}.${yyyy}${mm}${dd}_${hh}z.bin
echo "................................"
echo "Converting: " ${obsfile} "to nc4"
echo "................................"

# dmget above file from the archive
/usr/bin/dmget ${FPOUTPUT}/${obsfile}

# link above obsfile
/bin/ln -s ${FPOUTPUT}/${obsfile} .

# convert bin to nc4
gsidiag_rad_bin2nc4.x ${obsfile}

# get rid of the link
/bin/rm -f ${obsfile}

if (-e ${GMAO_FP}.diag_${sensor}_${satellite}_${outerLoopIt}.${yyyy}${mm}${dd}_${hh}z.nc4) then
  echo "All done"
endif
# -----------
