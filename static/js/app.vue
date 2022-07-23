<template lang="">
    <div class="panel">
        <sideBar id="side-bar"></sideBar>

        <div class="">
            <!-- Navbar Start -->

            <router-view></router-view>
            <!-- Navbar End -->
        </div>
    </div>
</template>
<script type="module">
import sideBar from "./components/sideBar.vue";
export default {
    components: {
        sideBar: sideBar,
    },
    data() {
        return {
            foo: "aaabbb",
        };
    },
    mounted() {
        // $("#spinner").removeClass("show");
        $(".sidebar-toggler").click(function () {
            $(".sidebar, .content").toggleClass("open");
            return false;
        });
    },
};
</script>
<style lang="less">
#spinner {
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-out, visibility 0s linear 0.5s;
    z-index: 99999;
}

#spinner.show {
    transition: opacity 0.5s ease-out, visibility 0s linear 0s;
    visibility: visible;
    opacity: 1;
}

.panel {
    display: grid;
    width: 100%;
    height: 100%;
    & {
        grid-template-rows: 1fr;
        grid-template-columns: 250px auto;
        grid-template-areas: "sidebar body";
    }
    #side-bar {
        position: sticky;
        top: 0;
        height: 100vh;
        grid-area: sidebar;
    }
    #nav-bar {
        grid-area: top;
        padding: 10px;
    }
}
</style>
