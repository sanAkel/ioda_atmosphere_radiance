#!/usr/bin/env python

'''
to write test (satellite) input data 

todo:
	1. fix global attributes, hard coded, but okay for now, since they are satellite/sensor indepedent
	   (but depend on the analysis):
	   - outer_Loop_Iteration
	   - number_of_Predictors
	   - ireal_radiag, ipchan_radiag, ... should be read in
	   - some variables (ijacob, jac_nnz, jac_nind) have been introduced, where is their description? 
	     for now populated their values from current test amsua_n19 file

	2. same as above #1 for: Observation_Class_maxstrlen, BC_angord_arr_dim, num_profile_levels

	3. crude sampling (nSkip hard coded)

Santha Akella, NASA, GSFC
Nov 2018
'''

#-----------------------------------------------------------------

import  argparse

import  time                 as      time_mod
import	netCDF4              as      nc4
import  numpy                as      np
import  matplotlib.pyplot    as      plt

from    datetime             import  datetime
#-----------------------------------------------------------------

def write_nc_obs( inFile, fName_out, date, sensor, satellite, \
                  nchans, nlocs, fileType, Observation_Class_maxstrlen, BC_angord_arr_dim, num_profile_levels):

	if (fileType == 'm'):
		nlocs = 75
	else:
		nlocs = 1
	#-----------------------------------------------------------------

	nobs = nchans * nlocs
	num_profile_levelsPone = num_profile_levels + 1

	file_ = nc4.Dataset(fName_out, 'w')#format='NETCDF4_CLASSIC')

	# create dimensions
	file_.createDimension('nchans',                       nchans)
	file_.createDimension('nobs',                         nobs)

	file_.createDimension('Observation_Class_maxstrlen',  Observation_Class_maxstrlen)
	file_.createDimension('BC_angord_arr_dim',            BC_angord_arr_dim)
	file_.createDimension('num_profile_levels',           num_profile_levels)
	file_.createDimension('num_profile_levels+1',         num_profile_levelsPone)

	file_.createDimension('nlocs',                        nlocs)
	file_.createDimension('nrecs',                        nlocs)
	file_.createDimension('nvars',                        nchans)
	#-----------------------------------------------------------------

	# create variables
	record_number   = file_.createVariable('record_number',  np.int32,   ('nlocs',))

	chaninfoidx     = file_.createVariable('chaninfoidx',    np.int32,   ('nchans',))
	frequency       = file_.createVariable('frequency',      np.float64, ('nchans',))
	polarization    = file_.createVariable('polarization',   np.int32,   ('nchans',))
	wavenumber      = file_.createVariable('wavenumber',     np.float64, ('nchans',))
	error_variance  = file_.createVariable('error_variance', np.float64, ('nchans',))
	mean_lapse_rate = file_.createVariable('mean_lapse_rate',np.float64, ('nchans',))
	use_flag        = file_.createVariable('use_flag',       np.int32,   ('nchans',))
	sensor_chan     = file_.createVariable('sensor_chan',    np.int32,   ('nchans',))
	satinfo_chan    = file_.createVariable('satinfo_chan',   np.int32,   ('nchans',))

	latitude   = file_.createVariable('latitude',            np.float32, ('nlocs',))
	longitude  = file_.createVariable('longitude',           np.float32, ('nlocs',))
	height     = file_.createVariable('height',              np.float32, ('nlocs',))
	time       = file_.createVariable('time',                np.float32, ('nlocs',))

	Scan_Position       = file_.createVariable('Scan_Position',           np.float32, ('nlocs',))
	Sat_Zenith_Angle    = file_.createVariable('Sat_Zenith_Angle',        np.float32, ('nlocs',))
	Sat_Azimuth_Angle   = file_.createVariable('Sat_Azimuth_Angle',       np.float32, ('nlocs',))
	Sol_Zenith_Angle    = file_.createVariable('Sol_Zenith_Angle',        np.float32, ('nlocs',))
	Sol_Azimuth_Angle   = file_.createVariable('Sol_Azimuth_Angle',       np.float32, ('nlocs',))
	Scan_Angle          = file_.createVariable('Scan_Angle',              np.float32, ('nlocs',))

	# loop over number of channels
	for iChan in range(1, nchans+1):
		tb_ob_str  = 'brightness_temperature'     + '_%i_'%(iChan)	
		obs_	  = file_.createVariable('%s'%(tb_ob_str), np.float32, ('nlocs',))	
	for iChan in range(1, nchans+1):
		tb_err_str = 'brightness_temperature_err' + '_%i_'%(iChan)	
		err_	  = file_.createVariable('%s'%(tb_err_str),np.float32, ('nlocs',))	
	for iChan in range(1, nchans+1):
		tb_qc_str  = 'brightness_temperature_qc'  + '_%i_'%(iChan)	
		qc_	  = file_.createVariable('%s'%(tb_qc_str), np.float32, ('nlocs',))	
	#-----------------------------------------------------------------

	# variable attributes
#	file_.variables['latitudes'].standard_name  = 'latitude'
  	file_.variables['latitude'].units   = 'degrees_north'
#	file_.variables['longitudes'].standard_name = 'longitude'
  	file_.variables['longitude'].units  = 'degrees_east'
  	file_.variables['height'].units     = 'm'
  	file_.variables['time'].units       = 'hours from start of analysis time window'
  	file_.variables['brightness_temperature_1_'].units = 'K'
#       and for all other variables... FILL them up later...
	#-----------------------------------------------------------------

	# global attributes
	file_.Satellite_Sensor      = '%s_%s'%(sensor, satellite)
	file_.Satellite             = '%s'%(satellite)
	file_.Observation_type      = '%s'%(sensor)
	file_.Outer_Loop_Iteration  = np.int32( 1,     dtype=np.int32) # should be read in
	file_.Number_of_channels    = np.int32('%d'%(nchans), dtype=np.int32)
	file_.Number_of_Predictors  = np.int32( 1,     dtype=np.int32) # It is set to 12 in the amsua_n19 test input. Shouldn't be 7?
	file_.date_time             = np.int32('%d'%(int(date.strftime('%Y%m%d%H'))), dtype=np.int32)
	file_.ireal_radiag          = np.int32( 30,    dtype=np.int32) # following are hard coded, should be read in.
	file_.ipchan_radiag         = np.int32( 8,     dtype=np.int32) 
	file_.iextra                = np.int32( 0,     dtype=np.int32)
	file_.jextra                = np.int32( 0,     dtype=np.int32)
	file_.idiag                 = np.int32( 23,    dtype=np.int32) # why not 17?
	file_.angord                = np.int32( 4,     dtype=np.int32) # why not 0?		
	file_.iversion_radiag       = np.int32( 40000, dtype=np.int32) # why not 30303?		
	file_.New_pc4pred	    = np.int32( 1,     dtype=np.int32) # why not 0?		
	file_.ioff0                 = np.int32( 23,    dtype=np.int32)# should be 17 as idiag		
	file_.ijacob                = np.int32( 0,     dtype=np.int32)# is this to write/read Jacobian? What is it?		
	file_.jac_nnz		    = np.int32( 323,   dtype=np.int32) # what's this??
	file_.jac_nind              = np.int32( 8,     dtype=np.int32) #and this as well??		

        file_.title       = 'satellite radiance observations test input file'
        file_.institution = 'NASA, GMAO'
	file_.source      = 'From NASA GMAO Forward Processing System: F517_FP and ncdiag (gsidiag_rad_bin2nc4.x) from W McCarty (GMAO)'
        file_.description = 'Test observations input file'
        file_.history     = 'Created ' + time_mod.ctime(time_mod.time())
	file_.references  = 'https://github.com/JCSDA/ioda/tree/develop/test/testinput/atmosphere'
	#-----------------------------------------------------------------

	# read GSI output
	[chaninfoidx_, frequency_, polarization_, wavenumber_, error_variance_, mean_lapse_rate_, use_flag_, sensor_chan_, satinfo_chan_, \
         latitude_, longitude_, height_, time_, Scan_Position_, Sat_Zenith_Angle_, Sat_Azimuth_Angle_, Sol_Zenith_Angle_, Sol_Azimuth_Angle_, Scan_Angle_, \
         brightness_temperature_, brightness_temperature_err_, brightness_temperature_qc_] = \
	read_ncdiag(inFile, nchans)
	#-----------------------------------------------------------------

	print 'Writing...\n[%s]\n'%(fName_out)
	# write data to above variables 
	record_number[:]   = np.arange( 1, nlocs+1)

	chaninfoidx     [:] = chaninfoidx_  [0:nchans]
	frequency       [:] = frequency_    [0:nchans]
	polarization    [:] = polarization_
	wavenumber      [:] = wavenumber_
	error_variance  [:] = error_variance_
	mean_lapse_rate [:] = mean_lapse_rate_
	use_flag        [:] = use_flag_
	sensor_chan     [:] = sensor_chan_
	satinfo_chan    [:] = satinfo_chan_

	latitude[:]	= latitude_ [0:nlocs]
	longitude[:]	= longitude_[0:nlocs]
	height[:]	= height_   [0:nlocs]
	time[:]		= time_     [0:nlocs]

	Scan_Position[:]      = Scan_Position_     [0:nlocs]
	Sat_Zenith_Angle[:]   = Sat_Zenith_Angle_  [0:nlocs]
	Sat_Azimuth_Angle[:]  = Sat_Azimuth_Angle_ [0:nlocs]
	Sol_Zenith_Angle[:]   = Sol_Zenith_Angle_  [0:nlocs]
	Sol_Azimuth_Angle[:]  = Sol_Azimuth_Angle_ [0:nlocs]
	Scan_Angle[:]         = Scan_Angle_        [0:nlocs]

	# TB obs
	for iChan in range(1, nchans+1):
		tb_ob_str = 'brightness_temperature'     + '_%i_'%(iChan)	
		file_.variables['%s'%(tb_ob_str)][:] = brightness_temperature_[iChan-1, 0:nlocs]

	# TB obs error
	for iChan in range(1, nchans+1):
		tb_err_str = 'brightness_temperature_err' + '_%i_'%(iChan)	
		file_.variables['%s'%(tb_err_str)][:] = 1./(brightness_temperature_err_[iChan-1, 0:nlocs])

	# TB obs qc flag
	for iChan in range(1, nchans+1):
		tb_qc_str  = 'brightness_temperature_qc'  + '_%i_'%(iChan)	
		file_.variables['%s'%(tb_qc_str)][:] = brightness_temperature_qc_[iChan-1, 0:nlocs]
	
	file_.close()
#-----------------------------------------------------------------
def read_ncdiag( infile, nchan):

	nSkip	= 75
	#-----------------------------------------------------------------

	print 'Reading...\n[%s]\n'%(infile)
	file_ = nc4.Dataset(infile, 'r')
	
	# nchans
	chaninfoidx	= file_.variables['chaninfoidx']    [:]
	frequency   	= file_.variables['frequency']      [:]
	polarization	= file_.variables['polarization']   [:]
	wavenumber	= file_.variables['wavenumber']     [:]
	error_variance 	= file_.variables['error_variance'] [:]
	mean_lapse_rate	= file_.variables['mean_lapse_rate'][:]
	use_flag	= file_.variables['use_flag']       [:]
	sensor_chan	= file_.variables['sensor_chan']    [:]
	satinfo_chan	= file_.variables['satinfo_chan']   [:]

	# read in (they are "super" sized)
	latitude0	= file_.variables['Latitude'] [:]
	longitude0	= file_.variables['Longitude'][:]
	height0		= file_.variables['Elevation'][:]
	time0		= file_.variables['Obs_Time'] [:]

	Scan_Position0     = file_.variables['Scan_Position']    [:]
	Sat_Zenith_Angle0  = file_.variables['Sat_Zenith_Angle'] [:]
	Sat_Azimuth_Angle0 = file_.variables['Sat_Azimuth_Angle'][:]
	Sol_Zenith_Angle0  = file_.variables['Sol_Zenith_Angle'] [:]
	Sol_Azimuth_Angle0 = file_.variables['Sol_Azimuth_Angle'][:]
	Scan_Angle0        = file_.variables['BC_Scan_Angle']    [:]

	brightness_temperature0		= file_.variables['Observation']              [:]
	brightness_temperature_err0	= file_.variables['Inverse_Observation_Error'][:]
	brightness_temperature_qc0	= file_.variables['QC_Flag']                  [:]
	file_.close()
	#-----------------------------------------------------------------

	# reshape above have to [nchans x len(latitude)/nchans]
	nobs = len(latitude0)/nchan
	latitude  = np.reshape( latitude0,  (nchan, nobs), order='F')[0,0:nobs:nSkip]
	longitude = np.reshape( longitude0, (nchan, nobs), order='F')[0,0:nobs:nSkip]
	height    = np.reshape( height0,    (nchan, nobs), order='F')[0,0:nobs:nSkip]
	time      = np.reshape( time0,      (nchan, nobs), order='F')[0,0:nobs:nSkip]

	Scan_Position     = np.reshape( Scan_Position0,     (nchan, nobs), order='F')[0,0:nobs:nSkip]
	Sat_Zenith_Angle  = np.reshape( Sat_Zenith_Angle0,  (nchan, nobs), order='F')[0,0:nobs:nSkip]
	Sat_Azimuth_Angle = np.reshape( Sat_Azimuth_Angle0, (nchan, nobs), order='F')[0,0:nobs:nSkip]
	Sol_Zenith_Angle  = np.reshape( Sol_Zenith_Angle0,  (nchan, nobs), order='F')[0,0:nobs:nSkip]
	Sol_Azimuth_Angle = np.reshape( Sol_Azimuth_Angle0, (nchan, nobs), order='F')[0,0:nobs:nSkip]
	Scan_Angle        = np.reshape( Scan_Angle0,        (nchan, nobs), order='F')[0,0:nobs:nSkip]

	brightness_temperature1		= np.reshape( brightness_temperature0,      (nchan, nobs), order='F')
	brightness_temperature_err1	= np.reshape( brightness_temperature_err0,  (nchan, nobs), order='F')
	brightness_temperature_qc1	= np.reshape( brightness_temperature_qc0,   (nchan, nobs), order='F')

	brightness_temperature		= np.squeeze( brightness_temperature1    [:, 0:nobs:nSkip])
	brightness_temperature_err	= np.squeeze( brightness_temperature_err1[:, 0:nobs:nSkip])
	brightness_temperature_qc	= np.squeeze( brightness_temperature_qc1 [:, 0:nobs:nSkip])
	#-----------------------------------------------------------------

	return chaninfoidx, frequency, polarization, wavenumber, error_variance, mean_lapse_rate, use_flag, sensor_chan, satinfo_chan, \
               latitude, longitude, height, time, Scan_Position, Sat_Zenith_Angle, Sat_Azimuth_Angle, Sol_Zenith_Angle, Sol_Azimuth_Angle, Scan_Angle, \
               brightness_temperature, brightness_temperature_err, brightness_temperature_qc
#-----------------------------------------------------------------

def main():

        comm_args       = parse_args()
	year_           = comm_args['year']
	month_          = comm_args['month']
	day_            = comm_args['day']
	hour_           = comm_args['hour']

	satellite_      = comm_args['satellite']
	sensor_         = comm_args['sensor']
	nchans_         = comm_args['nchans'] 	# in principle, this is redudant! since every sensor has a set num of chans

	fileType_       = comm_args['fileType']
	nlocs_          = comm_args['nlocs']

	infile_         = comm_args['inFile']
	#-----------------------------------------------------------------

	# form file name
	date_ = datetime( year_, month_, day_, hour_, 0, 0)	
	fName_out = sensor_ + '_obs_' + satellite_ + '_%s_'%(date_.strftime('%Y%m%d%H')) + '%s'%(fileType_) + '.nc4'
	#-----------------------------------------------------------------

        Observation_Class_maxstrlen, BC_angord_arr_dim, num_profile_levels = [7, 4, 71]
	write_nc_obs( infile_, fName_out, date_, sensor_, satellite_, nchans_, nlocs_, fileType_, Observation_Class_maxstrlen, BC_angord_arr_dim, num_profile_levels)
	#-----------------------------------------------------------------

#-----------------------------------------------------------------

def parse_args():
        p = argparse.ArgumentParser(description = \
            'Script to write out test input file for satellite radiance observations')

	p.add_argument('-year',     type=int, help= 'year',  		default=2018)
	p.add_argument('-month',    type=int, help= 'month',            default=4)
	p.add_argument('-day',      type=int, help= 'day',              default=15)
	p.add_argument('-hour',     type=int, help= 'hour (UTC)',	default=0)

	p.add_argument('-satellite',type=str, help= 'n19',              default='m1')
	p.add_argument('-sensor',   type=str, help= 'amsua',            default='avhrr')
	p.add_argument('-nchans',   type=int, help= '15',               default=3)

	p.add_argument('-fileType', type=str, help= 's or m',           default='s')
	p.add_argument('-nlocs',    type=int, help= '1(s) or 75(m)',    default=1)

 	p.add_argument('-inFile',   type=str, help= 'GSI output nc4 file', required=True)

        return vars(p.parse_args())
#-----------------------------------------------------------------

if __name__ == '__main__':

        main()
#-----------------------------------------------------------------
