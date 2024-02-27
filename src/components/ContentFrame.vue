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
type Ul = Array<{
  content: string;
  child?: Ul|Ol;
  parent?: Ul|Ol;
}>;
type Ol = Array<{
  content: string;
  parent?: Ul|Ol;
} | {
  content: string;
  first_number: number;
  child: Ul|Ol;
  parent?: Ul|Ol;
}>;
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
    li: Ul;
  };
  ol: {
    regexp: RegExp;
    li: Ol;
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
    const res = /^\n/.exec(state.value.z);
    if (res) state.value.z = state.value.z.slice(1);
    if (state.value.matchedKey === 'ul' || state.value.matchedKey === 'ol') {
      let key: 'ul'|'ol' = state.value.matchedKey;
      let elArray: Ul|Ol = regexps.value[key].li;
      const res = getListInfo(state.value.y, key);
      const n = key === 'ol' ? res.number.toString()
      while () {
        
      }
      // remove leading spaces
      const res = execNotNull(/^\s*/, state.value.y);
      state.value.y = state.value.y.slice(res.str.length);
    }
    if (state.value.matchedKey === 'ul') {
      regexps.value.ul.li.push({
        indent: 0,
        content: state.value.y.slice(2),
      });
      while (state.value.z) {
        const resUL = regexps.value.ul.regexp.exec(state.value.z);
        if (resUL && resUL.index === 0) {
          const resIndent = /^\s*/.exec(resUL[0]);
          if (!resIndent) break;
          const space = resIndent[0].length;
          const indentLevel = space === 0 ? 0 : (space+1)/2;
          const preIndentLevel = regexps.value.ul.li.slice(0,-1)[0].indent;
          regexps.value.ul.li.push({
            indent: Math.min(indentLevel, preIndentLevel+1),
            content: resUL[0].slice(space),
          });
          state.value.z = state.value.z.slice(resUL[0].length);
          const resLine = /^\n/.exec(state.value.z);
          if (resLine) state.value.z = state.value.z.slice(1);
        } else {
          break;
        }
      }
    } else if (state.value.matchedKey === 'ol') {
      
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

// content contains elements of ul or ol.
function getUlInfo(content: string) {
  const resSpace = execNotNull(/^\s*/, content);
  const spaces = resSpace.str.length;
  content = content.slice(spaces);
  const resContent = execNotNull(/\s+/, content);
  const c = content.slice(resContent.index + resContent.str.length);
  if (typeof e) {
    const res = execNotNull(/^\d+/, content);
    const number = parseInt(res.str);
    return { spaces, content: c, number };
  } else {
    return { spaces, content: c };
  }
}
</script>
<template>
  <div>
    {{ state.x }}
    <content-frame v-if="state.matched" :content="state.z"/>
  </div>
</template>