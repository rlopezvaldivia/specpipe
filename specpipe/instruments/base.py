"""
Base instrument configuration.
"""


class Instrument:

    name = "unknown"

    parameters = {}


    def get(self, key, default=None):
        return self.parameters.get(
            key,
            default
        )
