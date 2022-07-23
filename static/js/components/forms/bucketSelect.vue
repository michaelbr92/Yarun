<template lang="">
    <select v-model="selectedBucket" @change="fileBucketSelected">
        <option disabled selected value>--</option>
        <option :value="bucket" v-for="bucket in fileBuckets">{{ bucket }}</option>
    </select>

    <h3>Add tags</h3>
    <p>The result is the unioun of below selected</p>

    <!-- Tag add section -->
    <div class="tag-add">
        <select id="tag-key" v-model="tagKeyToAdd" class="tag-key-selector" @change="tagKeySelected">
            <option disabled selected value>--</option>
            <option :value="key" v-for="key in availbleTagTypes">{{ key }}</option>
        </select>

        <select id="tag-value" v-model="tagValueToAdd" class="tag-key-selector">
            <option disabled selected value>--</option>
            <option :value="value" v-for="value in availbleTagValues">{{ value }}</option>
        </select>

        <i class="fa-solid fa-plus" id="add-tag" @click="addTag"></i>
    </div>

    <!-- Tag list section -->
    <div id="tag-list">
        <li class="tag" v-for="([key, val], index) in selectedTags">
            <i class="remove fa-solid fa-minus-circle" @click="removeTag(index)"></i> <b>{{ key }}:</b> {{ val }}
        </li>
    </div>
</template>
<script>
import { API, getAPI } from "../../libs/api.mjs";
export default {
    props: {
        store: { type: Object },
    },
    data() {
        return {
            fileBuckets: [],
            tagKeyToAdd: "",
            tagValueToAdd: "",
            availbleTagValues: [],
            availbleTagTypes: [],
        };
    },
    async mounted() {
        this.fileBuckets = await getAPI("/bucket/list");
        if (this.selectedBucket !== "") {
            this.availbleTagTypes = await getAPI(`/bucket/${this.selectedBucket}/tags`);
        }
    },
    computed: {
        async tagValues() {
            if (this.tagKeyToAdd === "") {
                return [];
            }
            return await getAPI(`/bucket/${this.selectedBucket}/tag/${this.tagKeyToAdd}`);
        },
        selectedBucket: {
            get() {
                return this.store.selectedBucket;
            },
            set(val) {
                this.store.selectedBucket = val;
            },
        },
        selectedTags: {
            get() {
                return this.store.selectedTags;
            },
            set(val) {
                this.store.selectedTags = val;
            },
        },
    },
    methods: {
        removeTag(index) {
            this.store.removeTag(index);
        },
        clearTags() {
            this.store.clearTags();
        },
        addTag() {
            var tagKey = this.tagKeyToAdd;
            var tagValue = this.tagValueToAdd;
            if (!tagKey || !tagValue) {
                return;
            }
            this.store.addTag(tagKey, tagValue);
        },
        async fileBucketSelected(event) {
            this.store.selectedBucket = event.target.value;
            this.clearTags();

            this.availbleTagTypes = [];
            if (this.selectedBucket !== "") {
                this.availbleTagTypes = await getAPI(`/bucket/${this.selectedBucket}/tags`);
            }
        },
        async tagKeySelected(event) {
            if (this.tagKeyToAdd === "") {
                return;
            }
            this.availbleTagValues = await getAPI(`/bucket/${this.selectedBucket}/tag/${this.tagKeyToAdd}`);
        },
    },
};
</script>
<style lang="less" scoped>
#tag-list {
    list-style: none;
    max-width: 400px;
    padding-right: 20px;
    .tag {
        display: inline-block;
        color: var(--dark);
        background: var(--light);
        padding: 5px;
        margin: 5px;
        border-radius: 50px;
        .remove {
            // background: var(--light);
            color: var(--dark);
            border-radius: 100%;
            cursor: pointer;
        }
    }
}
#add-tag {
    cursor: pointer;
}
.tag-key-selector {
    width: 40%;
    display: inline-block;
}
</style>
