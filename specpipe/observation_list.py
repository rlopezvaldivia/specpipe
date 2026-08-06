"""
Observation list utilities.

Defines which science frames
will be processed and which
comparison lamp corresponds
to each one.
"""

from pathlib import Path


class ObservationList:


    def __init__(

        self,

        filename

    ):

        self.filename = Path(

            filename

        )

        self.entries = []

        self.read()



    def read(

        self

    ):

        """
        Read observation_list.txt
        """

        if not self.filename.exists():

            raise FileNotFoundError(

                f"{self.filename} not found"

            )


        with open(

            self.filename,

            "r"

        ) as f:


            for line in f:


                line = line.strip()


                if len(line) == 0:

                    continue


                if line.startswith("#"):

                    continue


                columns = line.split()


                if len(columns) < 2:

                    raise ValueError(

                        f"Invalid line:\n{line}"

                    )


                self.entries.append(

                    {

                        "science": columns[0],

                        "arc": columns[1]

                    }

                )



    def observations(

        self

    ):

        """
        Return all entries.
        """

        return self.entries



    def science_files(

        self

    ):

        """
        Return science files.
        """

        return [

            entry["science"]

            for entry in self.entries

        ]



    def arc_file(

        self,

        science

    ):

        """
        Return comparison lamp
        associated with one object.
        """

        science = Path(

            science

        ).name


        for entry in self.entries:


            if entry["science"] == science:

                return entry["arc"]


        raise KeyError(

            f"No arc assigned for {science}"

        )
