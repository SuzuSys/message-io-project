<script setup lang="ts">
import { ref } from 'vue';
interface ContentProps {
  content: string;
};
const props = defineProps<ContentProps>();
interface RegContent {
  regexp: RegExp;
  format: (str: string) => string;
}
type List = {
  content: string;
  currentArray: Array<List>;
  child?: Array<List>;
  parent?: List;
  first_number?: number; // If the list is ol, this type is number. If ul, then undefined.
};
interface MentionReg {
  regexp: RegExp;
  display: string;
}
interface Reg {
  italics: RegContent;
  bold: RegContent;
  bold_italics: RegContent;
  underline: RegContent;
  underline_italics: RegContent;
  underline_bold: RegContent;
  underline_bold_italics: RegContent;
  strickthrough: RegContent;
  masked_links: {
    regexp: RegExp;
    display: string;
    url: string;
  };
  code_block: RegContent;
  code_inline: RegContent;
  spoiler_tag: RegContent;
  ul: {
    regexp: RegExp;
    li: Array<List>;
  };
  ol: {
    regexp: RegExp;
    li: Array<List>;
  };
  h1: RegContent;
  h2: RegContent;
  h3: RegContent;
  block_quotes: {
    regexp: RegExp;
    content: string;
  };
  channel_mention: MentionReg;
  role_mention: MentionReg;
  member_mention: MentionReg;
}
const regexps = ref<Reg>({
  italics: {
    regexp: /(?<italics>(?:\*\S+[^]*\*)|(?:_[^_][^]*_))/m,
    format: str => str.slice(1, -1)
  },
  bold: {
    regexp: /(?<bold>\*{2}[^]+\*{2})/m,
    format: str => str.slice(2, -2),
  },
  bold_italics: {
    regexp: /(?<bold_italics>\*{3}[^]+\*{3})/m,
    format: str => str.slice(3, -3),
  },
  underline: {
    regexp: /(?<underline>_{2}[^]+_{2})/m,
    format: str => str.slice(2, -2),
  },
  underline_italics: {
    regexp: /(?<underline_italics>_{2}\*[^]+\*_{2})/m,
    format: str => str.slice(3, -3),
  },
  underline_bold: {
    regexp: /(?<underline_bold>_{2}\*{2}[^]+\*{2}_{2})/m,
    format: str => str.slice(4, -4),
  },
  underline_bold_italics: {
    regexp: /(?<underline_bold_italics>_{2}\*{3}[^]+\*{3}_{2})/m,
    format: str => str.slice(5, -5),
  },
  strickthrough: {
    regexp: /(?<strickthrough>\~{2}[^]+\~{2})/m,
    format: str => str.slice(2, -2),
  },
  masked_links: {
    regexp: /(?<masked_links>\[(?![^]*https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+\s*[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+\s*\))[^]*\S+[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+\s*\))/m,
    display: '',
    url: '',
  },
  code_block: {
    regexp: /(?<code_block>`{3}[^]+`{3})/m,
    format: str => str.slice(3, -3),
  },
  code_inline: {
    regexp: /(?<code_inline>(?:`[^]+`(?!`))|(?:`{2}[^]+`{2}(?!`)))/m,
    format: str => {
      const s = str.slice(1, -1);
      return s[s.length-1] === '`' ? s.slice(1, -1) : s;
    },
  },
  spoiler_tag: {
    regexp: /(?<spoiler_tag>\|{2}[^\n]+\|{2})/m,
    format: str => str.slice(2, -2),
  },
  ul: {
    regexp: /(?<ul>^\s*(?:\-|\*)\s+\S+.*$)/m,
    li: [],
  },
  ol: {
    regexp: /(?<ol>^\s*\d+\.\s+\S+.*$)/m,
    li: [],
  },
  h1: {
    regexp: /(?<h1>^#\s+\S+.*$)/m,
    format: str => str.slice(2),
  },
  h2: {
    regexp: /(?<h2>^#{2}\s+\S+.*$)/m,
    format: str => str.slice(3),
  },
  h3: {
    regexp: /(?<h3>^#{3}\s+\S+.*$)/m,
    format: str => str.slice(4),
  },
  block_quotes: {
    regexp: /(?<block_quotes>^>\s+\S+.*$)/m,
    content: '',
  },
  channel_mention: {
    regexp: /(?<channel_mention><#\d+>)/m,
    display: '',
  },
  role_mention: {
    regexp: /(?<role_mention><@&\d+>)/m,
    display: '',
  },
  member_mention: {
    regexp: /(?<member_mention><@&\d+>)/m,
    display: '',
  },
});
interface State {
  matched: boolean;
  matchedKey: string;
  x: string;
  y: string;
  z: string;
}
interface IncompleteState {
  matched: false;
  matchedKey: undefined;
  x: string;
  y: undefined;
  z: undefined;
}
const state = ref<IncompleteState|State>({
  matched: false,
  matchedKey: undefined,
  x: props.content,
  y: undefined,
  z: undefined,
});

const combinedReg = new RegExp(Object.values(regexps).map(r => r.regexp).join('|'), 'm');
// exec() follow the "greedy matching"!
const res = execCaptureGroup(combinedReg, props.content);
if (res) {
  state.value.matched = true;
  state.value.matchedKey = res.group;
  state.value.x = props.content.slice(0, res.index);
  state.value.y = res.str;
  state.value.z = props.content.slice(res.index + res.str.length);
  if (['ul', 'ol', 'h1', 'h2', 'h3', 'block_quotes'].includes(state.value.matchedKey)) {
    if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
    if (state.value.matchedKey === 'ul' || state.value.matchedKey === 'ol') {
      let key: 'ul'|'ol' = state.value.matchedKey;
      let elArray: Array<List> = regexps.value[key].li;
      let info = key === 'ul' ? getUlInfo(state.value.y) : getOlInfo(state.value.y);
      elArray.push({
        content: info.content,
        currentArray: regexps.value[key].li,
        first_number: info.first_number,
      });
      const n = info.n;
      let currentLevel = 0;
      const ulolreg = new RegExp([regexps.value.ul.regexp, regexps.value.ol.regexp].join('|'), 'm');
      let r;
      while (r = execCaptureGroup(ulolreg, state.value.z)) {
        if (r.group !== 'ul' && r.group !== 'ol') throw Error('An impossible error.');
        state.value.z = state.value.z.slice(r.index + r.str.length);
        if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
        info = r.group === 'ul' ? getUlInfo(r.str) : getOlInfo(r.str);
        const level = (info.spaces + n) / (n + 1);
        if (currentLevel < level) {
          const parent = elArray.slice(-1)[0];
          parent.child = [];
          parent.child.push({
            content: info.content,
            currentArray: parent.child,
            parent,
            first_number: info.first_number,
          });
          currentLevel += 1;
        } else {
          for (let i = level; i < currentLevel; i++) {
            const arr = elArray.slice(-1)[0].parent?.currentArray;
            if (!arr) throw Error('An impossible error.');
            elArray = arr;
          }
          elArray.push({
            content: info.content,
            currentArray: elArray,
            parent: currentLevel === 0 ? undefined : elArray[0].parent
          })
          currentLevel = level;
        }
      }
    } else if (state.value.z === 'block_quotes') {
      
    }
  }
  if (state.value.matchedKey === 'masked_links') {
    const reDisplay = /^\[(?![^]*https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+\s*[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+\s*\))[^]*\S+[^]*\]/;
    const resDisplay = reDisplay.exec(state.value.y);
    if (resDisplay) {
      regexps.value.masked_links.display = resDisplay[0].slice(1, -1);
    }
    const reUrl = /https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+\s*/;
    const resUrl = reUrl.exec(state.value.y);
    if (resUrl) {
      regexps.value.masked_links.url = resUrl[0];
    }
  } 
}

function execCaptureGroup(re: RegExp, str: string) {
  const res = re.exec(str);
  if (!res) return res;
  for (const key in res.groups) {
    if (res.groups[key]) {
      return {
        str: res[0],
        index: res.index,
        group: res.groups[key],
      };
    }
  }
  throw Error('Error occured in function "execCaptureGroup".');
}

function execNotNull(re: RegExp, str: string) {
  const res = re.exec(str);
  if (res) {
    return {
      str: res[0],
      index: res.index,
    }
  } else {
    throw Error('Error occured in function "execNotNull".');
  }
}

interface ListInfo {
  spaces: number;
  content: string;
  n: number;
  first_number?: number;
}

// content contains elements of ul
function getUlInfo(content: string): ListInfo {
  const resSpace = execNotNull(/^\s*/, content);
  const spaces = resSpace.str.length;
  content = content.slice(spaces);
  const resContent = execNotNull(/\s+/, content);
  content = content.slice(resContent.index + resContent.str.length);
  return { spaces, content, n: 1 };
}
// content contains elements of ol
function getOlInfo(content: string): ListInfo {
  const resSpace = execNotNull(/^\s*/, content);
  const spaces = resSpace.str.length;
  content = content.slice(spaces);
  const resContent = execNotNull(/\s+/, content);
  const c = content.slice(resContent.index + resContent.str.length);
  const res = execNotNull(/^\d+/, content);
  const n = res.str.length;
  const number = n > 9 ? 1000000000 : parseInt(res.str);
  return { spaces, content: c, n, first_number: number };
}
</script>
<template>
  <div>
    {{ state.x }}
    <content-frame v-if="state.matched" :content="state.z"/>
  </div>
</template>