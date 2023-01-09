class B25002:
    """
    OCCUPANCY STATUS
    universe: Housing units
    """

    @property
    def _001E(self):
        """
        OCCUPANCY STATUS
        universe: Estimate
                    Total:
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        OCCUPANCY STATUS
        universe: Estimate
                    Total:
                      Occupied
        """
        raise NotImplementedError()
    
    @property
    def _003E(self):
        """
        OCCUPANCY STATUS
        universe: Estimate
                    Total:
                      Vacant
        """
        raise NotImplementedError()
    
    