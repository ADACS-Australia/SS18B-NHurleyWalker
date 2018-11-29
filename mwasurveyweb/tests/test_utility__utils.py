"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.test import TestCase

from datetime import datetime, date

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
            [datetime.strptime('13/06/2018', '%d/%m/%Y'), '1212883218'],
            [datetime.strptime('13/06/2017', '%d/%m/%Y'), '1181347218'],
            [datetime.strptime('13/06/2016', '%d/%m/%Y'), '1149811217'],
            [datetime.strptime('13/06/2015', '%d/%m/%Y'), '1118188816'],
            [datetime.strptime('13/06/2014', '%d/%m/%Y'), '1086652816'],
            [datetime.strptime('31/12/2018 21:07:50', '%d/%m/%Y %H:%M:%S'), '1230325688'],
            [date(day=13, month=6, year=2018), '1212883218'],
        ]

        for input_output in input_outputs:
            gps_time = get_gps_time_from_date(input_output[0])
            self.assertEquals(gps_time, input_output[1])
