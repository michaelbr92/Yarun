// const { loadModule } = window["vue3-sfc-loader"];
import { loadModule } from "/lib/vue3-sfc-loader/dist/vue3-sfc-loader.esm.js";
async function sass_compile(source) {
    let sass = new Sass();
    result = new Promise((resolve) => {
        sass.compile(source, (result) => {
            resolve(result);
        });
    });
    return result;
}

const options = {
    moduleCache: {
        vue: Vue,
        less: less,
    },
    async getFile(url) {
        const res = await fetch(url);
        if (!res.ok) throw Object.assign(new Error(res.statusText + " " + url), { res });
        return {
            getContentData: (asBinary) => (asBinary ? res.arrayBuffer() : res.text()),
        };
    },
    compiledCache: {
        set(key, str) {
            for (;;) {
                try {
                    // window.localStorage.setItem(key, str);
                    break;
                } catch (ex) {
                    window.localStorage.removeItem(window.localStorage.key(0));
                }
            }
        },
        get(key) {
            return window.localStorage.getItem(key);
        },
    },
    addStyle(textContent) {
        const style = Object.assign(document.createElement("style"), { textContent });
        const ref = document.head.getElementsByTagName("style")[0] || null;
        document.head.insertBefore(style, ref);
    },
};

export function getModule(url) {
    return () => loadModule(url, options);
}
export function getApp(url) {
    return Vue.defineAsyncComponent(getModule(url));
}
