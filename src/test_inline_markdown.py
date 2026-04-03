import unittest
from inline_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestInlineMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

            md2 = """
This is **bolded** paragraph, but with added extra lines





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
    """
            blocks = markdown_to_blocks(md2)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph, but with added extra lines",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
    def test_block_to_block_type(self):
            md = """
This is some paragraph with dummy invalid partial markdown blocktype stuff
 ### no headings to see here
 -not an inordered list
 -seriously it isn't
 1.nor is it an ordered list
 >not a quote either
 ```codeblocks? ``` WHAT IS THAT
"""
            self.assertEqual(block_to_block_type(md), BlockType.paragraph)

            md2 = "###### This is a heading. Nothing else to say."
            self.assertEqual(block_to_block_type(md2), BlockType.heading)

            md3 = "```\nthis is some code for sure don't worry about the lack of syntax\n```"
            self.assertEqual(block_to_block_type(md3), BlockType.code)

            md4 = """
>this is a
> quote so
>return BlockType.quote please
> and thank you
"""
            self.assertEqual(block_to_block_type(md4), BlockType.quote)

            md5 = """
- unordered list
- must have a - followed by
- a blank space and this
- qualifies
"""
            self.assertEqual(block_to_block_type(md5), BlockType.unordered_list)
        
            md6 = """
1. an ordered list
2. must have digits that increment
3. by one and are followed by
4. a . for each line
5. and this one qualifies
"""
            self.assertEqual(block_to_block_type(md6), BlockType.ordered_list)

            md7 = """
- now we need to make sure
- it doesn't accept invalid
-unordered lists like this one
- because it doens't have a space
- on the third line
"""
            self.assertEqual(block_to_block_type(md7), BlockType.paragraph)
        
            md8 = """
1. and now we do the same
2. for an ordered list
3.the cursed third line
4. is incorrect so this one
5. doesn't qualify
"""
            self.assertEqual(block_to_block_type(md8), BlockType.paragraph)

    def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

Followed by some normal text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><p>Followed by some normal text</p></div>",
        )
    
    def test_ordered_list(self):
        md = """
1. Item 1
2. **Item 2**
3. _Item 3_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li><b>Item 2</b></li><li><i>Item 3</i></li></ol></div>",
        )
    
    def test_unordered_list(self):
        md = """
- Item 1
- **Item 2**
- _Item 3_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li><b>Item 2</b></li><li><i>Item 3</i></li></ul></div>",
        )
    
    def test_quotes(self):
        md = """
> Line One
> _Line Two_
> **Line Three**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Line One\n<i>Line Two</i>\n<b>Line Three</b></blockquote></div>",
        )