from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
)


def anchor_identifier_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the ANCHOR entities into <span> tags.
    """
    return DOM.create_element(
        "span",
        {
            "data-id": props["fragment"].lstrip("#"),
            "id": props["fragment"].lstrip("#"),
        },
        props["children"],
    )


class AnchorIndentifierEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the <a> tags into ANCHOR IDENTIFIER entities, with the right data.
    """

    # In Draft.js entity terms, anchors identifier are "mutable".
    mutability = "MUTABLE"

    def get_attribute_data(self, attrs):
        """
        Take the ``fragment`` value from the ``id`` HTML attribute.
        """
        return {
            "fragment": attrs["id"],
            "data-id": attrs["id"],
        }
