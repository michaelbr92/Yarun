<template lang="">
    <div class="task-result" :class="taskState">
        <div class="result-bar">
            <h2 class="file-name">{{ taskName }}</h2>
            <p class="subtitle">{{ taskSubtitle }}</p>
            <span class="buttons">
                <div class="btn copy" @click="copyToClipboard" tooltip="Copy to clipboard" flow="left">
                    <i class="fa-solid fa-copy"></i>
                </div>
                <div
                    class="btn terminal"
                    :class="{ toggled: isConsoleOpen }"
                    @click="isConsoleOpen = !isConsoleOpen"
                    v-if="consoleLines.length > 0"
                    tooltip="Toggle console"
                    flow="left"
                >
                    <i class="fa-solid fa-terminal"></i>
                </div>
            </span>
        </div>
        <div class="details" v-if="isConsoleOpen && consoleLines.length > 0">
            <p class="line" v-for="line in consoleLines">{{ line }}</p>
        </div>
    </div>
</template>
<script>
import { getAPI, postAPI } from "../../libs/api.mjs";
const taskState = {
    SUCCESS: "success",
    WARNNING: "warning",
    FAILURE: "fail",
    RUNNING: "running",
};
export default {
    props: {
        uid: { type: String },
        file: { type: Object },
    },
    data() {
        return {
            state: taskState.RUNNING,
            isConsoleOpen: false,
            result: {},
        };
    },
    methods: {
        resultToState(result) {
            if (result.status === "SUCCESS") {
                if (result.rule.strings.length === 1) {
                    return taskState.SUCCESS;
                }
                return taskState.WARNNING;
            }
            if (result.status === "FAILURE") {
                return taskState.FAILURE;
            }
            return taskState.RUNNING;
        },
        copyToClipboard() {
            navigator.clipboard.writeText(JSON.stringify(this.result));
        },
        async updateTask() {
            this.result = await getAPI(`/task/${this.uid}/result`);
            this.state = this.resultToState(this.result);
            if (this.state === taskState.RUNNING) {
                setTimeout(this.updateTask, 100);
            }
        },
    },
    mounted() {
        this.updateTask();
    },
    computed: {
        consoleLines() {
            try {
                return this.result.rule.console;
            } catch {
                return [];
            }
        },
        taskName() {
            return `${this.file.bucket}/${this.file.name}`;
        },
        taskState() {
            switch (this.state) {
                case taskState.FAILURE:
                case taskState.RUNNING:
                case taskState.WARNNING:
                case taskState.SUCCESS:
                    return this.state;
                default:
                    return "";
            }
        },
        taskSubtitle() {
            switch (this.state) {
                case taskState.FAILURE:
                    return "Failed";
                case taskState.SUCCESS:
                    return `Found ${this.result.rule.strings.length} match`;
                case taskState.WARNNING:
                    return `Found ${this.result.rule.strings.length} matches`;
                case taskState.RUNNING:
                    return "Running";
                default:
                    return "";
            }
        },
    },
};
</script>
<style lang="less">
@keyframes runningDots {
    0% {
        content: "";
    }
    20% {
        content: ".";
    }
    40% {
        content: "..";
    }
    60% {
        content: "...";
    }
    80% {
        content: "....";
    }
    100% {
        content: ".....";
    }
}
.task-result {
    background: var(--secondary-light);
    border-radius: 12px;
    --border-color: var(--light);
    overflow: hidden;
    &.running {
        .subtitle::after {
            content: "";
            animation: runningDots 1s infinite;
        }
    }
    &.success {
        --border-color: var(--success);
    }
    &.warning {
        --border-color: var(--warning);
    }
    &.fail {
        --border-color: var(--fail);
    }

    border-left: 12px solid var(--border-color);
    .result-bar {
        display: grid;
        grid-template-columns: 1fr 100px;
        grid-template-rows: repeat(2, 1fr);
        height: 80px;
        padding-left: 10px;
        grid-template:
            "title    buttons"
            "subtitle buttons";
        & > * {
            margin: 0;
            padding: 0;
        }
        .file-name {
            width: 80%;
            max-width: 400px;
            direction: rtl;
            text-align: left;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 24px;
            font-weight: 400;
            grid-area: title;
            align-self: end;
        }
        .subtitle {
            font-size: 16px;
            font-weight: 400;
            align-self: start;
            grid-area: subtitle;
        }
        .buttons {
            grid-area: buttons;
            height: 100%;
            width: 100%;
            display: grid;
            grid-auto-flow: column;
            grid-auto-columns: 40px;
            align-items: center;
            justify-items: end;
            justify-content: end;
            gap: 10px;
            padding-right: 10px;
            .btn {
                opacity: 0.3;
                aspect-ratio: 1/1;
                height: 50%;
                border-radius: 50%;
                background: var(--dark);
                display: flex;
                align-items: center;
                justify-content: space-around;
                color: var(--bright);
                transition: opacity var(--normal-speed), transform var(--quick-speed);
                cursor: pointer;
                &:hover,
                &.toggled {
                    opacity: 1;
                }
                &:active {
                    transform: translateY(-5px);
                }
            }
        }
    }
    &.running {
        .buttons {
            display: none;
        }
    }
    .details {
        background: var(--dark);
        color: var(--light);
        height: 200px;
        font-size: 16px;
        line-height: 16px;
        overflow-y: scroll;
        .line {
            padding: 2px;
            font-family: "Courier New", Courier, monospace;
            margin: 0;
            &::before {
                content: "> ";
            }
        }
    }
}
</style>
