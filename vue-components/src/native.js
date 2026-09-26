class RevealTrameApp extends HTMLElement {
  connectedCallback() {
    const name = this.getAttribute("name");
    const url = window.trame.state.state.app_urls[name];

    if (!url) {
      throw new Error(`Unknown trame application: ${name}`);
    }

    const iframe = document.createElement("iframe");
    iframe.src = url;
    iframe.width = "100%";
    iframe.height = "100%";
    iframe.loading = "eager";
    iframe.class = "trame-app";
    iframe.style = "border: none;";

    this.appendChild(iframe);
  }
}

customElements.define("reveal-trame-app", RevealTrameApp);
