<script setup lang="ts">
import { ref } from 'vue';
import ListFrame from './ListFrame.vue';
import { Message } from '../types/response';
import { ListStruct, Reg } from '../types/content';
interface ContentProps {
  content: string;
  except: Array<keyof Reg>;
  mention: {
    mentions: Message['mentions'];
    channel_mentions: Message['channel_mentions'];
    role_mentions: Message['role_mentions'];
  };
};
const props = defineProps<ContentProps>();

const regexps = ref<Reg>({
  italics: {
    regexp: /(?<italics>(?:\*[^\*\s]+[^]*\*)|(?:_[^_][^]*_))/m,
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
  links: {
    regexp: /(?<links>https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+)/m,
  },
  masked_links: {
    regexp: /(?<masked_links>\[(?![^]*https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*\))[^]*\S+[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*\))/m,
    display: '',
    url: '',
  },
  code_block: {
    regexp: /(?<code_block>`{3}(?:[^](?!`{3}))*[^]`{3})/m,
    format: str => str.slice(3, -3),
  },
  code_inline: {
    regexp: /(?<code_inline>(?:`[^`]+`(?!`))|(?:`{2}(?![^]*`{2}[^]*)[^]+`{2}(?!`)))/m,
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
    content: [],
  },
  channel_mention: {
    regexp: /(?<channel_mention><#\d+>)/m,
    display: '# ',
  },
  role_mention: {
    regexp: /(?<role_mention><@&\d+>)/m,
    display: '@ ',
  },
  member_mention: {
    regexp: /(?<member_mention><@&\d+>)/m,
    display: '@ ',
  },
});

interface State {
  matched: boolean;
  matchedKey: keyof Reg;
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

const keyofRegexps = Object.keys(regexps.value) as Array<keyof Reg>;
const valueofRegExps: Array<RegExp> = [];
keyofRegexps.forEach(key => {
  if (!props.except.includes(key)) {
    valueofRegExps.push(regexps.value[key].regexp);
  }
});
const combinedReg = new RegExp(valueofRegExps.map(r => r.source).join('|'), 'm');
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
    if (['ul', 'ol'].includes(state.value.matchedKey)) {
      let key = state.value.matchedKey as 'ul'|'ol';
      let elArray: Array<ListStruct> = regexps.value[key].li;
      let info = key === 'ul' ? getUlInfo(state.value.y) : getOlInfo(state.value.y);
      elArray.push({
        content: info.content,
        currentArray: regexps.value[key].li,
        first_number: info.first_number,
      });
      const n = info.n;
      let currentLevel = 0;
      const ulolreg = new RegExp([
        regexps.value.ul.regexp.source, 
        regexps.value.ol.regexp.source
      ].join('|'), 'm');
      let r;
      while (r = execCaptureGroup(ulolreg, state.value.z)) {
        if (r.index !== 0) break;
        if (r.group !== 'ul' && r.group !== 'ol') throw Error('An impossible error.');
        state.value.z = state.value.z.slice(r.index + r.str.length);
        if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
        info = r.group === 'ul' ? getUlInfo(r.str) : getOlInfo(r.str);
        const level = ((info.spaces-1) - (info.spaces-1) % (n+1)) / (n+1) + 1
        if (currentLevel < level) {
          const parent = elArray.slice(-1)[0];
          parent.child = [];
          parent.child.push({
            content: info.content,
            currentArray: parent.child,
            parent,
            first_number: info.first_number,
          });
          elArray = parent.child;
          currentLevel += 1;
        } else {
          for (let i = level; i < currentLevel; i++) {
            const arr = elArray[0].parent?.currentArray;
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
    } else if (state.value.matchedKey === 'block_quotes') {
      regexps.value.block_quotes.content.push(state.value.y.slice(2));
      let r;
      while (r = regexps.value.block_quotes.regexp.exec(state.value.z)) {
        if (r.index !== 0) break;
        regexps.value.block_quotes.content.push(r[0].slice(2));
        state.value.z = state.value.z.slice(r.index + r[0].length);
        if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
      }
    }
  } else if (state.value.matchedKey === 'masked_links') {
    const reDisplay = /^\[(?![^]*https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*\))[^]*\S+[^]*\]/;
    const resDisplay = reDisplay.exec(state.value.y);
    if (resDisplay) {
      regexps.value.masked_links.display = resDisplay[0].slice(1, -1);
    }
    const reUrl = /https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*/;
    const resUrl = reUrl.exec(state.value.y);
    if (resUrl) {
      regexps.value.masked_links.url = resUrl[0];
    }
  } else if (state.value.matchedKey === 'channel_mention') {
    const enteredId = execNotNull(/\d+/, state.value.y).str;
    const channel = props.mention.channel_mentions.find(channel => channel.id === enteredId);
    if (channel) {
      if (channel.category) {
        regexps.value.channel_mention.display += channel.category.name + ' > ';
      }
      regexps.value.channel_mention.display += channel.name;
    } else {
      regexps.value.channel_mention.display += '不明なチャンネル';
    }
  } else if (state.value.matchedKey === 'role_mention') {
    const enteredId = execNotNull(/\d+/, state.value.y).str;
    const role = props.mention.role_mentions.find(role => role.id === enteredId);
    regexps.value.role_mention.display += role ? role.name : '不明なロール';
  } else if (state.value.matchedKey === 'member_mention') {
    const enteredId = execNotNull(/\d+/, state.value.y).str;
    const member = props.mention.mentions.find(member => member.id === enteredId);
    if (member) {
      regexps.value.member_mention.display += member.nick ? member.nick : member.display_name;
    } else {
      regexps.value.member_mention.display += '不明なユーザー';
    }
  }
}

function execCaptureGroup(re: RegExp, str: string): null | {
  str: string;
  index: number;
  group: keyof Reg;
} {
  const res = re.exec(str);
  if (!res) return res;
  for (const key in res.groups) {
    if (res.groups[key]) {
      return {
        str: res[0],
        index: res.index,
        group: key as keyof Reg,
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
  const n = res.str.length + 1;
  const number = n > 9 ? 1000000000 : parseInt(res.str);
  return { spaces, content: c, n, first_number: number };
}
</script>
<template>
  {{ state.x }}
  <i v-if="state.matchedKey === 'italics'">
    <content-frame 
      :content="regexps.italics.format(state.y)" 
      :except="[]" 
      :mention="props.mention" 
    />
  </i>
  <strong v-else-if="state.matchedKey === 'bold'">
    <content-frame 
      :content="regexps.bold.format(state.y)" 
      :except="[]" 
      :mention="props.mention" 
    />
  </strong>
  <strong v-else-if="state.matchedKey === 'bold_italics'">
    <i>
      <content-frame 
        :content="regexps.bold_italics.format(state.y)" 
        :except="[]" 
        :mention="props.mention" 
      />
    </i>
  </strong>
  <u v-else-if="state.matchedKey === 'underline'">
    <content-frame 
      :content="regexps.underline.format(state.y)" 
      :except="[]" 
      :mention="props.mention" 
    />
  </u>
  <u v-else-if="state.matchedKey === 'underline_italics'">
    <i>
      <content-frame 
        :content="regexps.underline.format(state.y)" 
        :except="[]"
        :mention="props.mention" 
      />
    </i>
  </u>
  <u v-else-if="state.matchedKey === 'underline_bold'">
    <strong>
      <content-frame 
        :content="regexps.underline_bold.format(state.y)" 
        :except="[]"
        :mention="props.mention" 
      />
    </strong>
  </u>
  <u v-else-if="state.matchedKey === 'underline_bold_italics'">
    <strong>
      <i>
        <content-frame 
          :content="regexps.underline_bold_italics.format(state.y)" 
          :except="[]"
          :mention="props.mention" 
        />
      </i>
    </strong>
  </u>
  <span v-else-if="state.matchedKey === 'strickthrough'" style="text-decoration: line-through;">
    <content-frame 
      :content="regexps.strickthrough.format(state.y)" 
      :except="[]"
      :mention="props.mention" 
    />
  </span>
  <a v-else-if="state.matchedKey === 'links'" :href="state.y">
    {{ state.y }}
  </a>
  <a v-else-if="state.matchedKey === 'masked_links'" :href="regexps.masked_links.url">
    <content-frame 
      :content="regexps.masked_links.display" 
      :except="[]"
      :mention="props.mention" 
    />
  </a>
  <pre v-else-if="state.matchedKey === 'code_block'" class="px-1">
{{ regexps.code_block.format(state.y) }}
  </pre>
  <code v-else-if="state.matchedKey === 'code_inline'" class="px-1">
    {{ regexps.code_inline.format(state.y) }}
  </code>
  <span v-else-if="state.matchedKey === 'spoiler_tag'">
    <content-frame 
      :content="regexps.spoiler_tag.format(state.y)" 
      :except="[]"
      :mention="props.mention"
    />
  </span>
  <list-frame 
    v-else-if="state.matchedKey === 'ul'"
    :li="regexps.ul.li"
    :mention="props.mention" />
  <list-frame
    v-else-if="state.matchedKey === 'ol'"
    :li="regexps.ol.li"
    :mention="props.mention" />
  <h1 v-else-if="state.matchedKey === 'h1'">
    <content-frame 
      :content="regexps.h1.format(state.y)" 
      :except="[]"
      :mention="props.mention" 
    />
  </h1>
  <h2 v-else-if="state.matchedKey === 'h2'">
    <content-frame
      :content="regexps.h2.format(state.y)" 
      :except="[]"
      :mention="props.mention" 
    />
  </h2>
  <h3 v-else-if="state.matchedKey === 'h3'">
    <content-frame 
      :content="regexps.h3.format(state.y)" 
      :except="[]"
      :mention="props.mention" 
    />
  </h3>
  <blockquote v-else-if="state.matchedKey === 'block_quotes'" class="py-1 px-2">
    <p v-for="(str, index) in regexps.block_quotes.content" :key="index">
      <content-frame 
        :content="str" 
        :except="['block_quotes']"
        :mention="props.mention" 
      />
    </p>
  </blockquote>
  <span v-else-if="state.matchedKey === 'channel_mention'" class="mention px-1">
    {{ regexps.channel_mention.display }}
  </span>
  <span v-else-if="state.matchedKey === 'role_mention'" class="mention px-1">
    {{ regexps.role_mention.display }}
  </span>
  <span v-else-if="state.matchedKey === 'member_mention'" class="mention px-1">
    {{ regexps.member_mention.display }}
  </span>
  <content-frame 
    v-if="state.matched" 
    :content="state.z" 
    :except="[]"
    :mention="props.mention" 
  />
</template>
<style scoped>
code, pre {
  font-family: Consolas, monospace;
  background-color: #eeeeee;
  border-radius: 2px;
}
pre {
  white-space: pre-wrap;
}
blockquote {
  border-left: 5px solid gray;
}
.mention {
  background-color: #E6E6FA;
  border-radius: 2px;
}
</style>