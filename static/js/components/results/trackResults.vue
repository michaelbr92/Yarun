<template lang="">
    <div>
        <ul class="task-list">
            <li :key="task.uid" v-for="task in tasks">
                <trackResult :file="task.file" :uid="task.uid"></trackResult>
            </li>
        </ul>
    </div>
</template>
<script>
import { getAPI } from "../../libs/api.mjs";
import trackResult from "./trackResult.vue";
export default {
    components: {
        trackResult: trackResult,
    },
    props: { tasks: { type: Array } },
};
</script>
<style lang="less">
.task-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-height: 70vh;
    overflow: scroll;
    padding: 0;
    li {
        width: 80%;
        padding: 5px 10px;

        position: relative;
    }
}
</style>
