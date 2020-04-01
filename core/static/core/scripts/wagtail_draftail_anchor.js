const React = window.React;
const RichUtils = window.DraftJS.RichUtils;


// This is very basic – we do not even support editing existing anchors.
class AnchorIdentifierSource extends React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;
    const content = editorState.getCurrentContent();
    const fragment = window.prompt('Anker-ID:');

    // Uses the Draft.js API to create a new entity with the right data.
    const contentWithEntity = content.createEntity(
      entityType.type,
      'MUTABLE',
      {
        fragment: fragment,
      },
    );
    const entityKey = contentWithEntity.getLastCreatedEntityKey();
    const selection = editorState.getSelection();
    const nextState = RichUtils.toggleLink(
      editorState,
      selection,
      entityKey,
    );

    onComplete(nextState);
  }

  render() {
    return null;
  }
}

const AnchorIdentifier = props => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();

  return React.createElement(
    'span',
    {
      role: 'button',
      title: "Anker mit ID '" + data.fragment + "'",
      'data-id': data.fragment
    },
    '#',
    props.children,
  );
};

window.draftail.registerPlugin({
  type: 'ANCHOR-IDENTIFIER',
  source: AnchorIdentifierSource,
  decorator: AnchorIdentifier,
});