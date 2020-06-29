import traitlets

class Racecar(traitlets.HasTraits):
    steering = traitlets.Float()
    throttle = traitlets.Float()
    direction = traitlets.Int()
    
    @traitlets.default('direction')
    def _default_direction(self):
        return 1
    
    @traitlets.validate('steering')
    def _clip_steering(self, proposal):
        if proposal['value'] > 1.0:
            return 1.0
        elif proposal['value'] < -1.0:
            return -1.0
        else:
            return proposal['value']
        
    @traitlets.validate('throttle')
    def _clip_throttle(self, proposal):
        if proposal['value'] > 1.0:
            return 1.0
        elif proposal['value'] < -1.0:
            return -1.0
        else:
            return proposal['value']
    
    @traitlets.validate('direction')
    def _clip_direction(self, proposal):
        if proposal['value'] >= 0:
            return 1
        else:
            return -1
