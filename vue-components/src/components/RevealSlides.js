import { toRef, onMounted, nextTick } from "vue";

import "reveal.js/reset.css";
import "reveal.js/reveal.css";

import Reveal from "reveal.js";
import markdown from "reveal.js/plugin/markdown";
import highlight from "reveal.js/plugin/highlight";
import math from "reveal.js/plugin/math";
import notes from "reveal.js/plugin/notes";
import search from "reveal.js/plugin/search";
import zoom from "reveal.js/plugin/zoom";

export default {
  props: {
    tplName: {
      type: String,
      default: "slides",
    },
    theme: {
      type: String,
      default: "white",
    },
    config: {
      type: Object,
      default: null,
    },
  },
  setup(props) {
    const tplName = toRef(props, "tplName");

    onMounted(async () => {
      await nextTick();
      // await import(`reveal.js/dist/${props.theme}.css`);
      const deck = new Reveal({
        hash: true,
        plugins: [markdown, highlight, math, notes, search, zoom],
      });
      deck.initialize(props.config);
    });

    return {
      tplName,
    };
  },
  //
  template: `<div class="reveal"><trame-template :templateName="tplName"/></div>`,
};
