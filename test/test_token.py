import unittest
from components import *
from parser import build_list

class TestToken(unittest.TestCase):
    def test_tagify(self):
        self.assertEqual(Token.tagify('p', 'hello'), '<p>hello</p>')

    def test_tagify_attrs(self):
        attrs = {'class': 'myClass'}
        output = '<p class="myClass">hello</p>'
        self.assertEqual(Token.tagify_attrs('p', attrs, 'hello'), output)

class TestHeading(unittest.TestCase):
    def test_render(self):
        token = Heading('### heading 3\n')
        self.assertEqual(token.render(), '<h3>heading 3</h3>')

class TestQuote(unittest.TestCase):
    def test_render(self):
        lines = ['> line 1\n', '> line 2\n']
        token = Quote(lines)
        output = '<blockquote><p>line 1 line 2</p></blockquote>'
        self.assertEqual(token.render(), output)

    def test_inner_render(self):
        lines = ['> ## heading 2\n',
                 '> *hello* world\n',
                 '> \n',
                 '> **new** paragraph\n',
                 '> with [link](hello)\n']
        token = Quote(lines)
        output = """<blockquote>
                        <h2>heading 2</h2>
                        <p>
                            <em>hello</em> world
                        </p>
                        <p>
                            <b>new</b> paragraph with <a href="hello">
                            link</a>
                        </p>
                    </blockquote>"""
        output = ''.join([ line.strip() for line in output.split('\n') ])
        self.assertEqual(token.render(), output)

class TestBlockCode(unittest.TestCase):
    def test_render(self):
        lines = ['```sh\n', 'rm dir\n', 'mkdir test\n', '```\n']
        token = BlockCode(lines)
        output = '<pre><code class="sh">rm dir\nmkdir test\n</code></pre>'
        self.assertEqual(token.render(), output)

    def test_escape(self):
        lines = ['```html\n',
                 '<html>\n',
                 '<b>some text</b>\n',
                 '</html>\n',
                 '```\n']
        token = BlockCode(lines)
        output = '<pre><code class="html">&lt;html&gt;\n&lt;b&gt;some text&lt;/b&gt;\n&lt;/html&gt;\n</code></pre>'
        self.assertEqual(token.render(), output)

class TestBold(unittest.TestCase):
    def test_render(self):
        self.assertEqual(Bold('**a str**').render(), '<b>a str</b>')

    def test_escape(self):
        self.assertEqual(Bold('**an &**').render(), '<b>an &amp;</b>')

class TestItalic(unittest.TestCase):
    def test_render(self):
        self.assertEqual(Italic('*a str*').render(), '<em>a str</em>')

    def test_escape(self):
        self.assertEqual(Italic('*an &*').render(), '<em>an &amp;</em>')

class TestInlineCode(unittest.TestCase):
    def test_render(self):
        token = InlineCode('`rm dir`')
        self.assertEqual(token.render(), '<code>rm dir</code>')

    def test_escape(self):
        token = InlineCode('`<html></html>`')
        output = '<code>&lt;html&gt;&lt;/html&gt;</code>'
        self.assertEqual(token.render(), output)

class TestLink(unittest.TestCase):
    def test_render(self):
        token = Link('[link name](link target)')
        output = '<a href="link target">link name</a>'
        self.assertEqual(token.render(), output)

class TestParagraph(unittest.TestCase):
    def test_render(self):
        lines = ['some\n', 'continuous\n', 'lines\n']
        token = Paragraph(lines)
        output = '<p>some continuous lines</p>'
        self.assertEqual(token.render(), output)

    def test_inner_render(self):
        lines = ['some\n',
                 '**important**\n',
                 '[info](link),\n',
                 'with `code`, *etc*.\n']
        token = Paragraph(lines)
        output = """<p>
                       some <b>important</b> <a href="link">info</a>
                       , with <code>code</code>
                       , <em>etc</em>.
                    </p>"""
        output = ''.join([ line.strip() for line in output.split('\n') ])
        self.assertEqual(token.render(), output)

class TestListItem(unittest.TestCase):
    def test_render(self):
        token = ListItem('- some text\n')
        self.assertEqual(token.render(), '<li>some text</li>')

class TestList(unittest.TestCase):
    def test_render(self):
        lines = ['- item 1\n',
                 '- item 2\n',
                 '    - nested item 1\n',
                 '    - nested item 2\n',
                 '        - **further** nested item\n',
                 '    - nested item 3\n',
                 '- item 3\n']
        token = build_list(lines)
        output = """<ul>
                        <li>item 1</li>
                        <li>item 2</li>
                        <ul>
                            <li>nested item 1</li>
                            <li>nested item 2</li>
                            <ul>
                                <li><b>further</b> nested item</li>
                            </ul>
                            <li>nested item 3</li>
                        </ul>
                        <li>item 3</li>
                    </ul>"""
        output = ''.join([ line.strip() for line in output.split('\n') ])
        self.assertEqual(token.render(), output)

class TestSeparator(unittest.TestCase):
    def test_render(self):
        self.assertEqual(Separator.render(), '<hr>')

class TestRawText(unittest.TestCase):
    def test_render(self):
        self.assertEqual(RawText('some text').render(), 'some text')

    def test_escape(self):
        self.assertEqual(RawText('an &').render(), 'an &amp;')
