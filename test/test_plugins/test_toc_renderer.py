import unittest
import test.helpers as helpers
from mistletoe.block_token import Document, Heading, List
from plugins.toc_renderer import TOCRenderer

class TestTOCRenderer(unittest.TestCase):
    def test_store_rendered_heading(self):
        renderer = TOCRenderer()
        rendered_heading = '<h3>some <em>text</em></h3>\n'
        renderer.store_rendered_heading(rendered_heading)
        self.assertEqual(renderer._headings[0], (3, 'some text'))

    def test_render_heading(self):
        renderer = TOCRenderer()
        token = Heading(['### some *text*\n'])
        rendered_heading = renderer.render_heading(token, {})
        self.assertEqual(renderer._headings[0], (3, 'some text'))

    def test_omit_title(self):
        renderer = TOCRenderer(omit_title=True)
        token = Document(['# title\n', '\n', '## heading\n'])
        renderer.render(token)
        self.assertEqual(renderer._headings, [(2, 'heading')])

    def test_filter_conditions(self):
        import re
        filter_conds = [lambda x: re.match(r'<h2>', x),
                        lambda x: re.match(r'<h3>', x)]
        renderer = TOCRenderer(filter_conds=filter_conds)
        token = Document(['# title\n',
                          '\n',
                          '## heading\n',
                          '\n',
                          '#### heading \n'])
        renderer.render(token)
        self.assertEqual(renderer._headings, [(4, 'heading')])

    def test_get_toc(self):
        headings = [(1, 'heading 1'),
                    (2, 'subheading 1'),
                    (2, 'subheading 2'),
                    (3, 'subsubheading 1'),
                    (2, 'subheading 3'),
                    (1, 'heading 2')]
        renderer = TOCRenderer(omit_title=False)
        renderer._headings = headings
        toc = List(['- heading 1\n',
                    '    - subheading 1\n',
                    '    - subheading 2\n',
                    '        - subsubheading 1\n',
                    '    - subheading 3\n',
                    '- heading 2\n'])
        helpers.check_equal(self, renderer.toc, toc)
