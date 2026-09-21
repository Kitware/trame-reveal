class TrameEmbeddedAppElement extends HTMLElement {
    connectedCallback() {
        const appId = this.getAttribute("app-id");

        const url = trame.state.state.app_urls[appId];

        if (!url) {
            throw new Error(`Unknown trame application: ${appId}`);
        }

        const iframe = document.createElement("iframe");
        iframe.src = url;
        iframe.style.width = "100%";
        iframe.style.height = "100%";
        iframe.style.border = "0";
        iframe.dataset.preload = 'true';

        this.appendChild(iframe);
    }
}

customElements.define("trame-embedded-app", TrameEmbeddedAppElement);
