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
}
const props = defineProps<ContentProps>();

const regexps = ref<Reg>({
  italics: {
    regexp: /(?<italics>(?:\*[^\*\s]+[^]*\*)|(?:_[^_][^]*_))/m,
    format: (str) => str.slice(1, -1),
  },
  bold: {
    regexp: /(?<bold>\*{2}[^]+\*{2})/m,
    format: (str) => str.slice(2, -2),
  },
  boldItalics: {
    regexp: /(?<boldItalics>\*{3}[^]+\*{3})/m,
    format: (str) => str.slice(3, -3),
  },
  underline: {
    regexp: /(?<underline>_{2}[^]+_{2})/m,
    format: (str) => str.slice(2, -2),
  },
  underlineItalics: {
    regexp: /(?<underlineItalics>_{2}\*[^]+\*_{2})/m,
    format: (str) => str.slice(3, -3),
  },
  underlineBold: {
    regexp: /(?<underlineBold>_{2}\*{2}[^]+\*{2}_{2})/m,
    format: (str) => str.slice(4, -4),
  },
  underlineBoldItalics: {
    regexp: /(?<underlineBoldItalics>_{2}\*{3}[^]+\*{3}_{2})/m,
    format: (str) => str.slice(5, -5),
  },
  strickthrough: {
    regexp: /(?<strickthrough>\~{2}[^]+\~{2})/m,
    format: (str) => str.slice(2, -2),
  },
  links: {
    regexp: /(?<links>https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+)/m,
  },
  maskedLinks: {
    regexp:
      /(?<maskedLinks>\[(?![^]*https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*\))[^]*\S+[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*\))/m,
    display: '',
    url: '',
  },
  codeBlock: {
    regexp: /(?<codeBlock>`{3}(?:[^](?!`{3}))*[^]`{3})/m,
    format: (str) => {
      str = str.slice(3, -3);
      const res = /^\s*\n/.exec(str);
      if (res) str = str.slice(res[0].length);
      return str;
    },
  },
  codeInline: {
    regexp:
      /(?<codeInline>(?:`[^`]+`(?!`))|(?:`{2}(?![^]*`{2}[^]*)[^]+`{2}(?!`)))/m,
    format: (str) => {
      const s = str.slice(1, -1);
      return s[s.length - 1] === '`' ? s.slice(1, -1) : s;
    },
  },
  spoilerTag: {
    regexp: /(?<spoilerTag>\|{2}[^\n]+\|{2})/m,
    format: (str) => str.slice(2, -2),
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
    format: (str) => str.slice(2),
  },
  h2: {
    regexp: /(?<h2>^#{2}\s+\S+.*$)/m,
    format: (str) => str.slice(3),
  },
  h3: {
    regexp: /(?<h3>^#{3}\s+\S+.*$)/m,
    format: (str) => str.slice(4),
  },
  blockQuotes: {
    regexp: /(?<blockQuotes>^>\s+\S+.*$)/m,
    content: [],
  },
  channelMention: {
    regexp: /(?<channelMention><#\d+>)/m,
    display: '# ',
  },
  roleMention: {
    regexp: /(?<roleMention><@&\d+>)/m,
    display: '@ ',
  },
  memberMention: {
    regexp: /(?<memberMention><@&\d+>)/m,
    display: '@ ',
  },
  everyoneMention: {
    regexp: /(?<everyoneMention>@everyone)/m,
  },
  hereMention: {
    regexp: /(?<hereMention>@here)/m,
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
const state = ref<IncompleteState | State>({
  matched: false,
  matchedKey: undefined,
  x: props.content,
  y: undefined,
  z: undefined,
});

const keyofRegexps = Object.keys(regexps.value) as Array<keyof Reg>;
const valueofRegExps: Array<RegExp> = [];
keyofRegexps.forEach((key) => {
  if (!props.except.includes(key)) {
    valueofRegExps.push(regexps.value[key].regexp);
  }
});
const combinedReg = new RegExp(
  valueofRegExps.map((r) => r.source).join('|'),
  'm'
);
// exec() follow the "greedy matching"!
const res = execCaptureGroup(combinedReg, props.content);
if (res) {
  state.value.matched = true;
  state.value.matchedKey = res.group;
  state.value.x = props.content.slice(0, res.index);
  state.value.y = res.str;
  state.value.z = props.content.slice(res.index + res.str.length);
  if (
    ['ul', 'ol', 'h1', 'h2', 'h3', 'blockQuotes'].includes(
      state.value.matchedKey
    )
  ) {
    if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
    if (['ul', 'ol'].includes(state.value.matchedKey)) {
      let key = state.value.matchedKey as 'ul' | 'ol';
      let elArray: Array<ListStruct> = regexps.value[key].li;
      let info =
        key === 'ul' ? getUlInfo(state.value.y) : getOlInfo(state.value.y);
      elArray.push({
        content: info.content,
        currentArray: regexps.value[key].li,
        firstNumber: info.firstNumber,
      });
      const n = info.n;
      let currentLevel = 0;
      const ulolreg = new RegExp(
        [regexps.value.ul.regexp.source, regexps.value.ol.regexp.source].join(
          '|'
        ),
        'm'
      );
      let r;
      while ((r = execCaptureGroup(ulolreg, state.value.z))) {
        if (r.index !== 0) break;
        if (r.group !== 'ul' && r.group !== 'ol')
          throw Error('An impossible error.');
        state.value.z = state.value.z.slice(r.index + r.str.length);
        if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
        info = r.group === 'ul' ? getUlInfo(r.str) : getOlInfo(r.str);
        const level =
          (info.spaces - 1 - ((info.spaces - 1) % (n + 1))) / (n + 1) + 1;
        if (currentLevel < level) {
          const parent = elArray.slice(-1)[0];
          parent.child = [];
          parent.child.push({
            content: info.content,
            currentArray: parent.child,
            parent,
            firstNumber: info.firstNumber,
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
            parent: currentLevel === 0 ? undefined : elArray[0].parent,
          });
          currentLevel = level;
        }
      }
    } else if (state.value.matchedKey === 'blockQuotes') {
      regexps.value.blockQuotes.content.push(state.value.y.slice(2));
      let r;
      while ((r = regexps.value.blockQuotes.regexp.exec(state.value.z))) {
        if (r.index !== 0) break;
        regexps.value.blockQuotes.content.push(r[0].slice(2));
        state.value.z = state.value.z.slice(r.index + r[0].length);
        if (/^\n/.exec(state.value.z)) state.value.z = state.value.z.slice(1);
      }
    }
  } else if (['links', 'maskedLinks'].includes(state.value.matchedKey)) {
    let url;
    if (state.value.matchedKey === 'maskedLinks') {
      const reDisplay =
        /^\[(?![^]*https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*[^]*\]\(https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*\))[^]*\S+[^]*\]/;
      regexps.value.maskedLinks.display = execNotNull(
        reDisplay,
        state.value.y
      ).str.slice(1, -1);
      const reUrl = /https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]=]+\s*/;
      url = regexps.value.maskedLinks.url = execNotNull(
        reUrl,
        state.value.y
      ).str;
    } else {
      url = state.value.y;
      const re = /^https:\/\/cdn\.discordapp\.com\/attachments\/\d+\/\d+\/.+$/;
      if (re.test(url)) {
        // discord attachments
        const reLeft =
          /^https:\/\/cdn\.discordapp\.com\/attachments\/\d+\/\d+\//;
        const resLeft = execNotNull(reLeft, url);
        const resRight = /\?/.exec(url);
        const resRight2 = resRight ? resRight.index : undefined;
        regexps.value.links.file = url.slice(resLeft.str.length, resRight2);
      }
    }
  } else if (state.value.matchedKey === 'channelMention') {
    const enteredId = execNotNull(/\d+/, state.value.y).str;
    const channel = props.mention.channel_mentions.find(
      (channel) => channel.id === enteredId
    );
    if (channel) {
      if (channel.category) {
        regexps.value.channelMention.display += channel.category.name + ' > ';
      }
      regexps.value.channelMention.display += channel.name;
    } else {
      regexps.value.channelMention.display += '不明なチャンネル';
    }
  } else if (state.value.matchedKey === 'roleMention') {
    const enteredId = execNotNull(/\d+/, state.value.y).str;
    const role = props.mention.role_mentions.find(
      (role) => role.id === enteredId
    );
    regexps.value.roleMention.display += role ? role.name : '不明なロール';
  } else if (state.value.matchedKey === 'memberMention') {
    const enteredId = execNotNull(/\d+/, state.value.y).str;
    const member = props.mention.mentions.find(
      (member) => member.id === enteredId
    );
    if (member) {
      regexps.value.memberMention.display += member.nick
        ? member.nick
        : member.display_name;
    } else {
      regexps.value.memberMention.display += '不明なユーザー';
    }
  }
}

function execCaptureGroup(
  re: RegExp,
  str: string
): null | {
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
    };
  } else {
    throw Error('Error occured in function "execNotNull".');
  }
}

interface ListInfo {
  spaces: number;
  content: string;
  n: number;
  firstNumber?: number;
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
  return { spaces, content: c, n, firstNumber: number };
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
  <strong v-else-if="state.matchedKey === 'boldItalics'">
    <i>
      <content-frame
        :content="regexps.boldItalics.format(state.y)"
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
  <u v-else-if="state.matchedKey === 'underlineItalics'">
    <i>
      <content-frame
        :content="regexps.underline.format(state.y)"
        :except="[]"
        :mention="props.mention"
      />
    </i>
  </u>
  <u v-else-if="state.matchedKey === 'underlineBold'">
    <strong>
      <content-frame
        :content="regexps.underlineBold.format(state.y)"
        :except="[]"
        :mention="props.mention"
      />
    </strong>
  </u>
  <u v-else-if="state.matchedKey === 'underlineBoldItalics'">
    <strong>
      <i>
        <content-frame
          :content="regexps.underlineBoldItalics.format(state.y)"
          :except="[]"
          :mention="props.mention"
        />
      </i>
    </strong>
  </u>
  <span
    v-else-if="state.matchedKey === 'strickthrough'"
    style="text-decoration: line-through"
  >
    <content-frame
      :content="regexps.strickthrough.format(state.y)"
      :except="[]"
      :mention="props.mention"
    />
  </span>
  <span v-else-if="state.matchedKey === 'links'">
    <a v-if="regexps.links.file" :href="state.y" class="clip px-1">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        :style="{ marginBottom: '-3px' }"
      >
        <path
          fill="white"
          d="M10.57 4.01a6.97 6.97 0 0 1 9.86 0l.54.55a6.99 6.99 0 0 1 0 9.88l-7.26 7.27a1 1 0 0 1-1.42-1.42l7.27-7.26a4.99 4.99 0 0 0 0-7.06L19 5.43a4.97 4.97 0 0 0-7.02 0l-8.02 8.02a3.24 3.24 0 1 0 4.58 4.58l6.24-6.24a1.12 1.12 0 0 0-1.58-1.58l-3.5 3.5a1 1 0 0 1-1.42-1.42l3.5-3.5a3.12 3.12 0 1 1 4.42 4.42l-6.24 6.24a5.24 5.24 0 0 1-7.42-7.42l8.02-8.02Z"
          class=""
        ></path>
      </svg>
      {{ regexps.links.file }}
    </a>
    <a v-else :href="state.y">
      {{ state.y }}
    </a>
  </span>
  <a
    v-else-if="state.matchedKey === 'maskedLinks'"
    :href="regexps.maskedLinks.url"
  >
    <content-frame
      :content="regexps.maskedLinks.display"
      :except="[]"
      :mention="props.mention"
    />
  </a>
  <pre v-else-if="state.matchedKey === 'codeBlock'" class="px-1">{{
    regexps.codeBlock.format(state.y)
  }}</pre>
  <code v-else-if="state.matchedKey === 'codeInline'" class="px-1">
    {{ regexps.codeInline.format(state.y) }}
  </code>
  <span v-else-if="state.matchedKey === 'spoilerTag'">
    <content-frame
      :content="regexps.spoilerTag.format(state.y)"
      :except="[]"
      :mention="props.mention"
    />
  </span>
  <list-frame
    v-else-if="state.matchedKey === 'ul'"
    :li="regexps.ul.li"
    :mention="props.mention"
  />
  <list-frame
    v-else-if="state.matchedKey === 'ol'"
    :li="regexps.ol.li"
    :mention="props.mention"
  />
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
  <blockquote v-else-if="state.matchedKey === 'blockQuotes'" class="py-1 px-2">
    <p v-for="(str, index) in regexps.blockQuotes.content" :key="index">
      <content-frame
        :content="str"
        :except="['blockQuotes']"
        :mention="props.mention"
      />
    </p>
  </blockquote>
  <span v-else-if="state.matchedKey === 'channelMention'" class="mention px-1">
    {{ regexps.channelMention.display }}
  </span>
  <span v-else-if="state.matchedKey === 'roleMention'" class="mention px-1">
    {{ regexps.roleMention.display }}
  </span>
  <span v-else-if="state.matchedKey === 'memberMention'" class="mention px-1">
    {{ regexps.memberMention.display }}
  </span>
  <span v-else-if="state.matchedKey === 'everyoneMention'" class="mention px-1">
    @everyone
  </span>
  <span v-else-if="state.matchedKey === 'hereMention'" class="mention px-1">
    @here
  </span>
  <content-frame
    v-if="state.matched"
    :content="state.z"
    :except="[]"
    :mention="props.mention"
  />
</template>
<style scoped>
code,
pre {
  font-family: Consolas, monospace;
  background-color: #2b2d31;
  border-radius: 2px;
}
pre {
  white-space: pre-wrap;
}
blockquote {
  border-left: 5px solid gray;
}
.mention {
  background-color: #3b3b5f;
  border-radius: 2px;
}
.clip {
  background-color: #3b5e42;
  border-radius: 2px;
  text-decoration: none;
  color: white;
}
</style>
