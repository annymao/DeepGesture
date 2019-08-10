#include "Utility.h"

ostream& operator<<(ostream& os, const TouchAccommodationsPara& para){
	return os << para.holdDuration << " " << para.ignoreRepeat << " " << para.tapAssistance << " " << para.holdDurationTimer << " " << para.ignoreRepeatTimer << " " << para.tapAssistanceTimer;
}