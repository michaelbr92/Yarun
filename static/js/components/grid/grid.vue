<template lang="">
    <div class="grid">
        <slot></slot>
    </div>
</template>
<script>
export default {};
</script>
<style lang="less">
.grid {
    width: 100%;
    display: inline-flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: space-around;
    padding: 20px 20px 0 20px;
    .card {
        flex-grow: 2;
        background: var(--secondary);
        padding: 10px;
        min-width: 500px;

        position: relative;
        display: flex;
        flex-direction: column;
        border-radius: 5px;
        min-width: 300px;
        > * {
            display: inline-block;
        }
    }
}
</style>
