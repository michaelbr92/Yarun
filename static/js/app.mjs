const { reactive, ref, createApp, watch } = Vue;
import { router } from "./views/router.mjs";
import { getApp } from "/js/options.mjs";
const { createPinia } = Pinia;

function init() {
    const app = createApp(getApp("js/app.vue"));
    const pinia = createPinia();

    if (localStorage.getItem("state")) {
        pinia.state.value = JSON.parse(localStorage.getItem("state"));
    }

    // save the whole state
    watch(
        pinia.state,
        (state) => {
            localStorage.setItem("state", JSON.stringify(state));
        },
        { deep: true }
    );

    app.use(pinia);
    app.use(router);
    app.mount("#app");
}
init();
