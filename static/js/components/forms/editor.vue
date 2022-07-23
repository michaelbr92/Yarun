<template lang="">
    <textarea id="editor">{{ modelValue }} </textarea>
</template>
<script type="module">
export default {
    props: {
        modelValue: {
            type: String,
            default: `import "console"\nrule test{}`,
        },
    },
    data: () => ({
        highlightedCode: "",
    }),
    async mounted() {
        var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
            theme: "ayu-dark",
            styleActiveLine: true,
            lineNumbers: true,
            matchBrackets: true,
            indentUnit: 2,
            tabSize: 2,
            indentWithTabs: false,
            mode: "yara",
        });
        editor.on("change", (e) => {
            this.$emit("update:modelValue", e.getValue());
        });
    },
};
</script>
<style lang="less"></style>
