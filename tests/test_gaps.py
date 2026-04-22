"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.
"""

__author__ = "Kelson da Costa Medeiros <kelsoncm@gmail.com>"

from datetime import datetime
from unittest import TestCase

from pyfwf.columns import CharColumn, DateColumn, DateTimeColumn, TimeColumn
from pyfwf.descriptors import DetailRowDescriptor, HeaderRowDescriptor


class TestDateTimeColumnNoneValue(TestCase):
    """Test DateTimeColumn with None values"""

    def test_datetime_to_value_with_none_padding(self):
        """Test DateTimeColumn returns None for zero-padded input"""
        col = DateTimeColumn("dt")
        # Zeros should be treated as None (padding)
        result = col.to_value("000000000000")
        self.assertIsNone(result)

    def test_datetime_to_value_with_valid_date(self):
        """Test DateTimeColumn converts valid datetime"""
        col = DateTimeColumn("dt")
        result = col.to_value("280220010000")
        self.assertEqual(datetime(2001, 2, 28, 0, 0), result)

    def test_datetime_to_str_with_none(self):
        """Test DateTimeColumn serializes None"""
        col = DateTimeColumn("dt")
        result = col.to_str(None)
        self.assertEqual("000000000000", result)


class TestDateColumnNoneValue(TestCase):
    """Test DateColumn with None values"""

    def test_date_to_value_with_none_padding(self):
        """Test DateColumn returns None for zero-padded input"""
        col = DateColumn("date")
        result = col.to_value("00000000")
        self.assertIsNone(result)

    def test_date_to_str_with_none(self):
        """Test DateColumn serializes None"""
        col = DateColumn("date")
        result = col.to_str(None)
        self.assertEqual("00000000", result)


class TestTimeColumnNoneValue(TestCase):
    """Test TimeColumn with None values"""

    def test_time_to_value_with_none_padding(self):
        """Test TimeColumn returns None for zero-padded input"""
        col = TimeColumn("time")
        result = col.to_value("0000")
        self.assertIsNone(result)

    def test_time_to_str_with_none(self):
        """Test TimeColumn serializes None"""
        col = TimeColumn("time")
        result = col.to_str(None)
        self.assertEqual("0000", result)


class TestRowDescriptorGetValues(TestCase):
    """Test RowDescriptor get_values method"""

    def test_row_descriptor_get_values(self):
        """Test that RowDescriptor extracts values correctly"""
        rd = DetailRowDescriptor(
            [
                CharColumn("col1", 5),
                CharColumn("col2", 5),
                CharColumn("col3", 5),
            ]
        )
        row = "AAAAABBBBBCCCCC"
        values = rd.get_values(row)
        self.assertEqual({"col1": "AAAAA", "col2": "BBBBB", "col3": "CCCCC"}, values)

    def test_header_descriptor_get_values(self):
        """Test that HeaderRowDescriptor extracts values"""
        hd = HeaderRowDescriptor(
            [
                CharColumn("hdr1", 5),
                CharColumn("hdr2", 5),
            ]
        )
        row = "HHHHHHHHHHHHHHH"
        values = hd.get_values(row)
        self.assertEqual({"hdr1": "HHHHH", "hdr2": "HHHHH"}, values)

    def test_row_descriptor_with_whitespace(self):
        """Test row descriptor handles whitespace correctly"""
        rd = DetailRowDescriptor(
            [
                CharColumn("name", 10),
                CharColumn("code", 5),
            ]
        )
        row = "John      ABC  "
        values = rd.get_values(row)
        self.assertEqual({"name": "John", "code": "ABC"}, values)
