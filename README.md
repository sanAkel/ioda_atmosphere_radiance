# ioda_atmosphere_radiance
scripts to create observations file as test input for satellite radiance observations 
in following (two) steps:
#
STEP 1:
-------
prepare nc4 diag files
(need GSI output: "bin diag files" and a bin to nc4 converter)

example usage:
----------------
convert_bin2nc.csh airs aqua
convert_bin2nc.csh avhrr metop-a
convert_bin2nc.csh amsua metop-a
convert_bin2nc.csh iasi metop-a
convert_bin2nc.csh avhrr n18

example output:
---------------
f517_fp.diag_avhrr_metop-a_ges.20180415_00z.nc4

STEP 2:
-------
read in GSI output and write to an IODA test file

2.1 
in test_write.csh setenv INDATAPATH to be where data path in step 1 is located
#

2.2
 - to write an AMSU-A on Metop-A test file (medium sized): 
  test_write.csh 2018 04 15 00 metop-a amsua 15 m 75 f517_fp.diag_amsua_metop-a_ges.20180415_00z.nc4
 - AVHRR on NOAA-18:
  test_write.csh 2018 04 15 00 n18 avhrr 3 m 75 f517_fp.diag_avhrr_n18_ges.20180415_00z.nc4
 - IASI on Metop-A:
  test_write.csh 2018 04 15 00 metop-a iasi 616 m 75 f517_fp.diag_iasi_metop-a_ges.20180415_00z.nc4
 - AIRS on AQUA:
  test_write.csh 2018 04 15 00 aqua airs 281 m 75 f517_fp.diag_airs_aqua_ges.20180415_00z.nc4
