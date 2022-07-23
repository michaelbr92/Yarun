<template lang="">
    <div class="side-bar">
        <ul class="menu">
            <li class="logo"><i class="icon fa fa-signature"></i>Signatures</li>
            <router-link to="/" custom v-slot="{ route, navigate, isActive }">
                <li class="tab" :class="{ active: isActive }" :href="route.href" @click="navigate">
                    <i class="icon fa fa-home"></i><span>{{ route.name }}</span>
                </li>
            </router-link>
            <router-link to="/multi_run" custom v-slot="{ route, navigate, isActive }">
                <li class="tab" :class="{ active: isActive }" :href="route.href" @click="navigate">
                    <i class="icon fa fa-forward"></i><span>{{ route.name }}</span>
                </li>
            </router-link>
            <router-link to="/file_collector" custom v-slot="{ route, navigate, isActive }">
                <li class="tab" :class="{ active: isActive }" :href="route.href" @click="navigate">
                    <i class="icon fa fa-folder-tree"></i><span>{{ route.name }}</span>
                </li>
            </router-link>
            <router-link to="/run" custom v-slot="{ route, navigate, isActive }">
                <li class="tab" :class="{ active: isActive }" :href="route.href" @click="navigate">
                    <i class="icon fa fa-play"></i><span>{{ route.name }}</span>
                </li>
            </router-link>
            <router-link to="/settings" custom v-slot="{ route, navigate, isActive }">
                <li class="tab" :class="{ active: isActive }" :href="route.href" @click="navigate">
                    <i class="icon fa fa-gear"></i><span>{{ route.name }}</span>
                </li>
            </router-link>
        </ul>
    </div>
</template>
<script>
export default {};
</script>
<style lang="less" scoped>
.menu {
    --tab-height: 50px;
    list-style: none;
    width: 100%;
    padding: 10px 0px;

    .line {
        background: var(--light);
        width: 80%;
        height: 2px;
        margin: 10px;
    }
    li:not(.line) {
        width: 90%;
        height: 50px;
        padding: 10px;
        // border: 1px solid white;
        border-radius: 0px 50px 50px 0;
        font-size: 1em;
        display: flex;
        align-items: center;
        text-transform: capitalize;
    }
    li.logo {
        height: 60px;
        font-size: 1.3em;
        color: var(--primary);

        font-family: "Roboto", sans-serif;
        font-weight: 700;
        .icon {
            margin: 0 5px 0 10px;
            font-size: 1.5em;
        }
    }
    .tab {
        position: relative;
        transition: background 0.1s, color 0.1s;
        cursor: pointer;
        box-sizing: border-box;
        .icon {
            // font-size: 30px;
            margin: 0 10px;
            width: 40px;
            height: 40px;
            background: var(--dark);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        &.active,
        &:hover {
            background: var(--dark);
            color: var(--primary);
            &::before {
                content: "";
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
                width: 3px;
                background: var(--primary);
            }
        }
    }
}
.side-bar {
    display: inline-block;
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--secondary);
}
</style>
