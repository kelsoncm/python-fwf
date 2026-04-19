"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.
"""

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'

import io
from unittest import TestCase
from pyfwf.columns import CharColumn, PositiveIntegerColumn, DateColumn
from pyfwf.descriptors import (
    HeaderRowDescriptor, FooterRowDescriptor,
    DetailRowDescriptor, FileDescriptor
)
from pyfwf.renders import render_as_markdown


class TestRenderMarkdown(TestCase):
    """Test markdown rendering"""

    def test_render_detail_only(self):
        """Test rendering with detail rows only"""
        fd = FileDescriptor([
            DetailRowDescriptor([
                CharColumn('name', 10),
                CharColumn('status', 5),
            ])
        ])
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        self.assertIn('DETAILS', result)
        self.assertIn('name', result)
        self.assertIn('status', result)
        self.assertIn('CharColumn', result)

    def test_render_with_header(self):
        """Test rendering with header"""
        fd = FileDescriptor(
            [DetailRowDescriptor([CharColumn('col1', 5)])],
            HeaderRowDescriptor([CharColumn('hdr', 5)])
        )
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        self.assertIn('HEADER', result)
        self.assertIn('DETAILS', result)

    def test_render_with_footer(self):
        """Test rendering with footer"""
        fd = FileDescriptor(
            [DetailRowDescriptor([CharColumn('col1', 5)])],
            footer=FooterRowDescriptor([CharColumn('ftr', 5)])
        )
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        self.assertIn('FOOTER', result)
        self.assertIn('ftr', result)

    def test_render_with_all_rows(self):
        """Test rendering with header, footer and details"""
        fd = FileDescriptor(
            [DetailRowDescriptor([
                CharColumn('col1', 10),
                CharColumn('col2', 10),
            ])],
            HeaderRowDescriptor([
                CharColumn('hdr1', 10),
                CharColumn('hdr2', 10),
            ]),
            FooterRowDescriptor([
                CharColumn('ftr1', 10),
                CharColumn('ftr2', 10),
            ])
        )
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        self.assertIn('HEADER', result)
        self.assertIn('DETAILS', result)
        self.assertIn('FOOTER', result)
        self.assertIn('hdr1', result)
        self.assertIn('col1', result)
        self.assertIn('ftr1', result)

    def test_render_multiple_detail_descriptors(self):
        """Test rendering multiple detail descriptors"""
        fd = FileDescriptor([
            DetailRowDescriptor([CharColumn('det1', 5)]),
            DetailRowDescriptor([CharColumn('det2', 5)]),
        ])
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        self.assertIn('DETAILS 1', result)
        self.assertIn('DETAILS 2', result)

    def test_render_different_column_types(self):
        """Test rendering different column types"""
        fd = FileDescriptor([
            DetailRowDescriptor([
                CharColumn('name', 15),
                PositiveIntegerColumn('age', 3),
                DateColumn('birthday'),
            ])
        ])
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        self.assertIn('CharColumn', result)
        self.assertIn('PositiveIntegerColumn', result)
        self.assertIn('DateColumn', result)
        self.assertIn('name', result)
        self.assertIn('age', result)
        self.assertIn('birthday', result)

    def test_render_table_structure(self):
        """Test that rendered table has proper structure"""
        fd = FileDescriptor([
            DetailRowDescriptor([
                CharColumn('col1', 5),
                CharColumn('col2', 5),
            ])
        ])
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        # Check for markdown table structure
        self.assertIn('|', result)
        self.assertIn('#', result)
        self.assertIn('Column', result)
        self.assertIn('Size', result)
        self.assertIn('Start', result)
        self.assertIn('End', result)
        self.assertIn('Type', result)
        self.assertIn('Description', result)

    def test_render_column_positioning(self):
        """Test that column positions are rendered correctly"""
        fd = FileDescriptor([
            DetailRowDescriptor([
                CharColumn('first', 5),
                CharColumn('second', 10),
                CharColumn('third', 3),
            ])
        ])
        out = io.StringIO()
        render_as_markdown(fd, out)
        result = out.getvalue()
        # First column should start at 1
        self.assertIn('|    1 |', result)
        # Verify sizes are shown
        self.assertIn('5', result)
        self.assertIn('10', result)


