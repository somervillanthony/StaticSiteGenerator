import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        node3 = TextNode("This is a test node", TextType.link, "test")
        node4 = TextNode("This is a test node", TextType.link, "test")
        node5 = TextNode("This is a test node", TextType.link, None)
        node6 = TextNode("This is a test node", TextType.link, None)
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        
        self.assertEqual(node5, node6)
        
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node4 = TextNode("This is a test node", TextType.link, "test")
        node6 = TextNode("This is a test node", TextType.link, None)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node6, node4)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



if __name__ == "__main__":
    unittest.main()