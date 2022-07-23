<template lang="">
    <div id="collected-status">
        <span tooltip="Reload file selection" flow="down">
            <i @click="updateFiles" :class="{ loading: loading }" class="reload fa-solid fa-arrow-rotate-right"></i>
        </span>

        <h2 class="counter"><b>Files selected: </b>{{ store.fileList.length }}</h2>
        <h2 class="counter"><b>Signature selected: </b>{{ store.signatureList.length }}</h2>
    </div>
</template>
<script>
import { useFileCollectStore } from "../../store/fileCollectStore.mjs";

import { useFileSelectStore, useSignatureSelectStore } from "../../store/bucketStroe.mjs";
import { getAPI } from "../../libs/api.mjs";
const { watch } = Vue;
export default {
    data() {
        return {
            loading: 0,
            store: useFileCollectStore(),
            storeFile: useFileSelectStore(),
            storeSignature: useSignatureSelectStore(),
        };
    },
    methods: {
        async collectFromTags(bucket, tags) {
            if (tags.length) {
                let fileListPromises = [...tags].map(([tagKey, tagValue]) =>
                    getAPI(`/bucket/${bucket}/files`, {
                        tagKey: tagKey,
                        tagValue: tagValue,
                    })
                );

                let fileLists = await Promise.all(fileListPromises);

                var files = [].concat(...fileLists);
            } else {
                var files = await getAPI(`/bucket/${bucket}/files`);
            }

            let fileSet = new Set(files.map((item) => JSON.stringify(item)));
            return [...fileSet].map((item) => JSON.parse(item));
        },
        async updateFiles() {
            this.loading++;
            this.store.fileList = await this.collectFromTags(
                this.storeFile.selectedBucket,
                this.storeFile.selectedTags
            );
            this.store.signatureList = await this.collectFromTags(
                this.storeSignature.selectedBucket,
                this.storeSignature.selectedTags
            );
            this.loading--;
        },
    },
    mounted() {
        watch(
            () => this.storeFile,
            (_) => this.updateFiles(),
            { deep: true }
        );
        watch(
            () => this.storeSignature,
            (_) => this.updateFiles(),
            { deep: true }
        );
    },
};
</script>
<style lang="less" scoped>
@keyframes rotate {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(1turn);
    }
}
#collected-status {
    display: flex;
    flex-direction: row;
    align-items: center;
    > * {
        padding: 0 10px;
    }
    .counter {
        border-left: 1px solid var(--light);
    }
    .reload {
        font-size: 2em;
        color: var(--primary);
        cursor: pointer;
        &:hover {
            animation: rotate var(--normal-speed);
        }
        &.loading {
            animation: rotate var(--slow-speed) linear infinite;
        }
    }
}
</style>
