class B25069:
    """
    INCLUSION OF UTILITIES IN RENT
    universe: Renter-occupied housing units
    """

    @property
    def _003E(self):
        """
        INCLUSION OF UTILITIES IN RENT
        universe: Estimate
                    Total:
                      No extra payment for any utilities
        """
        raise NotImplementedError()
    
    @property
    def _001E(self):
        """
        INCLUSION OF UTILITIES IN RENT
        universe: Estimate
                    Total:
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        INCLUSION OF UTILITIES IN RENT
        universe: Estimate
                    Total:
                      Pay extra for one or more utilities
        """
        raise NotImplementedError()
    
    