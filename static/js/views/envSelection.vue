<template lang="">
    <Grid>
        <Card>
            <FileCollector></FileCollector>
        </Card>
    </Grid>
    <Grid>
        <Card>
            <h2>Select files <i class="fa-solid fa-file"></i></h2>
            <BucketSelect :store="fileBucketStore"></BucketSelect>
        </Card>
        <Card>
            <h2>Select signatures <i class="fa-solid fa-file-signature"></i></h2>
            <BucketSelect :store="signatureBucketStore"></BucketSelect>
        </Card>
    </Grid>
</template>
<script type="module">
import card from "../components/grid/card.vue";
import grid from "../components/grid/grid.vue";
import bucketSelect from "../components/forms/bucketSelect.vue";
import fileCollector from "../components/forms/fileCollectorPreview.vue";
import { useFileSelectStore, useSignatureSelectStore } from "../store/bucketStroe.mjs";

export default {
    components: {
        Grid: grid,
        Card: card,
        BucketSelect: bucketSelect,
        FileCollector: fileCollector,
    },
    data() {
        return {
            fileBucketStore: useFileSelectStore(),
            signatureBucketStore: useSignatureSelectStore(),
        };
    },
    computed: {
        counter() {
            return this.bucketStore.selectedBucket;
        },
    },
};
</script>
<style lang="less">
h2 i {
    color: var(--primary);
}
</style>
