import { getModule } from "/js/options.mjs";

export const home = getModule("js/views/home.vue");
export const envSelectionView = getModule("js/views/envSelection.vue");
export const fileCollector = getModule("js/views/fileCollector.vue");
export const multiRun = getModule("js/views/multiRun.vue");
export const runView = getModule("js/views/run.vue");

const routes = [
    {
        path: "/",
        component: home,
        name: "home",
    },
    {
        path: "/settings",
        component: envSelectionView,
        name: "settings",
    },
    {
        path: "/multi_run",
        component: multiRun,
        name: "Multi run",
    },
    {
        path: "/run",
        component: runView,
        name: "Run",
    },
    {
        path: "/file_collector",
        component: fileCollector,
        name: "File collector",
    },
];

export const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes,
});
