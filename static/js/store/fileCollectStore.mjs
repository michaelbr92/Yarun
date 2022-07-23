const { defineStore } = Pinia;

const storeObject = {
    state: () => ({
        fileList: [],
        signatureList: [],
    }),
    actions: {
        updateFiles(tagFilter) {},
        updateSignature(tagFilter) {},
    },
};

export const useFileCollectStore = defineStore("fileCollect", storeObject);
