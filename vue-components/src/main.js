import components from "./components";
import "./native";

export function install(Vue) {
  Object.keys(components).forEach((name) => {
    Vue.component(name, components[name]);
  });
}
