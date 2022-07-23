<template lang="">
    <Grid>
        <Card>
            <FileCollector></FileCollector>
        </Card>
    </Grid>
    <Grid>
        <Card>
            <h2>Yara rule</h2>
            <div>
                <div class="run-btn" :class="{ valid: signatureState === 'valid' }" @click="runSignature">
                    <i class="fa-solid fa-play"></i> Run
                </div>
                <i class="validating fa-solid fa-circle-notch fa-spin" v-if="signatureState === 'validating'"></i>
            </div>
            <Editor v-model="code"></Editor>
        </Card>
        <Card> <trackResults :tasks="taskUids"></trackResults></Card>
    </Grid>
</template>
<script type="module">
import editor from "../components/forms/editor.vue";
import card from "../components/grid/card.vue";
import grid from "../components/grid/grid.vue";
import { useFileCollectStore } from "../store/fileCollectStore.mjs";
import trackResults from "../components/results/trackResults.vue";
import FileCollector from "../components/forms/fileCollectorPreview.vue";
import { postAPI } from "../libs/api.mjs";
const status = {
    VALID: "valid",
    VALIDATING: "validating",
    INVALID: "invalid",
};
export default {
    components: {
        FileCollector: FileCollector,
        Editor: editor,
        Grid: grid,
        Card: card,
        trackResults: trackResults,
    },
    data() {
        return {
            code: `import "console"\nrule test{\n  condition: true\n}`,
            signatureState: status.VALIDATING,
            fileStore: useFileCollectStore(),
            taskUids: [],
        };
    },
    watch: {
        code: "update",
    },
    methods: {
        update(a) {
            this.signatureState = status.VALIDATING;
        },
        async codeValidation() {
            if (this.signatureState !== status.VALIDATING) {
                return;
            }
            if (await postAPI("/task/validate", { data: { signature: this.code } })) {
                this.signatureState = status.VALID;
            } else {
                this.signatureState = status.INVALID;
            }
        },
        async runSignature() {
            // if (this.signatureState !== status.VALID) {
            // return;
            // }
            let requestsData = this.fileStore.fileList.map((fileObj) => {
                return {
                    file: fileObj,
                    signature: this.code,
                };
            });
            this.taskUids = await Promise.all(
                requestsData.map(async (data) => {
                    return {
                        file: data.file,
                        uid: await postAPI("/task/new", { data: data }),
                    };
                })
            );
        },
    },
    mounted() {
        // this.runSignature();
        // this.codeValidation();
        this.updated = setInterval(this.codeValidation, 1000);
    },
};
</script>
<style lang="less">
.validating {
    font-size: 30px;
}
.run-btn {
    padding: 10px 20px;
    margin: 5px;
    border-radius: 10px;
    display: inline-block;
    box-shadow: inset 0px 0px 0px 1px var(--light);
    background: none;
    color: var(--light);
    &.valid {
        box-shadow: none;
        background: var(--primary);
        color: var(--dark);
        cursor: pointer;
        transition: color var(--quick-speed), background var(--quick-speed);
        &:hover {
            background: var(--dark);
            color: var(--primary);
        }
    }
}
</style>
