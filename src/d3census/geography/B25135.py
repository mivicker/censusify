class B25135:
    """
    ANNUAL OTHER FUEL COSTS
    universe: Occupied housing units
    """

    @property
    def _005E(self):
        """
        ANNUAL OTHER FUEL COSTS
        universe: Estimate
                    Total
                      Charged for other fuels
                        $250 to $749
        """
        raise NotImplementedError()
    
    @property
    def _004E(self):
        """
        ANNUAL OTHER FUEL COSTS
        universe: Estimate
                    Total
                      Charged for other fuels
                        Less than $250
        """
        raise NotImplementedError()
    
    @property
    def _006E(self):
        """
        ANNUAL OTHER FUEL COSTS
        universe: Estimate
                    Total
                      Charged for other fuels
                        $750 or more
        """
        raise NotImplementedError()
    
    @property
    def _001E(self):
        """
        ANNUAL OTHER FUEL COSTS
        universe: Estimate
                    Total
        """
        raise NotImplementedError()
    
    @property
    def _003E(self):
        """
        ANNUAL OTHER FUEL COSTS
        universe: Estimate
                    Total
                      Charged for other fuels
        """
        raise NotImplementedError()
    
    @property
    def _002E(self):
        """
        ANNUAL OTHER FUEL COSTS
        universe: Estimate
                    Total
                      Not charged, not used, or payment included in other fees
        """
        raise NotImplementedError()
    
    