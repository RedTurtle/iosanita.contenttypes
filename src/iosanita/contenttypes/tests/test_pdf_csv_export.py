from ..browser.export_view import image_to_html
from ..testing import INTEGRATION_TESTING
from io import BytesIO
from PIL import Image
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing.z2 import Browser
from transaction import commit
from zope.component import getMultiAdapter

import base64
import csv
import unittest
import uuid


class TestExport(unittest.TestCase):
    """Test PDF export functionality"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        login(self.portal, TEST_USER_NAME)

        self.doc = api.content.create(
            container=self.portal,
            type="Document",
            id="test-document",
            title="Test Document",
            description="This is a test document",
        )
        api.content.transition(self.doc, to_state="published")
        commit()

        self.browser = Browser(self.app)

    def tearDown(self):
        api.content.delete(self.doc)
        commit()
        logout()

    def test_pdf_export_view_exists(self):
        """Test that the PDF export view is registered and accessible

        TODO: view must be accessible only for IExportViewDownload context
        """
        view = getMultiAdapter((self.doc, self.request), name="export_pdf")
        self.assertTrue(view is not None)

    def test_searchblock_pdf(self):
        block_id = uuid.uuid4().hex
        self.doc.blocks = {
            block_id: {
                "@type": "search",
                "query": {
                    "query": [
                        {
                            "i": "portal_type",
                            "o": "plone.app.querystring.operation.selection.is",
                            "v": "Document",
                        }
                    ]
                },
            }
        }
        self.doc.blocks_layout = {"items": [block_id]}
        commit()

        self.browser.open(
            f"{self.doc.absolute_url()}/searchblock/@@download/{block_id}.pdf"
        )

        # Check response headers
        self.assertEqual(self.browser.headers["Content-Type"], "application/pdf")
        self.assertIn(
            "attachment;filename=", self.browser.headers["Content-Disposition"]
        )
        # Check that the response is not empty and looks like a PDF
        self.assertTrue(b"%PDF-" in self.browser.contents[:10])

        # TODO
        # api.portal.get_tool("portal_transforms").convertTo("plain/text", self.browser.contents, mimetype="application/pdf")
        # oppure con pypdf

    def test_searchblock_csv(self):
        block_id = uuid.uuid4().hex
        self.doc.blocks = {
            block_id: {
                "@type": "search",
                "query": {
                    "query": [
                        {
                            "i": "portal_type",
                            "o": "plone.app.querystring.operation.selection.is",
                            "v": "Document",
                        }
                    ]
                },
            }
        }
        self.doc.blocks_layout = {"items": [block_id]}
        commit()

        self.browser.open(
            f"{self.doc.absolute_url()}/searchblock/@@download/{block_id}.csv"
        )

        # Check response headers
        self.assertEqual(
            self.browser.headers["Content-Type"], "text/csv; charset=utf-8-sig"
        )
        self.assertIn(
            "attachment;filename=", self.browser.headers["Content-Disposition"]
        )

        # Check that the response is a CSV with expected data
        reader = csv.DictReader(self.browser.contents)
        self.assertEqual(reader.fieldnames, ["Titolo"])
        self.assertEqual([row for row in reader], [{"Titolo": "Test Document"}])


def _make_logo_str(img_bytes):
    """Build the input string expected by image_to_html from raw image bytes."""
    b64 = base64.b64encode(img_bytes).decode()
    return f"logo.test;base64:{b64}"


def _make_png_bytes():
    buf = BytesIO()
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    img.save(buf, format="PNG")
    return buf.getvalue()


def _make_jpeg_bytes():
    buf = BytesIO()
    img = Image.new("RGB", (10, 10), color=(0, 255, 0))
    img.save(buf, format="JPEG")
    return buf.getvalue()


class TestImageToHtml(unittest.TestCase):
    """Unit tests for image_to_html — no Plone layer needed."""

    def test_returns_empty_string_for_empty_input(self):
        self.assertEqual(image_to_html(""), "")

    def test_returns_none_for_svg(self):
        # SVG images are not supported by weasyprint; the function returns None
        svg_bytes = b"<?xml version='1.0'?><svg xmlns='http://www.w3.org/2000/svg'/>"
        result = image_to_html(_make_logo_str(svg_bytes))
        self.assertIsNone(result)

    def test_returns_empty_string_for_unknown_format(self):
        garbage = b"\x00\x01\x02\x03" * 20
        result = image_to_html(_make_logo_str(garbage))
        self.assertEqual(result, "")

    def test_png_produces_valid_img_tag(self):
        result = image_to_html(_make_logo_str(_make_png_bytes()))
        self.assertIsNotNone(result)
        self.assertIn('class="logo"', result)
        self.assertIn("data:image/png;base64,", result)

    def test_jpeg_produces_valid_img_tag(self):
        result = image_to_html(_make_logo_str(_make_jpeg_bytes()))
        self.assertIsNotNone(result)
        self.assertIn('class="logo"', result)
        self.assertIn("data:image/jpeg;base64,", result)
