"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.test import TestCase

from ..utility.utils import get_gps_time_from_date


class TestGPSTime(TestCase):
    """
    Class to test gps time
    """

    def test_gps_time(self):
        """
        Testing the gps time whether they are correctly calculated
        :return: None
        """

        # UTC date string and expected gps time
        input_outputs = [
            ['13/06/2018', '1212883218'],
            ['13/06/2017', '1181347218'],
            ['13/06/2016', '1149811217'],
            ['13/06/2015', '1118188816'],
            ['13/06/2014', '1086652816'],
            ['31/12/2018 21:07:50', '1230325688'],
            ['31/12/2018T21:07:50', '1230325688'],
            ['31-12-2018T21:07:50', None],
        ]

        for input_output in input_outputs:
            gps_time = get_gps_time_from_date(input_output[0])
            self.assertEquals(gps_time, input_output[1])
