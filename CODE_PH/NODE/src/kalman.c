#include "kalman.h"

extern float _err_measure, _err_estimate, _q;
extern double _current_estimate, _last_estimate, _kalman_gain;


void SimpleKalmanFilter(float mea_e, float est_e, float q)
{
	_err_measure = mea_e;
	_err_estimate = est_e;
	_q = q;	
}
float updateEstimate(float mea)
{
	_kalman_gain = _err_estimate/(_err_estimate + _err_measure);
  _current_estimate = _last_estimate + _kalman_gain * (mea - _last_estimate);
  _err_estimate =  (1.0 - _kalman_gain)*_err_estimate + fabs((float)_last_estimate - _current_estimate)*_q;
  _last_estimate=_current_estimate;

  return _current_estimate;	
}

void setMeasurementError(float mea_e)
{
	  _err_measure = mea_e;
}

void setEstimateError(float est_e)
{
	 _err_estimate = est_e;
}

void setProcessNoise(float q)
{ 
	 _q = q;
}

float getKalmanGain(void)
{
	return _kalman_gain;
}

float getEstimateError(void)
{
	 return _err_estimate;
}