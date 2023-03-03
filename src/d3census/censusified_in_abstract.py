from abc import abstractproperty

class AbstractCensusifiedFunction:
    @abstractproperty
    def shopping_list(self) -> set[str]:
        """
        Returns each census variable required by the function as a 
        set of strings.
        """
