/**
 * Common ERD (Entity Relationship Diagram) module.
 * Shared between spec-builder and merge pages.
 */
const ERD = (function() {
    // Private state
    let _network = null;
    let _nodes = null;
    let _edges = null;

    // Standard network options
    const OPTIONS = {
        layout: {
            improvedLayout: true,
            randomSeed: 42
        },
        physics: {
            enabled: true,
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
                gravitationalConstant: -100,
                centralGravity: 0.01,
                springLength: 200,
                springConstant: 0.08,
                damping: 0.5,
                avoidOverlap: 1
            },
            maxVelocity: 50,
            minVelocity: 0.1,
            stabilization: {
                enabled: true,
                iterations: 2000,
                updateInterval: 25
            }
        },
        interaction: {
            hover: true,
            zoomView: true,
            zoomSpeed: 0.5,
            dragView: true,
            dragNodes: true,
            navigationButtons: false,
            keyboard: { enabled: false }
        },
        nodes: {
            shape: 'box',
            margin: 12,
            widthConstraint: { minimum: 180 }
        },
        edges: {
            smooth: {
                type: 'cubicBezier',
                forceDirection: 'vertical',
                roundness: 0.4
            }
        }
    };

    return {
        /**
         * Get the network options.
         */
        getOptions() {
            return structuredClone(OPTIONS);
        },

        /**
         * Create a new network.
         */
        createNetwork(container, nodeData, edgeData, customOptions = {}) {
            _nodes = new vis.DataSet(nodeData);
            _edges = new vis.DataSet(edgeData);

            const options = { ...OPTIONS, ...customOptions };

            if (_network) {
                _network.destroy();
            }

            _network = new vis.Network(container, { nodes: _nodes, edges: _edges }, options);

            _network.once('stabilizationIterationsDone', () => {
                _network.setOptions({ physics: { enabled: false } });
            });

            return _network;
        },

        /**
         * Get the current network instance.
         */
        getNetwork() {
            return _network;
        },

        /**
         * Get the nodes DataSet.
         */
        getNodes() {
            return _nodes;
        },

        /**
         * Get the edges DataSet.
         */
        getEdges() {
            return _edges;
        },

        /**
         * Auto-layout using force-directed algorithm.
         */
        autoLayout() {
            if (!_network) return;

            _network.setOptions({
                physics: {
                    enabled: true,
                    solver: 'forceAtlas2Based',
                    forceAtlas2Based: {
                        gravitationalConstant: -100,
                        centralGravity: 0.01,
                        springLength: 150,
                        springConstant: 0.08,
                        damping: 0.4
                    },
                    stabilization: {
                        enabled: true,
                        iterations: 200,
                        updateInterval: 25
                    }
                }
            });

            _network.once('stabilizationIterationsDone', () => {
                _network.setOptions({ physics: { enabled: false } });
                _network.fit({ animation: true });
            });

            _network.stabilize();
        },

        /**
         * Zoom in.
         */
        zoomIn() {
            if (_network) {
                const scale = _network.getScale();
                _network.moveTo({ scale: scale * 1.15, animation: { duration: 200 } });
            }
        },

        /**
         * Zoom out.
         */
        zoomOut() {
            if (_network) {
                const scale = _network.getScale();
                _network.moveTo({ scale: scale / 1.15, animation: { duration: 200 } });
            }
        },

        /**
         * Fit graph to viewport.
         */
        fitGraph() {
            if (_network) {
                _network.fit({ animation: { duration: 300 } });
            }
        }
    };
})();

// Convenience functions for HTML onclick handlers
function autoLayout() { ERD.autoLayout(); }
function zoomIn() { ERD.zoomIn(); }
function zoomOut() { ERD.zoomOut(); }
function fitGraph() { ERD.fitGraph(); }
