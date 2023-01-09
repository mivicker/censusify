class B25003I:
    """
    TENURE (HISPANIC OR LATINO HOUSEHOLDER)
    universe: Occupied housing units with a householder who is Hispanic or Latino
    """

    @property
    def _003E(self):
        """
        TENURE (HISPANIC OR LATINO HOUSEHOLDER)
        universe: Estimate
                    Total:
                      Renter occupied
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        TENURE (HISPANIC OR LATINO HOUSEHOLDER)
        universe: Estimate
                    Total:
                      Owner occupied
        """
        raise NotImplementedError()
    
    @property
    def _001E(self):
        """
        TENURE (HISPANIC OR LATINO HOUSEHOLDER)
        universe: Estimate
                    Total:
        """
        raise NotImplementedError()
    
    