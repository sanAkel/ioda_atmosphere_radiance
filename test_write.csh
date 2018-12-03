#!/bin/csh

# test_write.csh - wrapper for the python writer
#
# !REVISION HISTORY:
#
#  Nov2017    Akella      first version
#                         TO DO: 
########################################################################

if ( !($?WRITE_VERBOSE) ) then
    setenv WRITE_VERBOSE 0
else
    if ( $WRITE_VERBOSE )  set echo
endif

setenv MYNAME       "test_write.csh"
setenv INDATAPATH   /discover/nobackup/sakella/JCSDA/myContrib/testinput/atmosphere/from_FP/nc4_ges_bin/

if ( $#argv < 10 ) then
   echo " "
   echo " \\begin{verbatim} "
   echo " "
   echo " NAME "
   echo " "
   echo "  $MYNAME  - To write test observations from satellites"
   echo " "
   echo " SYNOPSIS "
   echo " "
   echo "  $MYNAME  yyyy mm dd hh satellite sensor fileType "
   echo " "
   echo "  where"
   echo "   yyyy      -  year,  as YYYY   "
   echo "   mm        -  month, as MM     "
   echo "   dd        -  date,  as DD     "
   echo "   hh        -  hour,  as HH     "
   echo "   satellite -  satellite name   "
   echo "   sensor    -  sensor    name   "
   echo "   nchans    -  number of channels   "
   echo "   fileType  -  output file type: small(s) or medium(m)   "
   echo "   nlocs     -  number of locations (1:s) or medium(75:m)   "
   echo "   infile    -  a GSI output file (nc4 format produced using ncdiag)"
   echo " "
   echo " DESCRIPTION "
   echo " "
   echo "   To write out test input for satellite radiance observations"
   echo " "
   echo "   Example of valid command line:"
   echo "     $MYNAME 2018 04 15 00 metop-a amsua 15 m 75 f517_fp.diag_amsua_metop-a_ges.20180415_00z.nc4"
   echo " "
   echo " REQUIRED ENVIRONMENT VARIABLES:"
   echo "    INDATAPATH  - path to data file which will be read in"
   echo " "
   echo "    none"
   echo " "
   echo " AUTHOR"
   echo "   Santha Akella (Santha.Akella@nasa.gov), NASA/GMAO "
   echo "     Last modified: 26Nov2018      by: S. Akella"
   echo " "
   echo " \\end{verbatim} "
   echo " \\clearpage "
   exit(0)
endif

setenv FAILED 0
if ( !($?INDATAPATH) ) setenv FAILED 1

if ( $FAILED ) then
  env
  echo " ${MYNAME}: not all required vars defined"
  exit 1
endif

set yyyy      = $1
set mm        = $2
set dd        = $3
set hh        = $4
set satellite = $5
set sensor    = $6
set nchans    = $7
set fileType  = $8
set nlocs     = $9
set infile    = $10

setenv yyyymmddhh   ${yyyy}${mm}${dd}${hh}

set out_file = ${sensor}'_obs_'${satellite}'_'${yyyymmddhh}'_'${fileType}'.nc4'

# clean up if a file already exists
if (-e ${out_file}) then
  echo 'Output file: '${out_file} 'already exists, deleting it'
  /bin/rm -f ${sensor}'_obs_'${satellite}'_'${yyyy}${mm}${dd}${hh}'_'${fileType}'.nc4'
endif

# write out the test obs file
test_wr.py -year ${yyyy} -month ${mm} -day ${dd} -hour ${hh} -satellite ${satellite} -sensor ${sensor} -nchans ${nchans} -fileType ${fileType} -nlocs ${nlocs} -inFile ${INDATAPATH}/${infile}

if (-e ${out_file}) then
  echo " ${MYNAME}: Complete "
  exit(0)
else
  echo " ${MYNAME}: Failed, something went wrong. Check above! " "to write: "${out_file}
  exit 1
endif

# other valid examples:
#
# AVHRR
# test_write.csh 2018 04 15 00 n18 avhrr 3 m 75 f517_fp.diag_avhrr_n18_ges.20180415_00z.nc4
# test_write.csh 2018 04 15 00 n18 avhrr 3 s 1  f517_fp.diag_avhrr_n18_ges.20180415_00z.nc4
#
# IASI
# test_write.csh 2018 04 15 00 metop-a iasi 616 m 75 f517_fp.diag_iasi_metop-a_ges.20180415_00z.nc4
#
# AIRS
# test_write.csh 2018 04 15 00 aqua airs 281 m 75 f517_fp.diag_airs_aqua_ges.20180415_00z.nc4
#
