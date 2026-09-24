import { inject, computed } from "vue";

export default {
  props: {
    appId: {
      type: String,
    },
  },
  setup(props) {
    const trame = inject("trame");
    const url = computed(() => trame.state.state.app_urls[props.appId]);

    if (!url.value) {
      throw new Error(`Unknown trame application: ${props.appId}`);
    }

    return {
      url,
    };
  },
  template: `
    <iframe
      :src="url"
      width="100%"
      height="100%"
      loading="eager"
      style="border: none;"
    ></iframe>`,
};
