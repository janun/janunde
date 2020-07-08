from wagtail.core import blocks

from core.blocks import ParagraphBlock, ImageBlock, VideoLink


class WimmelbildStreamBlock(blocks.StreamBlock):
    paragraph = ParagraphBlock(
        features=["h2", "h3", "bold", "italic", "link", "ol", "ul", "document-link",]
    )
    image = ImageBlock()
    video_link = VideoLink()
