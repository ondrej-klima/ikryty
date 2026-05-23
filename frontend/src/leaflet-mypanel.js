import * as L from "leaflet";

L.Control.MyPanel = L.Control.extend({
    initialize: function (placeholder, options) {
        this.placeholder = placeholder
        L.setOptions(this, options);
    },
    onAdd: function (map) {
        // Avatar content
        // Find content container
        let content = L.DomUtil.get(this.placeholder);

        // Remove the content container from its original parent
        if (content.parentNode != undefined) {
            content.parentNode.removeChild(content);
        }
        let l = 'leaflet-';

        // Create sidebar container
        let container = this._container =
            L.DomUtil.create('div', l + this.placeholder);

        // Style and attach content container
        L.DomUtil.addClass(content, l + 'control' + this.placeholder);
        container.appendChild(content);

        let controlContainer = map._controlContainer;
        controlContainer.insertBefore(container, controlContainer.firstChild);

        return content;
    },
    onRemove: function () {
        // Nothing to do here
    }
});

L.control.mypanel = function (placeholder, opts) {
    return new L.Control.MyPanel(placeholder, opts);
}