class B17101:
    """
    POVERTY STATUS IN THE PAST 12 MONTHS OF PEOPLE IN HOUSING UNITS
    universe: Population in occupied housing units for whom poverty status is determined
    """

    @property
    def _003E(self):
        """
        POVERTY STATUS IN THE PAST 12 MONTHS OF PEOPLE IN HOUSING UNITS
        universe: Estimate
                    Total:
                      Income in the past 12 months at or above poverty level
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        POVERTY STATUS IN THE PAST 12 MONTHS OF PEOPLE IN HOUSING UNITS
        universe: Estimate
                    Total:
                      Income in the past 12 months below poverty level
        """
        raise NotImplementedError()
    
    @property
    def _001E(self):
        """
        POVERTY STATUS IN THE PAST 12 MONTHS OF PEOPLE IN HOUSING UNITS
        universe: Estimate
                    Total:
        """
        raise NotImplementedError()
    
    