class B25003:
    """
    TENURE
    universe: Occupied housing units
    """

    @property
    def _003E(self):
        """
        TENURE
        universe: Estimate
                    Total:
                      Renter occupied
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        TENURE
        universe: Estimate
                    Total:
                      Owner occupied
        """
        raise NotImplementedError()
    
    @property
    def _001E(self):
        """
        TENURE
        universe: Estimate
                    Total:
        """
        raise NotImplementedError()
    
    