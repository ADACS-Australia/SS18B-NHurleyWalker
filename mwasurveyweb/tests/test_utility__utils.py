"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.test import TestCase

from datetime import datetime, date

from ..utility.utils import (
    get_gps_time_from_date,
    get_date_from_gps_time,
)


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

    def test_date_from_gps_time(self):
        """
        Testing whether date are correctly calculated from gps time
        :return: None
        """

        # GPS time and expected date time
        input_outputs = [
            ['1230325688', datetime(2018, 12, 31, 21, 7, 50)],
            ['1086652816', datetime(2014, 6, 13)],
            ['1118188816', datetime(2015, 6, 13)],
            ['1149811217', datetime(2016, 6, 13)],
            ['1181347218', datetime(2017, 6, 13)],
            ['1212883218', datetime(2018, 6, 13)],
        ]

        for input_output in input_outputs:
            utc_date_time = get_date_from_gps_time(input_output[0])
            self.assertEquals(utc_date_time, input_output[1])
