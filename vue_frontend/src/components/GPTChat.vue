<template>
  <div class="container-fluid p-3 d-flex flex-column vh-100">
    <!-- Scrollable row for output areas -->
    <div class="row flex-grow-1 mb-2">
      <!-- First output area -->
      <div class="col-md-6 output-container">
        <div class="output" ref="outputContainer" v-html="formattedOutput"></div>
      </div>
      <!-- Second output area -->
      <div class="col-md-6 output-container">
        <div class="output-code" ref="outputCodeContainer" v-html="outputCodeText"></div>
      </div>
    </div>

    <!-- Fixed row for textarea and buttons -->
    <div class="row">
      <div class="col-9">
        <textarea v-model="prompt" class="form-control" placeholder="Enter your prompt" @keydown="handleKeydown"
                  :style="{ height: inputHeight }"></textarea>
      </div>
      <div class="col-3 d-flex flex-column">
        <button @click="sendPrompt" class="btn btn-primary mb-2">Generate</button>
        <button @click="clearConversation" class="btn btn-secondary mb-2">Clear Conversation</button>
        <button @click="sendTestPrompt" class="btn btn-primary">Test Code</button>
      </div>
    </div>
  </div>
</template>


<script>
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";

export default {
  data() {
    return {
      prompt: '',
      outputText: '',
      outputCodeText: '',
      inputHeight: '',
      websocket: null,
      outputCompleted: false
    };
  },
  methods: {
    appendOutputText(text) {
      this.outputText += text;
      this.$nextTick(() => {
        if (this.$refs.outputContainer) {
          this.$refs.outputContainer.scrollTop = this.$refs.outputContainer.scrollHeight;
        }
      });
    },

    appendOutputCodeText(text) {
      this.outputCodeText += text;
      this.$nextTick(() => {
        if (this.$refs.outputCodeContainer) {
          this.$refs.outputCodeContainer.scrollTop = this.$refs.outputCodeContainer.scrollHeight;
        }
      });
    },
    async sendTestPrompt() {
      this.prompt = "Write a python program to get fives jokes from a public api.  Use only built in libraries.  Make sure the indentation is correct for Python.  Do not use example.com";
      await this.sendPrompt();
    },
    async sendPrompt() {
      this.outputCompleted = false;
      if (this.outputText.length > 0) {
        this.outputText += '\n\n';
      }
      this.outputText += "User: " + this.prompt + '\n\n';
      this.outputText += "Computer Machine: \n\n";
      if (!this.websocket || this.websocket.readyState === WebSocket.CLOSED) {
        this.websocket = new WebSocket('ws://localhost:8000/generate');
        this.websocket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.code) {
            if (this.outputCodeText.length > 0) {
              this.outputCodeText += '\n\n';
            }
            this.outputCodeText += data.code;
            this.scrollOutputCodeToBottom();
          }
          if (data.completed) {
            this.outputCompleted = true;
            this.applyHighlighting();
          } else {
            if (data.response) {
              this.outputText += data.response;
              this.scrollOutputToBottom();
            }
          }
        };
        this.websocket.onopen = () => {
          this.websocket.send(JSON.stringify({prompt: this.prompt}));
          this.prompt = '';
          this.outputCodeText = '';
        };
      } else {
        this.websocket.send(JSON.stringify({prompt: this.prompt}));
        this.prompt = '';
        this.outputCodeText = '';
      }
    },
    handleKeydown(event) {
      if (event.key === 'Enter') {
        if (!event.shiftKey) {
          event.preventDefault();
          this.sendPrompt();
        }
      }
    },
    adjustHeight() {
      const textarea = this.$el.querySelector('textarea');
      // Reset the height to shrink if text has been removed
      textarea.style.height = 'auto';
      const scrollHeight = textarea.scrollHeight;
      // Set a minimum height of one line and maximum height for five lines
      const maxHeight = parseInt(getComputedStyle(textarea).lineHeight) * 5;
      this.inputHeight = `${Math.min(scrollHeight, maxHeight)}px`;
    },
    clearConversation() {
      this.outputText = '';
      this.outputCodeText = '';
    },
    applyHighlighting() {
      this.$nextTick(() => {
        if (this.outputCompleted) {
          const blocks = this.$refs.outputContainer.querySelectorAll('pre code');
          blocks.forEach((block) => {
            hljs.highlightBlock(block);
          });
        }
      });
    },
    scrollOutputToBottom() {
      this.$nextTick(() => {
        if (this.$refs.outputContainer) {
          this.$refs.outputContainer.scrollTop = this.$refs.outputContainer.scrollHeight;
        }
      });
    },

    scrollOutputCodeToBottom() {
      this.$nextTick(() => {
        if (this.$refs.outputCodeContainer) {
          this.$refs.outputCodeContainer.scrollTop = this.$refs.outputCodeContainer.scrollHeight;
        }
      });
    },
  },
  computed: {
    formattedOutput() {
      let formatted = this.outputText.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');

      formatted = formatted.split(/(<pre><code>[\s\S]*?<\/code><\/pre>)/g).map((part, index) => {
        // Only replace \n with <br> in non-code parts (odd indices are code parts)
        return index % 2 === 0 ? part.replace(/\n/g, '<br>') : part;
      }).join('');

      return formatted;
    }
  },

  watch: {
    prompt() {
      this.adjustHeight();
    },
    outputCompleted(newVal) {
      if (newVal) {
        this.applyHighlighting();
      }
    },
    outputText(newValue, oldValue) {
      this.$nextTick(() => {
        const outputContainer = this.$refs.outputContainer;
        if (outputContainer) {
          outputContainer.scrollTop = outputContainer.scrollHeight;
        }
      });
    },
    outputCodeText(newValue, oldValue) {
      this.$nextTick(() => {
        const outputCodeContainer = this.$refs.outputCodeContainer;
        if (outputCodeContainer) {
          outputCodeContainer.scrollTop = outputCodeContainer.scrollHeight;
        }
      });
    }
  },
  directives: {
    'scrollBottom': {
      updated(el) {
        el.scrollTop = el.scrollHeight;
      }
    }
  },
  mounted() {
    this.adjustHeight();
    this.applyHighlighting();
  },

}
</script>

<style>
.output-container {
  overflow-y: auto;
  height: calc(100vh - 150px); /* Adjust the height based on your header/footer size */
}

.output, .output-code {
  flex-grow: 1;
}

.output pre {
  margin: 0; /* Reset margin for pre element */
  white-space: pre-wrap; /* Wrap text inside pre element */
}
</style>
