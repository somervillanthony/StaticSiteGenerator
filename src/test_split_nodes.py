import unittest

from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.text), TextNode("code block", TextType.code), TextNode(" word", TextType.text)])

        node2 = TextNode("This is text with a **bold block** word with two **bold block** sections", TextType.text)
        new_nodes = split_nodes_delimiter([node2], "**", TextType.bold)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.text), TextNode("bold block", TextType.bold), TextNode(" word with two ", TextType.text), TextNode("bold block", TextType.bold), TextNode(" sections", TextType.text)])
        
        node3 = TextNode("This is text with a _italic block_ word", TextType.text)
        new_nodes = split_nodes_delimiter([node3], "_", TextType.italic)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.text), TextNode("italic block", TextType.italic), TextNode(" word", TextType.text)])

    def test_no_delimiter(self):
        node = TextNode("This is a text node with not delimiter", TextType.text)
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "_", TextType.italic)
    
    def test_not_text_type(self):
        node = TextNode("THIS IS A BOLD TEXT TYPE", TextType.bold)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        self.assertEqual(new_nodes, [node])
    
    def test_split_nodes_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        node2 = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) some more text too",
        TextType.text,
        )
        new_nodes = split_nodes_image([node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" some more text too", TextType.text)
            ],
            new_nodes,
        )
        node3 = TextNode(
        "This is text with two images back to back ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.text,
        )
        new_nodes = split_nodes_image([node3])
        self.assertListEqual(
            [
                TextNode("This is text with two images back to back ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.text),
                TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
                TextNode(" and ", TextType.text),
                TextNode(
                    "to youtube", TextType.link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
        node2 = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and some more text too",
        TextType.text,
        )
        new_nodes = split_nodes_link([node2])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.text),
                TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
                TextNode(" and ", TextType.text),
                TextNode(
                    "to youtube", TextType.link, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" and some more text too", TextType.text)
            ],
            new_nodes,
        )
        node3 = TextNode(
        "This is text with two links back to back [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.text,
        )
        new_nodes = split_nodes_link([node3])
        self.assertListEqual(
            [
                TextNode("This is text with two links back to back ", TextType.text),
                TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TextType.link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result,
                          [
                            TextNode("This is ", TextType.text),
                            TextNode("text", TextType.bold),
                            TextNode(" with an ", TextType.text),
                            TextNode("italic", TextType.italic),
                            TextNode(" word and a ", TextType.text),
                            TextNode("code block", TextType.code),
                            TextNode(" and an ", TextType.text),
                            TextNode("obi wan image", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.text),
                            TextNode("link", TextType.link, "https://boot.dev"),
                        ])

        text2 = "This is **text** with an _italic_ word and a `code block`"
        result = text_to_textnodes(text2)
        self.assertEqual(result,
                         [
                             TextNode("This is ", TextType.text),
                             TextNode("text", TextType.bold),
                             TextNode(" with an ", TextType.text),
                             TextNode("italic", TextType.italic),
                             TextNode(" word and a ", TextType.text),
                             TextNode("code block", TextType.code)
                         ])
