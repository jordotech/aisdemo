const fetch = require("node-fetch")
const queryString = require("query-string")
exports.sourceNodes = (
    {actions, createNodeId, createContentDigest},
    configOptions
) => {
    const {createNode} = actions;
    // Gatsby adds a configOption that's not needed for this plugin, delete it
    delete configOptions.plugins;
    const processVessel = mmsi => {
        const nodeId = createNodeId(`vessel-${mmsi.id}`);
        console.log(nodeId);
        const nodeData = Object.assign({}, mmsi, {
            id: nodeId,
            parent: null,
            children: [],
            internal: {
                type: `Vessel`,
                contentDigest: createContentDigest(mmsi),
            },
        })
        return nodeData
    }
    return (
        fetch("http://django:8000/api/vessels/?format=json")
            .then(response => response.json())
            .then(data => {
                data.results.forEach(mmsi => {
                    const nodeData = processVessel(mmsi);
                    createNode(nodeData)
                })
            })
    )
}
