const { defineStore } = Pinia;

const bucketStore = {
    state: () => ({
        selectedBucket: "",
        selectedTags: [],
    }),
    actions: {
        addTag(key, value) {
            this.selectedTags = [...this.selectedTags, [key, value]];
            let selectedTagsSet = new Set(this.selectedTags.map((item) => JSON.stringify(item)));
            this.selectedTags = [...selectedTagsSet].map((item) => JSON.parse(item));
        },
        removeTag(index) {
            this.selectedTags.pop(index);
        },
        clearTags() {
            this.selectedTags = [];
        },
    },
};

export const useFileSelectStore = defineStore("filesSelect", bucketStore);
export const useSignatureSelectStore = defineStore("segnatureSelect", bucketStore);
