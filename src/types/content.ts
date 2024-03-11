export interface RegContent {
  regexp: RegExp;
  format: (str: string) => string;
}
export interface ListStruct {
  content: string;
  currentArray: Array<ListStruct>;
  child?: Array<ListStruct>;
  parent?: ListStruct;
  first_number?: number; // If the list is ol, this type is number. If ul, then undefined.
}
export interface MentionReg {
  regexp: RegExp;
  display: string;
}
export interface Reg {
  italics: RegContent;
  bold: RegContent;
  bold_italics: RegContent;
  underline: RegContent;
  underline_italics: RegContent;
  underline_bold: RegContent;
  underline_bold_italics: RegContent;
  strickthrough: RegContent;
  links: {
    regexp: RegExp;
    file?: string;
  };
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
    li: Array<ListStruct>;
  };
  ol: {
    regexp: RegExp;
    li: Array<ListStruct>;
  };
  h1: RegContent;
  h2: RegContent;
  h3: RegContent;
  block_quotes: {
    regexp: RegExp;
    content: Array<string>;
  };
  channel_mention: MentionReg;
  role_mention: MentionReg;
  member_mention: MentionReg;
  everyone_mention: {
    regexp: RegExp;
  };
  here_mention: {
    regexp: RegExp;
  };
}
