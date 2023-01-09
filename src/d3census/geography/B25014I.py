class B25014I:
    """
    OCCUPANTS PER ROOM (HISPANIC OR LATINO HOUSEHOLDER)
    universe: Occupied housing units with a householder who is Hispanic or Latino
    """

    @property
    def _003E(self):
        """
        OCCUPANTS PER ROOM (HISPANIC OR LATINO HOUSEHOLDER)
        universe: Estimate
                    Total:
                      1.01 or more occupants per room
        """
        raise NotImplementedError()
    
    @property
    def _001E(self):
        """
        OCCUPANTS PER ROOM (HISPANIC OR LATINO HOUSEHOLDER)
        universe: Estimate
                    Total:
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        OCCUPANTS PER ROOM (HISPANIC OR LATINO HOUSEHOLDER)
        universe: Estimate
                    Total:
                      1.00 or less occupants per room
        """
        raise NotImplementedError()
    
    