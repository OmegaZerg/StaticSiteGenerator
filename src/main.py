from textnode import TextNode, TextType

def main():
    testing = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(testing)
    print(repr(testing))

main()